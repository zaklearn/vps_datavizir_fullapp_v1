# report_statistical.py
# Statistical report generator for analyse1.py

import os
from language_utils import get_text
from report.report_base import BaseReportGenerator

class StatisticalReportGenerator(BaseReportGenerator):
    """
    Report generator for statistical analysis (analyse1.py).
    """
    
    def create_report(self, df, selected_columns, title=None, temp_dir=None):
        """
        Create a statistical overview report.
        
        Args:
            df: DataFrame with data
            selected_columns: List of columns to include
            title: Report title
            temp_dir: Directory for temporary files
            
        Returns:
            tuple: (doc, docx_bytes, filename)
        """
        # Common setup
        title, doc = self._common_setup(title, "title_statistics")
        filename = "statistical_report.docx"
        
        # Calculate statistics
        stats_summary = df[selected_columns].describe(percentiles=[.25, .5, .75, .9]).round(2)
        
        # Add executive summary
        summary_text = get_text("statistical_overview_summary", 
                              "This report provides a statistical overview of the assessment results.")
        self.word_gen.add_executive_summary(summary_text)
        
        # Add methodology section
        methodology_text = get_text("statistical_methodology", 
                                "This analysis calculates descriptive statistics for the selected assessment variables. " +
                                "It includes measures of central tendency (mean, median), dispersion (standard deviation, range), " +
                                "and distribution characteristics for each variable.")
        self.word_gen.add_methodology(methodology_text)
        
        # Add results section
        self.word_gen.add_section(get_text("results", "Results"), level=1)
        
        # Add statistics table
        self.word_gen.add_table(
            stats_summary, 
            title=get_text("descriptive_statistics", "Descriptive Statistics")
        )
        
        # Add visualizations
        self.word_gen.add_section(get_text("visualizations", "Visualizations"), level=2)
        
        for column in selected_columns:
            column_name = get_text("columns_of_interest", {}).get(column, column)
            
            # Create histogram
            fig = self.viz.viz_utils.create_histogram(
                df[column],
                title=get_text("histogram_title", "Distribution of {}").format(column_name),
                show_normal=True
            )
            
            # Save figure for inclusion in report
            img_path = self.viz.save_figure_for_word(fig, f"{column}_histogram.png")
            
            # Add to report
            self.word_gen.add_picture(
                img_path,
                title=get_text("histogram_title", "Distribution of {}").format(column_name),
                width=6
            )
        
        # Add interpretation section
        self.word_gen.add_section(get_text("interpretation", "Interpretation"), level=1)
        
        for column in selected_columns:
            column_name = get_text("columns_of_interest", {}).get(column, column)
            mean_score = stats_summary.loc['mean', column]
            
            # Determine interpretation based on mean score
            if mean_score < 30:
                interp_text = get_text("very_low_interpretation", 
                                    "Performance is at a very low level, requiring immediate intervention.")
                rec_text = get_text("very_low_recommendation", 
                                 "Focus on strengthening fundamental skills through targeted interventions.")
            elif mean_score < 50:
                interp_text = get_text("low_interpretation", 
                                    "Performance is below average, suggesting need for targeted support.")
                rec_text = get_text("low_recommendation", 
                                 "Provide additional support and practice opportunities.")
            elif mean_score < 70:
                interp_text = get_text("average_interpretation", 
                                    "Performance is at an average level.")
                rec_text = get_text("average_recommendation", 
                                 "Continue with current instructional approach while monitoring progress.")
            elif mean_score < 85:
                interp_text = get_text("good_interpretation", 
                                    "Performance is at a good level.")
                rec_text = get_text("good_recommendation", 
                                 "Maintain current effective practices and consider enrichment for advanced students.")
            else:
                interp_text = get_text("excellent_interpretation", 
                                    "Performance is at an excellent level.")
                rec_text = get_text("excellent_recommendation", 
                                 "Continue successful practices and consider extending with more advanced content.")
            
            # Add interpretation for this column
            self.word_gen.add_section(column_name, level=2)
            self.word_gen.add_interpretation(interp_text, column_name, mean_score)
            self.word_gen.add_recommendation(rec_text, column_name, mean_score)
        
        # Set up headers and footers
        self.word_gen.setup_headers_and_footers(title=title)
        
        # Save document and return
        doc, docx_bytes = self._save_and_get_bytes(doc, temp_dir, filename)
        
        return doc, docx_bytes, filename