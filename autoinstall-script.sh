#!/bin/bash
# ================================================================
# Script d'installation automatisée pour déploiement Streamlit
# Ce script automatise entièrement l'installation et la configuration
# de trois applications Streamlit derrière Nginx avec SSL.
# ================================================================

set -e # Exit on error

# Variables de configuration - À MODIFIER
GITHUB_REPO="https://github.com/votre-username/streamlit-project.git"
DOMAIN_NAME="demo.datavizir.site"
EMAIL_ADMIN="support@datavizir.site"
USE_GITHUB=true # true si le code est dans GitHub, false pour utiliser les templates locaux
SSH_PORT=22 # Port SSH standard, modifiable pour plus de sécurité

# Couleurs pour le terminal
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# ================================================================
# FONCTIONS UTILITAIRES
# ================================================================

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

check_command() {
    if ! command -v "$1" &> /dev/null; then
        log_warning "La commande $1 n'est pas installée. Installation en cours..."
        return 1
    fi
    return 0
}

wait_for_service() {
    local service_name="$1"
    local max_attempts=30
    local attempt=1
    
    log_info "Attente du démarrage du service $service_name..."
    
    while [ $attempt -le $max_attempts ]; do
        if systemctl is-active --quiet "$service_name"; then
            log_info "Le service $service_name est actif."
            return 0
        fi
        sleep 2
        attempt=$((attempt + 1))
    done
    
    log_error "Échec du démarrage du service $service_name après $max_attempts tentatives."
    return 1
}

# ================================================================
# 1. PRÉPARATION DU SYSTÈME
# ================================================================

check_root() {
    if [ "$(id -u)" -ne 0 ]; then
        log_error "Ce script doit être exécuté avec les privilèges root."
        log_info "Veuillez exécuter: sudo bash $0"
        exit 1
    fi
}

update_system() {
    log_info "Mise à jour du système..."
    apt-get update
    apt-get upgrade -y
}

install_dependencies() {
    log_info "Installation des utilitaires nécessaires..."
    apt-get install -y apt-transport-https ca-certificates curl gnupg lsb-release \
    software-properties-common git unzip jq ufw nano certbot python3-certbot-nginx
}

create_user() {
    local username="deployer"
    
    if id "$username" &>/dev/null; then
        log_info "L'utilisateur $username existe déjà."
    else
        log_info "Création de l'utilisateur $username..."
        adduser --disabled-password --gecos "" "$username"
        usermod -aG sudo "$username"
        
        # Configurer SSH pour l'utilisateur (optionnel)
        mkdir -p /home/$username/.ssh
        touch /home/$username/.ssh/authorized_keys
        chmod 700 /home/$username/.ssh
        chmod 600 /home/$username/.ssh/authorized_keys
        chown -R $username:$username /home/$username/.ssh
        
        log_info "Utilisateur $username créé avec succès."
    fi
}

configure_firewall() {
    log_info "Configuration du pare-feu..."
    
    if ! check_command ufw; then
        apt-get install -y ufw
    fi
    
    # Configurer les règles de base
    ufw default deny incoming
    ufw default allow outgoing
    
    # Autoriser SSH (utiliser le port personnalisé si spécifié)
    if [ "$SSH_PORT" -ne 22 ]; then
        ufw allow "$SSH_PORT"/tcp
        log_info "Port SSH configuré sur $SSH_PORT."
        
        # Modifier la configuration SSH si nécessaire
        sed -i "s/^#Port 22/Port $SSH_PORT/" /etc/ssh/sshd_config
        systemctl restart sshd
    else
        ufw allow ssh
    fi
    
    # Autoriser HTTP et HTTPS
    ufw allow 80/tcp
    ufw allow 443/tcp
    
    # Activer le pare-feu s'il n'est pas déjà activé
    if ! ufw status | grep -q "Status: active"; then
        log_info "Activation du pare-feu..."
        echo "y" | ufw enable
    else
        log_info "Le pare-feu est déjà actif."
    fi
    
    log_info "Configuration du pare-feu terminée."
}

# ================================================================
# 2. INSTALLATION DE DOCKER ET DOCKER COMPOSE
# ================================================================

