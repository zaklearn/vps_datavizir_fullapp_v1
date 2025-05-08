# config.py - Centralized configuration for the application (English only)

"""
This module provides centralized configuration for the application,
including paths, constants, standards, and translations.
"""

import os

# Application paths
APP_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(APP_DIR, "data")
TEMP_DIR = os.path.join(APP_DIR, "temp")

# Make sure directories exist
for directory in [DATA_DIR, TEMP_DIR]:
    if not os.path.exists(directory):
        os.makedirs(directory)

# Application constants
APP_VERSION = "3.0.2"
APP_NAME = "Datavizir Pupil Clsch"
DEFAULT_LANGUAGE = "en"

# Standard evaluation thresholds for each category
STANDARDS = {
    # EGRA standards
    "clpm": {"Mastery": 44, "Developing": (31, 43), "Emerging": (0, 30)},
    "phoneme": {"Mastery": 41, "Developing": (24, 40), "Emerging": (0, 23)},
    "sound_word": {"Mastery": 60, "Developing": (30, 59), "Emerging": (0, 29)},
    "cwpm": {"Mastery": 29, "Developing": (17, 28), "Emerging": (0, 16)},
    "listening": {"Mastery": 75, "Developing": (50, 74), "Emerging": (0, 49)},
    "orf": {"Mastery": 50, "Developing": (30, 49), "Emerging": (0, 29)},
    "comprehension": {"Mastery": 75, "Developing": (50, 74), "Emerging": (0, 49)},
    
    # EGMA standards
    "number_id": {"Mastery": 56, "Developing": (49, 55), "Emerging": (0, 48)},
    "discrimin": {"Mastery": 60, "Developing": (30, 59), "Emerging": (0, 29)},
    "missing_number": {"Mastery": 60, "Developing": (30, 59), "Emerging": (0, 29)},
    "addition": {"Mastery": 10, "Developing": (6, 9), "Emerging": (0, 5)},
    "subtraction": {"Mastery": 10, "Developing": (6, 9), "Emerging": (0, 5)},
    "problems": {"Mastery": 60, "Developing": (30, 59), "Emerging": (0, 29)}
}

# Group indicators by assessment type for easier access
EGRA_INDICATORS = ["clpm", "phoneme", "sound_word", "cwpm", "listening", "orf", "comprehension"]
EGMA_INDICATORS = ["number_id", "discrimin", "missing_number", "addition", "subtraction", "problems"]

# English translations only
TRANSLATIONS = {
    # General UI elements
    "app_title": "Performance Analysis",
    "data_source": "Data Source",
    "upload_excel": "Or load an Excel file",
    "choose_data": "Please choose a data source",
    "navigation": "Navigation",
    "use_demo": "Use demo data",
    "choose_application": "Choose application",
    
    # Pupil Report Card module
    "pupil_report_card": "Pupil Report Card",
    "view_list": "View complete student list",
    "search_student": "Search for a student",
    "complete_list": "Complete Student List",
    "return_list": "Return to list",
    "search_title": "Search for a student",
    "profile_for": "Profile for",
    "student_perf": "Student Performance",
    "age": "Age",
    "gender": "Gender",
    "language": "Language",
    "class": "Class",
    "years": "years",
    "boy": "Boy",
    "girl": "Girl",
    "no_data": "No data available for",
    "export_report": "Export report",
    "export_word": "Export to Word",
    "download": "Download Word report",
    "success_report": "Word report generated successfully!",
    "error_report": "Error generating report",
    "no_student": "No student found with ID",
    "what_to_do": "What would you like to do?",
    "student_list": "Student List",
    "student": "Student",
    "view_profile": "View Profile",
    "name": "Name",
    "student_report": "Student Report",
    "report_for": "Report for",
    "personal_info": "Personal Information",
    "missing_columns": "The following columns are missing",
    "required_columns": "Required columns",
    "available_columns": "Available columns",
    "error_data_prep": "Error during data preparation",
    "error_displaying_profile": "Error displaying student profile",
    "no_students_in_class": "No students found in this class",
    "insufficient_data": "Insufficient data to generate a complete report",
    "error_retrieving_data": "Error retrieving student data",
    "unexpected_error": "Unexpected error in student search",
    "error_processing_data": "Error processing student data",
    "problematic_values": "Problematic values",
    "error_creating_table": "Error creating scores table",
    "error_creating_chart": "Error creating chart",
    "error": "Error",
    "egra_egma_required": "EGRA and EGMA scores are required to generate the report",
    "student_info_required": "Student information is required to generate the report",
    "charts_required": "EGRA and EGMA charts are required to generate the report",
    "error_generating_chart": "Error generating chart",
    "error_generating_report": "Error generating report",
    "error_occurred": "An error occurred",
    "comparison": "Comparison",
    "no_data_available": "No data available",
    "please_try_again": "Please try again",
    
    # EGRA/EGMA indicators
    "egra_results": "EGRA Results",
    "egma_results": "EGMA Results",
    "indicator": "Indicator",
    "student_score": "Student Score",
    "standard_score": "Standard Score",
    "status": "Status",
    "mastery": "Mastery",
    "developing": "Developing",
    "emerging": "Emerging",
    
    # Class Comparison module
    "class_comparison": "Class Comparison",
    "select_school": "Select a school",
    "class_insights": "Class Insights",
    "systematic_summary": "Systematic Summary",
    "llm_interpretation": "LLM Interpretation",
    "generate_report": "Generate Report",
    "download_report": "Download Word Report",
    
    # School Comparison module
    "school_comparison": "School Comparison",
    "select_schools": "Select schools to compare",
    "school_insights": "School Insights",
    "school": "School",
    "score": "Score",
    "standard": "Standard",
    
    # Interpretation module
    "interpretation": "Interpretation (hybrid system)",
    "systematic_analysis": "Systematic Analysis",
    "enriched_synthesis": "Enriched Synthesis",
    "interpretation_recs": "Interpretation & Recommendations",
    
    # Labels for indicators
    "clpm": "Letters per minute",
    "phoneme": "Correct phonemes (%)",
    "sound_word": "Words read correctly (%)",
    "cwpm": "Correct words per minute",
    "listening": "Listening comprehension (%)",
    "orf": "Reading fluency",
    "comprehension": "Reading comprehension (%)",
    "number_id": "Number identification",
    "discrimin": "Number discrimination (%)",
    "missing_number": "Missing number (%)",
    "addition": "Additions per minute",
    "subtraction": "Subtractions per minute",
    "problems": "Problems solved (%)"
}

# Default message templates for interpretations (English only)
INTERPRETATION_TEMPLATES = {
    "rule_based": {
        "emerging": "Low performance in {indicator} ({score}). Recommended: additional practice.",
        "developing": "Developing skill in {indicator} ({score}). Recommended: targeted support.",
        "mastery": "Confirmed mastery in {indicator} ({score})."
    },
    "fallback": [
        "Encourage regular reading practice to improve fluency.",
        "Provide targeted exercises for developing skills.",
        "Praise the student for strengths and encourage progress in weaker areas.",
        "Implement review sessions to reinforce basics.",
        "Use educational games to make learning more engaging.",
        "Encourage the student to verbalize reasoning when solving problems.",
        "Suggest group activities to promote peer learning.",
        "Set achievable short-term goals to maintain motivation."
    ]
}

# API configurations (for environment or deployment settings)
API_CONFIG = {
    "anthropic_model": "claude-3-haiku-20240307",
    "max_tokens": 500,
    "temperature": 0.7
}