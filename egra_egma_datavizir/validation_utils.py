import pandas as pd
import numpy as np
import logging
import os
from datetime import datetime
import traceback
import matplotlib.pyplot as plt
import seaborn as sns
from typing import List, Dict, Optional, Tuple, Union, Any, Callable
import streamlit as st

# Import language module (assuming you have a language utility module)
try:
    from language_utils import get_text
except ImportError:
    # Fallback if language module isn't available
    def get_text(key, default=""):
        """Fallback function if language utils not available"""
        return default

# Configure logging
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)
log_filename = f"datavizir_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    filename=os.path.join(LOG_DIR, log_filename),
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger("datavizir_validation")

# Define assessment-specific constants
VALID_SCORE_RANGES = {
    # EGRA variables
    "clpm": (0, 200),           # Correct Letters Per Minute
    "phoneme": (0, 10),         # Phoneme Awareness (out of 10)
    "sound_word": (0, 50),      # Correctly Read Words
    "cwpm": (0, 200),           # Correct Words Per Minute
    "listening": (0, 5),        # Listening Comprehension (out of 5)
    "orf": (0, 200),            # Oral Reading Fluency
    "comprehension": (0, 5),    # Reading Comprehension (out of 5)
    
    # EGMA variables
    "number_id": (0, 20),       # Number Identification (out of 20)
    "discrimin": (0, 10),       # Number Discrimination (out of 10)
    "missing_number": (0, 10),  # Missing Number (out of 10)
    "addition": (0, 20),        # Addition Problems (out of 20)
    "subtraction": (0, 20),     # Subtraction Problems (out of 20)
    "problems": (0, 5)          # Word Problems (out of 5)
}

# Expected data types for columns
EXPECTED_TYPES = {
    # Assessment variables - numeric
    "clpm": "numeric",
    "phoneme": "numeric",
    "sound_word": "numeric",
    "cwpm": "numeric",
    "listening": "numeric",
    "orf": "numeric",
    "comprehension": "numeric",
    "number_id": "numeric",
    "discrimin": "numeric",
    "missing_number": "numeric",
    "addition": "numeric",
    "subtraction": "numeric",
    "problems": "numeric",
    
    # Demographic variables
    "school": "categorical",
    "stgender": "categorical",  # Student gender
    "language_teaching": "categorical",
    "st_english_home": "categorical",
    "st_dutch_home": "categorical",
    "st_other_language": "categorical",
    "ses": "numeric",          # Socioeconomic status
    "home_support": "categorical"
}

# Required columns for different analyses
REQUIRED_COLUMNS = {
    "statistical": ["school"],  # At least one assessment variable will be added in validation function
    "zero_scores": [],          # At least one assessment variable will be added in validation function
    "school_comparison": ["school"],
    "gender_effect": ["stgender"],
    "language_effect": ["language_teaching"],
    "correlation": [],          # At least two assessment variables will be added in validation function
    "reliability": [],          # At least two assessment variables will be added in validation function
    "international_comparison": []  # At least one assessment variable will be added in validation function
}

# Error and warning message translations
ERROR_MESSAGES = {
    "en": {
        "missing_required_columns": "Missing required columns: {}",
        "invalid_data_type": "Invalid data type for column '{}'. Expected {}, found {}.",
        "out_of_range_values": "Column '{}' contains values outside valid range ({} to {}).",
        "missing_values": "Column '{}' contains {} missing values ({}% of data).",
        "potential_outliers": "Column '{}' contains {} potential outliers.",
        "insufficient_data": "Insufficient data for analysis. Need at least {} rows, found {}.",
        "no_variation": "Column '{}' has no variation (all values are the same).",
        "empty_selection": "No variables selected for analysis.",
        "unknown_analysis": "Unknown analysis type: {}",
        "general_error": "An error occurred during analysis: {}",
        "file_read_error": "Error reading file: {}",
        "processing_error": "Error processing data: {}"
    },
    "fr": {
        "missing_required_columns": "Colonnes requises manquantes : {}",
        "invalid_data_type": "Type de données invalide pour la colonne '{}'. Attendu {}, trouvé {}.",
        "out_of_range_values": "La colonne '{}' contient des valeurs hors de la plage valide ({} à {}).",
        "missing_values": "La colonne '{}' contient {} valeurs manquantes ({}% des données).",
        "potential_outliers": "La colonne '{}' contient {} valeurs aberrantes potentielles.",
        "insufficient_data": "Données insuffisantes pour l'analyse. Besoin d'au moins {} lignes, trouvé {}.",
        "no_variation": "La colonne '{}' n'a pas de variation (toutes les valeurs sont identiques).",
        "empty_selection": "Aucune variable sélectionnée pour l'analyse.",
        "unknown_analysis": "Type d'analyse inconnu : {}",
        "general_error": "Une erreur s'est produite pendant l'analyse : {}",
        "file_read_error": "Erreur lors de la lecture du fichier : {}",
        "processing_error": "Erreur lors du traitement des données : {}"
    }
}

