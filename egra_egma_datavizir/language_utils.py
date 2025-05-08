# language_utils.py
import streamlit as st
from config import language_manager, AVAILABLE_LANGUAGES, translations

def setup_language_selector():
    """
    Set up a language selector in the Streamlit sidebar.
    
    Returns:
        str: Selected language code
    """
    # Get current language from session state or use default
    if 'language' not in st.session_state:
        st.session_state.language = language_manager.current_language
    
    # Create language options with flags
    language_options = {
        f"{lang_info['flag']} {lang_info['name']}": code
        for code, lang_info in AVAILABLE_LANGUAGES.items()
    }
    
    # Language selector in sidebar
    selected_display = st.sidebar.selectbox(
        language_manager.get_text("language_selector", "Select Language"),
        options=list(language_options.keys()),
        index=list(language_options.values()).index(st.session_state.language),
        key="language_display"
    )
    
    # Get language code from display name
    selected_language = language_options[selected_display]
    
    # Update session state and language manager if language changed
    if selected_language != st.session_state.language:
        st.session_state.language = selected_language
        language_manager.change_language(selected_language)
        try:
            # Experimental rerun is sometimes unavailable in deployment environments
            st.experimental_rerun()  # Rerun the app to apply language change
        except:
            st.warning("Please refresh the page to fully apply language changes.")
    
    return selected_language

def get_text(key, default=""):
    """
    Get translated text for a specific key.
    Shorthand for language_manager.get_text().
    
    Args:
        key (str): Translation key
        default (str): Default value if key not found
        
    Returns:
        str: Translated text
    """
    # Get language from session state or use default
    language = st.session_state.get('language', language_manager.current_language)
    
    # Try to get translation from translations dictionary directly
    if isinstance(key, dict):
        # If key is a dictionary, assume it's a custom translation dictionary
        return key.get(language, default)
        
    # Get from main translations dictionary
    if key in translations.get(language, {}):
        return translations[language][key]
    
    # Fallback to language_manager method
    return language_manager.get_text(key, default)

def format_number(number, decimal_places=2):
    """
    Format a number according to locale conventions.
    Shorthand for language_manager.format_number().
    
    Args:
        number (float): Number to format
        decimal_places (int): Number of decimal places
        
    Returns:
        str: Formatted number
    """
    return language_manager.format_number(number, decimal_places)

def format_percentage(value):
    """
    Format a value as a percentage according to locale conventions.
    Shorthand for language_manager.format_percentage().
    
    Args:
        value (float): Value to format as percentage (0.1 = 10%)
        
    Returns:
        str: Formatted percentage
    """
    return language_manager.format_percentage(value)

def format_date(date, short=False):
    """
    Format a date according to locale conventions.
    Shorthand for language_manager.format_date().
    
    Args:
        date (datetime): Date to format
        short (bool): Whether to use short date format
        
    Returns:
        str: Formatted date
    """
    return language_manager.format_date(date, short)

def get_current_language():
    """
    Get the current language code.
    
    Returns:
        str: Current language code
    """
    return st.session_state.get('language', language_manager.current_language)

def translate_column_names(columns, language=None):
    """
    Translate column names for display.
    
    Args:
        columns (list): List of column names
        language (str, optional): Language code (if None, uses current language)
        
    Returns:
        dict: Dictionary mapping original column names to translated names
    """
    if language is None:
        language = get_current_language()
    
    translated = {}
    for col in columns:
        if col in translations.get(language, {}).get('columns_of_interest', {}):
            translated[col] = translations[language]['columns_of_interest'][col]
        else:
            translated[col] = col
    
    return translated