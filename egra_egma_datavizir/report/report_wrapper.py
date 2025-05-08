# report_wrapper.py
# Main module that integrates report generation functionalities

import streamlit as st
import pandas as pd
import tempfile
import os
import importlib
from io import BytesIO
from datetime import datetime
from language_utils import get_text, get_current_language, format_date
from report_utils import AnalysisReportGenerator
from word_report import WordReportGenerator
from viz_wrapper import StandardVisualization

# Import specialized report generators
from report.report_statistical import StatisticalReportGenerator
from report.report_zero_scores import ZeroScoresReportGenerator
from report.report_correlation import CorrelationReportGenerator
from report.report_reliability import ReliabilityReportGenerator
from report.report_school import SchoolReportGenerator
from report.report_gender import GenderReportGenerator
from report.report_international import InternationalReportGenerator
from report.report_language import LanguageReportGenerator

class StandardReportGenerator:
    """
    Standardized report generator wrapper that integrates specialized report generators
    for different analysis types.
    """
    
    def __init__(self):
        """Initialize the report generators."""
        self.language = get_current_language()
        self.report_gen = AnalysisReportGenerator()
        self.word_gen = WordReportGenerator(language=self.language)
        self.viz = StandardVisualization()
        self.temp_dir = None
        
        # Initialize specialized report generators
        self.statistical_generator = StatisticalReportGenerator(self.word_gen, self.viz)
        self.zero_scores_generator = ZeroScoresReportGenerator(self.word_gen, self.viz)
        self.correlation_generator = CorrelationReportGenerator(self.word_gen, self.viz)
        self.reliability_generator = ReliabilityReportGenerator(self.word_gen, self.viz)
        self.school_generator = SchoolReportGenerator(self.word_gen, self.viz)
        self.gender_generator = GenderReportGenerator(self.word_gen, self.viz)
        self.international_generator = InternationalReportGenerator(self.word_gen, self.viz)
        self.language_generator = LanguageReportGenerator(self.word_gen, self.viz)
    
    def update_language(self, language=None):
        """Update the language setting."""
        if language is None:
            language = get_current_language()
        self.language = language
        self.word_gen = WordReportGenerator(language=language)
        self.viz.update_language(language)
        
        # Update language for all specialized generators
        self.statistical_generator.update_word_generator(self.word_gen)
        self.zero_scores_generator.update_word_generator(self.word_gen)
        self.correlation_generator.update_word_generator(self.word_gen)
        self.reliability_generator.update_word_generator(self.word_gen)
        self.school_generator.update_word_generator(self.word_gen)
        self.gender_generator.update_word_generator(self.word_gen)
        self.international_generator.update_word_generator(self.word_gen)
        self.language_generator.update_word_generator(self.word_gen)
    
    def _ensure_temp_dir(self):
        """Ensure a temporary directory exists."""
        if self.temp_dir is None:
            self.temp_dir = tempfile.mkdtemp()
        return self.temp_dir
    
    def cleanup(self):
        """Clean up temporary files."""
        if self.temp_dir:
            import shutil
            try:
                shutil.rmtree(self.temp_dir)
                self.temp_dir = None
            except:
                pass
        self.viz.cleanup()
    
    def create_statistical_report(self, df, selected_columns, title=None):
        """
        Create a statistical overview report (analyse1.py).
        
        Args:
            df (pd.DataFrame): DataFrame containing the data
            selected_columns (list): List of columns to include in the report
            title (str, optional): Report title
            
        Returns:
            tuple: (doc, docx_bytes, filename)
        """
        return self.statistical_generator.create_report(
            df, selected_columns, title, self._ensure_temp_dir()
        )
    
    def create_zero_scores_report(self, df, selected_columns, title=None):
        """
        Create a zero scores analysis report (analyse2.py).
        
        Args:
            df (pd.DataFrame): DataFrame containing the data
            selected_columns (list): List of columns to include in the report
            title (str, optional): Report title
            
        Returns:
            tuple: (doc, docx_bytes, filename)
        """
        return self.zero_scores_generator.create_report(
            df, selected_columns, title, self._ensure_temp_dir()
        )
    
    def create_correlation_report(self, df, selected_columns, title=None):
        """
        Create a correlation analysis report (analyse5.py).
        
        Args:
            df (pd.DataFrame): DataFrame containing the data
            selected_columns (list): List of columns to include in the report
            title (str, optional): Report title
            
        Returns:
            tuple: (doc, docx_bytes, filename)
        """
        return self.correlation_generator.create_report(
            df, selected_columns, title, self._ensure_temp_dir()
        )
    
    def create_reliability_report(self, df, selected_columns, title=None):
        """
        Create a reliability analysis report (analyse6.py).
        
        Args:
            df (pd.DataFrame): DataFrame containing the data
            selected_columns (list): List of columns to include in the report
            title (str, optional): Report title
            
        Returns:
            tuple: (doc, docx_bytes, filename)
        """
        return self.reliability_generator.create_report(
            df, selected_columns, title, self._ensure_temp_dir()
        )
    
    def create_school_report(self, df, selected_columns, title=None):
        """
        Create a school performance analysis report (analyse7.py).
        
        Args:
            df (pd.DataFrame): DataFrame containing the data
            selected_columns (list): List of columns to include in the report
            title (str, optional): Report title
            
        Returns:
            tuple: (doc, docx_bytes, filename)
        """
        return self.school_generator.create_report(
            df, selected_columns, title, self._ensure_temp_dir()
        )
    
    def create_gender_report(self, df, selected_columns, title=None):
        """
        Create a gender effect analysis report (analyse10.py).
        
        Args:
            df (pd.DataFrame): DataFrame containing the data
            selected_columns (list): List of columns to include in the report
            title (str, optional): Report title
            
        Returns:
            tuple: (doc, docx_bytes, filename)
        """
        return self.gender_generator.create_report(
            df, selected_columns, title, self._ensure_temp_dir()
        )
    
    def create_international_report(self, df, selected_columns, benchmarks, title=None):
        """
        Create an international standards comparison report (analyse12.py).
        
        Args:
            df (pd.DataFrame): DataFrame containing the data
            selected_columns (list): List of columns to include in the report
            benchmarks (dict): Dictionary of benchmark values
            title (str, optional): Report title
            
        Returns:
            tuple: (doc, docx_bytes, filename)
        """
        return self.international_generator.create_report(
            df, selected_columns, benchmarks, title, self._ensure_temp_dir()
        )
    
    def create_language_report(self, df, selected_columns, title=None):
        """
        Create a language of instruction comparison report (analyse13.py).
        
        Args:
            df (pd.DataFrame): DataFrame containing the data
            selected_columns (list): List of columns to include in the report
            title (str, optional): Report title
            
        Returns:
            tuple: (doc, docx_bytes, filename)
        """
        return self.language_generator.create_report(
            df, selected_columns, title, self._ensure_temp_dir()
        )
    
    def offer_download(self, docx_bytes, filename):
        """
        Offer a download button for the Word report.
        
        Args:
            docx_bytes (bytes): Word document as bytes
            filename (str): Filename for download
            
        Returns:
            bool: True if button was clicked
        """
        return st.download_button(
            get_text("download_word", "📥 Download Word Report"),
            docx_bytes,
            filename,
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )