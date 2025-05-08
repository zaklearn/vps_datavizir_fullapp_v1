# report_school.py
# School performance report generator for analyse7.py

import os
import pandas as pd
import numpy as np
from language_utils import get_text
from report.report_base import BaseReportGenerator

class SchoolReportGenerator(BaseReportGenerator):
    """
    Report generator for school performance analysis (analyse7.py).
    """
    
    def create_report(self, df, selected_columns, title=None, temp_dir=None):
        """
        Create a school performance analysis report.
        
        Args:
            df: DataFrame with data
            selected_columns: List of columns to include
            title: Report title
            temp_dir: Directory for temporary files
            
        Returns:
            tuple: (doc, docx_bytes, filename)
        """
        # Common setup
        title, doc = self._common_setup(title, "title_school_performance")
        filename = "school_performance_report.docx"
        
        # Make sure school column exists
        if "school" not in df.columns:
            # Add error handling here as appropriate
            raise ValueError("School column not found in data")
        
        # Calculate mean scores by school
        mean_scores_by_school = df.groupby("school")[selected_columns].mean().round(2)
        
        # Calculate sample sizes by school
        sample_sizes = df.groupby("school").size().rename(get_text("sample_size", "Sample Size"))
        
        # Combine with mean scores for display
        performance_table = pd.concat([mean_scores_by_school, sample_sizes], axis=1)
        
        # Identify highest and lowest performing schools for each variable
        highlight_data = []
        
        for col in selected_columns:
            # Get translated column name
            col_name = get_text("columns_of_interest", {}).get(col, col)
            
            # Find highest and lowest performing schools
            highest_school = mean_scores_by_school[col].idxmax()
            highest_score = mean_scores_by_school.loc[highest_school, col]
            
            lowest_school = mean_scores_by_school[col].idxmin()
            lowest_score = mean_scores_by_school.loc[lowest_school, col]
            
            # Store in highlight data
            highlight_data.append({
                "variable": col_name,
                "highest_school": highest_school,
                "highest_score": highest_score,
                "lowest_school": lowest_school,
                "lowest_score": lowest_score,
                "range": highest_score - lowest_score
            })
        
        # Convert to DataFrame for display
        highlight_df = pd.DataFrame(highlight_data)
        highlight_df.columns = [
            get_text("variable", "Variable"),
            get_text("highest_school", "Highest School"),
            get_text("highest_score", "Highest Score"),
            get_text("lowest_school", "Lowest School"),
            get_text("lowest_score", "Lowest Score"),
            get_text("score_range", "Score Range")
        ]
        
        # Create visualizations for each variable
        visualization_paths = []
        
        for column in selected_columns:
            # Create box plot comparing schools
            fig = self.viz.show_school_comparison(df, column)
            
            # Save figure for inclusion in report
            img_path = self.viz.save_figure_for_word(fig, f"{column}_school_comparison.png")
            
            # Store path for later inclusion in report
            visualization_paths.append((column, img_path))
        
        # Add executive summary
        summary_text = get_text("school_performance_summary", 
                              "This report analyzes and compares performance across different schools to identify patterns and areas for improvement.")
        self.word_gen.add_executive_summary(summary_text)
        
        # Add methodology section
        methodology_text = get_text("school_performance_methodology", 
                                 "This analysis compares assessment results across different schools. " +
                                 "It identifies areas where certain schools may need additional support and " +
                                 "highlights successful practices from high-performing schools.")
        self.word_gen.add_methodology(methodology_text)
        
        # Add results section
        self.word_gen.add_section(get_text("results", "Results"), level=1)
        
        # Add mean scores table
        self.word_gen.add_table(
            performance_table.reset_index(), 
            title=get_text("school_performance_table", "Mean Scores by School")
        )
        
        # Add performance highlights
        self.word_gen.add_section(get_text("performance_highlights", "Performance Highlights"), level=2)
        
        # Add highlights table
        self.word_gen.add_table(
            highlight_df, 
            title=get_text("highest_lowest_performers", "Highest and Lowest Performing Schools")
        )
        
        # Add visualizations
        self.word_gen.add_section(get_text("school_distributions", "Score Distributions by School"), level=2)
        
        for column, img_path in visualization_paths:
            column_name = get_text("columns_of_interest", {}).get(column, column)
            
            # Add visualization to document
            self.word_gen.add_picture(
                img_path,
                title=f"{column_name} - {get_text('by_school', 'by School')}",
                width=6
            )
        
        # Add interpretation section
        self.word_gen.add_section(get_text("interpretation", "Interpretation"), level=1)
        
        # Calculate overall ranks for schools
        school_ranks = mean_scores_by_school.rank(ascending=False, method="min").mean(axis=1).sort_values()
        best_school = school_ranks.index[0]
        worst_school = school_ranks.index[-1]
        
        # Add overall performance summary
        overall_text = get_text("overall_performance_summary", 
                              "Overall, {} shows the strongest performance across multiple measures, " +
                              "while {} shows areas where additional support may be needed.").format(
                                  best_school, worst_school
                              )
        self.word_gen.add_paragraph(overall_text)
        
        # Identify variables with large disparities between schools
        large_gaps = pd.DataFrame(highlight_data).sort_values("range", ascending=False)
        
        if not large_gaps.empty:
            # Add information about largest gaps
            top_gap_var = large_gaps.iloc[0]["variable"]
            top_gap_best = large_gaps.iloc[0]["highest_school"]
            top_gap_worst = large_gaps.iloc[0]["lowest_school"]
            top_gap_range = large_gaps.iloc[0]["range"]
            
            gap_text = get_text("largest_performance_gap", 
                             "The largest performance gap was found in {}, with a difference of {:.2f} points " +
                             "between {} (highest) and {} (lowest).").format(
                                 top_gap_var, top_gap_range, top_gap_best, top_gap_worst
                             )
            self.word_gen.add_paragraph(gap_text)
        
        # Add recommendations section
        self.word_gen.add_section(get_text("recommendations", "Recommendations"), level=1)
        
        # Add general recommendations
        self.word_gen.add_paragraph(get_text("school_performance_recommendations", 
                                    "Based on the analysis of performance differences between schools, " +
                                    "the following recommendations are provided:"))
        
        # Add recommendations for low-performing schools
        self.word_gen.add_section(get_text("low_performing_recommendations", "For Lower-Performing Schools:"), level=2)
        self.word_gen.add_bullet_point(get_text("investigate_practices", 
                                       "Investigate successful practices from high-performing schools that could be adopted."))
        self.word_gen.add_bullet_point(get_text("targeted_professional_development", 
                                       "Provide targeted professional development in areas with the largest performance gaps."))
        self.word_gen.add_bullet_point(get_text("resource_allocation", 
                                       "Review resource allocation to ensure adequate support for improvement efforts."))
        
        # Add recommendations for high-performing schools
        self.word_gen.add_section(get_text("high_performing_recommendations", "For Higher-Performing Schools:"), level=2)
        self.word_gen.add_bullet_point(get_text("share_practices", 
                                       "Share successful instructional practices with other schools."))
        self.word_gen.add_bullet_point(get_text("mentorship", 
                                       "Consider mentorship or peer coaching programs to support struggling schools."))
        
        # Add system-level recommendations
        self.word_gen.add_section(get_text("system_recommendations", "System-Level Recommendations:"), level=2)
        self.word_gen.add_bullet_point(get_text("performance_monitoring", 
                                       "Establish regular performance monitoring to track progress in reducing school disparities."))
        self.word_gen.add_bullet_point(get_text("equity_review", 
                                       "Conduct an equity review to ensure all schools have access to necessary resources."))
        self.word_gen.add_bullet_point(get_text("professional_learning", 
                                       "Facilitate professional learning communities across schools to share best practices."))
        
        # Set up headers and footers
        self.word_gen.setup_headers_and_footers(title=title)
        
        # Save document and return
        doc, docx_bytes = self._save_and_get_bytes(doc, temp_dir, filename)
        
        return doc, docx_bytes, filename
            # Create box plot comparing schools