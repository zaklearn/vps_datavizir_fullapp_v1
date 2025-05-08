# main.py
import streamlit as st
import pandas as pd
import base64
import os
from pathlib import Path
from config import translations
from logging_config import LoggerSetup
from error_handling import error_handler, validate_dataframe, DataValidationError
import logging
import traceback

# Import the filtered modules focusing on contextual variables
from modules.school_comparison import show_school_comparison
from modules.language_effect import show_language_effect
from modules.contextual_factors import show_contextual_factors
from modules.gender_effect import show_gender_effect
from modules.ses_analysis import show_ses_home_support

# Initialize logging
app_logger, module_loggers = LoggerSetup.initialize_application_logging()

def get_image_base64(image_path):
    """Convert image to base64 string for embedding in app"""
    logger = app_logger
    try:
        if os.path.exists(image_path):
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode()
                logger.info(f"Successfully loaded logo from: {image_path}")
                return encoded_string
        else:
            logger.warning(f"Logo file not found at: {image_path}")
            st.warning(f"Logo file not found at: {image_path}")
            return ""
    except Exception as e:
        logger.error(f"Error reading logo: {str(e)}")
        st.warning(f"Error reading logo: {str(e)}")
        return ""

@error_handler('eduinsight')
def load_data():
    """
    Load data from various file formats with appropriate error handling.
    
    Returns:
        pandas.DataFrame or None: Loaded dataframe or None if loading failed
    """
    logger = app_logger
    logger.info("Starting data loading process")
    
    try:
        # Define supported formats
        supported_formats = {
            "xlsx": "Excel",
            "xls": "Excel",
            "csv": "CSV"
        }
        
        # File uploader with supported formats
        uploaded_file = st.file_uploader(
            t.get("upload_file", "Upload data file"),
            type=list(supported_formats.keys()),
            help=t.get("upload_help", "Supported formats: Excel and CSV")
        )
        
        if uploaded_file is not None:
            logger.info(f"File uploaded: {uploaded_file.name}")
            
            # Get file extension for processing
            file_extension = uploaded_file.name.split('.')[-1].lower()
            logger.debug(f"File extension: {file_extension}")
            
            # Show loading spinner
            with st.spinner(t.get("loading_data", "Loading data...")):
                
                # Process based on file type
                if file_extension in ['xlsx', 'xls']:
                    logger.debug("Processing Excel file")
                    # For Excel files, allow sheet selection if multiple sheets exist
                    xls = pd.ExcelFile(uploaded_file)
                    logger.debug(f"Found sheets: {xls.sheet_names}")
                    
                    if len(xls.sheet_names) > 1:
                        sheet_name = st.selectbox(
                            t.get("select_sheet", "Select sheet"),
                            options=xls.sheet_names
                        )
                        logger.info(f"User selected sheet: {sheet_name}")
                    else:
                        sheet_name = xls.sheet_names[0]
                        logger.info(f"Using single sheet: {sheet_name}")
                    
                    df = pd.read_excel(uploaded_file, sheet_name=sheet_name)
                
                elif file_extension == 'csv':
                    logger.debug("Processing CSV file")
                    # For CSV, allow configuration of encoding and separator
                    encodings = ['utf-8', 'latin1', 'iso-8859-1', 'cp1252']
                    separators = [',', ';', '\t', '|']
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        encoding = st.selectbox(
                            t.get("select_encoding", "Encoding"),
                            options=encodings,
                            index=0
                        )
                    with col2:
                        separator = st.selectbox(
                            t.get("select_separator", "Separator"),
                            options=separators,
                            index=0
                        )
                    
                    logger.info(f"Using encoding: {encoding}, separator: {separator}")
                    
                    try:
                        df = pd.read_csv(
                            uploaded_file,
                            encoding=encoding,
                            sep=separator,
                            engine='python'
                        )
                    except UnicodeDecodeError:
                        logger.error("Unicode decode error, trying different encoding")
                        # Try different encodings if the first one fails
                        for enc in encodings:
                            try:
                                df = pd.read_csv(
                                    uploaded_file,
                                    encoding=enc,
                                    sep=separator,
                                    engine='python'
                                )
                                logger.info(f"Successfully read file with encoding: {enc}")
                                break
                            except:
                                continue
                        else:
                            raise ValueError("Unable to read file with any supported encoding")
                
                # Validate that key variables exist
                required_columns = [
                    "school", 
                    "stgender", 
                    "language_teaching",
                    "ses",
                    "home_support"
                ]
                
                try:
                    validate_dataframe(df, required_columns, 'eduinsight')
                except DataValidationError as e:
                    st.warning(f"{e.message}")
                    st.info(t.get('column_info', 'This application requires contextual variables for analysis.'))
                    return None
                
                # Display data info
                st.success(f"{t.get('upload_success', 'File loaded successfully')}: {uploaded_file.name}")
                st.write(f"{t.get('rows_count', 'Rows')}: {df.shape[0]}")
                st.write(f"{t.get('columns_count', 'Columns')}: {df.shape[1]}")
                logger.info(f"Successfully loaded file with {df.shape[0]} rows and {df.shape[1]} columns")
                
                # Show data preview if desired
                if st.checkbox(t.get("show_preview", "Show data preview")):
                    st.dataframe(df.head())
                
                return df
            
        else:
            st.info(t.get("upload_info", "Please upload a file to begin analysis"))
            return None
            
    except Exception as e:
        logger.exception("Error during data loading")
        
        # Handle different error types
        error_msg = str(e)
        if "UnicodeDecodeError" in error_msg:
            st.error(t.get('encoding_error', 'Encoding error. Try a different encoding.'))
        elif "ParserError" in error_msg:
            st.error(t.get('parser_error', 'Parser error. Check file format.'))
        elif "ValueError" in error_msg:
            st.error(t.get('value_error', 'Value error. File may be corrupted.'))
        else:
            st.error(f"{t.get('upload_error', 'Error loading file')}: {error_msg}")
        return None

