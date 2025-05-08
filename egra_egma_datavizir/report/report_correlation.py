# report_correlation.py
# Correlation report generator for analyse5.py

import os
import pandas as pd
from language_utils import get_text
from report.report_base import BaseReportGenerator

class CorrelationReportGenerator(BaseReportGenerator):
    """
    Report generator for correlation analysis (analyse5.py).
    """
    
    def create_report(self, df, selected_columns, title=None, temp_dir=None):
        """
        Create a correlation analysis report.
        
        Args:
            df: DataFrame with data
            selected_columns: List of columns to include
            title: Report title
            temp_dir: Directory for temporary files
            
        Returns:
            tuple: (doc, docx_bytes, filename)
        """
        # Common setup
        title, doc = self._common_setup(title, "title_correlation")
        filename = "correlation_report.docx"
        
        # Calculate correlation matrix
        corr_matrix = df[selected_columns].corr().round(2)
        
        # Create visualization
        fig, _ = self.viz.show_correlation_matrix(df, selected_columns)
        
        # Save figure for inclusion in report
        img_path = self.viz.save_figure_for_word(fig, "correlation_matrix.png")
        
        # Find significant correlations (above 0.5 or below -0.5)
        strong_correlations = []
        for i in range(len(corr_matrix)):
            for j in range(i + 1, len(corr_matrix)):  # Upper triangle only to avoid duplicates
                correlation = corr_matrix.iloc[i, j]
                if abs(correlation) >= 0.5:  # Threshold for significant correlation
                    strong_correlations.append({
                        "task1": corr_matrix.index[i],
                        "task2": corr_matrix.columns[j],
                        "correlation": correlation,
                        "abs_correlation": abs(correlation)
                    })
        
        # Convert to DataFrame and sort by absolute correlation (strongest first)
        if strong_correlations:
            df_strong = pd.DataFrame(strong_correlations)
            df_strong = df_strong.sort_values("abs_correlation", ascending=False).drop("abs_correlation", axis=1)
            
            # Translate column names for display
            df_display = df_strong.copy()
            df_display["task1"] = df_display["task1"].map(lambda x: get_text("columns_of_interest", {}).get(x, x))
            df_display["task2"] = df_display["task2"].map(lambda x: get_text("columns_of_interest", {}).get(x, x))
            
            # Format column names for display
            df_display.columns = [
                get_text("task_1", "Task 1"),
                get_text("task_2", "Task 2"),
                get_text("correlation", "Correlation")
            ]
        else:
            df_strong = pd.DataFrame()
            df_display = pd.DataFrame()
        
        # Add executive summary
        summary_text = get_text("correlation_summary", 
                              "This report analyzes the relationships between different assessment tasks to identify patterns and connections.")
        self.word_gen.add_executive_summary(summary_text)
        
        # Add methodology section
        methodology_text = get_text("correlation_methodology", 
                                 "This analysis calculates correlation coefficients between assessment variables. " +
                                 "Correlations range from -1 to 1, with values closer to ±1 indicating stronger relationships " +
                                 "and values closer to 0 indicating weaker relationships.")
        self.word_gen.add_methodology(methodology_text)
        
        # Add interpretation guide
        self.word_gen.add_paragraph(get_text("correlation_interpretation", "Interpretation Guide:"))
        self.word_gen.add_bullet_point(get_text("correlation_point1", "A correlation close to 1 indicates a strong positive relationship"))
        self.word_gen.add_bullet_point(get_text("correlation_point2", "A correlation close to -1 indicates a strong negative relationship"))
        self.word_gen.add_bullet_point(get_text("correlation_point3", "A correlation close to 0 indicates a weak or no relationship"))
        self.word_gen.add_bullet_point(get_text("correlation_point4", "Correlations > 0.5 or < -0.5 are considered significant"))
        
        # Add results section
        self.word_gen.add_section(get_text("results", "Results"), level=1)
        
        # Add correlation matrix visualization
        self.word_gen.add_picture(
            img_path,
            title=get_text("correlation_matrix", "Correlation Matrix"),
            width=6
        )
        
        # Add significant correlations if any
        if not df_display.empty:
            self.word_gen.add_section(get_text("strong_correlations", "Significant Correlations (>|0.5|)"), level=2)
            
            # Add significant correlations table
            self.word_gen.add_table(
                df_display, 
                title=get_text("significant_correlations", "Significant Correlations")
            )
            
            # Add interpretation section
            self.word_gen.add_section(get_text("interpretation", "Interpretation"), level=1)
            
            # Group correlations by type
            reading_correlations = []
            math_correlations = []
            cross_domain_correlations = []
            
            for _, row in df_strong.iterrows():
                task1_domain = self._get_domain(row["task1"])
                task2_domain = self._get_domain(row["task2"])
                
                if task1_domain == "reading" and task2_domain == "reading":
                    reading_correlations.append(row)
                elif task1_domain == "math" and task2_domain == "math":
                    math_correlations.append(row)
                else:
                    cross_domain_correlations.append(row)
            
            # Interpret cross-domain correlations (most interesting)
            if cross_domain_correlations:
                self.word_gen.add_section(get_text("cross_domain_correlations", "Reading-Math Connections"), level=2)
                
                for row in cross_domain_correlations:
                    task1_name = get_text("columns_of_interest", {}).get(row["task1"], row["task1"])
                    task2_name = get_text("columns_of_interest", {}).get(row["task2"], row["task2"])
                    corr_value = row["correlation"]
                    
                    # Create interpretation based on specific task pairs
                    interp_text = self._get_cross_domain_interpretation(row["task1"], row["task2"], corr_value)
                    
                    # Add to document
                    para = self.word_gen.add_paragraph()
                    para.add_run(f"{task1_name} & {task2_name} ({corr_value:.2f})").bold = True
                    self.word_gen.add_bullet_point(interp_text)
            
            # Interpret reading correlations
            if reading_correlations:
                self.word_gen.add_section(get_text("reading_correlations", "Within Reading Skills"), level=2)
                
                for row in reading_correlations:
                    task1_name = get_text("columns_of_interest", {}).get(row["task1"], row["task1"])
                    task2_name = get_text("columns_of_interest", {}).get(row["task2"], row["task2"])
                    corr_value = row["correlation"]
                    
                    # Create interpretation
                    interp_text = self._get_reading_interpretation(row["task1"], row["task2"], corr_value)
                    
                    # Add to document
                    para = self.word_gen.add_paragraph()
                    para.add_run(f"{task1_name} & {task2_name} ({corr_value:.2f})").bold = True
                    self.word_gen.add_bullet_point(interp_text)
            
            # Interpret math correlations
            if math_correlations:
                self.word_gen.add_section(get_text("math_correlations", "Within Math Skills"), level=2)
                
                for row in math_correlations:
                    task1_name = get_text("columns_of_interest", {}).get(row["task1"], row["task1"])
                    task2_name = get_text("columns_of_interest", {}).get(row["task2"], row["task2"])
                    corr_value = row["correlation"]
                    
                    # Create interpretation
                    interp_text = self._get_math_interpretation(row["task1"], row["task2"], corr_value)
                    
                    # Add to document
                    para = self.word_gen.add_paragraph()
                    para.add_run(f"{task1_name} & {task2_name} ({corr_value:.2f})").bold = True
                    self.word_gen.add_bullet_point(interp_text)
            
            # Add recommendations section
            self.word_gen.add_section(get_text("recommendations", "Recommendations"), level=1)
            
            # Add recommendations based on correlation patterns
            if cross_domain_correlations:
                self.word_gen.add_section(get_text("integrated_instruction", "Integrated Instruction"), level=2)
                self.word_gen.add_bullet_point(get_text("integrated_instruction_text", 
                                                  "Consider integrated lessons that combine reading and math skills that show strong correlations"))
                self.word_gen.add_bullet_point(get_text("integrated_instruction_example", 
                                                  "For example, use story problems that incorporate both mathematical thinking and reading comprehension"))
            
            if reading_correlations:
                self.word_gen.add_section(get_text("reading_instruction", "Reading Instruction"), level=2)
                self.word_gen.add_bullet_point(get_text("reading_progression", 
                                                  "Build instruction that follows developmental progression of correlated skills"))
                self.word_gen.add_bullet_point(get_text("reading_practice", 
                                                  "Provide integrated practice activities that target multiple related skills"))
            
            if math_correlations:
                self.word_gen.add_section(get_text("math_instruction", "Math Instruction"), level=2)
                self.word_gen.add_bullet_point(get_text("math_progression", 
                                                  "Ensure that foundational skills that correlate with advanced skills are well established"))
                self.word_gen.add_bullet_point(get_text("math_practice", 
                                                  "Create practice opportunities that develop connected mathematical understandings"))
                
        else:
            # No significant correlations found
            self.word_gen.add_section(get_text("no_significant_correlations", "No Significant Correlations"), level=2)
            self.word_gen.add_paragraph(get_text("no_strong_correlation", 
                                           "No significant correlations (>|0.5|) were found."))
            self.word_gen.add_paragraph(get_text("weak_correlation_note", 
                                           "This suggests that the measured skills may be developing independently or that the assessment measures distinct constructs."))
        
        # Set up headers and footers
        self.word_gen.setup_headers_and_footers(title=title)
        
        # Save document and return
        doc, docx_bytes = self._save_and_get_bytes(doc, temp_dir, filename)
        
        return doc, docx_bytes, filename
    
    def _get_domain(self, task):
        """
        Determine whether a task is in the reading or math domain.
        
        Args:
            task: Task code
            
        Returns:
            str: "reading" or "math"
        """
        reading_tasks = ["clpm", "phoneme", "sound_word", "cwpm", "listening", "orf", "comprehension"]
        math_tasks = ["number_id", "discrimin", "missing_number", "addition", "subtraction", "problems"]
        
        if task in reading_tasks:
            return "reading"
        elif task in math_tasks:
            return "math"
        else:
            return "unknown"
    
    def _get_cross_domain_interpretation(self, task1, task2, correlation):
        """
        Generate interpretation for cross-domain correlations.
        
        Args:
            task1: First task code
            task2: Second task code
            correlation: Correlation value
            
        Returns:
            str: Interpretation text
        """
        # Ensure task1 is reading and task2 is math
        if self._get_domain(task1) == "math":
            task1, task2 = task2, task1
        
        # Determine correlation direction
        direction = "positive" if correlation > 0 else "negative"
        
        # Define interpretations for specific task pairs
        interpretations = {
            "clpm_number_id": {
                "positive": get_text("clpm_number_id_pos", 
                                  "Symbol recognition is a common cognitive skill underlying both letter and number identification."),
                "negative": get_text("clpm_number_id_neg", 
                                  "Students may be showing a preference or strength in one symbol system over the other.")
            },
            "comprehension_problems": {
                "positive": get_text("comprehension_problems_pos", 
                                  "Reading comprehension and math problem solving both require similar analytical thinking skills."),
                "negative": get_text("comprehension_problems_neg", 
                                  "Students may be developing different approaches to comprehension in different domains.")
            }
        }
        
        # Look for matching task pair
        task_pair = f"{task1}_{task2}"
        if task_pair in interpretations:
            return interpretations[task_pair][direction]
        
        # Default interpretations
        if direction == "positive":
            return get_text("cross_domain_positive", 
                         "This positive correlation suggests that these reading and math skills share underlying cognitive processes or instructional influences.")
        else:
            return get_text("cross_domain_negative", 
                         "This negative correlation might indicate competing cognitive resources or different developmental trajectories for these skills.")
    
    def _get_reading_interpretation(self, task1, task2, correlation):
        """
        Generate interpretation for reading skill correlations.
        
        Args:
            task1: First task code
            task2: Second task code
            correlation: Correlation value
            
        Returns:
            str: Interpretation text
        """
        # Determine correlation direction
        direction = "positive" if correlation > 0 else "negative"
        
        # Define reading skill interpretations for specific task pairs
        skill_pairs = {
            "clpm_phoneme": get_text("clpm_phoneme", 
                                  "Letter recognition and phonemic awareness are foundational alphabetic skills that typically develop together."),
            "phoneme_sound_word": get_text("phoneme_sound_word", 
                                       "Phonemic awareness is essential for decoding and sounding out words."),
            "cwpm_comprehension": get_text("cwpm_comprehension", 
                                       "Reading fluency supports comprehension by freeing cognitive resources for understanding.")
        }
        
        # Sort task names to match skill pairs dictionary format
        sorted_pair = "_".join(sorted([task1, task2]))
        
        # Look for matching task pair
        if sorted_pair in skill_pairs and direction == "positive":
            return skill_pairs[sorted_pair]
        
        # Unexpected negative correlation
        if direction == "negative":
            return get_text("reading_unexpected_negative", 
                         "This negative correlation is unexpected and may indicate measurement issues or competing instructional focus.")
        
        # Default positive correlation interpretation
        return get_text("general_reading", 
                     "These reading skills show a relationship that suggests shared cognitive or instructional factors.")
    
    def _get_math_interpretation(self, task1, task2, correlation):
        """
        Generate interpretation for math skill correlations.
        
        Args:
            task1: First task code
            task2: Second task code
            correlation: Correlation value
            
        Returns:
            str: Interpretation text
        """
        # Determine correlation direction
        direction = "positive" if correlation > 0 else "negative"
        
        # Define math skill interpretations for specific task pairs
        skill_pairs = {
            "addition_subtraction": get_text("addition_subtraction", 
                                         "Addition and subtraction are related operations that often develop together."),
            "number_id_discrimin": get_text("number_id_discrimin", 
                                        "Number identification and magnitude comparison both involve number sense."),
            "addition_problems": get_text("addition_problems", 
                                      "Addition skills contribute to problem-solving ability.")
        }
        
        # Sort task names to match skill pairs dictionary format
        sorted_pair = "_".join(sorted([task1, task2]))
        
        # Look for matching task pair
        if sorted_pair in skill_pairs and direction == "positive":
            return skill_pairs[sorted_pair]
        
        # Unexpected negative correlation
        if direction == "negative":
            return get_text("math_unexpected_negative", 
                         "This negative correlation is unexpected and may indicate measurement issues or competing instructional focus.")
        
        # Default positive correlation interpretation
        return get_text("general_math", 
                     "These math skills show a relationship that suggests shared cognitive or instructional factors.")