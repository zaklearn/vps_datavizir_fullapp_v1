"""
Module language.py - Language support for the application.

This module provides language support for the application,
simplified to only include English.
"""

import streamlit as st
from config import TRANSLATIONS, DEFAULT_LANGUAGE

def init_language():
    """
    Initialize language in session state if not already present
    """
    if 'language' not in st.session_state:
        st.session_state.language = DEFAULT_LANGUAGE

def get_language():
    """
    Get current language from session state
    """
    init_language()
    return st.session_state.language

def language_selector():
    """
    Adds a language selector to the sidebar
    """
    # Since we only have English in this version, we'll just show a static dropdown
    # but keep the function to maintain compatibility with the multilingual version
    init_language()
    with st.sidebar:
        st.markdown("### 🌐 Language")
        language = st.selectbox(
            "Select language",
            ["English"],
            index=0
        )
        # If we had multiple languages, we would set it here
        # st.session_state.language = language

def t(key):
    """
    Get translated text for a key
    
    Args:
        key: Translation key
        
    Returns:
        str: Translated text
    """
    # Try to get translation
    if key in TRANSLATIONS:
        return TRANSLATIONS[key]
    
    # Return key if not found (for debugging)
    return key

def get_label(indicator):
    """
    Get label for an indicator
    
    Args:
        indicator: Indicator key
        
    Returns:
        str: Label for the indicator
    """
    return t(indicator)