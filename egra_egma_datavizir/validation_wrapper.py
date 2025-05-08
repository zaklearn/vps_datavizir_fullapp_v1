# validation_wrapper.py
# This wrapper standardizes data validation across existing analysis modules

import streamlit as st
import pandas as pd
import numpy as np
from language_utils import get_text, get_current_language
from validation_utils import DataValidator, ErrorHandler, ValidationResult
from config import egra_columns, egma_columns

class StandardValidator:
    """
    Standardized data validation wrapper for analysis modules.
    This class provides easy-to-use methods for validating data
    for specific analysis types across different modules.
    """
    
    def __init__(self):
        """Initialize the validator."""
        self.language = get_current_language()
        self.validator = DataValidator(language=self.language)
        self.error_handler = ErrorHandler(language=self.language)
    
    def update_language(self, language=None):
        """Update the language setting."""
        if language is None:
            language = get_current_language()
        self.language = language
        self.validator = DataValidator(language=language)
        self.error_handler = ErrorHandler(language=language)
    
    def validate_data(self, df, analysis_type, selected_columns=None):
        """
        Validate data for a specific analysis type.
        
        Args:
            df (pd.DataFrame): The data to validate
            analysis_type (str): Type of analysis (e.g., "statistical", "zero_scores")
            selected_columns (list, optional): Selected columns for analysis
            
        Returns:
            ValidationResult: Validation result object
        """
        # Validate the data
        validation_result = self.validator.validate_dataframe(
            df, analysis_type=analysis_type, selected_columns=selected_columns
        )
        
        # Display validation results
        self.error_handler.display_validation_results(validation_result)
        
        return validation_result
    
    def validate_statistical_analysis(self, df, selected_columns):
        """
        Validate data for statistical analysis (analyse1.py).
        
        Args:
            df (pd.DataFrame): The data to validate
            selected_columns (list): Selected columns for analysis
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Validate the data
        validation_result = self.validate_data(df, "statistical", selected_columns)
        
        # Check if we have at least one column selected
        if len(selected_columns) == 0:
            validation_result.add_error(get_text("empty_selection", "No variables selected for analysis."))
            self.error_handler.display_validation_results(validation_result)
        
        # Check if we have enough data for statistical analysis
        min_rows = 5
        if len(df) < min_rows:
            validation_result.add_error(
                get_text("insufficient_data", "Insufficient data for analysis. Need at least {} rows, found {}.").format(
                    min_rows, len(df)
                )
            )
            self.error_handler.display_validation_results(validation_result)
        
        return validation_result.valid
    
    def validate_zero_scores_analysis(self, df, selected_columns):
        """
        Validate data for zero scores analysis (analyse2.py).
        
        Args:
            df (pd.DataFrame): The data to validate
            selected_columns (list): Selected columns for analysis
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Validate the data
        validation_result = self.validate_data(df, "zero_scores", selected_columns)
        
        # Check if we have at least one column selected
        if len(selected_columns) == 0:
            validation_result.add_error(get_text("empty_selection", "No variables selected for analysis."))
            self.error_handler.display_validation_results(validation_result)
        
        # Verify that all selected columns are numeric
        non_numeric_cols = []
        for col in selected_columns:
            try:
                pd.to_numeric(df[col], errors='raise')
            except:
                non_numeric_cols.append(col)
        
        if non_numeric_cols:
            validation_result.add_warning(
                get_text("non_numeric_columns", "Some selected columns are not numeric: {}").format(
                    ", ".join(non_numeric_cols)
                )
            )
            self.error_handler.display_validation_results(validation_result)
        
        return validation_result.valid
    
    def validate_correlation_analysis(self, df, selected_columns):
        """
        Validate data for correlation analysis (analyse5.py).
        
        Args:
            df (pd.DataFrame): The data to validate
            selected_columns (list): Selected columns for analysis
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Validate the data
        validation_result = self.validate_data(df, "correlation", selected_columns)
        
        # Check if we have at least two columns selected
        if len(selected_columns) < 2:
            validation_result.add_error(
                get_text("insufficient_columns", "Correlation analysis requires at least 2 variables (found {}).").format(
                    len(selected_columns)
                )
            )
            self.error_handler.display_validation_results(validation_result)
            return False
        
        # Verify that all selected columns are numeric
        non_numeric_cols = []
        for col in selected_columns:
            try:
                pd.to_numeric(df[col], errors='raise')
            except:
                non_numeric_cols.append(col)
        
        if non_numeric_cols:
            validation_result.add_warning(
                get_text("non_numeric_columns", "Some selected columns are not numeric: {}").format(
                    ", ".join(non_numeric_cols)
                )
            )
            self.error_handler.display_validation_results(validation_result)
        
        return validation_result.valid
    
    def validate_reliability_analysis(self, df, selected_columns):
        """
        Validate data for reliability analysis (analyse6.py).
        
        Args:
            df (pd.DataFrame): The data to validate
            selected_columns (list): Selected columns for analysis
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Validate the data
        validation_result = self.validate_data(df, "reliability", selected_columns)
        
        # Check if we have at least two columns selected
        if len(selected_columns) < 2:
            validation_result.add_error(
                get_text("insufficient_items", "Reliability analysis requires at least 2 items/variables (found {}).").format(
                    len(selected_columns)
                )
            )
            self.error_handler.display_validation_results(validation_result)
            return False
        
        # Check if we have enough data rows for reliability analysis
        min_rows = 10
        if len(df) < min_rows:
            validation_result.add_error(
                get_text("insufficient_data_reliability", "Reliability analysis requires at least {} cases (found {}).").format(
                    min_rows, len(df)
                )
            )
            self.error_handler.display_validation_results(validation_result)
            return False
        
        # Verify that all selected columns are numeric
        non_numeric_cols = []
        for col in selected_columns:
            try:
                pd.to_numeric(df[col], errors='raise')
            except:
                non_numeric_cols.append(col)
        
        if non_numeric_cols:
            validation_result.add_error(
                get_text("non_numeric_reliability", "Reliability analysis requires numeric variables. Non-numeric variables found: {}").format(
                    ", ".join(non_numeric_cols)
                )
            )
            self.error_handler.display_validation_results(validation_result)
            return False
        
        return validation_result.valid
    
    def validate_school_performance(self, df, selected_columns):
        """
        Validate data for school performance analysis (analyse7.py).
        
        Args:
            df (pd.DataFrame): The data to validate
            selected_columns (list): Selected columns for analysis
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Validate the data
        validation_result = self.validate_data(df, "school_comparison", selected_columns)
        
        # Check if we have the school column
        if "school" not in df.columns:
            validation_result.add_error(get_text("no_school_column", "Error: No 'school' column found in the data."))
            self.error_handler.display_validation_results(validation_result)
            return False
        
        # Check if we have at least one column selected
        if len(selected_columns) == 0:
            validation_result.add_error(get_text("empty_selection", "No variables selected for analysis."))
            self.error_handler.display_validation_results(validation_result)
            return False
        
        # Check if we have enough schools for comparison
        school_counts = df["school"].value_counts()
        if len(school_counts) < 2:
            validation_result.add_error(
                get_text("insufficient_schools", "At least two schools are needed for comparison. Only {} found.").format(
                    len(school_counts)
                )
            )
            self.error_handler.display_validation_results(validation_result)
            return False
        
        # Verify that all selected columns are numeric
        non_numeric_cols = []
        for col in selected_columns:
            try:
                pd.to_numeric(df[col], errors='raise')
            except:
                non_numeric_cols.append(col)
        
        if non_numeric_cols:
            validation_result.add_warning(
                get_text("non_numeric_columns", "Some selected columns are not numeric: {}").format(
                    ", ".join(non_numeric_cols)
                )
            )
            self.error_handler.display_validation_results(validation_result)
        
        return validation_result.valid
    
    def validate_gender_analysis(self, df, selected_columns):
        """
        Validate data for gender effect analysis (analyse10.py).
        
        Args:
            df (pd.DataFrame): The data to validate
            selected_columns (list): Selected columns for analysis
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Validate the data
        validation_result = self.validate_data(df, "gender_effect", selected_columns)
        
        # Check if we have the gender column
        if "stgender" not in df.columns:
            validation_result.add_error(get_text("no_gender_column", "Error: No 'stgender' column found in the data."))
            self.error_handler.display_validation_results(validation_result)
            return False
        
        # Check if we have at least one column selected
        if len(selected_columns) == 0:
            validation_result.add_error(get_text("empty_selection", "No variables selected for analysis."))
            self.error_handler.display_validation_results(validation_result)
            return False
        
        # Check if gender column has enough categories (at least 2)
        gender_counts = df["stgender"].value_counts()
        if len(gender_counts) < 2:
            validation_result.add_error(
                get_text("insufficient_gender_categories", "At least two gender categories are needed. Only {} found.").format(
                    len(gender_counts)
                )
            )
            self.error_handler.display_validation_results(validation_result)
            return False
        
        return validation_result.valid
    
    def validate_international_comparison(self, df, selected_columns):
        """
        Validate data for international standards comparison (analyse12.py).
        
        Args:
            df (pd.DataFrame): The data to validate
            selected_columns (list): Selected columns for analysis
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Validate the data
        validation_result = self.validate_data(df, "international_comparison", selected_columns)
        
        # Check if we have at least one column selected
        if len(selected_columns) == 0:
            validation_result.add_error(get_text("empty_selection", "No variables selected for analysis."))
            self.error_handler.display_validation_results(validation_result)
            return False
        
        # Check if all selected columns have defined international benchmarks
        from analyse12 import international_benchmarks
        
        missing_benchmarks = [col for col in selected_columns if col not in international_benchmarks]
        if missing_benchmarks:
            validation_result.add_error(
                get_text("missing_benchmarks", "Some selected variables have no defined international benchmarks: {}").format(
                    ", ".join(missing_benchmarks)
                )
            )
            self.error_handler.display_validation_results(validation_result)
            return False
        
        return validation_result.valid
    
    def validate_language_comparison(self, df, selected_columns):
        """
        Validate data for language of instruction comparison (analyse13.py).
        
        Args:
            df (pd.DataFrame): The data to validate
            selected_columns (list): Selected columns for analysis
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Validate the data
        validation_result = self.validate_data(df, "language_effect", selected_columns)
        
        # Check if we have the language column
        if "language_teaching" not in df.columns:
            validation_result.add_error(get_text("no_language_column", "Error: No 'language_teaching' column found in the data."))
            self.error_handler.display_validation_results(validation_result)
            return False
        
        # Check if we have at least one column selected
        if len(selected_columns) == 0:
            validation_result.add_error(get_text("empty_selection", "No variables selected for analysis."))
            self.error_handler.display_validation_results(validation_result)
            return False
        
        # Check if language column has enough categories (at least 2)
        language_counts = df["language_teaching"].value_counts()
        if len(language_counts) < 2:
            validation_result.add_error(
                get_text("insufficient_language_categories", "At least two language categories are needed. Only {} found.").format(
                    len(language_counts)
                )
            )
            self.error_handler.display_validation_results(validation_result)
            return False
        
        return validation_result.valid
    
    def show_missing_values_analysis(self, df):
        """
        Show analysis of missing values in the data.
        
        Args:
            df (pd.DataFrame): The data to analyze
            
        Returns:
            pd.DataFrame: DataFrame with missing values analysis
        """
        missing_report = self.validator.get_missing_value_report(df)
        
        st.subheader(get_text("missing_values_analysis", "Missing Values Analysis"))
        st.dataframe(missing_report)
        
        # Option to visualize missing values
        if st.checkbox(get_text("visualize_missing", "Visualize missing values")):
            missing_fig = self.validator.plot_missing_values(df)
            st.pyplot(missing_fig)
        
        return missing_report
    
    def handle_missing_values(self, df):
        """
        Offer options to handle missing values in the data.
        
        Args:
            df (pd.DataFrame): The data to process
            
        Returns:
            pd.DataFrame: DataFrame with handled missing values
        """
        # Check if there are any missing values
        if not df.isna().any().any():
            st.info(get_text("no_missing_values", "No missing values found in the data."))
            return df
        
        st.subheader(get_text("handle_missing_values", "Handle Missing Values"))
        
        # Method selection
        method = st.selectbox(
            get_text("missing_method", "Method:"),
            options=["drop_rows", "fill_mean", "fill_median", "fill_mode"]
        )
        
        # Apply selected method
        if st.button(get_text("apply_method", "Apply method")):
            processed_df = self.validator.handle_missing_values(df, method=method)
            st.success(get_text("missing_handled", "Missing values handled successfully."))
            
            # Show comparison of rows before and after
            st.text(get_text("rows_before", "Rows before: {}").format(len(df)))
            st.text(get_text("rows_after", "Rows after: {}").format(len(processed_df)))
            
            return processed_df
        
        return df