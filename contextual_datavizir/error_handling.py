# error_handling.py
import streamlit as st
import logging
import functools
from typing import Callable, Any, Dict

class EduInsightError(Exception):
    """Base exception class for EduInsight application errors."""
    def __init__(self, message: str, error_code: str = None, details: Dict = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)

class DataValidationError(EduInsightError):
    """Raised when data validation fails."""
    pass

class VisualizationError(EduInsightError):
    """Raised when visualization creation fails."""
    pass

class ReportGenerationError(EduInsightError):
    """Raised when report generation fails."""
    pass

def error_handler(logger_name: str):
    """
    Decorator for handling errors in module functions.
    
    Args:
        logger_name (str): Name of the logger to use
        
    Returns:
        Callable: Decorated function
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger = logging.getLogger(logger_name)
            try:
                return func(*args, **kwargs)
            except EduInsightError as e:
                logger.error(f"{e.__class__.__name__}: {e.message}", 
                            extra={'error_code': e.error_code, 'details': e.details})
                st.error(f"{e.message} (Error code: {e.error_code})")
                return None
            except Exception as e:
                logger.exception(f"Unexpected error in {func.__name__}")
                st.error(f"An unexpected error occurred: {str(e)}")
                return None
        return wrapper
    return decorator

def validate_dataframe(df, required_columns, logger_name):
    """
    Validate a dataframe for required columns.
    
    Args:
        df (pd.DataFrame): DataFrame to validate
        required_columns (list): List of required column names
        logger_name (str): Name of the logger to use
        
    Raises:
        DataValidationError: If validation fails
    """
    logger = logging.getLogger(logger_name)
    
    if df is None:
        logger.error("Dataframe is None")
        raise DataValidationError("No data provided", error_code="DF_NONE")
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        logger.error(f"Missing columns: {missing_columns}")
        raise DataValidationError(
            f"Missing required columns: {', '.join(missing_columns)}",
            error_code="DF_MISSING_COLUMNS",
            details={"missing": missing_columns}
        )
    
    logger.debug(f"Dataframe validated successfully with columns: {list(df.columns)}")
    return True

def safe_plot_creation(plot_func, func_name, error_message, logger_name):
    """
    Safely create a plot with error handling.
    
    Args:
        plot_func (Callable): Function that creates the plot
        func_name (str): Name of the function for logging
        error_message (str): Message to display on error
        logger_name (str): Name of the logger to use
        
    Returns:
        plotly.Figure: The created plot, or None if creation failed
    """
    logger = logging.getLogger(logger_name)
    try:
        fig = plot_func()
        logger.debug(f"Successfully created plot: {func_name}")
        return fig
    except Exception as e:
        logger.error(f"Error creating plot {func_name}: {str(e)}")
        st.warning(error_message)
        return None

def safe_data_operation(operation_func, func_name, error_message, logger_name):
    """
    Safely perform a data operation with error handling.
    
    Args:
        operation_func (Callable): Function that performs the operation
        func_name (str): Name of the function for logging
        error_message (str): Message to display on error
        logger_name (str): Name of the logger to use
        
    Returns:
        Any: Result of the operation, or None if operation failed
    """
    logger = logging.getLogger(logger_name)
    try:
        result = operation_func()
        logger.debug(f"Successfully completed operation: {func_name}")
        return result
    except Exception as e:
        logger.error(f"Error in operation {func_name}: {str(e)}")
        st.warning(error_message)
        return None
