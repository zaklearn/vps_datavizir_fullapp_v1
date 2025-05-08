# report_base.py
# Base class for report generators

import os
import streamlit as st
from language_utils import get_text, get_current_language

class BaseReportGenerator:
    """
    Base class for all specialized report generators.
    """
    
    def __init__(self, word_generator, visualization):
        """
        Initialize the base report generator.
        
        Args:
            word_generator: WordReportGenerator instance
            visualization: StandardVisualization instance
        """
        self.word_gen = word_generator
        self.viz = visualization
        self.language = get_current_language()
    
    def update_word_generator(self, word_generator):
        """
        Update the word generator, typically after language change.
        
        Args:
            word_generator: New WordReportGenerator instance
        """
        self.word_gen = word_generator
        self.language = get_current_language()
    
    def create_report(self, df, selected_columns, title=None, temp_dir=None):
        """
        Base method for creating reports. To be implemented by subclasses.
        
        Args:
            df: DataFrame with data
            selected_columns: List of columns to include
            title: Report title
            temp_dir: Directory for temporary files
            
        Returns:
            tuple: (doc, docx_bytes, filename)
        """
        raise NotImplementedError("Subclasses must implement create_report method")
    
    def _save_and_get_bytes(self, doc, temp_dir, filename):
        """
        Save document to temporary file and read it as bytes.
        
        Args:
            doc: Document to save
            temp_dir: Directory for temporary files
            filename: Filename to use
            
        Returns:
            tuple: (doc, docx_bytes)
        """
        # Save document to temporary file
        temp_file = os.path.join(temp_dir, filename)
        self.word_gen.save(temp_file)
        
        # Read file as bytes
        with open(temp_file, 'rb') as f:
            docx_bytes = f.read()
        
        return doc, docx_bytes
    
    def _common_setup(self, title, default_title):
        """
        Common setup for report generation.
        
        Args:
            title: Custom title or None
            default_title: Default title to use if none provided
            
        Returns:
            str: Final title to use
            Document: Initialized Word document
        """
        # Generate report title
        if title is None:
            title = get_text(default_title, default_title)
        
        # Create Word document
        doc = self.word_gen.create_new_report(title)
        
        return title, doc