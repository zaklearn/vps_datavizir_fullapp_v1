# report_gender.py
# Gender effect report generator for analyse10.py

import os
import pandas as pd
import numpy as np
from language_utils import get_text
from report.report_base import BaseReportGenerator

class GenderReportGenerator(BaseReportGenerator):
    """
    Report generator for gender effect analysis (analyse10.py).
    """
    
    def create_report(self, df, selected_columns, title=None, temp_dir=None):
        """
        Create a gender effect analysis report.
        
        Args:
            df: DataFrame with data
            selected_columns: List of columns to include
            title: Report title
            temp_dir: Directory for temporary files
            
        Returns:
            tuple: (doc, docx_bytes, filename)
        """
        # Common setup
        title, doc = self._common_setup(title, "title_gender_effect")
        filename = "gender_effect_report.docx"
        
        # Make sure gender column exists
        if "stgender" not in df.columns:
            # Add error handling here as appropriate
            raise ValueError("Gender column (stgender) not found in data")
        
        # Prepare data - map gender codes to labels and handle missing values
        df_analysis = df.copy()
        
        # Check the unique values in stgender to determine mapping approach
        gender_values = df_analysis['stgender'].dropna().unique()
        
        # Determine if gender is coded as 0/1 or has string values
        if all(isinstance(x, (int, float)) for x in gender_values):
            # Numeric coding
            df_analysis["gender"] = df_analysis["stgender"].map({
                1: get_text("boy", "Boy"), 
                0: get_text("girl", "Girl")
            }).fillna(get_text("unknown", "Unknown"))
        else:
            # Try to map using common string values (case-insensitive)
            gender_map = {}
            for val in gender_values:
                if isinstance(val, str):
                    if val.lower() in ['boy', 'boys', 'male', 'm', 'homme', 'garçon']:
                        gender_map[val] = get_text("boy", "Boy")
                    elif val.lower() in ['girl', 'girls', 'female', 'f', 'femme', 'fille']:
                        gender_map[val] = get_text("girl", "Girl")
                    else:
                        gender_map[val] = get_text("unknown", "Unknown")
                else:
                    gender_map[val] = get_text("unknown", "Unknown")
            
            df_analysis["gender"] = df_analysis["stgender"].map(gender_map).fillna(get_text("unknown", "Unknown"))
        
        # Remove unknown gender for analysis
        df_analysis = df_analysis[df_analysis["gender"] != get_text("unknown", "Unknown")]
        
        # Calculate mean scores by gender
        mean_scores_by_gender = df_analysis.groupby("gender")[selected_columns].mean().round(2)
        
        # Calculate sample sizes by gender for reference
        sample_sizes = df_analysis.groupby("gender").size().rename(get_text("sample_size", "Sample Size"))
        
        # Combine with mean scores for display
        performance_table = pd.concat([mean_scores_by_gender, sample_sizes], axis=1)
        
        # Create visualizations for each variable
        visualization_paths = []
        
        for column in selected_columns:
            # Create box plot comparing genders
            fig = self.viz.show_gender_comparison(df_analysis, column, gender_col="gender")
            
            # Save figure for inclusion in report
            img_path = self.viz.save_figure_for_word(fig, f"{column}_gender_comparison.png")
            
            # Store path for later inclusion in report
            visualization_paths.append((column, img_path))
        
        # Perform statistical significance testing (Mann-Whitney U test) for each variable
        from scipy import stats
        
        test_results = []
        for col in selected_columns:
            col_name = get_text("columns_of_interest", {}).get(col, col)
            
            # Get data for boys and girls
            boys_data = df_analysis[df_analysis["gender"] == get_text("boy", "Boy")][col].dropna()
            girls_data = df_analysis[df_analysis["gender"] == get_text("girl", "Girl")][col].dropna()
            
            # Calculate means for effect direction
            boys_mean = boys_data.mean()
            girls_mean = girls_data.mean()
            
            # Perform Mann-Whitney test if we have data for both groups
            if len(boys_data) > 0 and len(girls_data) > 0:
                try:
                    u_stat, p_value = stats.mannwhitneyu(boys_data, girls_data, alternative='two-sided')
                    
                    # Determine which gender performed better
                    better_gender = get_text("boy", "Boy") if boys_mean > girls_mean else get_text("girl", "Girl")
                    
                    test_results.append({
                        "variable": col_name,
                        "boys_mean": boys_mean,
                        "girls_mean": girls_mean,
                        "difference": abs(boys_mean - girls_mean),
                        "percent_diff": abs(boys_mean - girls_mean) / ((boys_mean + girls_mean) / 2) * 100 if boys_mean + girls_mean > 0 else 0,
                        "better_gender": better_gender,
                        "u_statistic": u_stat,
                        "p_value": p_value,
                        "significant": p_value < 0.05
                    })
                except Exception as e:
                    # Handle errors in statistical testing
                    test_results.append({
                        "variable": col_name,
                        "boys_mean": boys_mean,
                        "girls_mean": girls_mean,
                        "difference": abs(boys_mean - girls_mean),
                        "percent_diff": abs(boys_mean - girls_mean) / ((boys_mean + girls_mean) / 2) * 100 if boys_mean + girls_mean > 0 else 0,
                        "better_gender": None,
                        "u_statistic": None,
                        "p_value": None,
                        "significant": None,
                        "error": str(e)
                    })
        
        # Identify significant differences
        sig_differences = [r for r in test_results if r.get("significant")]
        boy_advantage = [r for r in sig_differences if r.get("better_gender") == get_text("boy", "Boy")]
        girl_advantage = [r for r in sig_differences if r.get("better_gender") == get_text("girl", "Girl")]
        
        # Add executive summary
        summary_text = get_text("gender_effect_summary", 
                              "This report analyzes differences in performance between boys and girls across assessment variables.")
        self.word_gen.add_executive_summary(summary_text)
        
        # Add methodology section
        methodology_text = get_text("gender_effect_methodology", 
                                 "This analysis compares assessment results between boys and girls using both descriptive statistics " +
                                 "and the Mann-Whitney U test, which is appropriate for comparing two independent groups. " +
                                 "The analysis identifies areas where significant gender differences exist and their educational implications.")
        self.word_gen.add_methodology(methodology_text)
        
        # Add results section
        self.word_gen.add_section(get_text("results", "Results"), level=1)
        
        # Add gender performance table
        self.word_gen.add_table(
            performance_table.reset_index(), 
            title=get_text("gender_performance_table", "Mean Scores by Gender")
        )
        
        # Add visualizations
        self.word_gen.add_section(get_text("gender_distributions", "Score Distributions by Gender"), level=2)
        
        for column, img_path in visualization_paths:
            column_name = get_text("columns_of_interest", {}).get(column, column)
            
            # Add visualization to document
            self.word_gen.add_picture(
                img_path,
                title=f"{column_name} - {get_text('by_gender', 'by Gender')}",
                width=6
            )
        
        # Add statistical test results
        if test_results:
            self.word_gen.add_section(get_text("statistical_testing", "Statistical Significance Testing"), level=2)
            
            # Create a DataFrame from test results
            test_df = pd.DataFrame(test_results)
            
            # Format columns for display
            display_df = test_df[["variable", "boys_mean", "girls_mean", "difference", "better_gender", "p_value", "significant"]]
            display_df.columns = [
                get_text("variable", "Variable"),
                get_text("boys_mean", "Boys Mean"),
                get_text("girls_mean", "Girls Mean"),
                get_text("difference", "Difference"),
                get_text("better_gender", "Better Performance"),
                get_text("p_value", "p-value"),
                get_text("significant", "Significant")
            ]
            
            # Format p-values for display
            display_df[get_text("p_value", "p-value")] = display_df[get_text("p_value", "p-value")].apply(
                lambda x: f"{x:.4f}" if pd.notnull(x) else "N/A"
            )
            
            # Format significant column
            display_df[get_text("significant", "Significant")] = display_df[get_text("significant", "Significant")].apply(
                lambda x: get_text("significant_yes", "Yes") if x else get_text("significant_no", "No") if pd.notnull(x) else "N/A"
            )
            
            # Add test results table
            self.word_gen.add_table(
                display_df, 
                title=get_text("gender_test_results", "Statistical Test Results")
            )
        
        # Add interpretation section
        self.word_gen.add_section(get_text("interpretation", "Interpretation"), level=1)
        
        # Add summary of gender differences
        if sig_differences:
            interp_text = get_text("significant_diff_found", 
                               "Significant gender differences were found in {} out of {} variables analyzed.").format(
                                   len(sig_differences), len(test_results)
                               )
            self.word_gen.add_paragraph(interp_text)
            
            # Add details about boy advantages
            if boy_advantage:
                self.word_gen.add_section(get_text("boy_advantage", "Areas Where Boys Performed Better:"), level=2)
                
                for result in boy_advantage:
                    adv_text = get_text("gender_advantage_detail", 
                                    "{}: Boys outperformed girls by {:.2f} points ({:.1f}%).").format(
                                        result["variable"], result["difference"], result["percent_diff"]
                                    )
                    self.word_gen.add_bullet_point(adv_text)
            
            # Add details about girl advantages
            if girl_advantage:
                self.word_gen.add_section(get_text("girl_advantage", "Areas Where Girls Performed Better:"), level=2)
                
                for result in girl_advantage:
                    adv_text = get_text("gender_advantage_detail", 
                                    "{}: Girls outperformed boys by {:.2f} points ({:.1f}%).").format(
                                        result["variable"], result["difference"], result["percent_diff"]
                                    )
                    self.word_gen.add_bullet_point(adv_text)
        else:
            # No significant differences
            interp_text = get_text("no_significant_diff", """
            No statistically significant gender differences were found.
            
            This suggests that both boys and girls are performing at similar levels across the assessed skills,
            indicating equitable educational outcomes between genders.
            """)
            self.word_gen.add_paragraph(interp_text)
        
        # Add recommendations section
        self.word_gen.add_section(get_text("recommendations", "Recommendations"), level=1)
        
        # Add educational implications and recommendations
        if sig_differences:
            # Check which types of variables show gender differences
            reading_diffs = [r for r in sig_differences if any(col in r["variable"] for col in ["Letter", "Phon", "Word", "Reading", "Comprehension"])]
            math_diffs = [r for r in sig_differences if any(col in r["variable"] for col in ["Number", "Addition", "Subtraction", "Problem"])]
            
            if reading_diffs:
                self.word_gen.add_section(get_text("reading_recommendations", "For Reading Skills:"), level=2)
                self.word_gen.add_bullet_point(get_text("reading_implications", 
                                              "Consider gender-responsive teaching strategies to address observed differences in reading."))
                
                for diff in reading_diffs:
                    if diff["better_gender"] == get_text("boy", "Boy"):
                        self.word_gen.add_bullet_point(get_text("boy_reading_advantage_rec", 
                                                      "Provide additional support for girls in {} through targeted activities.").format(
                                                          diff["variable"]
                                                      ))
                    else:
                        self.word_gen.add_bullet_point(get_text("girl_reading_advantage_rec", 
                                                      "Provide additional support for boys in {} through targeted activities.").format(
                                                          diff["variable"]
                                                      ))
            
            if math_diffs:
                self.word_gen.add_section(get_text("math_recommendations", "For Math Skills:"), level=2)
                self.word_gen.add_bullet_point(get_text("math_implications", 
                                              "Implement targeted interventions to close gender gaps in mathematical performance."))
                
                for diff in math_diffs:
                    if diff["better_gender"] == get_text("boy", "Boy"):
                        self.word_gen.add_bullet_point(get_text("boy_math_advantage_rec", 
                                                      "Provide additional support for girls in {} through targeted activities.").format(
                                                          diff["variable"]
                                                      ))
                    else:
                        self.word_gen.add_bullet_point(get_text("girl_math_advantage_rec", 
                                                      "Provide additional support for boys in {} through targeted activities.").format(
                                                          diff["variable"]
                                                      ))
            
            # Add general recommendations
            self.word_gen.add_section(get_text("general_recommendations", "General Recommendations:"), level=2)
            self.word_gen.add_bullet_point(get_text("review_materials", 
                                          "Review teaching materials and methods for potential gender bias."))
            self.word_gen.add_bullet_point(get_text("collaborative_learning", 
                                          "Consider mixed-gender collaborative learning activities to leverage strengths of both genders."))
            self.word_gen.add_bullet_point(get_text("targeted_support", 
                                          "Provide targeted support for the lower-performing gender in specific skill areas."))
            self.word_gen.add_bullet_point(get_text("monitor_progress", 
                                          "Monitor progress to ensure equitable outcomes."))
        else:
            # Recommendations for equitable performance
            self.word_gen.add_bullet_point(get_text("maintain_equity", 
                                          "Continue with current equitable instructional practices."))
            self.word_gen.add_bullet_point(get_text("monitor_equity", 
                                          "Continue monitoring gender differences to ensure equitable outcomes are maintained."))
            self.word_gen.add_bullet_point(get_text("inclusive_strategies", 
                                          "Maintain gender-inclusive strategies that have proven effective for both boys and girls."))
        
        # Set up headers and footers
        self.word_gen.setup_headers_and_footers(title=title)
        
        # Save document and return
        doc, docx_bytes = self._save_and_get_bytes(doc, temp_dir, filename)
        
        return doc, docx_bytes, filename