install_docker() {
    log_info "Installation de Docker..."
    
    # Supprimer les anciennes versions
    for pkg in docker.io docker-doc docker-compose podman-docker containerd runc; do
        apt-get remove -y $pkg 2>/dev/null || true
    done
    
    # Installer les prérequis
    apt-get install -y ca-certificates curl
    
    # Ajouter la clé GPG Docker
    install -m 0755 -d /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    chmod a+r /etc/apt/keyrings/docker.gpg
    
    # Ajouter le référentiel Docker
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    
    # Mettre à jour la liste des paquets
    apt-get update
    
    # Installer Docker et Docker Compose
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    
    # Démarrer et activer Docker
    systemctl enable --now docker
    
    # Ajouter l'utilisateur au groupe docker
    usermod -aG docker deployer
    
    log_info "Docker et Docker Compose ont été installés avec succès."
}

test_docker() {
    log_info "Test de l'installation Docker..."
    docker run --rm hello-world
    
    if [ $? -eq 0 ]; then
        log_info "Docker fonctionne correctement."
    else
        log_error "Un problème est survenu avec l'installation de Docker."
        exit 1
    fi
}

# ================================================================
# 3. CONFIGURATION DU PROJET
# ================================================================

setup_project_structure() {
    local project_dir="/home/deployer/streamlit-project"
    
    log_info "Configuration de la structure du projet..."
    
    # Création du répertoire de projet
    mkdir -p $project_dir
    
    if [ "$USE_GITHUB" = true ]; then
        # Clone le dépôt GitHub
        log_info "Clonage du dépôt GitHub $GITHUB_REPO..."
        git clone $GITHUB_REPO $project_dir
    else
        # Création de la structure de base
        log_info "Création de la structure de projet à partir des templates..."
        
        # Création des répertoires
        mkdir -p $project_dir/{apps,nginx,certbot,scripts,data}
        mkdir -p $project_dir/apps/{egra_egma_datavizir,pupilcard_datavizir,contextual_datavizir}
        mkdir -p $project_dir/nginx/{conf,html}
        mkdir -p $project_dir/certbot/{conf,www}
        mkdir -p $project_dir/data/{egra,pupilcard,contextual}
        
        # Création des fichiers de base (sera complété par generate_project_files)
        touch $project_dir/{.env,.env.example,docker-compose.yml}
        touch $project_dir/nginx/html/index.html
        touch $project_dir/nginx/conf/{default.conf,security_headers.conf}
        touch $project_dir/apps/egra_egma_datavizir/{app.py,requirements.txt,Dockerfile}
        touch $project_dir/apps/pupilcard_datavizir/{app.py,requirements.txt,Dockerfile}
        touch $project_dir/apps/contextual_datavizir/{app.py,requirements.txt,Dockerfile}
    fi
    
    # Définir les permissions
    chown -R deployer:deployer $project_dir
    
    log_info "Structure du projet créée avec succès."
}

