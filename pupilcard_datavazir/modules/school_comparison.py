"""
Module school_comparison.py - Comparison of school performances.

This module provides functionality for comparing student performance
across different schools. It visualizes EGRA and EGMA results for 
multiple schools and provides insights using an AI-enhanced
interpretation system.
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import traceback
from modules import comparative_common as cc
from modules import interpretation
from modules import language
from datetime import datetime
import random

def load_demo_data():
    """
    Generate demo data for testing purposes
    
    Returns:
        DataFrame: Demo data with random values
    """
    try:
        school_names = [
            "Greenwood International School", "Maplewood Academy", "Oxford Preparatory School",
            "Global Leaders Institute", "Harborview High School", "Sunrise International Academy",
            "Everest Learning Center", "Cambridge Excellence Academy", "Horizon Charter School",
            "New Dawn Academy"
        ]
        
        class_names = ["3A", "3B", "4A", "4B", "5A", "5B", "5C"]
        
        last_names = ["Smith", "Johnson", "Brown", "Garcia", "Williams", "Lee", "Kim", "Patel", "Schneider", "Ivanov"]
        first_names = ["Emma", "Liam", "Olivia", "Noah", "Sophia", "Lucas", "Mia", "Ethan", "Isabella", "Nathan"]
        
        # Generate 100 records for better demonstration
        num_records = 100
        
        demo_data = {
            "school": [random.choice(school_names) for _ in range(num_records)],
            "group": [random.choice(class_names) for _ in range(num_records)],
            "pupil_id": list(range(1, num_records + 1)),
            "last_name": [random.choice(last_names) for _ in range(num_records)],
            "first_name": [random.choice(first_names) for _ in range(num_records)],
            "language": ["English", "French", "Spanish", "German", "Mandarin"] * 20,
            "st_gender": [random.choice(["M", "F"]) for _ in range(num_records)],
            "st_age": [random.randint(6, 12) for _ in range(num_records)],
            "clpm": [random.randint(10, 60) for _ in range(num_records)],
            "phoneme": [random.randint(10, 50) for _ in range(num_records)],
            "sound_word": [random.randint(30, 80) for _ in range(num_records)],
            "cwpm": [random.randint(5, 35) for _ in range(num_records)],
            "listening": [random.randint(40, 90) for _ in range(num_records)],
            "orf": [random.randint(20, 70) for _ in range(num_records)],
            "comprehension": [random.randint(30, 85) for _ in range(num_records)],
            "number_id": [random.randint(10, 50) for _ in range(num_records)],
            "discrimin": [random.randint(20, 60) for _ in range(num_records)],
            "missing_number": [random.randint(15, 55) for _ in range(num_records)],
            "addition": [random.randint(5, 25) for _ in range(num_records)],
            "subtraction": [random.randint(5, 25) for _ in range(num_records)],
            "problems": [random.randint(10, 50) for _ in range(num_records)]
        }
        
        return pd.DataFrame(demo_data)
    except Exception as e:
        print(f"Error generating demo data: {str(e)}")
        print(traceback.format_exc())
        # Return a minimal dataframe to avoid crashing
        return pd.DataFrame()

def main():
    """
    Main function for the school comparison module
    """
    try:
        # Sidebar for data loading
        with st.sidebar:
            st.header("📂 Data Source")
            use_demo = st.checkbox("Use demo data")
            uploaded_file = st.file_uploader("Or load an Excel file", type=["xlsx"])
            
        if use_demo:
            try:
                df = load_demo_data()
                if df.empty:
                    st.error("Failed to generate demo data.")
                    return
                st.success("✅ Demo data loaded successfully!")
            except Exception as e:
                st.error(f"Error loading demo data: {str(e)}")
                return
        elif uploaded_file is not None:
            try:
                df = pd.read_excel(uploaded_file)
                st.success("✅ File loaded successfully!")
                # Basic validation
                required_columns = ["school", "group", "clpm", "phoneme", "number_id"]
                missing = [col for col in required_columns if col not in df.columns]
                if missing:
                    st.error(f"Missing required columns: {', '.join(missing)}")
                    return
            except Exception as e:
                st.error(f"Error reading Excel file: {str(e)}")
                return
        else:
            st.info("👈 Please choose a data source.")
            return
        
        st.header("🏫 School Comparison")
        
        # School selection with error handling
        try:
            # Get unique schools and sort alphabetically
            unique_schools = sorted(df['school'].unique())
            
            if len(unique_schools) < 2:
                st.warning(f"At least two schools are required for comparison. Found {len(unique_schools)} schools.")
                return
            
            # Select up to 5 schools by default or as many as available
            default_count = min(5, len(unique_schools))
            selected_schools = st.multiselect(
                "Select schools to compare",
                unique_schools,
                default=unique_schools[0:default_count] if len(unique_schools) >= default_count else unique_schools
            )
        except Exception as e:
            st.error(f"Error retrieving schools: {str(e)}")
            st.error(traceback.format_exc())
            return

        if selected_schools:
            try:
                if len(selected_schools) < 1:
                    st.warning("Please select at least one school for comparison.")
                    return
                
                # Define indicator lists
                egra_indicators = ["clpm", "phoneme", "sound_word", "cwpm", "listening", "orf", "comprehension"]
                egma_indicators = ["number_id", "discrimin", "missing_number", "addition", "subtraction", "problems"]
                
                # Calculate means by school
                try:
                    school_means = df[df['school'].isin(selected_schools)].groupby('school')[egra_indicators + egma_indicators].mean()
                    
                    if school_means.empty:
                        st.warning("No data available for the selected schools.")
                        return
                except Exception as e:
                    st.error(f"Error calculating school means: {str(e)}")
                    st.error(traceback.format_exc())
                    return
                
                # Generate interpretations
                summary_text = None
                llm_summary = None
                
                try:
                    summary_text = interpretation.generate_group_summary(school_means, level='school')
                    prompt = interpretation.create_group_prompt(summary_text)
                    llm_summary = interpretation.generate_llm_message(prompt)

                    # Display insights
                    st.subheader("🧠 School Insights")
                    st.markdown("**Systematic Summary**")
                    st.info(summary_text)
                    st.markdown("**LLM Interpretation**")
                    st.success(llm_summary)
                except Exception as e:
                    st.error(f"Error generating interpretation: {str(e)}")
                    st.error(traceback.format_exc())
                
                # Lists to store the figures and tables for reporting
                egra_figures = []
                egma_figures = []
                egra_tables = []
                egma_tables = []
                
                # EGRA Results
                st.subheader("📖 EGRA Results")
                
                for indicator in egra_indicators:
                    with st.expander(f"📊 {cc.get_labels()[indicator]}", expanded=True if indicator == egra_indicators[0] else False):
                        col1, col2 = st.columns(2)
                        indicator_data = []
                        
                        # Retrieve scores by school
                        try:
                            for school in selected_schools:
                                score = school_means.loc[school, indicator]
                                indicator_data.append({
                                    'School': school,
                                    'Score': f"{score:.1f}",
                                    'Standard': cc.STANDARDS[indicator]['Mastery'],
                                    'Status': cc.get_status(score, indicator)
                                })

                            # Display the data table
                            with col1:
                                df_indicator = pd.DataFrame(indicator_data)
                                st.dataframe(df_indicator, use_container_width=True)
                                egra_tables.append(df_indicator)
                            
                            # Create and display the chart
                            with col2:
                                fig = go.Figure()
                                
                                # Generate a list of colors from the viridis palette
                                num_schools = len(selected_schools)
                                colors = px.colors.sequential.Viridis  # List of viridis colors
                                colors = colors[:num_schools]  # Adjust the color list if necessary

                                # Add bars for each school with colors
                                fig.add_trace(go.Bar(
                                    name='Score',
                                    x=[school for school in selected_schools],
                                    y=[float(row['Score']) for row in indicator_data],
                                    text=[row['Score'] for row in indicator_data],
                                    textposition='outside',
                                    marker=dict(color=colors)  # Distinct colors for each bar
                                ))

                                # Add trace for standard
                                fig.add_trace(go.Scatter(
                                    name='Standard',
                                    x=[school for school in selected_schools],
                                    y=[cc.STANDARDS[indicator]['Mastery']] * len(selected_schools),
                                    mode='lines',
                                    line=dict(color='red', dash='dash'),
                                ))

                                # Update layout
                                fig.update_layout(
                                    title=f"Comparison - {cc.get_labels()[indicator]}",
                                    xaxis_title="Schools",
                                    yaxis_title="Score",
                                    showlegend=True,
                                    height=400
                                )
                                st.plotly_chart(fig, use_container_width=True)
                                egra_figures.append(fig)
                        except Exception as e:
                            st.error(f"Error displaying EGRA indicator {indicator}: {str(e)}")
                            continue
                            
                # EGMA Results
                st.subheader("🔢 EGMA Results")
                
                for indicator in egma_indicators:
                    with st.expander(f"📊 {cc.get_labels()[indicator]}", expanded=True if indicator == egma_indicators[0] else False):
                        col1, col2 = st.columns(2)
                        indicator_data = []
                        
                        # Retrieve scores by school
                        try:
                            for school in selected_schools:
                                score = school_means.loc[school, indicator]
                                indicator_data.append({
                                    'School': school,
                                    'Score': f"{score:.1f}",
                                    'Standard': cc.STANDARDS[indicator]['Mastery'],
                                    'Status': cc.get_status(score, indicator)
                                })

                            # Display the data table
                            with col1:
                                df_indicator = pd.DataFrame(indicator_data)
                                st.dataframe(df_indicator, use_container_width=True)
                                egma_tables.append(df_indicator)
                            
                            # Create and display the chart
                            with col2:
                                fig = go.Figure()
                                
                                # Generate a list of colors from the viridis palette
                                num_schools = len(selected_schools)
                                colors = px.colors.sequential.Viridis  # List of viridis colors
                                colors = colors[:num_schools]  # Adjust the color list if necessary

                                # Add bars for each school with colors
                                fig.add_trace(go.Bar(
                                    name='Score',
                                    x=[school for school in selected_schools],
                                    y=[float(row['Score']) for row in indicator_data],
                                    text=[row['Score'] for row in indicator_data],
                                    textposition='outside',
                                    marker=dict(color=colors)  # Distinct colors for each bar
                                ))

                                # Add trace for standard
                                fig.add_trace(go.Scatter(
                                    name='Standard',
                                    x=[school for school in selected_schools],
                                    y=[cc.STANDARDS[indicator]['Mastery']] * len(selected_schools),
                                    mode='lines',
                                    line=dict(color='red', dash='dash'),
                                ))

                                # Update layout
                                fig.update_layout(
                                    title=f"Comparison - {cc.get_labels()[indicator]}",
                                    xaxis_title="Schools",
                                    yaxis_title="Score",
                                    showlegend=True,
                                    height=400
                                )
                                st.plotly_chart(fig, use_container_width=True)
                                egma_figures.append(fig)
                        except Exception as e:
                            st.error(f"Error displaying EGMA indicator {indicator}: {str(e)}")
                            continue
                            
                # Create combined overview figures for export
                try:
                    overview_egra_fig = go.Figure()
                    overview_egma_fig = go.Figure()
                    
                    # Add school bars for EGRA overview
                    for i, school in enumerate(selected_schools):
                        overview_egra_fig.add_trace(go.Bar(
                            name=school,
                            x=[cc.get_labels()[ind] for ind in egra_indicators],
                            y=[school_means.loc[school, ind] for ind in egra_indicators],
                            text=[f"{school_means.loc[school, ind]:.1f}" for ind in egra_indicators],
                            textposition='outside',
                            marker=dict(color=colors[i % len(colors)])
                        ))
                        
                    # Add standard line for EGRA overview
                    overview_egra_fig.add_trace(go.Scatter(
                        name='Standard',
                        x=[cc.get_labels()[ind] for ind in egra_indicators],
                        y=[cc.STANDARDS[ind]['Mastery'] for ind in egra_indicators],
                        mode='lines+markers',
                        line=dict(color='red', dash='dash', width=2),
                        marker=dict(symbol='diamond', size=10)
                    ))
                    
                    # Update EGRA overview layout
                    overview_egra_fig.update_layout(
                        title="EGRA Indicators by School",
                        xaxis_title="Indicators",
                        yaxis_title="Score",
                        xaxis={'tickangle': -45},
                        barmode='group',
                        showlegend=True,
                        height=500
                    )
                    
                    # Add school bars for EGMA overview
                    for i, school in enumerate(selected_schools):
                        overview_egma_fig.add_trace(go.Bar(
                            name=school,
                            x=[cc.get_labels()[ind] for ind in egma_indicators],
                            y=[school_means.loc[school, ind] for ind in egma_indicators],
                            text=[f"{school_means.loc[school, ind]:.1f}" for ind in egma_indicators],
                            textposition='outside',
                            marker=dict(color=colors[i % len(colors)])
                        ))
                        
                    # Add standard line for EGMA overview
                    overview_egma_fig.add_trace(go.Scatter(
                        name='Standard',
                        x=[cc.get_labels()[ind] for ind in egma_indicators],
                        y=[cc.STANDARDS[ind]['Mastery'] for ind in egma_indicators],
                        mode='lines+markers',
                        line=dict(color='red', dash='dash', width=2),
                        marker=dict(symbol='diamond', size=10)
                    ))
                    
                    # Update EGMA overview layout
                    overview_egma_fig.update_layout(
                        title="EGMA Indicators by School",
                        xaxis_title="Indicators",
                        yaxis_title="Score",
                        xaxis={'tickangle': -45},
                        barmode='group',
                        showlegend=True,
                        height=500
                    )
                except Exception as e:
                    st.error(f"Error creating overview figures: {str(e)}")
                    st.error(traceback.format_exc())
                    overview_egra_fig = None
                    overview_egma_fig = None
                
                # Export option
                st.markdown("### 💾 Export Report")
                if st.button("📝 Generate Report"):
                    try:
                        # Create a combined table for export
                        egra_report_df = pd.concat(egra_tables) if egra_tables else pd.DataFrame()
                        egma_report_df = pd.concat(egma_tables) if egma_tables else pd.DataFrame()
                        
                        report_title = "School Comparison Report"
                        word_file = cc.export_comparison_to_word(
                            report_title,
                            egra_report_df, 
                            egma_report_df, 
                            [overview_egra_fig, overview_egma_fig],
                            summary_text,
                            llm_summary
                        )
                        
                        now = datetime.now().strftime("%Y%m%d_%H%M%S")
                        # Limit the filename length to avoid errors
                        schools_str = "_".join([s.replace(" ", "")[:10] for s in selected_schools])[:30]
                        filename = f"school_comparison_{schools_str}_{now}.docx"
                        
                        st.download_button(
                            label="📝 Download Word Report",
                            data=word_file,
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                        )
                        st.success("✅ Word report generated successfully!")
                    except Exception as e:
                        st.error(f"Error generating report: {str(e)}")
                        st.error(traceback.format_exc())
            except Exception as e:
                st.error(f"Unexpected error during school comparison: {str(e)}")
                st.error(traceback.format_exc())
    except Exception as e:
        st.error(f"Critical application error: {str(e)}")
        st.error(traceback.format_exc())
        st.info("Please refresh the page and try again. If the problem persists, contact support.")

if __name__ == '__main__':
    main()