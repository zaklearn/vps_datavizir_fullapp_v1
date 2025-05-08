# report_international.py
# International comparison report generator for analyse12.py

import os
import pandas as pd
from language_utils import get_text
from report.report_base import BaseReportGenerator

class InternationalReportGenerator(BaseReportGenerator):
    """
    Report generator for international standards comparison (analyse12.py).
    """
    
    def create_report(self, df, selected_columns, benchmarks, title=None, temp_dir=None):
        """
        Create an international standards comparison report.
        
        Args:
            df: DataFrame with data
            selected_columns: List of columns to include
            benchmarks: Dictionary of benchmark values
            title: Report title
            temp_dir: Directory for temporary files
            
        Returns:
            tuple: (doc, docx_bytes, filename)
        """
        # Common setup
        title, doc = self._common_setup(title, "title_international_comparison")
        filename = "international_comparison_report.docx"
        
        # Calculate local mean scores
        local_means = df[selected_columns].mean().round(2)
        
        # Get international benchmarks for selected columns
        benchmark_values = {col: benchmarks[col]["standard"] for col in selected_columns if col in benchmarks}
        
        # Calculate gaps between local means and benchmarks
        gaps = pd.Series({col: local_means[col] - benchmark_values[col] for col in selected_columns if col in benchmark_values})
        
        # Calculate percentage of benchmark achieved
        percentage_achieved = pd.Series({
            col: (local_means[col] / benchmark_values[col] * 100).round(1) for col in selected_columns if col in benchmark_values
        })
        
        # Prepare data for display
        comparison_data = pd.DataFrame({
            "variable": selected_columns,
            "local_mean": local_means.values,
            "benchmark": [benchmark_values.get(col, float('nan')) for col in selected_columns],
            "gap": [gaps.get(col, float('nan')) for col in selected_columns],
            "percentage": [percentage_achieved.get(col, float('nan')) for col in selected_columns]
        })
        
        # Add translated column names for display
        comparison_data["variable_name"] = comparison_data["variable"].apply(
            lambda x: get_text("columns_of_interest", {}).get(x, x)
        )
        
        # Remove rows with missing benchmarks
        comparison_data = comparison_data.dropna()
        
        # Order by gap (worst performing first)
        comparison_data = comparison_data.sort_values("gap", ascending=True)
        
        # Create benchmark comparison visualization
        benchmark_fig = self.viz.show_international_benchmark_comparison(
            local_means.to_dict(),
            benchmark_values
        )
        
        # Save figure for inclusion in report
        benchmark_img_path = self.viz.save_figure_for_word(benchmark_fig, "benchmark_comparison.png")
        
        # Create percentage chart data
        percentage_df = comparison_data.copy()
        percentage_df["achievement_level"] = percentage_df["percentage"].apply(
            lambda x: get_text("critical", "Critical") if x < 70 else (
                get_text("concerning", "Concerning") if x < 85 else (
                    get_text("approaching", "Approaching") if x < 100 else get_text("meeting", "Meeting")
                )
            )
        )
        
        # Create percentage chart
        percentage_fig = self.viz.show_benchmark_percentage(percentage_df)
        
        # Save figure for inclusion in report
        percentage_img_path = self.viz.save_figure_for_word(percentage_fig, "benchmark_percentage.png")
        
        # Categorize variables by achievement level
        critical_vars = percentage_df[percentage_df["percentage"] < 70]
        concerning_vars = percentage_df[(percentage_df["percentage"] >= 70) & (percentage_df["percentage"] < 85)]
        approaching_vars = percentage_df[(percentage_df["percentage"] >= 85) & (percentage_df["percentage"] < 100)]
        meeting_vars = percentage_df[percentage_df["percentage"] >= 100]
        
        # Add executive summary
        if not critical_vars.empty:
            summary_status = get_text("critical_status_summary", 
                                    "The analysis reveals critical gaps between local performance and international benchmarks in some areas.")
        elif not concerning_vars.empty:
            summary_status = get_text("concerning_status_summary", 
                                    "The analysis shows concerning gaps between local performance and international benchmarks in some areas.")
        elif not approaching_vars.empty:
            summary_status = get_text("approaching_status_summary", 
                                    "The analysis indicates that local performance is approaching international benchmarks in most areas.")
        else:
            summary_status = get_text("meeting_status_summary", 
                                    "The analysis shows that local performance meets or exceeds international benchmarks in all assessed areas.")
        
        summary_text = get_text("international_summary", 
                              "This report compares local performance against international benchmarks to identify improvement areas. ") + summary_status
        self.word_gen.add_executive_summary(summary_text)
        
        # Add methodology section
        methodology_text = get_text("international_methodology", 
                                 "This analysis compares local assessment results against international benchmarks. " +
                                 "It identifies areas where performance meets, exceeds, or falls below international standards, " +
                                 "and provides recommendations for improving performance in critical areas.")
        self.word_gen.add_methodology(methodology_text)
        
        # Add results section
        self.word_gen.add_section(get_text("results", "Results"), level=1)
        
        # Add comparison table
        display_df = comparison_data[["variable_name", "local_mean", "benchmark", "gap", "percentage"]]
        display_df.columns = [
            get_text("variable", "Variable"),
            get_text("local_mean", "Local Mean"),
            get_text("benchmark", "Benchmark"),
            get_text("gap", "Gap"),
            get_text("percentage", "% of Benchmark")
        ]
        
        self.word_gen.add_table(
            display_df, 
            title=get_text("international_comparison_table", "Comparison with International Benchmarks")
        )
        
        # Add benchmark comparison visualization
        self.word_gen.add_picture(
            benchmark_img_path,
            title=get_text("comparison_chart_title", "Local Performance vs. International Benchmarks"),
            width=6
        )
        
        # Add percentage achievement visualization
        self.word_gen.add_picture(
            percentage_img_path,
            title=get_text("percentage_chart_title", "Percentage of International Benchmark Achieved"),
            width=6
        )
        
        # Add performance categories section
        self.word_gen.add_section(get_text("performance_categories", "Performance Categories"), level=2)
        
        # Critical areas section
        if not critical_vars.empty:
            self.word_gen.add_section(get_text("critical_areas", "Critical Areas (<70% of benchmark)"), level=3)
            for _, row in critical_vars.iterrows():
                self.word_gen.add_bullet_point(
                    f"{row['variable_name']}: {row['percentage']}% {get_text('of_benchmark', 'of benchmark')} "
                    f"({abs(row['gap']):.2f} {get_text('points_below', 'points below')})"
                )
        
        # Concerning areas section
        if not concerning_vars.empty:
            self.word_gen.add_section(get_text("concerning_areas", "Concerning Areas (70-84% of benchmark)"), level=3)
            for _, row in concerning_vars.iterrows():
                self.word_gen.add_bullet_point(
                    f"{row['variable_name']}: {row['percentage']}% {get_text('of_benchmark', 'of benchmark')} "
                    f"({abs(row['gap']):.2f} {get_text('points_below', 'points below')})"
                )
        
        # Approaching benchmark section
        if not approaching_vars.empty:
            self.word_gen.add_section(get_text("approaching_areas", "Approaching Benchmark (85-99% of benchmark)"), level=3)
            for _, row in approaching_vars.iterrows():
                self.word_gen.add_bullet_point(
                    f"{row['variable_name']}: {row['percentage']}% {get_text('of_benchmark', 'of benchmark')} "
                    f"({abs(row['gap']):.2f} {get_text('points_below', 'points below')})"
                )
        
        # Meeting benchmark section
        if not meeting_vars.empty:
            self.word_gen.add_section(get_text("meeting_areas", "Meeting or Exceeding Benchmark (≥100% of benchmark)"), level=3)
            for _, row in meeting_vars.iterrows():
                text = (f"{row['variable_name']}: {row['percentage']}% {get_text('of_benchmark', 'of benchmark')} "
                       f"({row['gap']:.2f} {get_text('points_above', 'points above')})" if row['gap'] > 0
                       else f"{row['variable_name']}: {row['percentage']}% {get_text('of_benchmark', 'of benchmark')} "
                       f"({get_text('at_benchmark', 'at benchmark')})")
                self.word_gen.add_bullet_point(text)
        
        # Calculate overall stats for reading and math domains
        reading_vars = [var for var in selected_columns if var in ["clpm", "phoneme", "sound_word", "cwpm", "listening", "orf", "comprehension"]]
        math_vars = [var for var in selected_columns if var in ["number_id", "discrimin", "missing_number", "addition", "subtraction", "problems"]]
        
        reading_percentage = percentage_df[percentage_df["variable"].isin(reading_vars)]["percentage"].mean() if reading_vars else None
        math_percentage = percentage_df[percentage_df["variable"].isin(math_vars)]["percentage"].mean() if math_vars else None
        overall_percentage = percentage_df["percentage"].mean()
        
        # Add interpretation section
        self.word_gen.add_section(get_text("interpretation", "Interpretation"), level=1)
        
        # Overall performance summary
        self.word_gen.add_paragraph(f"{get_text('average_achievement', 'Average achievement across all skills')}: "
                             f"**{overall_percentage:.1f}%** {get_text('of_benchmark', 'of benchmark')}")
        
        if reading_percentage is not None:
            self.word_gen.add_paragraph(f"{get_text('reading_average', 'Reading skills average')}: "
                                 f"**{reading_percentage:.1f}%** {get_text('of_benchmark', 'of benchmark')}")
        
        if math_percentage is not None:
            self.word_gen.add_paragraph(f"{get_text('math_average', 'Math skills average')}: "
                                 f"**{math_percentage:.1f}%** {get_text('of_benchmark', 'of benchmark')}")
        
        # Domain-specific interpretations
        if reading_vars and math_vars:
            if reading_percentage > math_percentage:
                self.word_gen.add_paragraph(get_text("reading_stronger", 
                                                   "Reading skills are stronger than math skills relative to international benchmarks."))
            elif math_percentage > reading_percentage:
                self.word_gen.add_paragraph(get_text("math_stronger", 
                                                   "Math skills are stronger than reading skills relative to international benchmarks."))
            else:
                self.word_gen.add_paragraph(get_text("balanced_performance", 
                                                   "Reading and math skills show similar levels of performance relative to international benchmarks."))
        
        # Add recommendations section
        self.word_gen.add_section(get_text("recommendations", "Recommendations"), level=1)
        
        # Critical areas recommendations
        if not critical_vars.empty:
            self.word_gen.add_section(get_text("critical_recommendations", "For Critical Areas:"), level=2)
            self.word_gen.add_bullet_point(get_text("critical_rec1", 
                                               "Implement intensive intervention programs to address critical performance gaps."))
            self.word_gen.add_bullet_point(get_text("critical_rec2", 
                                               "Provide specialized teacher training in critical skill areas."))
            self.word_gen.add_bullet_point(get_text("critical_rec3", 
                                               "Allocate additional instructional time for these foundational skills."))
            self.word_gen.add_bullet_point(get_text("critical_rec4", 
                                               "Conduct frequent progress monitoring to track improvement."))
        
        # Concerning areas recommendations
        if not concerning_vars.empty:
            self.word_gen.add_section(get_text("concerning_recommendations", "For Concerning Areas:"), level=2)
            self.word_gen.add_bullet_point(get_text("concerning_rec1", 
                                                 "Strengthen instructional approaches and provide targeted support."))
            self.word_gen.add_bullet_point(get_text("concerning_rec2", 
                                                 "Review and enhance instructional materials and methods."))
            self.word_gen.add_bullet_point(get_text("concerning_rec3", 
                                                 "Provide regular formative assessments to track progress."))
        
        # Approaching areas recommendations
        if not approaching_vars.empty:
            self.word_gen.add_section(get_text("approaching_recommendations", "For Areas Approaching Benchmark:"), level=2)
            self.word_gen.add_bullet_point(get_text("approaching_rec1", 
                                                 "Continue current strategies with minor adjustments to reach standards."))
            self.word_gen.add_bullet_point(get_text("approaching_rec2", 
                                                 "Target specific areas for improvement to close the remaining gap."))
        
        # Meeting areas recommendations
        if not meeting_vars.empty:
            self.word_gen.add_section(get_text("meeting_recommendations", "For Areas Meeting Benchmark:"), level=2)
            self.word_gen.add_bullet_point(get_text("meeting_rec1", 
                                                 "Maintain successful practices and consider setting higher goals."))
            self.word_gen.add_bullet_point(get_text("meeting_rec2", 
                                                 "Share effective practices with colleagues who teach other skill areas."))
        
        # Systemic recommendations
        self.word_gen.add_section(get_text("systemic_recommendations", "Systemic Recommendations:"), level=2)
        self.word_gen.add_bullet_point(get_text("systemic_rec1", 
                                           "Ensure curriculum alignment with international standards."))
        self.word_gen.add_bullet_point(get_text("systemic_rec2", 
                                           "Invest in ongoing professional development for teachers."))
        self.word_gen.add_bullet_point(get_text("systemic_rec3", 
                                           "Allocate resources based on identified performance gaps."))
        self.word_gen.add_bullet_point(get_text("systemic_rec4", 
                                           "Engage parents and communities in supporting student learning."))
        
        # About international benchmarks
        self.word_gen.add_section(get_text("about_benchmarks", "About International Benchmarks"), level=1)
        self.word_gen.add_paragraph(get_text("benchmark_info", """
        The international benchmarks used in this analysis are based on research and standards from multiple sources including RTI International, USAID, World Bank, and UNESCO. These benchmarks represent achievement levels that have been associated with successful educational outcomes in various international contexts.
        
        These benchmarks should be interpreted as goals to work toward rather than absolute standards, as educational contexts can vary significantly across countries and regions. They provide valuable reference points for understanding local performance in a global context.
        """))
        
        # Set up headers and footers
        self.word_gen.setup_headers_and_footers(title=title)
        
        # Save document and return
        doc, docx_bytes = self._save_and_get_bytes(doc, temp_dir, filename)
        
        return doc, docx_bytes, filename