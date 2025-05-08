# main.py
import streamlit as st
import pandas as pd
import base64
import os
import sys
import traceback
from pathlib import Path

# Import configuration and utility modules
from config import translations
from language_utils import setup_language_selector, get_text
from validation_utils import DataValidator, ErrorHandler

# Import only the analysis modules that exist in the repository
from analyse1 import show_statistical_overview
from analyse2 import show_zero_scores
from analyse5 import show_correlation
from analyse6 import show_reliability
from analyse7 import show_performance_school
from analyse10 import show_gender_effect
from analyse12 import show_international_comparison
from analyse13 import show_language_comparison

# Set page configuration
st.set_page_config(
    page_title="Datavizir Analytics",
    page_icon="📊",
    layout="wide"
)

import pandas as pd
import streamlit as st


import pandas as pd
import streamlit as st


def load_data():
    """
    Loads data from various file formats (Excel, JSON, CSV, Stata DTA).
    Returns:
        pandas.DataFrame or None: The loaded DataFrame or None if error
    """
    # Initialize error handler
    error_handler = ErrorHandler(language=st.session_state.get('language', 'en'))

    try:
        # Supported formats
        supported_formats = {
            "xlsx": "Excel",
            "xls": "Excel",
            "json": "JSON",
            "csv": "CSV",
            "dta": "Stata"
        }

        # Load translations
        language = st.session_state.get('language', 'en')
        t = translations[language]

        # File uploader in sidebar
        uploaded_file = st.sidebar.file_uploader(
            t["upload_file"],
            type=list(supported_formats.keys()),
            help=t["upload_help"]
        )

        if uploaded_file is None:
            st.sidebar.info(t["upload_info"])
            return None

        # Wrap all loaded-data UI in a sidebar expander
        exp = st.sidebar.expander(
            t.get("loaded_data_section", "Données chargées"),
            expanded=True
        )
        with exp:
            # Determine file extension
            ext = uploaded_file.name.split('.')[-1].lower()

            # Loading spinner
            with st.spinner(t["loading_data"]):
                if ext in ("xlsx", "xls"):
                    xls = pd.ExcelFile(uploaded_file)
                    sheet = (
                        xls.sheet_names[0]
                        if len(xls.sheet_names) == 1
                        else st.selectbox(t["select_sheet"], xls.sheet_names)
                    )
                    df = pd.read_excel(uploaded_file, sheet_name=sheet)

                elif ext == "json":
                    try:
                        df = pd.read_json(uploaded_file)
                    except ValueError:
                        df = pd.read_json(uploaded_file, orient="records")

                elif ext == "csv":
                    encodings = ["utf-8", "latin1", "iso-8859-1", "cp1252"]
                    separators = [",", ";", "\t", "|"]
                    col1, col2 = st.columns(2)
                    with col1:
                        encoding = st.selectbox(t["select_encoding"], encodings)
                    with col2:
                        separator = st.selectbox(t["select_separator"], separators)
                    df = pd.read_csv(uploaded_file, encoding=encoding, sep=separator, engine="python")

                else:  # dta
                    df = pd.read_stata(uploaded_file)

            # Validate dataframe
            validator = DataValidator(language=language)
            validation = validator.validate_dataframe(df, analysis_type="general")
            for warning in validation.warnings:
                st.warning(warning)

            # Success message
            st.success(f"{t['upload_success']} {uploaded_file.name}")
            st.write(f"{t.get('rows_count', 'Rows')}: {df.shape[0]}")
            st.write(f"{t.get('columns_count', 'Columns')}: {df.shape[1]}")

            # Data preview
            if st.checkbox(t.get("show_preview", "Afficher un aperçu")):
                st.dataframe(df.head(), use_container_width=True)

            # Column data types
            if st.checkbox(t.get("show_dtypes", "Types de colonnes")):
                st.write(df.dtypes)

            # Missing values analysis
            if st.checkbox(t.get("show_missing_values", "Analyse des valeurs manquantes")):
                missing_report = validator.get_missing_value_report(df)
                st.dataframe(missing_report)

                if st.checkbox(t.get("visualize_missing", "Visualiser les valeurs manquantes")):
                    missing_fig = validator.plot_missing_values(df)
                    st.pyplot(missing_fig)

                if st.checkbox(t.get("handle_missing", "Gérer les valeurs manquantes")):
                    method = st.selectbox(
                        t.get("missing_method", "Méthode :"),
                        ["drop_rows", "fill_mean", "fill_median", "fill_mode"]
                    )
                    df = validator.handle_missing_values(df, method=method)
                    st.success(t.get("missing_handled", "Valeurs manquantes traitées avec succès"))

        return df

    except Exception as e:
        error_handler.display_streamlit_error(e, "file_read_error")
        return None

def main():
    """Main function to run the Streamlit application."""
    
    # Set up language selector using language_utils
    selected_language = setup_language_selector()
    
    # Store language in session state
    st.session_state['language'] = selected_language
    t = translations[selected_language]
    
    # Main title
    st.title(t["app_title"])
    
    # Sidebar for navigation
    st.sidebar.title(t["nav_title"])
    
    # Dictionary of available analyses with proper function references
    # Only include modules that exist in the repository
    ANALYSES = {
        t["analysis1_title"]: show_statistical_overview,
        t["analysis2_title"]: show_zero_scores,
        t["analysis5_title"]: show_correlation,
        t["analysis6_title"]: show_reliability,
        t["analysis7_title"]: show_performance_school,
        t["analysis10_title"]: show_gender_effect,
        t["analysis12_title"]: show_international_comparison,
        t["analysis13_title"]: show_language_comparison
    }
    
    # Analysis selection
    analysis = st.sidebar.radio(
        t["select_analysis"],
        options=list(ANALYSES.keys()),
        key="analysis_selector"
    )
    
    # Load data
    df = load_data()
    
    # Run selected analysis if data is loaded
    if df is not None:
        # Display analysis title
        st.header(analysis)
        st.divider()
        
        # Get the selected analysis function
        selected_function = ANALYSES[analysis]
        
        # Wrap the analysis function with error handling
        error_handler = ErrorHandler(language=selected_language)
        error_handler.wrap_analysis_function(selected_function, df, selected_language)
    
if __name__ == "__main__":
    main()