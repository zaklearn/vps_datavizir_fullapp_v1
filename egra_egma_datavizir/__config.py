# config.py
import locale
from datetime import datetime

# Available languages
AVAILABLE_LANGUAGES = {
    "en": {"name": "English", "locale": "en_US.UTF-8", "flag": "🇬🇧"},
    "fr": {"name": "Français", "locale": "fr_FR.UTF-8", "flag": "🇫🇷"},
    # Add more languages here in the future
}

# Default language
DEFAULT_LANGUAGE = "en"

# Translation dictionary
translations = {
    "en": {
        # Application title and navigation
        "app_title": "Educational Assessment Analytics",
        "welcome": "Welcome to the Educational Assessment Analytics application",
        "language_selector": "Select Language",
        "nav_title": "Navigation",
        "select_analysis": "Select Analysis Type",
        
        # Data loading and management
        "upload_file": "Upload Data File",
        "upload_help": "Supported formats: CSV, Excel, JSON, Stata DTA",
        "upload_info": "Please upload a file to begin analysis",
        "loading_data": "Loading data...",
        "upload_success": "File loaded successfully:",
        "upload_error": "Error loading file:",
        "select_sheet": "Select sheet",
        "select_encoding": "Encoding",
        "select_separator": "Separator",
        "rows_count": "Number of rows",
        "columns_count": "Number of columns",
        "show_preview": "Show data preview",
        "show_dtypes": "Show data types",
        
        # Error messages
        "encoding_error": "Encoding error. Try another encoding.",
        "parser_error": "Reading error. Check file format.",
        "value_error": "Value error. File might be corrupted.",
        "no_data_error": "Please upload data before running analysis.",
        
        # Analysis module titles
        "analysis1_title": "Statistical Overview",
        "analysis2_title": "Zero Scores Analysis",
        "analysis3_title": "School Comparison",
        "analysis4_title": "Language Effect Analysis",
        "analysis5_title": "Correlation Analysis",
        "analysis6_title": "Test Reliability (Cronbach Alpha)",
        "analysis7_title": "School Performance Analysis",
        "analysis8_title": "Contextual Factors Analysis",
        "analysis10_title": "Gender Effect Analysis",
        "analysis12_title": "International Standards Comparison",
        "analysis13_title": "Language of Instruction Comparison",
        
        # Common UI elements
        "select_variables": "Select Variables",
        "select_indicators": "Select Indicators",
        "export_csv": "Download CSV",
        "export_excel": "Download Excel",
        "export_word": "Export to Word",
        "export_ppt": "Export to PowerPoint",
        "download_word": "Download Word Report",
        "download_ppt": "Download PowerPoint",
        "generate_report": "Generate Report",
        "warning_select_variable": "Please select at least one variable to analyze.",
        
        # Educational assessment terminology
        "score": "Score",
        "mean_score": "Mean Score",
        "median_score": "Median Score",
        "std_dev": "Standard Deviation",
        "min_score": "Minimum Score",
        "max_score": "Maximum Score",
        "percentile_25": "25th Percentile",
        "percentile_50": "50th Percentile (Median)",
        "percentile_75": "75th Percentile",
        "distribution": "Distribution",
        "histogram": "Histogram",
        "frequency": "Frequency",
        "count": "Count",
        "percentage": "Percentage",
        "correlation": "Correlation",
        "significance": "Statistical Significance",
        "p_value": "p-value",
        "significant_difference": "Significant Difference",
        "no_significant_difference": "No Significant Difference",
        "columns_of_interest":{
             # Assessment variables
        "clpm": "Correct Letters Per Minute",
        "phoneme": "Phoneme Awareness",
        "sound_word": "Correctly Read Words",
        "cwpm": "Correct Words Per Minute",
        "listening": "Listening Comprehension",
        "orf": "Oral Reading Fluency",
        "comprehension": "Reading Comprehension",
        "number_id": "Number Identification",
        "discrimin": "Number Discrimination",
        "missing_number": "Missing Number",
        "addition": "Addition",
        "subtraction": "Subtraction",
        "problems": "Problems"
        },
       
        
        # Grouping variables
        "school": "School",
        "gender": "Gender",
        "boy": "Boy",
        "girl": "Girl",
        "language_teaching": "Language of Instruction",
        "english": "English",
        "dutch": "Dutch",
        "language_home": "Home Language",
        
        # Report and visualization elements
        "report_title": "Analysis Report",
        "report_date": "Report generated on",
        "executive_summary": "Executive Summary",
        "key_findings": "Key Findings",
        "recommendations": "Recommendations",
        "methodology": "Methodology",
        "conclusion": "Conclusion",
        "appendix": "Appendix",
        "figure": "Figure",
        "table": "Table",
        "page": "Page",
        "of": "of",
        
        # Dates and numbers formatting
        "date_format": "%B %d, %Y",
        "date_format_short": "%m/%d/%Y",
        "decimal_separator": ".",
        "thousands_separator": ",",
        "percentage_format": "{:.1f}%",
        
        # Assessment levels and interpretations
        "critical_level": "Critical",
        "concerning_level": "Concerning",
        "watch_level": "Watch",
        "satisfactory_level": "Satisfactory",
        "excellent_level": "Excellent",
        
        # Zero scores interpretation
        "zero_score_critical": "Critical concern - Immediate intervention required",
        "zero_score_concerning": "Concerning - Targeted support needed",
        "zero_score_watch": "Monitor closely - Provide additional practice",
        "zero_score_satisfactory": "Satisfactory - Continue with current approach"
    },
    
    "fr": {
        # Application title and navigation
        "app_title": "Analyse d'Évaluations Éducatives",
        "welcome": "Bienvenue dans l'application d'Analyse d'Évaluations Éducatives",
        "language_selector": "Sélectionner la Langue",
        "nav_title": "Navigation",
        "select_analysis": "Sélectionner le Type d'Analyse",
        
        # Data loading and management
        "upload_file": "Télécharger un Fichier de Données",
        "upload_help": "Formats supportés : CSV, Excel, JSON, Stata DTA",
        "upload_info": "Veuillez télécharger un fichier pour commencer l'analyse",
        "loading_data": "Chargement des données...",
        "upload_success": "Fichier chargé avec succès :",
        "upload_error": "Erreur lors du chargement du fichier :",
        "select_sheet": "Sélectionner une feuille",
        "select_encoding": "Encodage",
        "select_separator": "Séparateur",
        "rows_count": "Nombre de lignes",
        "columns_count": "Nombre de colonnes",
        "show_preview": "Afficher un aperçu des données",
        "show_dtypes": "Afficher les types de données",
        
        # Error messages
        "encoding_error": "Erreur d'encodage. Essayez un autre encodage.",
        "parser_error": "Erreur de lecture. Vérifiez le format du fichier.",
        "value_error": "Erreur de valeur. Le fichier pourrait être corrompu.",
        "no_data_error": "Veuillez télécharger des données avant de lancer l'analyse.",
        
        # Analysis module titles
        "analysis1_title": "Aperçu Statistique",
        "analysis2_title": "Analyse des Scores Zéro",
        "analysis3_title": "Comparaison entre Écoles",
        "analysis4_title": "Analyse de l'Effet de la Langue",
        "analysis5_title": "Analyse des Corrélations",
        "analysis6_title": "Fiabilité des Tests (Alpha de Cronbach)",
        "analysis7_title": "Analyse de Performance par École",
        "analysis8_title": "Analyse des Facteurs Contextuels",
        "analysis10_title": "Analyse de l'Effet du Genre",
        "analysis12_title": "Comparaison aux Standards Internationaux",
        "analysis13_title": "Comparaison par Langue d'Instruction",
        
        # Common UI elements
        "select_variables": "Sélectionner les Variables",
        "select_indicators": "Sélectionner les Indicateurs",
        "export_csv": "Télécharger CSV",
        "export_excel": "Télécharger Excel",
        "export_word": "Exporter en Word",
        "export_ppt": "Exporter en PowerPoint",
        "download_word": "Télécharger le Rapport Word",
        "download_ppt": "Télécharger PowerPoint",
        "generate_report": "Générer le Rapport",
        "warning_select_variable": "Veuillez sélectionner au moins une variable à analyser.",
        
        # Educational assessment terminology
        "score": "Score",
        "mean_score": "Score Moyen",
        "median_score": "Score Médian",
        "std_dev": "Écart-Type",
        "min_score": "Score Minimum",
        "max_score": "Score Maximum",
        "percentile_25": "25ème Percentile",
        "percentile_50": "50ème Percentile (Médiane)",
        "percentile_75": "75ème Percentile",
        "distribution": "Distribution",
        "histogram": "Histogramme",
        "frequency": "Fréquence",
        "count": "Nombre",
        "percentage": "Pourcentage",
        "correlation": "Corrélation",
        "significance": "Signification Statistique",
        "p_value": "Valeur p",
        "significant_difference": "Différence Significative",
        "no_significant_difference": "Pas de Différence Significative",
        "columns_of_interest":{
            # Assessment variables
            "clpm": "Lettres Correctes Par Minute",
            "phoneme": "Conscience Phonémique",
            "sound_word": "Mots Lus Correctement",
            "cwpm": "Mots Corrects Par Minute",
            "listening": "Compréhension Orale",
            "orf": "Fluidité de Lecture Orale",
            "comprehension": "Compréhension de Lecture",
            "number_id": "Identification des Nombres",
            "discrimin": "Discrimination des Nombres",
            "missing_number": "Nombre Manquant",
            "addition": "Addition",
            "subtraction": "Soustraction",
            "problems": "Problèmes"
        },
        
        
        # Grouping variables
        "school": "École",
        "gender": "Genre",
        "boy": "Garçon",
        "girl": "Fille",
        "language_teaching": "Langue d'Enseignement",
        "english": "Anglais",
        "dutch": "Néerlandais",
        "language_home": "Langue à la Maison",
        
        # Report and visualization elements
        "report_title": "Rapport d'Analyse",
        "report_date": "Rapport généré le",
        "executive_summary": "Résumé Exécutif",
        "key_findings": "Résultats Clés",
        "recommendations": "Recommandations",
        "methodology": "Méthodologie",
        "conclusion": "Conclusion",
        "appendix": "Annexe",
        "figure": "Figure",
        "table": "Tableau",
        "page": "Page",
        "of": "sur",
        
        # Dates and numbers formatting
        "date_format": "%d %B %Y",
        "date_format_short": "%d/%m/%Y",
        "decimal_separator": ",",
        "thousands_separator": " ",
        "percentage_format": "{:.1f} %",
        
        # Assessment levels and interpretations
        "critical_level": "Critique",
        "concerning_level": "Préoccupant",
        "watch_level": "À Surveiller",
        "satisfactory_level": "Satisfaisant",
        "excellent_level": "Excellent",
        
        # Zero scores interpretation
        "zero_score_critical": "Préoccupation critique - Intervention immédiate requise",
        "zero_score_concerning": "Préoccupant - Soutien ciblé nécessaire",
        "zero_score_watch": "Surveiller de près - Fournir des exercices supplémentaires",
        "zero_score_satisfactory": "Satisfaisant - Continuer avec l'approche actuelle"
    }
}