generate_project_files() {
    local project_dir="/home/deployer/streamlit-project"
    
    if [ "$USE_GITHUB" = true ]; then
        log_info "Utilisation des fichiers du dépôt GitHub..."
        return 0
    fi
    
    log_info "Génération des fichiers de projet..."
    
    # docker-compose.yml
    cat > $project_dir/docker-compose.yml << 'EOF'
version: "3.8"

services:
  egra_egma_datavizir:
    build: 
      context: ./apps/egra_egma_datavizir
    container_name: egra_app
    restart: unless-stopped
    volumes:
      - ${DATA_PATH:-./data}/egra:/app/data
    env_file:
      - .env
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  pupilcard_datavizir:
    build: 
      context: ./apps/pupilcard_datavizir
    container_name: pupilcard_app
    restart: unless-stopped
    volumes:
      - ${DATA_PATH:-./data}/pupilcard:/app/data
    env_file:
      - .env
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  contextual_datavizir:
    build: 
      context: ./apps/contextual_datavizir
    container_name: contextual_app
    restart: unless-stopped
    volumes:
      - ${DATA_PATH:-./data}/contextual:/app/data
    env_file:
      - .env
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    deploy:
      resources:
        limits:
          cpus: '0.50'
          memory: 512M
        reservations:
          cpus: '0.25'
          memory: 256M
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

  nginx:
    build: ./nginx
    container_name: nginx_proxy
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/conf:/etc/nginx/conf.d
      - ./nginx/html:/var/www/streamlit
      - ./certbot/conf:/etc/letsencrypt
      - ./certbot/www:/var/www/certbot
    depends_on:
      - egra_egma_datavizir
      - pupilcard_datavizir
      - contextual_datavizir
    env_file:
      - .env
    restart: unless-stopped
    logging:
      driver: "json-file"
      options:
        max-size: "10m"
        max-file: "3"

networks:
  default:
    driver: bridge

volumes:
  egra_data:
  pupilcard_data:
  contextual_data:
  certbot_conf:
  certbot_www:
EOF

    # docker-compose.initial.yml
    cat > $project_dir/docker-compose.initial.yml << 'EOF'
version: "3.8"

services:
  nginx:
    build: ./nginx
    container_name: nginx_proxy
    ports:
      - "80:80"
    volumes:
      - ./nginx/conf:/etc/nginx/conf.d
      - ./nginx/html:/var/www/streamlit
      - ./certbot/www:/var/www/certbot
    env_file:
      - .env
    restart: unless-stopped

networks:
  default:
    driver: bridge
EOF

    # .env.example
    cat > $project_dir/.env.example << 'EOF'
# Configuration du domaine
DOMAIN_NAME=votre-domaine.com
EMAIL_ADMIN=admin@votre-domaine.com

# Configuration des conteneurs
COMPOSE_PROJECT_NAME=streamlit-apps

# Volumes persistants
DATA_PATH=./data

# Versions des images
PYTHON_VERSION=3.11-slim
NGINX_VERSION=alpine
EOF

    # .env réel
    cat > $project_dir/.env << EOF
# Configuration du domaine
DOMAIN_NAME=$DOMAIN_NAME
EMAIL_ADMIN=$EMAIL_ADMIN

# Configuration des conteneurs
COMPOSE_PROJECT_NAME=streamlit-apps

# Volumes persistants
DATA_PATH=./data

# Versions des images
PYTHON_VERSION=3.11-slim
NGINX_VERSION=alpine
EOF

    # nginx/Dockerfile
    cat > $project_dir/nginx/Dockerfile << 'EOF'
FROM nginx:alpine

# Copier les fichiers de configuration
COPY conf/default.conf /etc/nginx/conf.d/default.conf
COPY conf/security_headers.conf /etc/nginx/conf.d/security_headers.conf
COPY html/index.html /var/www/streamlit/index.html

# Créer le répertoire pour certbot
RUN mkdir -p /var/www/certbot

# Exposer les ports HTTP et HTTPS
EXPOSE 80 443
EOF

    # nginx/conf/default.conf
    cat > $project_dir/nginx/conf/default.conf << 'EOF'
# Configuration des en-têtes de sécurité
include /etc/nginx/conf.d/security_headers.conf;

# Redirection HTTP vers HTTPS
server {
    listen 80;
    server_name ${DOMAIN_NAME};
    
    # Pour le défi Let's Encrypt
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }
    
    # Redirection vers HTTPS
    location / {
        return 301 https://$host$request_uri;
    }
}

