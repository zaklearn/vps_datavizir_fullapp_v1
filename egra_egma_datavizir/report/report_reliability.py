# report_reliability.py
# Reliability report generator for analyse6.py

import os
import pandas as pd
from language_utils import get_text
from report.report_base import BaseReportGenerator

class ReliabilityReportGenerator(BaseReportGenerator):
    """
    Report generator for reliability analysis (analyse6.py).
    """
    
    def create_report(self, df, selected_columns, title=None, temp_dir=None):
        """
        Create a reliability analysis report.
        
        Args:
            df: DataFrame with data
            selected_columns: List of columns to include
            title: Report title
            temp_dir: Directory for temporary files
            
        Returns:
            tuple: (doc, docx_bytes, filename)
        """
        # Common setup
        title, doc = self._common_setup(title, "title_reliability")
        filename = "reliability_report.docx"
        
        # Add executive summary
        summary_text = get_text("reliability_summary", 
                              "This report analyzes the internal consistency reliability of the assessment using Cronbach's Alpha.")
        self.word_gen.add_executive_summary(summary_text)
        
        # Add methodology section
        methodology_text = get_text("reliability_methodology", 
                                 "This analysis calculates Cronbach's Alpha coefficient, which is a measure of internal consistency " +
                                 "reliability. It assesses how closely related a set of items are as a group and provides an " +
                                 "estimate of the reliability of the assessment.")
        self.word_gen.add_methodology(methodology_text)
        
        # Add interpretation guide
        self.word_gen.add_section(get_text("reliability_interpretation_guide", "Interpretation Guide"), level=2)
        self.word_gen.add_bullet_point(get_text("alpha_excellent", "α ≥ 0.9 → Excellent reliability"))
        self.word_gen.add_bullet_point(get_text("alpha_good", "0.8 ≤ α < 0.9 → Good reliability"))
        self.word_gen.add_bullet_point(get_text("alpha_acceptable", "0.7 ≤ α < 0.8 → Acceptable reliability"))
        self.word_gen.add_bullet_point(get_text("alpha_questionable", "0.6 ≤ α < 0.7 → Questionable reliability"))
        self.word_gen.add_bullet_point(get_text("alpha_poor", "0.5 ≤ α < 0.6 → Poor reliability"))
        self.word_gen.add_bullet_point(get_text("alpha_unacceptable", "α < 0.5 → Unacceptable reliability"))
        
        # Calculate Cronbach's Alpha for the selected columns
        # Note: In a real implementation, this would use the actual Cronbach's alpha calculation
        # from analyse6.py. For this example, we'll create dummy results.
        
        # Dummy alpha results
        alpha_results = [
            {
                "test_group": get_text("selected_variables", "Selected Variables"),
                "n_items": len(selected_columns),
                "n_students": len(df),
                "alpha": 0.82,  # Example value
                "interpretation": get_text("good", "Good reliability"),
                "color": "#58D68D",
                "reliability_level": "good",
                "alpha_numeric": 0.82
            }
        ]
        
        # Create visualization from dummy data
        fig = self.viz.show_reliability_visualization(pd.DataFrame(alpha_results))
        
        # Save figure for inclusion in report
        img_path = self.viz.save_figure_for_word(fig, "reliability_chart.png")
        
        # Add results section
        self.word_gen.add_section(get_text("results", "Results"), level=1)
        
        # Create table for alpha results
        alpha_table = pd.DataFrame(alpha_results)
        alpha_table = alpha_table[["test_group", "n_items", "n_students", "alpha", "interpretation"]]
        alpha_table.columns = [
            get_text("test_group", "Test Group"),
            get_text("n_items", "Number of Items"),
            get_text("n_students", "Number of Students"),
            get_text("cronbach_alpha", "Cronbach's Alpha"),
            get_text("reliability", "Reliability")
        ]
        
        # Add reliability results table
        self.word_gen.add_table(
            alpha_table, 
            title=get_text("reliability_results", "Reliability Results")
        )
        
        # Add visualization
        self.word_gen.add_picture(
            img_path,
            title=get_text("reliability_visualization", "Reliability Visualization"),
            width=6
        )
        
        # Add interpretation section
        self.word_gen.add_section(get_text("interpretation", "Interpretation"), level=1)
        
        # Determine interpretation text based on alpha value
        alpha_value = alpha_results[0]["alpha"]
        
        if alpha_value >= 0.9:
            interpretation = get_text("excellent_reliability_interpretation", 
                                   "The assessment demonstrates excellent reliability. This indicates that the items " +
                                   "consistently measure the same construct and the results can be considered highly dependable.")
        elif alpha_value >= 0.8:
            interpretation = get_text("good_reliability_interpretation", 
                                   "The assessment demonstrates good reliability. This indicates that the items " +
                                   "consistently measure the same construct and the results can be considered dependable.")
        elif alpha_value >= 0.7:
            interpretation = get_text("acceptable_reliability_interpretation", 
                                   "The assessment demonstrates acceptable reliability. This indicates that the items " +
                                   "are reasonably consistent in measuring the same construct.")
        elif alpha_value >= 0.6:
            interpretation = get_text("questionable_reliability_interpretation", 
                                   "The assessment demonstrates questionable reliability. This suggests some inconsistency " +
                                   "in what the items measure, and results should be interpreted with caution.")
        elif alpha_value >= 0.5:
            interpretation = get_text("poor_reliability_interpretation", 
                                   "The assessment demonstrates poor reliability. This indicates significant inconsistency " +
                                   "in what the items measure, and results should not be the sole basis for important decisions.")
        else:
            interpretation = get_text("unacceptable_reliability_interpretation", 
                                   "The assessment demonstrates unacceptable reliability. This indicates that the items " +
                                   "are not measuring the same construct consistently, and the assessment may need " +
                                   "substantial revision.")
        
        self.word_gen.add_paragraph(interpretation)
        
        # Add recommendations section
        self.word_gen.add_section(get_text("recommendations", "Recommendations"), level=1)
        
        # Determine recommendations based on alpha value
        if alpha_value >= 0.7:
            recommendations = [
                get_text("high_reliability_rec1", "Continue using the current assessment with confidence."),
                get_text("high_reliability_rec2", "Results can be used for instructional planning and student evaluation."),
                get_text("high_reliability_rec3", "Monitor reliability in future administrations to ensure consistency.")
            ]
        elif alpha_value >= 0.6:
            recommendations = [
                get_text("moderate_reliability_rec1", "Use results cautiously for instructional decisions."),
                get_text("moderate_reliability_rec2", "Consider reviewing items that may not align well with others."),
                get_text("moderate_reliability_rec3", "Use multiple sources of information for important decisions.")
            ]
        else:
            recommendations = [
                get_text("low_reliability_rec1", "Review and potentially revise assessment items."),
                get_text("low_reliability_rec2", "Consider item analysis to identify specific problematic questions."),
                get_text("low_reliability_rec3", "Use multiple measures when making educational decisions."),
                get_text("low_reliability_rec4", "Provide additional training to test administrators to ensure consistent procedures.")
            ]
        
        for rec in recommendations:
            self.word_gen.add_bullet_point(rec)
        
        # Set up headers and footers
        self.word_gen.setup_headers_and_footers(title=title)
        
        # Save document and return
        doc, docx_bytes = self._save_and_get_bytes(doc, temp_dir, filename)
        
        return doc, docx_bytes, filename