class LanguageManager:
    """
    Manager for handling translations and localization in the application.
    """
    
    def __init__(self, initial_language=DEFAULT_LANGUAGE):
        """
        Initialize the language manager with a default language.
        
        Args:
            initial_language (str): Initial language code (default: from DEFAULT_LANGUAGE)
        """
        self.current_language = initial_language if initial_language in AVAILABLE_LANGUAGES else DEFAULT_LANGUAGE
        self._set_locale()
    
    def _set_locale(self):
        """Set the system locale based on the current language."""
        try:
            locale.setlocale(locale.LC_ALL, AVAILABLE_LANGUAGES[self.current_language]["locale"])
        except locale.Error:
            # Fall back to basic locale if specific one not available
            try:
                basic_locale = self.current_language + ".UTF-8"
                locale.setlocale(locale.LC_ALL, basic_locale)
            except locale.Error:
                # If all else fails, use system default
                locale.setlocale(locale.LC_ALL, '')
    
    def get_text(self, key, default=""):
        """
        Get translated text for a specific key.
        
        Args:
            key (str): Translation key
            default (str): Default value if key not found
            
        Returns:
            str: Translated text
        """
        return translations.get(self.current_language, {}).get(key, default)
    
    def get_all_texts(self):
        """
        Get all translations for the current language.
        
        Returns:
            dict: All translations for current language
        """
        return translations.get(self.current_language, {})
    
    def change_language(self, language_code):
        """
        Change the current language.
        
        Args:
            language_code (str): Language code to switch to
            
        Returns:
            bool: True if language was changed, False if language code was invalid
        """
        if language_code in AVAILABLE_LANGUAGES:
            self.current_language = language_code
            self._set_locale()
            return True
        return False
    
    def get_available_languages(self):
        """
        Get list of available languages.
        
        Returns:
            dict: Available languages with metadata
        """
        return AVAILABLE_LANGUAGES
    
    def format_number(self, number, decimal_places=2):
        """
        Format a number according to locale conventions.
        
        Args:
            number (float): Number to format
            decimal_places (int): Number of decimal places
            
        Returns:
            str: Formatted number
        """
        # Get separators from translation dictionary
        decimal_sep = self.get_text("decimal_separator", ".")
        thousands_sep = self.get_text("thousands_separator", ",")
        
        # Format with locale settings
        try:
            if decimal_places == 0:
                return locale.format_string("%d", number, grouping=True)
            else:
                locale_format = f"%.{decimal_places}f"
                formatted = locale.format_string(locale_format, number, grouping=True)
                
                # Replace with custom separators if they don't match locale
                if locale.localeconv()['decimal_point'] != decimal_sep:
                    formatted = formatted.replace(locale.localeconv()['decimal_point'], decimal_sep)
                
                if locale.localeconv()['thousands_sep'] != thousands_sep:
                    formatted = formatted.replace(locale.localeconv()['thousands_sep'], thousands_sep)
                
                return formatted
        except:
            # Fallback method if locale formatting fails
            if decimal_places == 0:
                return format(int(number), ",").replace(",", thousands_sep)
            else:
                return format(round(number, decimal_places), f",.{decimal_places}f").replace(",", thousands_sep).replace(".", decimal_sep)
    
    def format_percentage(self, value):
        """
        Format a value as a percentage according to locale conventions.
        
        Args:
            value (float): Value to format as percentage (0.1 = 10%)
            
        Returns:
            str: Formatted percentage
        """
        percentage_format = self.get_text("percentage_format", "{:.1f}%")
        return percentage_format.format(value * 100)
    
    def format_date(self, date, short=False):
        """
        Format a date according to locale conventions.
        
        Args:
            date (datetime): Date to format
            short (bool): Whether to use short date format
            
        Returns:
            str: Formatted date
        """
        if short:
            date_format = self.get_text("date_format_short", "%m/%d/%Y")
        else:
            date_format = self.get_text("date_format", "%B %d, %Y")
        
        if isinstance(date, datetime):
            return date.strftime(date_format)
        else:
            return date


# Create a global instance of the language manager
language_manager = LanguageManager()

# Export commonly used assessment variables
egra_columns = ["clpm", "phoneme", "sound_word", "cwpm", "listening", "orf", "comprehension"]
egma_columns = ["number_id", "discrimin", "missing_number", "addition", "subtraction", "problems"]