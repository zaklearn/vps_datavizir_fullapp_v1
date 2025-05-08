# logging_config.py
import logging
import os
from datetime import datetime

class LoggerSetup:
    """Centralized logging configuration for EduInsight application."""
    
    @staticmethod
    def setup_logger(name, log_file=None, level=logging.INFO):
        """
        Set up a logger with the specified name and optional file handler.
        
        Args:
            name (str): Name of the logger
            log_file (str, optional): Path to log file
            level (int): Logging level
            
        Returns:
            logging.Logger: Configured logger instance
        """
        # Create logger
        logger = logging.getLogger(name)
        logger.setLevel(level)
        
        # Create formatters
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_formatter = logging.Formatter(
            '%(levelname)s: %(message)s'
        )
        
        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)
        
        # File handler (if log_file is provided)
        if log_file:
            # Ensure log directory exists
            log_dir = os.path.dirname(log_file)
            if log_dir and not os.path.exists(log_dir):
                os.makedirs(log_dir)
                
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(level)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        
        return logger

    @staticmethod
    def get_default_log_file():
        """
        Get default log file path with date.
        
        Returns:
            str: Path to log file
        """
        log_dir = os.path.join(os.path.dirname(__file__), 'logs')
        date_str = datetime.now().strftime('%Y-%m-%d')
        return os.path.join(log_dir, f'eduinsight_{date_str}.log')

    @staticmethod
    def initialize_application_logging():
        """
        Initialize application-wide logging with default settings.
        
        Returns:
            logging.Logger: Main application logger
        """
        default_log_file = LoggerSetup.get_default_log_file()
        
        # Main application logger
        app_logger = LoggerSetup.setup_logger(
            'eduinsight',
            log_file=default_log_file,
            level=logging.INFO
        )
        
        # Module-specific loggers
        module_loggers = {
            'school_comparison': 'eduinsight.school_comparison',
            'ses_analysis': 'eduinsight.ses_analysis',
            'gender_effect': 'eduinsight.gender_effect',
            'language_effect': 'eduinsight.language_effect',
            'contextual_factors': 'eduinsight.contextual_factors',
            'report_generator': 'eduinsight.report_generator'
        }
        
        loggers = {name: LoggerSetup.setup_logger(logger_name, log_file=default_log_file) 
                  for name, logger_name in module_loggers.items()}
        
        app_logger.info("EduInsight logging system initialized")
        return app_logger, loggers
