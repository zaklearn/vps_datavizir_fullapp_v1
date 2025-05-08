# Configuration file for EduInsight

# Define the assessment columns for selection
egra_columns = ["clpm", "phoneme", "sound_word", "cwpm", "listening", "orf", "comprehension"]
egma_columns = ["number_id", "discrimin", "missing_number", "addition", "subtraction", "problems"]

# Define translations for multi-language support
translations = {
    "fr": {
        # General UI elements
        "welcome_title": "Bienvenue sur EduInsight",
        "welcome_message": """
            ### Plateforme d'Analyse EduInsight
            
            **EduInsight** vous aide à analyser comment les facteurs contextuels influencent les performances des élèves.
            
            Cette plateforme se concentre sur cinq dimensions contextuelles clés:
            
            1. **Environnement Scolaire**: Comparez les performances entre différentes écoles
            2. **Contexte Linguistique**: Analysez l'effet de la langue sur l'apprentissage
            3. **Facteurs Contextuels**: Examinez comment les facteurs externes affectent les résultats
            4. **Analyse de Genre**: Explorez les différences de performance selon le genre
            5. **Statut Socio-économique**: Comprenez comment le SES et le soutien familial influencent les résultats
            
            Pour commencer, téléchargez un fichier de données en utilisant la barre latérale à gauche, puis sélectionnez un type d'analyse.
        """,
        "data_format": "Format de Données Requis",
        "data_format_details": """
            Votre ensemble de données doit inclure les variables clés suivantes:
            
            - `school`: Identifiant de l'école
            - `stgender`: Genre de l'élève (codé comme 0/1)
            - `language_teaching`: Langue d'enseignement
            - `ses`: Statut socio-économique
            - `home_support`: Niveau de soutien à domicile
            
            Les variables de performance (scores de lecture, scores de mathématiques, etc.) doivent également être incluses pour l'analyse.
        """,

        # Navigation and selection
        "select_analysis": "Sélectionnez une analyse",
        "upload_file": "Télécharger un fichier de données",
        "upload_help": "Formats supportés: Excel et CSV",
        "upload_info": "Veuillez télécharger un fichier pour commencer l'analyse",
        "loading_data": "Chargement des données...",
        "select_sheet": "Sélectionner une feuille",
        "select_encoding": "Encodage",
        "select_separator": "Séparateur",
        "rows_count": "Nombre de lignes",
        "columns_count": "Nombre de colonnes",
        "show_preview": "Afficher un aperçu des données",
        "upload_success": "Fichier chargé avec succès",
        "missing_columns": "Colonnes requises manquantes",
        "column_info": "Cette application nécessite des variables contextuelles pour l'analyse.",

        # Error messages
        "encoding_error": "Erreur d'encodage. Essayez un encodage différent.",
        "parser_error": "Erreur d'analyse. Vérifiez le format du fichier.",
        "value_error": "Erreur de valeur. Le fichier pourrait être corrompu.",
        "upload_error": "Erreur lors du chargement du fichier",
        "analysis_error": "Erreur dans l'analyse",

        # Analysis titles
        "title_school_comparison": "Comparaison entre Écoles",
        "title_language_effect": "Effet de la Langue",
        "title_contextual_factors": "Facteurs Contextuels",
        "title_gender_effect": "Effet du Genre",
        "title_ses_home_support": "SES et Soutien Familial",

        # Common analysis elements
        "select_variables": "Sélectionnez les variables",
        "variables_all": "Variables",
        "download_csv": "Télécharger en CSV",
        "export_word": "Exporter en Word",
        "download_word": "Télécharger le rapport Word",
        "warning_select_variable": "Veuillez sélectionner au moins une variable à analyser.",
        
        # School comparison elements
        "table_school_comparison": "Statistiques descriptives par école",
        "export_school_comparison_csv": "Télécharger en CSV",
        "export_school_comparison_word": "Exporter en Word",
        "download_school_comparison_word": "Télécharger le rapport Word",
        "school_comparison_chart_title": "Distribution des scores par école",
        "warning_select_indicator": "Veuillez sélectionner au moins un indicateur à analyser.",
        
        # Language effect elements
        "table_language_effect": "Statistiques descriptives par groupe linguistique",
        "export_language_effect_csv": "Télécharger en CSV",
        "export_language_effect_word": "Exporter en Word",
        "download_language_effect_word": "Télécharger le rapport Word",
        "language_effect_chart_title": "Distribution des scores par groupe linguistique",
        "language_group": "Groupe linguistique",
        
        # Gender analysis elements
        "gender": "Genre",
        "boy": "Garçon",
        "girl": "Fille",
        "unknown": "Inconnu",
        "mean_score_gender": "Score moyen par genre et par tâche",
        "score_distribution_gender": "Distribution des scores selon le genre",
        "stat_tests": "Tests statistiques (Mann-Whitney)",
        "significant": "Différence significative",
        "not_significant": "Pas de différence significative",
        
        # SES analysis elements
        "title_ses_home_support": "Impact du SES et du Soutien Parental",
        "ses_relation": "Relation entre SES et les Scores",
        "home_support_impact": "Impact du Soutien Parental sur les Scores",
        "correlation_matrix": "Matrice de Corrélation",
        "ses": "Statut Socio-Économique",
        "home_support": "Soutien Parental",
        "total_score": "Score Total",
        
        # Contextual factors elements
        "ses_relation": "Relation entre SES et Scores",
        "home_support_impact": "Impact du Soutien Parental sur les Scores",
        "language_impact": "Impact de la Langue Parlée à la Maison",
        
        # Column translations
        "columns_of_interest": {
            "clpm": "Lettres Correctes Par Minute",
            "phoneme": "Phonème",
            "sound_word": "Mot Lu Correctement",
            "cwpm": "Mots Corrects Par Minute",
            "listening": "Écoute",
            "orf": "Fluidité de Lecture Orale",
            "comprehension": "Compréhension",
            "number_id": "Identification des Nombres",
            "discrimin": "Discrimination des Nombres",
            "missing_number": "Nombre Manquant",
            "addition": "Addition",
            "subtraction": "Soustraction",
            "problems": "Résolution de Problèmes",
            "st_nb_miss_school": "Nombre d'Absences",
            "st_nb_beenlate_school": "Nombre de Retards",
            "ses": "Statut Socio-Économique",
            "home_support": "Soutien à la Maison"
        },
        
        # Score columns
        "score_columns": {
            "clpm": "Lettres Correctes Par Minute",
            "phoneme": "Phonème",
            "sound_word": "Mot Lu Correctement",
            "cwpm": "Mots Corrects Par Minute",
            "listening": "Écoute",
            "orf": "Fluidité de Lecture Orale",
            "comprehension": "Compréhension",
            "number_id": "Identification des Nombres",
            "discrimin": "Discrimination des Nombres",
            "missing_number": "Nombre Manquant",
            "addition": "Addition",
            "subtraction": "Soustraction",
            "problems": "Résolution de Problèmes"
        },
        
        # Report elements
        "histogram_title": "Distribution de {}",
        "distribution": "Distribution",
        "export_csv": "Télécharger en CSV",
        "export_word": "Exporter en Word",
        "download_word": "Télécharger le rapport Word",
        "error_message": "Une erreur est survenue"
    },
    
    "en": {
        # General UI elements
        "welcome_title": "Welcome to EduInsight",
        "welcome_message": """
            ### EduInsight Analytics Platform
            
            **EduInsight** helps you analyze how contextual factors impact student performance.
            
            This platform focuses on five key contextual dimensions:
            
            1. **School Environment**: Compare performance across different schools
            2. **Language Background**: Analyze the effect of language on learning
            3. **Contextual Factors**: Examine how external factors affect outcomes
            4. **Gender Analysis**: Explore performance differences by gender
            5. **Socioeconomic Status**: Understand how SES and home support influence results
            
            To begin, upload a data file using the sidebar on the left, then select an analysis type.
        """,
        "data_format": "Required Data Format",
        "data_format_details": """
            Your dataset should include the following key variables:
            
            - `school`: School identifier
            - `stgender`: Student gender (coded as 0/1)
            - `language_teaching`: Language of instruction
            - `ses`: Socioeconomic status
            - `home_support`: Level of home support
            
            Performance variables (reading scores, math scores, etc.) should also be included for analysis.
        """,
        
        # Navigation and selection
        "select_analysis": "Select Analysis",
        "upload_file": "Upload data file",
        "upload_help": "Supported formats: Excel and CSV",
        "upload_info": "Please upload a file to begin analysis",
        "loading_data": "Loading data...",
        "select_sheet": "Select sheet",
        "select_encoding": "Encoding",
        "select_separator": "Separator",
        "rows_count": "Rows",
        "columns_count": "Columns",
        "show_preview": "Show data preview",
        "upload_success": "File loaded successfully",
        "missing_columns": "Missing required columns",
        "column_info": "This application requires contextual variables for analysis.",
        
        # Error messages
        "encoding_error": "Encoding error. Try a different encoding.",
        "parser_error": "Parser error. Check file format.",
        "value_error": "Value error. File may be corrupted.",
        "upload_error": "Error loading file",
        "analysis_error": "Error in analysis",
        
        # Analysis titles
        "title_school_comparison": "School Comparison",
        "title_language_effect": "Language Effect",
        "title_contextual_factors": "Contextual Factors",
        "title_gender_effect": "Gender Effect",
        "title_ses_home_support": "SES & Home Support",
        
        # Common analysis elements
        "select_variables": "Select Variables",
        "variables_all": "Variables",
        "download_csv": "Download CSV",
        "export_word": "Export to Word",
        "download_word": "Download Word Report",
        "warning_select_variable": "Please select at least one variable to analyze.",
        
        # School comparison elements
        "table_school_comparison": "Descriptive Statistics by School",
        "export_school_comparison_csv": "Download CSV",
        "export_school_comparison_word": "Export to Word",
        "download_school_comparison_word": "Download Word Report",
        "school_comparison_chart_title": "Score Distribution by School",
        "warning_select_indicator": "Please select at least one indicator to analyze.",
        
        # Language effect elements
        "table_language_effect": "Descriptive Statistics by Language Group",
        "export_language_effect_csv": "Download CSV",
        "export_language_effect_word": "Export to Word",
        "download_language_effect_word": "Download Word Report",
        "language_effect_chart_title": "Score Distribution by Language Group",
        "language_group": "Language Group",
        
        # Gender analysis elements
        "gender": "Gender",
        "boy": "Boy",
        "girl": "Girl",
        "unknown": "Unknown",
        "mean_score_gender": "Average scores by gender and task",
        "score_distribution_gender": "Score distribution by gender",
        "stat_tests": "Statistical Tests (Mann-Whitney)",
        "significant": "Significant difference",
        "not_significant": "No significant difference",
        
        # SES analysis elements
        "title_ses_home_support": "SES & Home Support Impact",
        "ses_relation": "Relationship Between SES and Scores",
        "home_support_impact": "Impact of Home Support on Scores",
        "correlation_matrix": "Correlation Matrix",
        "ses": "Socioeconomic Status",
        "home_support": "Home Support",
        "total_score": "Total Score",
        
        # Contextual factors elements
        "ses_relation": "Relationship Between SES and Scores",
        "home_support_impact": "Impact of Home Support on Scores",
        "language_impact": "Impact of Home Language",
        
        # Column translations
        "columns_of_interest": {
            "clpm": "Correct Letters Per Minute",
            "phoneme": "Phoneme",
            "sound_word": "Correctly Read Word",
            "cwpm": "Correct Words Per Minute",
            "listening": "Listening",
            "orf": "Oral Reading Fluency",
            "comprehension": "Comprehension",
            "number_id": "Number Identification",
            "discrimin": "Number Discrimination",
            "missing_number": "Missing Number",
            "addition": "Addition",
            "subtraction": "Subtraction",
            "problems": "Problem Solving",
            "st_nb_miss_school": "Number of Absences",
            "st_nb_beenlate_school": "Number of Tardies",
            "ses": "Socioeconomic Status",
            "home_support": "Home Support"
        },
        
        # Score columns
        "score_columns": {
            "clpm": "Correct Letters Per Minute",
            "phoneme": "Phoneme",
            "sound_word": "Correctly Read Word",
            "cwpm": "Correct Words Per Minute",
            "listening": "Listening",
            "orf": "Oral Reading Fluency",
            "comprehension": "Comprehension",
            "number_id": "Number Identification",
            "discrimin": "Number Discrimination",
            "missing_number": "Missing Number",
            "addition": "Addition",
            "subtraction": "Subtraction",
            "problems": "Problem Solving"
        },
        
        # Report elements
        "histogram_title": "Distribution of {}",
        "distribution": "Distribution",
        "export_csv": "Download CSV",
        "export_word": "Export to Word",
        "download_word": "Download Word Report",
        "error_message": "An error occurred"
    }
}

# International benchmarks for comparison
international_benchmarks = {
    "clpm": {"standard": 60, "name": "Correct Letters Per Minute"},
    "phoneme": {"standard": 8, "name": "Phoneme"},
    "sound_word": {"standard": 6, "name": "Correctly Read Word"},
    "cwpm": {"standard": 50, "name": "Correct Words Per Minute"},
    "listening": {"standard": 3, "name": "Listening"},
    "orf": {"standard": 55, "name": "Oral Reading Fluency"},
    "comprehension": {"standard": 4, "name": "Comprehension"},
    "number_id": {"standard": 25, "name": "Number Identification"},
    "discrimin": {"standard": 8, "name": "Number Discrimination"},
    "missing_number": {"standard": 7, "name": "Missing Number"},
    "addition": {"standard": 8, "name": "Addition"},
    "subtraction": {"standard": 7, "name": "Subtraction"},
    "problems": {"standard": 4, "name": "Problem Solving"}
}