class ValidationResult:
    """Class to store validation results."""
    
    def __init__(self):
        """Initialize validation result."""
        self.valid = True
        self.errors = []
        self.warnings = []
        self.info = []
    
    def add_error(self, message):
        """Add an error message and set valid to False."""
        self.errors.append(message)
        self.valid = False
    
    def add_warning(self, message):
        """Add a warning message."""
        self.warnings.append(message)
    
    def add_info(self, message):
        """Add an informational message."""
        self.info.append(message)
    
    def get_summary(self):
        """Get a summary of validation results."""
        return {
            "valid": self.valid,
            "errors": self.errors,
            "warnings": self.warnings,
            "info": self.info
        }

class DataValidator:
    """Class for validating educational assessment data."""
    
    def __init__(self, language="en", min_rows=10, outlier_threshold=3):
        """
        Initialize the data validator.
        
        Args:
            language (str): Language for error messages ('en' or 'fr')
            min_rows (int): Minimum number of rows required for analysis
            outlier_threshold (float): Z-score threshold for outlier detection
        """
        self.language = language
        self.min_rows = min_rows
        self.outlier_threshold = outlier_threshold
        self.result = None
    
    def get_error_message(self, key, *args):
        """Get a translated error message."""
        message_template = ERROR_MESSAGES.get(self.language, ERROR_MESSAGES["en"]).get(key, "")
        return message_template.format(*args)
    
    def validate_dataframe(self, df, analysis_type="statistical", selected_columns=None):
        """
        Validate a DataFrame for a specific analysis type.
        
        Args:
            df (pd.DataFrame): DataFrame to validate
            analysis_type (str): Type of analysis to validate for
            selected_columns (list): List of columns selected for analysis
            
        Returns:
            ValidationResult: Validation result
        """
        self.result = ValidationResult()
        
        # Log validation start
        logger.info(f"Starting validation for analysis type: {analysis_type}")
        
        # Check if DataFrame is empty
        if df is None or df.empty:
            self.result.add_error(self.get_error_message("insufficient_data", self.min_rows, 0))
            logger.error("Validation failed: DataFrame is empty or None")
            return self.result
        
        # Check minimum number of rows
        if len(df) < self.min_rows:
            self.result.add_error(self.get_error_message("insufficient_data", self.min_rows, len(df)))
            logger.warning(f"Insufficient data: {len(df)} rows (minimum {self.min_rows})")
        
        # Check selected columns
        if selected_columns is None or len(selected_columns) == 0:
            if analysis_type != "general":  # Only add error for specific analyses
                self.result.add_error(self.get_error_message("empty_selection"))
                logger.warning("No columns selected for analysis")
            selected_columns = []
        
        # Get required columns for the analysis type
        required_columns = list(REQUIRED_COLUMNS.get(analysis_type, []))
        
        # Add selected assessment columns to required columns
        if analysis_type in ["correlation", "reliability"]:
            # These analyses need at least two assessment variables
            if len(selected_columns) < 2:
                self.result.add_error(self.get_error_message("insufficient_data", 2, len(selected_columns)))
                logger.warning(f"Insufficient assessment variables: {len(selected_columns)} (minimum 2)")
        elif selected_columns:
            required_columns.extend(selected_columns)
        
        # Check for missing required columns
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            self.result.add_error(self.get_error_message("missing_required_columns", ", ".join(missing_columns)))
            logger.error(f"Missing required columns: {missing_columns}")
        
        # Validate each column
        for column in df.columns:
            if column in selected_columns or column in REQUIRED_COLUMNS.get(analysis_type, []):
                self._validate_column(df, column)
        
        # Log validation result
        if self.result.valid:
            logger.info("Validation passed successfully")
        else:
            logger.warning(f"Validation completed with {len(self.result.errors)} errors and {len(self.result.warnings)} warnings")
        
        return self.result
    
    def _validate_column(self, df, column):
        """
        Validate a specific column in the DataFrame.
        
        Args:
            df (pd.DataFrame): DataFrame containing the column
            column (str): Column name to validate
        """
        # Check data type
        expected_type = EXPECTED_TYPES.get(column)
        if expected_type:
            if expected_type == "numeric":
                # Check if column can be converted to numeric
                try:
                    # Try to convert to numeric, coerce errors to NaN
                    numeric_data = pd.to_numeric(df[column], errors='coerce')
                    
                    # Check if conversion created a lot of NaN values
                    new_null_count = numeric_data.isna().sum() - df[column].isna().sum()
                    if new_null_count > 0:
                        pct_invalid = (new_null_count / len(df)) * 100
                        if pct_invalid > 10:  # If more than 10% values couldn't be converted
                            self.result.add_warning(self.get_error_message("invalid_data_type", column, "numeric", "mixed"))
                            logger.warning(f"Column '{column}' expected numeric but contains mixed types ({pct_invalid:.1f}% non-numeric)")
                except:
                    self.result.add_warning(self.get_error_message("invalid_data_type", column, "numeric", "non-numeric"))
                    logger.warning(f"Column '{column}' failed numeric conversion")
            
            elif expected_type == "categorical":
                # Nothing specific to validate for categorical data
                pass
        
        # Check for missing values
        null_count = df[column].isna().sum()
        if null_count > 0:
            null_percent = (null_count / len(df)) * 100
            self.result.add_warning(self.get_error_message("missing_values", column, null_count, f"{null_percent:.1f}"))
            logger.warning(f"Column '{column}' has {null_count} missing values ({null_percent:.1f}%)")
        
        # Check for no variation
        if df[column].nunique() <= 1:
            self.result.add_warning(self.get_error_message("no_variation", column))
            logger.warning(f"Column '{column}' has no variation (unique values: {df[column].nunique()})")
        
        # Check valid ranges for assessment variables
        if column in VALID_SCORE_RANGES:
            min_val, max_val = VALID_SCORE_RANGES[column]
            
            # Handle potential non-numeric data
            try:
                numeric_data = pd.to_numeric(df[column], errors='coerce')
                out_of_range = ((numeric_data < min_val) | (numeric_data > max_val)).sum()
                
                if out_of_range > 0:
                    out_of_range_pct = (out_of_range / numeric_data.notna().sum()) * 100
                    self.result.add_warning(self.get_error_message("out_of_range_values", column, min_val, max_val))
                    logger.warning(f"Column '{column}' has {out_of_range} values outside range {min_val}-{max_val} ({out_of_range_pct:.1f}%)")
                
                # Check for potential outliers in numeric assessment variables
                self._check_outliers(numeric_data, column)
            except:
                # Column can't be analyzed as numeric
                self.result.add_warning(self.get_error_message("invalid_data_type", column, "numeric", "non-numeric"))
                logger.warning(f"Column '{column}' couldn't be analyzed for range validation")
    
    def _check_outliers(self, series, column_name):
        """
        Check for potential outliers in a numeric series using z-score.
        
        Args:
            series (pd.Series): Numeric series to check
            column_name (str): Name of the column for logging
        """
        # Remove NaN values
        clean_series = series.dropna()
        
        if len(clean_series) >= 10:  # Only check if we have enough data
            # Calculate z-scores
            mean = clean_series.mean()
            std = clean_series.std()
            
            if std > 0:  # Avoid division by zero
                z_scores = (clean_series - mean) / std
                outliers = (z_scores.abs() > self.outlier_threshold)
                outlier_count = outliers.sum()
                
                if outlier_count > 0:
                    outlier_pct = (outlier_count / len(clean_series)) * 100
                    self.result.add_warning(self.get_error_message("potential_outliers", column_name, outlier_count))
                    logger.warning(f"Column '{column_name}' has {outlier_count} potential outliers ({outlier_pct:.1f}%)")
    
    def get_missing_value_report(self, df):
        """
        Get a report of missing values in the DataFrame.
        
        Args:
            df (pd.DataFrame): DataFrame to analyze
            
        Returns:
            pd.DataFrame: Report of missing values
        """
        missing_data = pd.DataFrame({
            'Column': df.columns,
            'Missing Values': df.isna().sum().values,
            'Percentage': (df.isna().sum() / len(df) * 100).round(2).values
        })
        missing_data = missing_data.sort_values('Percentage', ascending=False)
        
        return missing_data
    
    def handle_missing_values(self, df, method='drop_rows', threshold=50, fill_value=None, knn_neighbors=5):
        """
        Handle missing values in the DataFrame.
        
        Args:
            df (pd.DataFrame): DataFrame with missing values
            method (str): Method to handle missing values
                'drop_rows': Drop rows with missing values
                'drop_columns': Drop columns with missing values exceeding threshold
                'fill_mean': Fill missing values with column mean
                'fill_median': Fill missing values with column median
                'fill_mode': Fill missing values with column mode
                'fill_value': Fill missing values with a specific value
                'knn_impute': Use KNN imputation (requires scikit-learn)
            threshold (float): Threshold percentage for dropping columns
            fill_value: Value to use when method is 'fill_value'
            knn_neighbors (int): Number of neighbors for KNN imputation
            
        Returns:
            pd.DataFrame: DataFrame with handled missing values
        """
        # Make a copy of the DataFrame to avoid modifying the original
        result_df = df.copy()
        
        # Log missing values before handling
        logger.info(f"Handling missing values using method: {method}")
        logger.info(f"Missing values before handling: {result_df.isna().sum().sum()}")
        
        if method == 'drop_rows':
            # Drop rows with any missing values
            result_df = result_df.dropna()
            logger.info(f"Dropped rows with missing values. Remaining rows: {len(result_df)}")
        
        elif method == 'drop_columns':
            # Calculate missing percentage for each column
            missing_pct = result_df.isna().mean() * 100
            
            # Identify columns exceeding threshold
            cols_to_drop = missing_pct[missing_pct > threshold].index.tolist()
            
            if cols_to_drop:
                result_df = result_df.drop(columns=cols_to_drop)
                logger.info(f"Dropped columns with >{threshold}% missing values: {cols_to_drop}")
        
        elif method == 'fill_mean':
            # Fill numeric columns with mean
            for col in result_df.select_dtypes(include=['number']).columns:
                result_df[col] = result_df[col].fillna(result_df[col].mean())
            logger.info("Filled numeric missing values with column means")
        
        elif method == 'fill_median':
            # Fill numeric columns with median
            for col in result_df.select_dtypes(include=['number']).columns:
                result_df[col] = result_df[col].fillna(result_df[col].median())
            logger.info("Filled numeric missing values with column medians")
        
        elif method == 'fill_mode':
            # Fill all columns with mode
            for col in result_df.columns:
                result_df[col] = result_df[col].fillna(result_df[col].mode()[0] if not result_df[col].mode().empty else None)
            logger.info("Filled missing values with column modes")
        
        elif method == 'fill_value':
            # Fill with specified value
            result_df = result_df.fillna(fill_value)
            logger.info(f"Filled missing values with specified value: {fill_value}")
        
        elif method == 'knn_impute':
            # Try to import scikit-learn for KNN imputation
            try:
                from sklearn.impute import KNNImputer
                
                # Get numeric columns
                numeric_cols = result_df.select_dtypes(include=['number']).columns.tolist()
                
                if numeric_cols:
                    # Create imputer
                    imputer = KNNImputer(n_neighbors=knn_neighbors)
                    
                    # Impute numeric columns
                    result_df[numeric_cols] = pd.DataFrame(
                        imputer.fit_transform(result_df[numeric_cols]),
                        columns=numeric_cols,
                        index=result_df.index
                    )
                    logger.info(f"Used KNN imputation for numeric columns with {knn_neighbors} neighbors")
                else:
                    logger.warning("No numeric columns found for KNN imputation")
            except ImportError:
                logger.error("scikit-learn not installed. KNN imputation not available.")
                # Fallback to median imputation
                for col in result_df.select_dtypes(include=['number']).columns:
                    result_df[col] = result_df[col].fillna(result_df[col].median())
                logger.info("Fallback: Filled numeric missing values with column medians")
        
        # Log missing values after handling
        logger.info(f"Missing values after handling: {result_df.isna().sum().sum()}")
        
        return result_df
    
    def plot_missing_values(self, df):
        """
        Create a visualization of missing values.
        
        Args:
            df (pd.DataFrame): DataFrame to visualize
            
        Returns:
            matplotlib.figure.Figure: Missing values heatmap
        """
        # Create a mask of missing values
        plt.figure(figsize=(10, 6))
        plt.title('Missing Values Heatmap')
        
        # Only show columns with at least some missing values
        na_cols = [col for col in df.columns if df[col].isna().any()]
        
        if na_cols:
            # Create a subset of the DataFrame with only columns that have missing values
            miss_df = df[na_cols].isna()
            
            # Limit to max 100 rows for visualization
            if len(miss_df) > 100:
                miss_df = miss_df.iloc[:100]
            
            # Plot heatmap
            sns.heatmap(miss_df, cbar=False, cmap='viridis')
            plt.xlabel('Columns')
            plt.ylabel('Rows')
            plt.tight_layout()
            
            return plt.gcf()
        else:
            # No missing values
            plt.text(0.5, 0.5, 'No missing values', ha='center', va='center', fontsize=14)
            plt.tight_layout()
            return plt.gcf()

