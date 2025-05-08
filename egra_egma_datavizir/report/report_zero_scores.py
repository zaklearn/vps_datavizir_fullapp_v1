# report_zero_scores.py
# Zero scores report generator for analyse2.py

import os
import pandas as pd
from language_utils import get_text
from report.report_base import BaseReportGenerator

class ZeroScoresReportGenerator(BaseReportGenerator):
    """
    Report generator for zero scores analysis (analyse2.py).
    """
    
    def create_report(self, df, selected_columns, title=None, temp_dir=None):
        """
        Create a zero scores analysis report.
        
        Args:
            df: DataFrame with data
            selected_columns: List of columns to include
            title: Report title
            temp_dir: Directory for temporary files
            
        Returns:
            tuple: (doc, docx_bytes, filename)
        """
        # Common setup
        title, doc = self._common_setup(title, "title_zero_scores")
        filename = "zero_scores_report.docx"
        
        # Calculate zero scores
        zero_scores = (df[selected_columns] == 0).sum()
        total_students = len(df)
        percentage_zero = ((zero_scores / total_students) * 100).round(2)
        
        # Create DataFrame for display and visualization
        df_zero_scores = pd.DataFrame({
            "Task": [get_text("columns_of_interest", {}).get(col, col) for col in selected_columns],
            "Task_Code": selected_columns,
            "Zero_Count": zero_scores.values,
            "Percentage": percentage_zero.values
        })
        
        # Sort by percentage for visualization
        df_zero_scores_sorted = df_zero_scores.sort_values("Percentage", ascending=True)
        
        # Create visualization
        fig = self.viz.show_zero_scores_chart(
            df_zero_scores,
            df_zero_scores["Task"].tolist(),
            df_zero_scores["Percentage"].tolist()
        )
        
        # Save figure for inclusion in report
        img_path = self.viz.save_figure_for_word(fig, "zero_scores_chart.png")
        
        # Add executive summary
        summary_text = get_text("zero_scores_summary", 
                              "This report analyzes the percentage of students scoring zero on each assessment task.")
        self.word_gen.add_executive_summary(summary_text)
        
        # Add methodology section
        methodology_text = get_text("zero_scores_methodology", 
                                 "This analysis focuses on the percentage of students who scored zero on each assessment task. " +
                                 "Zero scores often indicate a lack of basic skills or understanding in a particular area, " +
                                 "and can help identify critical intervention needs.")
        self.word_gen.add_methodology(methodology_text)
        
        # Add results section
        self.word_gen.add_section(get_text("results", "Results"), level=1)
        
        # Add zero scores table
        self.word_gen.add_table(
            df_zero_scores[["Task", "Zero_Count", "Percentage"]], 
            title=get_text("zero_scores_table", "Proportion of Students with Zero Scores")
        )
        
        # Add visualization
        self.word_gen.add_picture(
            img_path,
            title=get_text("zero_scores_chart_title", "Percentage of Students with Zero Scores by Task"),
            width=6
        )
        
        # Add interpretation section based on thresholds
        self.word_gen.add_section(get_text("interpretation", "Interpretation"), level=1)
        
        # Categorize tasks based on percentage thresholds
        critical_tasks = df_zero_scores[df_zero_scores["Percentage"] >= 30]
        concerning_tasks = df_zero_scores[(df_zero_scores["Percentage"] < 30) & (df_zero_scores["Percentage"] >= 20)]
        watchlist_tasks = df_zero_scores[(df_zero_scores["Percentage"] < 20) & (df_zero_scores["Percentage"] >= 10)]
        acceptable_tasks = df_zero_scores[df_zero_scores["Percentage"] < 10]
        
        # Determine overall status based on categories
        if not critical_tasks.empty:
            status_text = get_text("critical_status", "Critical areas requiring immediate intervention")
        elif not concerning_tasks.empty:
            status_text = get_text("concerning_status", "Areas of concern requiring attention")
        elif not watchlist_tasks.empty:
            status_text = get_text("watch_status", "Some skills need monitoring")
        else:
            status_text = get_text("acceptable_status", "All skills are at acceptable levels")
        
        # Add overall status
        self.word_gen.add_paragraph(status_text, style='Intense Quote')
        
        # Add critical tasks section
        if not critical_tasks.empty:
            self.word_gen.add_section(get_text("critical_areas", "Critical Areas (≥30% zero scores)"), level=2)
            for _, row in critical_tasks.iterrows():
                self.word_gen.add_bullet_point(f"{row['Task']}: {row['Percentage']}% {get_text('zero_score_text', 'of students scored zero')}")
        
        # Add concerning tasks section
        if not concerning_tasks.empty:
            self.word_gen.add_section(get_text("concerning_areas", "Concerning Areas (20-29% zero scores)"), level=2)
            for _, row in concerning_tasks.iterrows():
                self.word_gen.add_bullet_point(f"{row['Task']}: {row['Percentage']}% {get_text('zero_score_text', 'of students scored zero')}")
        
        # Add watchlist tasks section
        if not watchlist_tasks.empty:
            self.word_gen.add_section(get_text("watch_areas", "Areas to Watch (10-19% zero scores)"), level=2)
            for _, row in watchlist_tasks.iterrows():
                self.word_gen.add_bullet_point(f"{row['Task']}: {row['Percentage']}% {get_text('zero_score_text', 'of students scored zero')}")
        
        # Add recommendations section
        self.word_gen.add_section(get_text("recommendations", "Recommendations"), level=1)
        
        # Add specific recommendations based on critical and concerning areas
        if not critical_tasks.empty:
            self.word_gen.add_section(get_text("critical_recommendations", "For Critical Areas:"), level=2)
            for _, row in critical_tasks.iterrows():
                task_code = row["Task_Code"]
                task_name = row["Task"]
                
                # Get skill-specific recommendations if available
                rec_text = self._get_skill_recommendation(task_code, "critical")
                
                para = self.word_gen.add_paragraph()
                para.add_run(f"{task_name}:").bold = True
                self.word_gen.add_paragraph(rec_text)
        
        if not concerning_tasks.empty:
            self.word_gen.add_section(get_text("concerning_recommendations", "For Concerning Areas:"), level=2)
            for _, row in concerning_tasks.iterrows():
                task_code = row["Task_Code"]
                task_name = row["Task"]
                
                # Get skill-specific recommendations if available
                rec_text = self._get_skill_recommendation(task_code, "concerning")
                
                para = self.word_gen.add_paragraph()
                para.add_run(f"{task_name}:").bold = True
                self.word_gen.add_paragraph(rec_text)
        
        # Add general monitoring recommendations
        self.word_gen.add_section(get_text("monitoring_recommendations", "General Monitoring:"), level=2)
        self.word_gen.add_bullet_point(get_text("general_rec1", "Conduct regular progress monitoring assessments."))
        self.word_gen.add_bullet_point(get_text("general_rec2", "Use formative assessments to adjust instruction."))
        self.word_gen.add_bullet_point(get_text("general_rec3", "Re-assess all skills after 8-10 weeks of intervention."))
        
        # Set up headers and footers
        self.word_gen.setup_headers_and_footers(title=title)
        
        # Save document and return
        doc, docx_bytes = self._save_and_get_bytes(doc, temp_dir, filename)
        
        return doc, docx_bytes, filename
    
    def _get_skill_recommendation(self, task_code, level):
        """
        Get a skill-specific recommendation based on task code and severity level.
        
        Args:
            task_code: Task code (e.g., "clpm", "phoneme")
            level: Severity level ("critical", "concerning", "watch")
            
        Returns:
            str: Recommendation text
        """
        # Default recommendations if specific ones aren't available
        default_critical = get_text("default_critical_rec", 
                                 "Implement intensive intervention focusing on this fundamental skill.")
        default_concerning = get_text("default_concerning_rec", 
                                   "Strengthen instruction and provide additional practice opportunities.")
        default_watch = get_text("default_watch_rec", 
                              "Monitor progress while maintaining regular instruction.")
        
        # Skill-specific recommendations
        recommendations = {
            "clpm": {
                "critical": get_text("clpm_critical", "Implement daily letter recognition activities; Use flashcards and letter games; Provide intensive small-group interventions focusing on alphabet knowledge."),
                "concerning": get_text("clpm_concerning", "Increase letter recognition practice; Include more alphabet activities in regular instruction."),
                "watch": get_text("clpm_monitor", "Continue regular letter recognition activities while monitoring progress.")
            },
            "phoneme": {
                "critical": get_text("phoneme_critical", "Implement intensive phonemic awareness training; Use sound isolation, blending, and segmentation exercises daily; Provide structured small-group interventions."),
                "concerning": get_text("phoneme_concerning", "Strengthen phonemic awareness instruction; Increase sound manipulation activities in regular classroom work."),
                "watch": get_text("phoneme_monitor", "Maintain regular phonemic awareness activities and monitor student progress.")
            },
            "comprehension": {
                "critical": get_text("comprehension_critical", "Implement explicit reading comprehension strategy instruction; Use scaffolded reading experiences; Provide small-group interventions focusing on comprehension strategies."),
                "concerning": get_text("comprehension_concerning", "Strengthen comprehension strategy instruction; Increase guided reading with comprehension focus."),
                "watch": get_text("comprehension_monitor", "Continue comprehension strategy instruction while monitoring progress.")
            }
            # Add more skill recommendations as needed
        }
        
        # Return skill-specific recommendation if available, otherwise default
        if task_code in recommendations and level in recommendations[task_code]:
            return recommendations[task_code][level]
        elif level == "critical":
            return default_critical
        elif level == "concerning":
            return default_concerning
        else:
            return default_watch