# Serveur HTTPS principal
server {
    listen 443 ssl;
    server_name ${DOMAIN_NAME};
    
    # Configuration SSL
    ssl_certificate /etc/letsencrypt/live/${DOMAIN_NAME}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${DOMAIN_NAME}/privkey.pem;
    include /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam /etc/letsencrypt/ssl-dhparams.pem;
    
    # Page d'accueil
    root /var/www/streamlit;
    index index.html;
    
    # Page d'accueil principale
    location / {
        try_files $uri $uri/ =404;
    }
    
    # Configuration pour egra_egma_datavizir
    location /egra/ {
        rewrite ^/egra(/.*)$ $1 break;
        proxy_pass http://egra_app:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
    
    # Configuration pour pupilcard_datavizir
    location /pupilcard/ {
        rewrite ^/pupilcard(/.*)$ $1 break;
        proxy_pass http://pupilcard_app:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
    
    # Configuration pour contextual_datavizir
    location /contextual/ {
        rewrite ^/contextual(/.*)$ $1 break;
        proxy_pass http://contextual_app:8501;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_read_timeout 86400;
    }
    
    # Limitation de la taille des requêtes
    client_max_body_size 100M;
}
EOF

    # nginx/conf/security_headers.conf
    cat > $project_dir/nginx/conf/security_headers.conf << 'EOF'
# En-têtes de sécurité
add_header X-Frame-Options "SAMEORIGIN" always;
add_header X-Content-Type-Options "nosniff" always;
add_header X-XSS-Protection "1; mode=block" always;
add_header Referrer-Policy "strict-origin-when-cross-origin" always;
add_header Content-Security-Policy "default-src 'self'; script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; img-src 'self' data: https:; font-src 'self' https://fonts.gstatic.com; connect-src 'self' https:; frame-ancestors 'self';" always;
add_header Permissions-Policy "camera=(), geolocation=(), microphone=(), payment=()" always;
add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
EOF

    # nginx/html/index.html
    cat > $project_dir/nginx/html/index.html << 'EOF'
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portail des Applications DataViz</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f9f9f9;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        .app-container {
            display: flex;
            flex-wrap: wrap;
            justify-content: space-around;
            gap: 20px;
        }
        .app-card {
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
            width: 250px;
            padding: 20px;
            transition: transform 0.3s ease;
        }
        .app-card:hover {
            transform: translateY(-5px);
        }
        .app-title {
            font-size: 1.2em;
            font-weight: bold;
            color: #3498db;
            margin-bottom: 10px;
        }
        .app-desc {
            margin-bottom: 15px;
            font-size: 0.9em;
        }
        .app-link {
            display: inline-block;
            background-color: #3498db;
            color: white;
            padding: 8px 15px;
            border-radius: 4px;
            text-decoration: none;
            font-weight: bold;
            transition: background-color 0.3s ease;
        }
        .app-link:hover {
            background-color: #2980b9;
        }
        footer {
            margin-top: 40px;
            text-align: center;
            font-size: 0.8em;
            color: #7f8c8d;
        }
    </style>
</head>
<body>
    <h1>Portail des Applications DataViz</h1>
    
    <div class="app-container">
        <div class="app-card">
            <div class="app-title">EGRA/EGMA DataVizir</div>
            <div class="app-desc">Visualisation des données EGRA/EGMA pour analyse des compétences fondamentales.</div>
            <a href="/egra/" class="app-link">Accéder</a>
        </div>
        
        <div class="app-card">
            <div class="app-title">PupilCard DataVizir</div>
            <div class="app-desc">Analyse visuelle des données de cartes d'élèves et de leurs performances.</div>
            <a href="/pupilcard/" class="app-link">Accéder</a>
        </div>
        
        <div class="app-card">
            <div class="app-title">Contextual DataVizir</div>
            <div class="app-desc">Visualisation de données contextuelles pour l'analyse approfondie.</div>
            <a href="/contextual/" class="app-link">Accéder</a>
        </div>
    </div>
    
    <footer>
        &copy; 2025 - Portail DataViz - Tous droits réservés
    </footer>
</body>
</html>
EOF

    # Template Dockerfile pour les applications Streamlit
    for app_dir in egra_egma_datavizir pupilcard_datavizir contextual_datavizir; do
        cat > $project_dir/apps/$app_dir/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Créer un utilisateur non-root pour l'application
RUN groupadd -r streamlit && useradd -r -g streamlit streamlit

# Installer les dépendances de base
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libc6-dev \
    && rm -rf /var/lib/apt/lists/*

# Installer les dépendances Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copier l'application et les configurations
COPY app.py ./
COPY .streamlit /app/.streamlit

# Créer un dossier pour les données persistantes
RUN mkdir -p /app/data && chown -R streamlit:streamlit /app

# Exposer le port Streamlit
EXPOSE 8501

# Passer à l'utilisateur non-root
USER streamlit

# Commande de démarrage
CMD ["streamlit", "run", "app.py", \
     "--server.port=8501", \
     "--server.address=0.0.0.0", \
     "--server.headless=true"]
EOF

        # Exemple de requirements.txt pour chaque application
        cat > $project_dir/apps/$app_dir/requirements.txt << 'EOF'
streamlit==1.31.1
pandas==2.1.4
numpy==1.26.3
matplotlib==3.8.2
plotly==5.18.0
pydeck==0.8.0
watchdog==3.0.0
EOF

        # Exemple minimal d'application Streamlit
        cat > $project_dir/apps/$app_dir/app.py << EOF
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Configuration de la page
st.set_page_config(
    page_title="${app_dir}",
    page_icon="📊",
    layout="wide"
)

# Titre et description
st.title("Application ${app_dir}")
st.markdown("Bienvenue dans l'application de visualisation de données.")

# Exemple de données fictives
data = pd.DataFrame({
    'x': np.random.normal(0, 1, 100),
    'y': np.random.normal(0, 1, 100)
})

# Visualisation
st.subheader("Exemple de visualisation")
fig, ax = plt.subplots()
ax.scatter(data['x'], data['y'], alpha=0.5)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Nuage de points')
st.pyplot(fig)

# Sidebar
st.sidebar.title("Options")
st.sidebar.markdown("Ce panneau latéral peut contenir des options de filtrage.")

# Informations supplémentaires
st.info("Cette application est un exemple. Remplacez-la par votre code réel.")
EOF

        # Créer le dossier .streamlit et le fichier de configuration
        mkdir -p $project_dir/apps/$app_dir/.streamlit
        cat > $project_dir/apps/$app_dir/.streamlit/config.toml << 'EOF'
[server]
enableCORS = true
enableXsrfProtection = true
maxUploadSize = 200
maxMessageSize = 200

[browser]
gatherUsageStats = false
EOF
    done

    # Scripts d'automatisation et de maintenance
    mkdir -p $project_dir/scripts

    # Script de renouvellement des certificats
    cat > $project_dir/scripts/renew-certs.sh << 'EOF'
#!/bin/bash
set -e

# Renouveler les certificats
certbot renew --quiet

# Redémarrer Nginx pour appliquer les nouveaux certificats
docker compose restart nginx

# Journal de renouvellement
echo "Certificats Let's Encrypt renouvelés le $(date)" >> /var/log/letsencrypt-renew.log
EOF

    # Script de sauvegarde
    cat > $project_dir/scripts/backup.sh << 'EOF'
#!/bin/bash
set -e

# Configuration
BACKUP_DIR="/home/deployer/backups"
DATE=$(date +%Y-%m-%d_%H-%M-%S)
DATA_DIR="/home/deployer/streamlit-project/data"
BACKUP_FILE="${BACKUP_DIR}/streamlit_backup_${DATE}.tar.gz"

# Créer le répertoire de sauvegarde s'il n'existe pas
mkdir -p "${BACKUP_DIR}"

# Sauvegarde des données
echo "Sauvegarde des données en cours..."
tar -czf "${BACKUP_FILE}" -C "${DATA_DIR}" .

# Sauvegarde des configurations
echo "Sauvegarde des configurations en cours..."
tar -rf "${BACKUP_FILE}" -C "/home/deployer/streamlit-project" .env docker-compose.yml
tar -rf "${BACKUP_FILE}" -C "/home/deployer/streamlit-project/nginx" conf html
tar -rf "${BACKUP_FILE}" -C "/home/deployer/streamlit-project/certbot" conf

# Compression finale
gzip -f "${BACKUP_FILE}"

# Rotation des sauvegardes (garder les 7 plus récentes)
ls -t "${BACKUP_DIR}"/streamlit_backup_*.tar.gz | tail -n +8 | xargs -r rm

echo "Sauvegarde terminée : ${BACKUP_FILE}"
EOF

    # Script de vérification d'état
    cat > $project_dir/scripts/check-status.sh << 'EOF'
#!/bin/bash

# Configuration des couleurs
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m' # No Color

# Chemin du projet
PROJECT_DIR="/home/deployer/streamlit-project"

# Se déplacer dans le répertoire du projet
cd "${PROJECT_DIR}"

# Vérifier l'état des conteneurs
echo -e "${YELLOW}Vérification de l'état des conteneurs...${NC}"
echo "-------------------------------------------------"

containers=("egra_app" "pupilcard_app" "contextual_app" "nginx_proxy")

for container in "${containers[@]}"; do
    status=$(docker inspect -f '{{.State.Status}}' "${container}" 2>/dev/null || echo "not_found")
    health=$(docker inspect -f '{{if .State.Health}}{{.State.Health.Status}}{{else}}N/A{{end}}' "${container}" 2>/dev/null || echo "N/A")
    
    if [ "${status}" == "running" ]; then
        if [ "${health}" == "healthy" ] || [ "${health}" == "N/A" ]; then
            echo -e "${GREEN}✓ ${container} : En cours d'exécution${NC}"
        else
            echo -e "${YELLOW}⚠ ${container} : En cours d'exécution, mais état de santé : ${health}${NC}"
        fi
    elif [ "${status}" == "not_found" ]; then
        echo -e "${RED}✗ ${container} : Conteneur non trouvé${NC}"
    else
        echo -e "${RED}✗ ${container} : ${status}${NC}"
    fi
done

echo "-------------------------------------------------"

# Vérifier l'espace disque
echo -e "${YELLOW}Utilisation de l'espace disque :${NC}"
df -h | grep -E '(Filesystem|/dev/sda|/$)'

# Vérifier les certificats SSL
if [ -d "${PROJECT_DIR}/certbot/conf/live" ]; then
    domain=$(ls "${PROJECT_DIR}/certbot/conf/live" | head -n 1)
    if [ -n "${domain}" ]; then
        expiry=$(openssl x509 -enddate -noout -in "${PROJECT_DIR}/certbot/conf/live/${domain}/cert.pem" | cut -d= -f2)
        echo -e "${YELLOW}Expiration des certificats SSL pour ${domain} : ${expiry}${NC}"
    fi
fi

# Vérifier les journaux d'erreur de Nginx
echo -e "${YELLOW}Dernières erreurs Nginx :${NC}"
docker logs nginx_proxy --tail 20 2>&1 | grep -i error

echo "-------------------------------------------------"
echo -e "${GREEN}Vérification terminée.${NC}"
EOF

    # Rendre les scripts exécutables
    chmod +x $project_dir/scripts/*.sh
    
    log_info "Tous les fichiers du projet ont été générés."
}

# ================================================================
# 4. CONFIGURATION SSL ET DÉMARRAGE
# ================================================================

configure_ssl() {
    log_info "Configuration du SSL avec Let's Encrypt..."
    
    local project_dir="/home/deployer/streamlit-project"
    
    # Démarrer nginx pour validation du domaine
    cd $project_dir
    docker compose -f docker-compose.initial.yml up -d
    
    # Attendre que nginx soit prêt
    sleep 10
    
    # Obtenir les certificats Let's Encrypt
    certbot certonly --webroot \
        --webroot-path=$project_dir/certbot/www \
        --email $EMAIL_ADMIN \
        --agree-tos \
        --no-eff-email \
        -d $DOMAIN_NAME
    
    # Créer les fichiers SSL nécessaires pour Nginx s'ils n'existent pas
    if [ ! -f "$project_dir/certbot/conf/options-ssl-nginx.conf" ]; then
        curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot-nginx/certbot_nginx/_internal/tls_configs/options-ssl-nginx.conf > "$project_dir/certbot/conf/options-ssl-nginx.conf"
    fi
    
    if [ ! -f "$project_dir/certbot/conf/ssl-dhparams.pem" ]; then
        curl -s https://raw.githubusercontent.com/certbot/certbot/master/certbot/certbot/ssl-dhparams.pem > "$project_dir/certbot/conf/ssl-dhparams.pem"
    fi
    
    # Arrêter la configuration initiale
    docker compose -f docker-compose.initial.yml down
    
    log_info "Configuration SSL terminée."
}

start_services() {
    log_info "Démarrage des services..."
    
    local project_dir="/home/deployer/streamlit-project"
    
    # Aller dans le répertoire du projet
    cd $project_dir
    
    # Démarrer tous les services
    docker compose up -d --build
    
    # Vérifier l'état des services
    docker compose ps
    
    log_info "Services démarrés avec succès."
}

configure_cron_jobs() {
    log_info "Configuration des tâches cron..."
    
    # Planifier le renouvellement des certificats
    (crontab -l 2>/dev/null; echo "0 3 * * * /home/deployer/streamlit-project/scripts/renew-certs.sh") | crontab -
    
    # Planifier les sauvegardes quotidiennes
    (crontab -l 2>/dev/null; echo "0 2 * * * /home/deployer/streamlit-project/scripts/backup.sh") | crontab -
    
    log_info "Tâches cron configurées."
}

# ================================================================
# EXÉCUTION PRINCIPALE
# ================================================================

main() {
    log_info "Démarrage de l'installation automatisée..."
    
    # Vérifier les privilèges root
    check_root
    
    # Préparer le système
    update_system
    install_dependencies
    create_user
    configure_firewall
    
    # Installer Docker
    install_docker
    test_docker
    
    # Configurer le projet
    setup_project_structure
    generate_project_files
    
    # Configurer SSL et démarrer les services
    configure_ssl
    start_services
    configure_cron_jobs
    
    log_info "Installation automatisée terminée avec succès!"
    log_info "Votre serveur est accessible à l'adresse: https://$DOMAIN_NAME"
    log_info "Pour vérifier l'état du système, exécutez: sudo -u deployer /home/deployer/streamlit-project/scripts/check-status.sh"
}

# Exécuter le script principal
main