class ErrorHandler:
    """Class for handling errors in a consistent way across the application."""
    
    def __init__(self, language="en"):
        """
        Initialize the error handler.
        
        Args:
            language (str): Language for error messages ('en' or 'fr')
        """
        self.language = language
    
    def get_error_message(self, key, *args):
        """Get a translated error message."""
        message_template = ERROR_MESSAGES.get(self.language, ERROR_MESSAGES["en"]).get(key, "")
        return message_template.format(*args)
    
    def handle_error(self, error, error_type="general_error"):
        """
        Handle an error and return an appropriate error message.
        
        Args:
            error (Exception): The error to handle
            error_type (str): Type of error for translation
            
        Returns:
            str: Translated error message
        """
        # Log the error
        logger.error(f"Error ({error_type}): {str(error)}")
        logger.error(traceback.format_exc())
        
        # Return translated error message
        return self.get_error_message(error_type, str(error))
    
    def display_streamlit_error(self, error, error_type="general_error"):
        """
        Display an error message in Streamlit.
        
        Args:
            error (Exception): The error to handle
            error_type (str): Type of error for translation
        """
        error_message = self.handle_error(error, error_type)
        st.error(error_message)
    
    def display_validation_results(self, validation_result):
        """
        Display validation results in Streamlit.
        
        Args:
            validation_result (ValidationResult): Validation results to display
        """
        # Display errors
        for error in validation_result.errors:
            st.error(error)
        
        # Display warnings
        for warning in validation_result.warnings:
            st.warning(warning)
        
        # Display info messages
        for info in validation_result.info:
            st.info(info)
    
    def wrap_analysis_function(self, func, df, language, *args, **kwargs):
        """
        Wrap an analysis function with error handling.
        
        Args:
            func (callable): Analysis function to wrap
            df (pd.DataFrame): DataFrame to analyze
            language (str): Language for error messages
            *args, **kwargs: Additional arguments for the analysis function
            
        Returns:
            dict or None: Analysis results or None if an error occurred
        """
        # Update language
        self.language = language
        
        try:
            # Run the analysis function
            return func(df, language, *args, **kwargs)
        except Exception as e:
            # Handle the error
            self.display_streamlit_error(e)
            
            # Log the error
            logger.error(f"Error in analysis function {func.__name__}: {str(e)}")
            logger.error(traceback.format_exc())
            
            return None


# Usage example:
# 
# def analyze_data_with_validation(df, language, analysis_type, selected_columns):
#     # Create validator and error handler
#     validator = DataValidator(language=language)
#     error_handler = ErrorHandler(language=language)
#     
#     # Validate data
#     validation_result = validator.validate_dataframe(df, analysis_type, selected_columns)
#     
#     # Display validation results
#     error_handler.display_validation_results(validation_result)
#     
#     # Only proceed if validation passed
#     if not validation_result.valid:
#         return None
#     
#     try:
#         # Handle missing values
#         if st.checkbox(get_text("handle_missing_values", "Handle Missing Values")):
#             missing_method = st.selectbox(
#                 get_text("missing_method", "Method"),
#                 ["drop_rows", "fill_mean", "fill_median"]
#             )
#             df = validator.handle_missing_values(df, method=missing_method)
#         
#         # Perform analysis
#         results = do_actual_analysis(df, selected_columns)
#         return results
#     
#     except Exception as e:
#         error_handler.display_streamlit_error(e)
#         return None