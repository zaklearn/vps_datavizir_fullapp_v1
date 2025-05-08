# viz_wrapper.py
# Standardized wrapper around viz_utils.py for consistent visualization across
# existing analysis modules

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
import tempfile
import os
from language_utils import get_text, get_current_language
from viz_utils import VisualizationUtilities

class StandardVisualization:
    """
    Standardized visualization wrapper for analysis modules.
    This class provides visualization methods specifically for the
    existing analysis modules in the repository.
    """
    
    def __init__(self):
        """Initialize the visualization utilities."""
        self.language = get_current_language()
        self.viz_utils = VisualizationUtilities(language=self.language)
        self.temp_dir = None
    
    def update_language(self, language=None):
        """Update the language setting."""
        if language is None:
            language = get_current_language()
        self.language = language
        self.viz_utils = VisualizationUtilities(language=language)
    
    def cleanup(self):
        """Clean up temporary files."""
        if self.temp_dir:
            import shutil
            try:
                shutil.rmtree(self.temp_dir)
                self.temp_dir = None
            except:
                pass
    
    # analyse1.py: Statistical Overview visualizations
    
    def show_histogram_with_stats(self, df, column, title=None, description=None):
        """
        Display a histogram with summary statistics for a column.
        For analyse1.py (Statistical Overview).
        
        Args:
            df (pd.DataFrame): DataFrame containing the data
            column (str): Column name to visualize
            title (str, optional): Custom title
            description (str, optional): Additional description text
        """
        if column not in df.columns:
            st.error(f"Column '{column}' not found in data")
            return None
            
        col1, col2 = st.columns(2)
        
        with col1:
            # Show statistics
            st.write(f"**{get_text('columns_of_interest', {}).get(column, column)}**")
            stats = df[column].describe(percentiles=[.25, .5, .75, .9]).round(2)
            st.dataframe(stats)
        
        with col2:
            try:
                # Create and display histogram
                fig = self.viz_utils.create_histogram(
                    df[column],
                    title=title or get_text("histogram_title", "Distribution of {}").format(
                        get_text("columns_of_interest", {}).get(column, column)
                    ),
                    show_normal=True
                )
                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Error creating histogram for {column}: {str(e)}")
                fig = None
        
        # Show description if provided
        if description:
            st.markdown(description)
            
        return fig
    
    # analyse2.py: Zero Scores Analysis visualizations
    
    def show_zero_scores_chart(self, df_zero_scores, task_names=None, percentages=None):
        """
        Display a horizontal bar chart for zero scores analysis.
        For analyse2.py (Zero Scores Analysis).
        
        Args:
            df_zero_scores (pd.DataFrame): DataFrame with zero scores data
            task_names (list, optional): List of task display names (if not in df_zero_scores)
            percentages (list, optional): List of percentage values (if not in df_zero_scores)
        """
        try:
            # Create DataFrame for visualization if not provided
            if isinstance(df_zero_scores, pd.DataFrame):
                if 'Task' in df_zero_scores.columns and 'Percentage' in df_zero_scores.columns:
                    df_viz = df_zero_scores.copy()
                elif task_names and percentages and len(task_names) == len(percentages):
                    df_viz = pd.DataFrame({
                        "Task": task_names,
                        "Percentage": percentages
                    })
                else:
                    st.error("Invalid input for zero scores chart. Provide either a DataFrame with Task and Percentage columns, or both task_names and percentages lists")
                    return None
            elif task_names and percentages and len(task_names) == len(percentages):
                df_viz = pd.DataFrame({
                    "Task": task_names,
                    "Percentage": percentages
                })
            else:
                st.error("Invalid input for zero scores chart")
                return None
            
            # Sort by percentage for better visualization
            df_viz = df_viz.sort_values("Percentage", ascending=True)
            
            # Create horizontal bar chart
            fig = px.bar(
                df_viz,
                x="Percentage",
                y="Task",
                orientation="h",
                text="Percentage",
                color="Percentage",
                color_continuous_scale="Viridis",
                title=get_text("zero_scores_chart_title", "Percentage of Students with Zero Scores by Task")
            )
            
            # Add threshold lines
            fig.add_vline(x=10, line_width=1, line_dash="dash", line_color="yellow")
            fig.add_vline(x=20, line_width=1, line_dash="dash", line_color="orange")
            fig.add_vline(x=30, line_width=1, line_dash="dash", line_color="red")
            
            # Add annotations for thresholds
            fig.add_annotation(
                x=10, y=0,
                text=get_text("acceptable_threshold", "Acceptable"),
                showarrow=False,
                yshift=-20
            )
            fig.add_annotation(
                x=20, y=0,
                text=get_text("concerning_threshold", "Concerning"),
                showarrow=False,
                yshift=-20
            )
            fig.add_annotation(
                x=30, y=0,
                text=get_text("critical_threshold", "Critical"),
                showarrow=False,
                yshift=-20
            )
            
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
            
            return fig
        except Exception as e:
            st.error(f"Error creating zero scores chart: {str(e)}")
            return None
    
    # analyse5.py: Correlation Analysis visualizations
    
    def show_correlation_matrix(self, df, columns):
        """
        Display a correlation matrix heatmap.
        For analyse5.py (Correlation Analysis).
        
        Args:
            df (pd.DataFrame): DataFrame containing the data
            columns (list): List of columns to include in correlation
            
        Returns:
            tuple: (figure, correlation_matrix)
        """
        try:
            # Validate input columns
            valid_columns = [col for col in columns if col in df.columns]
            
            if len(valid_columns) < 2:
                st.error("At least two valid columns are required for correlation analysis")
                return None, None
                
            # Calculate correlation matrix
            corr_matrix = df[valid_columns].corr().round(2)
            
            # Get translated column names for display
            translated_labels = [get_text("columns_of_interest", {}).get(col, col) for col in corr_matrix.columns]
            
            # Create heatmap using figure_factory for annotated heatmap
            fig = ff.create_annotated_heatmap(
                z=corr_matrix.values,
                x=translated_labels,
                y=translated_labels,
                annotation_text=corr_matrix.values.round(2),
                colorscale='Viridis',
                showscale=True,
                zmin=-1, zmax=1
            )
            
            # Update layout for better appearance
            fig.update_layout(
                title=get_text("correlation_matrix", "Correlation Matrix"),
                height=600,
                xaxis={'side': 'bottom'}
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            return fig, corr_matrix
        except Exception as e:
            st.error(f"Error creating correlation matrix: {str(e)}")
            return None, None
    
    # analyse6.py: Test Reliability (Cronbach Alpha) visualizations
    
    def show_reliability_visualization(self, alpha_results):
        """
        Display a bar chart of Cronbach's Alpha results.
        For analyse6.py (Test Reliability).
        
        Args:
            alpha_results (pd.DataFrame): DataFrame with alpha results
            
        Returns:
            figure: The created plot
        """
        try:
            # Validate input data
            required_columns = ['test_group', 'alpha_numeric', 'reliability_level']
            if not all(col in alpha_results.columns for col in required_columns):
                missing = [col for col in required_columns if col not in alpha_results.columns]
                st.error(f"Missing required columns for reliability visualization: {', '.join(missing)}")
                return None
                
            # Create a bar chart of alpha values
            fig = px.bar(
                alpha_results,
                x="test_group",
                y="alpha_numeric",
                color="reliability_level",
                labels={
                    "alpha_numeric": get_text("cronbach_alpha", "Cronbach's Alpha"),
                    "reliability_level": get_text("reliability_level", "Reliability Level")
                },
                color_discrete_map={
                    "excellent": "#1E8449",
                    "good": "#58D68D",
                    "acceptable": "#F4D03F",
                    "questionable": "#F39C12",
                    "poor": "#E74C3C",
                    "unacceptable": "#922B21",
                    "insufficient_data": "#CCCCCC"
                },
                title=get_text("reliability_comparison", "Reliability Comparison")
            )
            
            # Add threshold lines
            fig.add_hline(y=0.9, line_dash="dash", line_color="#1E8449", annotation_text=get_text("excellent_threshold", "Excellent (0.9)"))
            fig.add_hline(y=0.8, line_dash="dash", line_color="#58D68D", annotation_text=get_text("good_threshold", "Good (0.8)"))
            fig.add_hline(y=0.7, line_dash="dash", line_color="#F4D03F", annotation_text=get_text("acceptable_threshold", "Acceptable (0.7)"))
            fig.add_hline(y=0.6, line_dash="dash", line_color="#F39C12", annotation_text=get_text("questionable_threshold", "Questionable (0.6)"))
            fig.add_hline(y=0.5, line_dash="dash", line_color="#E74C3C", annotation_text=get_text("poor_threshold", "Poor (0.5)"))
            
            # Update layout
            fig.update_layout(
                yaxis_range=[0, 1],
                xaxis_title=get_text("test_group", "Test Group"),
                yaxis_title=get_text("cronbach_alpha", "Cronbach's Alpha"),
                height=500
            )
            
            st.plotly_chart(fig, use_container_width=True)
            return fig
        except Exception as e:
            st.error(f"Error creating reliability visualization: {str(e)}")
            return None
    
    # analyse7.py: School Performance Analysis visualizations
    
    def show_school_comparison(self, df, column, group_col="school"):
        """
        Display a box plot comparing schools for a specific variable.
        For analyse7.py (School Performance Analysis).
        
        Args:
            df (pd.DataFrame): DataFrame containing the data
            column (str): Column name to visualize
            group_col (str): Column to group by (default: "school")
            
        Returns:
            figure: The created plot
        """
        try:
            # Validate inputs
            if column not in df.columns:
                st.error(f"Column '{column}' not found in data")
                return None
                
            if group_col not in df.columns:
                st.error(f"Group column '{group_col}' not found in data")
                return None
                
            # Get translated column name
            column_name = get_text("columns_of_interest", {}).get(column, column)
            group_label = get_text(group_col, group_col.capitalize())
            
            # Create the box plot
            fig = self.viz_utils.create_box_plot(
                df,
                x=group_col,
                y=column,
                color=group_col,
                title=f"{column_name} - {get_text('by_group', 'by')} {group_label}",
                xaxis_title=group_label,
                yaxis_title=column_name
            )
            
            st.plotly_chart(fig, use_container_width=True)
            return fig
        except Exception as e:
            st.error(f"Error creating school comparison: {str(e)}")
            return None
    
    # analyse10.py: Gender Effect Analysis visualizations
    
    def show_gender_comparison(self, df, column, gender_col="stgender"):
        """
        Display a comparison of scores by gender for a column.
        For analyse10.py (Gender Effect Analysis).
        
        Args:
            df (pd.DataFrame): DataFrame containing the data
            column (str): Column name to visualize
            gender_col (str): Name of the gender column
            
        Returns:
            figure: The created plot
        """
        try:
            # Validate inputs
            if column not in df.columns:
                st.error(f"Column '{column}' not found in data")
                return None
                
            if gender_col not in df.columns:
                st.error(f"Gender column '{gender_col}' not found in data")
                return None
                
            # Get translated column name
            column_name = get_text("columns_of_interest", {}).get(column, column)
            
            # Create the box plot
            fig = self.viz_utils.create_box_plot(
                df,
                x=gender_col,
                y=column,
                color=gender_col,
                title=f"{column_name} - {get_text('by_gender', 'by Gender')}",
                xaxis_title=get_text("gender", "Gender"),
                yaxis_title=column_name,
                color_scheme="binary"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            return fig
        except Exception as e:
            st.error(f"Error creating gender comparison: {str(e)}")
            return None
    
    # analyse12.py: International Standards Comparison visualizations
    
    def show_international_benchmark_comparison(self, local_means, benchmarks):
        """
        Display a comparison of local means against international benchmarks.
        For analyse12.py (International Standards Comparison).
        
        Args:
            local_means (dict): Dictionary of local mean values
            benchmarks (dict): Dictionary of benchmark values
            
        Returns:
            figure: The created plot
        """
        try:
            # Validate inputs
            if not isinstance(local_means, dict) or not isinstance(benchmarks, dict):
                st.error("Local means and benchmarks must be dictionaries")
                return None
                
            if not local_means or not benchmarks:
                st.error("Local means and benchmarks cannot be empty")
                return None
                
            # Check that keys in local_means exist in benchmarks
            missing_benchmarks = [key for key in local_means if key not in benchmarks]
            if missing_benchmarks:
                st.warning(f"Missing benchmarks for: {', '.join(missing_benchmarks)}")
                # Filter out variables without benchmarks
                local_means = {k: v for k, v in local_means.items() if k in benchmarks}
                if not local_means:
                    st.error("No valid variables with benchmarks remaining")
                    return None
            
            # Prepare data for chart
            variables = list(local_means.keys())
            var_names = [get_text("columns_of_interest", {}).get(var, var) for var in variables]
            
            # Create comparison data
            chart_data = []
            for var, var_name in zip(variables, var_names):
                # Add local mean
                chart_data.append({
                    "variable": var_name,
                    "score": local_means[var],
                    "type": get_text("local_mean", "Local Mean")
                })
                
                # Add benchmark
                chart_data.append({
                    "variable": var_name,
                    "score": benchmarks[var],
                    "type": get_text("benchmark", "Benchmark")
                })
            
            chart_df = pd.DataFrame(chart_data)
            
            # Create and display bar chart
            fig = px.bar(
                chart_df,
                x="variable",
                y="score",
                color="type",
                barmode="group",
                title=get_text("comparison_chart_title", "Local Performance vs. International Benchmarks"),
                labels={
                    "variable": get_text("assessment_variable", "Assessment Variable"),
                    "score": get_text("score", "Score"),
                    "type": get_text("value_type", "Value Type")
                },
                color_discrete_map={
                    get_text("local_mean", "Local Mean"): "#3498DB",  # Blue
                    get_text("benchmark", "Benchmark"): "#F39C12"   # Orange
                }
            )
            
            # Update layout
            fig.update_layout(
                xaxis_tickangle=-45,
                legend_title=get_text("value_type", "Value Type"),
                height=600
            )
            
            st.plotly_chart(fig, use_container_width=True)
            return fig
        except Exception as e:
            st.error(f"Error creating benchmark comparison: {str(e)}")
            return None
    
    def show_benchmark_percentage(self, percentage_df):
        """
        Display a percentage achievement chart compared to benchmarks.
        For analyse12.py (International Standards Comparison).
        
        Args:
            percentage_df (pd.DataFrame): DataFrame with percentage data
            
        Returns:
            figure: The created plot
        """
        try:
            # Validate inputs
            required_columns = ["variable_name", "percentage", "achievement_level"]
            if not all(col in percentage_df.columns for col in required_columns):
                missing = [col for col in required_columns if col not in percentage_df.columns]
                st.error(f"Missing required columns for percentage visualization: {', '.join(missing)}")
                return None
            
            # Create percentage chart
            fig = px.bar(
                percentage_df,
                x="variable_name",
                y="percentage",
                color="achievement_level",
                title=get_text("percentage_chart_title", "Percentage of International Benchmark Achieved"),
                labels={
                    "variable_name": get_text("assessment_variable", "Assessment Variable"),
                    "percentage": get_text("percentage_of_benchmark", "% of Benchmark"),
                    "achievement_level": get_text("achievement_level", "Achievement Level")
                },
                color_discrete_map={
                    get_text("critical", "Critical"): "#E74C3C",  # Red
                    get_text("concerning", "Concerning"): "#F39C12",  # Orange
                    get_text("approaching", "Approaching"): "#F1C40F",  # Yellow
                    get_text("meeting", "Meeting"): "#2ECC71"  # Green
                }
            )
            
            # Add reference line at 100%
            fig.add_hline(
                y=100, 
                line_dash="dash", 
                line_color="black",
                annotation_text=get_text("benchmark_line", "Benchmark")
            )
            
            # Add reference lines for achievement levels
            fig.add_hline(y=85, line_dash="dot", line_color="#F1C40F")  # Approaching (Yellow)
            fig.add_hline(y=70, line_dash="dot", line_color="#F39C12")  # Concerning (Orange)
            
            # Update layout
            fig.update_layout(
                xaxis_tickangle=-45,
                legend_title=get_text("achievement_level", "Achievement Level"),
                height=600
            )
            
            st.plotly_chart(fig, use_container_width=True)
            return fig
        except Exception as e:
            st.error(f"Error creating percentage visualization: {str(e)}")
            return None
    
    # analyse13.py: Language of Instruction Comparison visualizations
    
    def show_language_comparison(self, df, column, language_col="language_teaching"):
        """
        Display a comparison of scores by language of instruction.
        For analyse13.py (Language of Instruction Comparison).
        
        Args:
            df (pd.DataFrame): DataFrame containing the data
            column (str): Column name to visualize
            language_col (str): Name of the language column
            
        Returns:
            figure: The created plot
        """
        try:
            # Validate inputs
            if column not in df.columns:
                st.error(f"Column '{column}' not found in data")
                return None
                
            if language_col not in df.columns:
                st.error(f"Language column '{language_col}' not found in data")
                return None
                
            # Get translated column name
            column_name = get_text("columns_of_interest", {}).get(column, column)
            
            # Create the box plot
            fig = px.box(
                df,
                x=language_col,
                y=column,
                color=language_col,
                title=f"{column_name} - {get_text('by_language', 'by Language of Instruction')}",
                labels={
                    language_col: get_text("language_of_instruction", "Language of Instruction"),
                    column: column_name
                },
                color_discrete_map={
                    "English": "#3498DB",  # Blue
                    "Dutch": "#F39C12"     # Orange
                }
            )
            
            # Update layout
            fig.update_layout(
                showlegend=False,
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
            return fig
        except Exception as e:
            st.error(f"Error creating language comparison: {str(e)}")
            return None
    
    # Utility methods for saving figures
    
    def _ensure_temp_dir(self):
        """Ensure a temporary directory exists."""
        if self.temp_dir is None:
            self.temp_dir = tempfile.mkdtemp()
        return self.temp_dir
    
    def save_figure_for_word(self, fig, filename):
        """
        Save a figure to a temporary file for use in Word documents.
        
        Args:
            fig: Plotly figure to save
            filename (str): Base filename (without path)
            
        Returns:
            str: Full path to saved image or None if saving failed
        """
        try:
            if fig is None:
                return None
                
            # Create a temporary directory if it doesn't exist
            temp_dir = self._ensure_temp_dir()
            
            # Save the figure
            img_path = os.path.join(temp_dir, filename)
            fig.write_image(img_path, width=800, height=500)
            
            return img_path
        except Exception as e:
            st.error(f"Error saving figure: {str(e)}")
            return None