def create_footer():
    """Create a branded footer for the application"""
    logger = app_logger
    try:
        # Get logo path relative to current file
        logo_path = os.path.join(Path(__file__).parent, "assets", "logo.png")
        logger.debug(f"Looking for logo at: {logo_path}")
        
        # Convert logo to base64
        logo_base64 = get_image_base64(logo_path)
        
        if logo_base64:
            # Create footer with CSS
            st.sidebar.markdown(
                f"""
                <style>
                .footer {{
                    position: fixed;
                    left: 0;
                    bottom: 0;
                    width: 100%;
                    background-color: white;
                    padding: 10px;
                    text-align: center;
                    border-top: 1px solid #e6e6e6;
                    z-index: 999;
                }}
                .footer img {{
                    height: 30px;
                    margin-bottom: 5px;
                }}
                .footer p {{
                    margin: 0;
                    font-size: 12px;
                    color: #666;
                }}
                </style>
                <div class="footer">
                    <img src="data:image/png;base64,{logo_base64}" alt="Logo">
                    <p>EduInsight v1.0 © 2025</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    except Exception as e:
        logger.error(f"Error creating footer: {str(e)}")

@error_handler('eduinsight')
def main():
    """Main application entry point"""
    global t  # Make translation dictionary accessible to all functions
    logger = app_logger
    
    try:
        logger.info("Starting EduInsight application")
        
        # Configure page
        st.set_page_config(
            page_title="EduInsight Analytics",
            page_icon="📊",
            layout="wide"
        )
        
        # Sidebar for language selection
        st.sidebar.title("🌍 Language / Langue")
        language = st.sidebar.radio(
            "Choose language / Choisir la langue",
            ["en", "fr"],
            format_func=lambda x: "🇬🇧 English" if x == "en" else "🇫🇷 Français"
        )
        t = translations[language]  # Load translations
        logger.info(f"Language selected: {language}")
        
        # Sidebar for navigation
        st.sidebar.title("📊 Navigation")
        
        # Define the analysis modules with consistent naming
        ANALYSES = {
            t.get("title_school_comparison", "School Comparison"): {
                'function': show_school_comparison,
                'logger_name': 'eduinsight.school_comparison'
            },
            t.get("title_language_effect", "Language Effect"): {
                'function': show_language_effect,
                'logger_name': 'eduinsight.language_effect'
            },
            t.get("title_contextual_factors", "Contextual Factors"): {
                'function': show_contextual_factors,
                'logger_name': 'eduinsight.contextual_factors'
            },
            t.get("title_gender_effect", "Gender Effect"): {
                'function': show_gender_effect,
                'logger_name': 'eduinsight.gender_effect'
            },
            t.get("title_ses_home_support", "SES & Home Support"): {
                'function': show_ses_home_support,
                'logger_name': 'eduinsight.ses_analysis'
            }
        }
        
        # Analysis selection
        analysis = st.sidebar.radio(
            t.get("select_analysis", "Select Analysis"),
            options=list(ANALYSES.keys())
        )
        
        logger.info(f"Selected analysis: {analysis}")
        
        # Load data
        df = load_data()
        
        if df is not None:
            # Show selected analysis
            st.title(analysis)
            st.divider()
            
            try:
                # Call the selected analysis function
                selected_analysis = ANALYSES[analysis]
                module_logger = logging.getLogger(selected_analysis['logger_name'])
                module_logger.info(f"Starting {analysis} analysis")
                
                selected_analysis['function'](df, language)
                
                module_logger.info(f"Completed {analysis} analysis successfully")
            except Exception as e:
                module_logger = logging.getLogger(selected_analysis['logger_name'] if 'selected_analysis' in locals() else 'eduinsight')
                module_logger.exception(f"Error in {analysis} analysis")
                st.error(f"{t.get('analysis_error', 'Error in analysis')}: {str(e)}")
                
                # Show detailed error in development mode
                if os.getenv('DEVELOPMENT_MODE', 'false').lower() == 'true':
                    st.exception(e)
        else:
            # Welcome message when no data is loaded
            st.title(t.get("welcome_title", "Welcome to EduInsight"))
            
            st.markdown(t.get("welcome_message", 
                """
                ### EduInsight Analytics Platform
                
                **EduInsight** helps you analyze how contextual factors impact student performance.
                
                This platform focuses on five key contextual dimensions:
                
                1. **School Environment**: Compare performance across different schools
                2. **Language Background**: Analyze the effect of language on learning
                3. **Contextual Factors**: Examine how external factors affect outcomes
                4. **Gender Analysis**: Explore performance differences by gender
                5. **Socioeconomic Status**: Understand how SES and home support influence results
                
                To begin, upload a data file using the sidebar on the left, then select an analysis type.
                """
            ))
            
            # Add information about required data format
            with st.expander(t.get("data_format", "Required Data Format")):
                st.markdown(t.get("data_format_details", 
                    """
                    Your dataset should include the following key variables:
                    
                    - `school`: School identifier
                    - `stgender`: Student gender (coded as 0/1)
                    - `language_teaching`: Language of instruction
                    - `ses`: Socioeconomic status
                    - `home_support`: Level of home support
                    
                    Performance variables (reading scores, math scores, etc.) should also be included for analysis.
                    """
                ))
        
        # Create footer
        create_footer()
        
    except Exception as e:
        logger.critical("Critical error in main function", exc_info=True)
        st.error("A critical error occurred. Please restart the application.")
        if os.getenv('DEVELOPMENT_MODE', 'false').lower() == 'true':
            st.exception(e)

if __name__ == "__main__":
    main()
