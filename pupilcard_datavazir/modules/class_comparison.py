"""
Module class_comparison.py - Comparison of class performances.

This module provides functionality for comparing student performance
across different classes within a school. It visualizes EGRA and EGMA
results for multiple classes and provides insights using an AI-enhanced
interpretation system.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import traceback
from modules import comparative_common as cc
from modules import interpretation
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
            "Everest Learning Center", "Cambridge Excellence Academy"
        ]
        
        class_names = ["3A", "3B", "4A", "4B", "5A", "5B"]
        
        last_names = ["Smith", "Johnson", "Brown", "Garcia", "Williams", "Lee", "Kim", "Patel", "Schneider", "Ivanov"]
        first_names = ["Emma", "Liam", "Olivia", "Noah", "Sophia", "Lucas", "Mia", "Ethan", "Isabella", "Nathan"]
        
        # Generate 50 records for better demonstration
        num_records = 50
        
        demo_data = {
            "school": [random.choice(school_names) for _ in range(num_records)],
            "group": [random.choice(class_names) for _ in range(num_records)],
            "pupil_id": list(range(1, num_records + 1)),
            "last_name": [random.choice(last_names) for _ in range(num_records)],
            "first_name": [random.choice(first_names) for _ in range(num_records)],
            "language": ["English", "French", "Spanish", "German", "Mandarin"] * 10,
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
        st.error(f"Error generating demo data: {str(e)}")
        st.error(traceback.format_exc())
        # Return a minimal dataframe to avoid crashing
        return pd.DataFrame()


def main():
    """
    Main function for the class comparison module
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
        
        st.header("📚 Class Comparison")
        
        # School selection with error handling
        try:
            selected_school = st.selectbox("Select a school", sorted(df['school'].unique()))
        except Exception as e:
            st.error(f"Error retrieving schools: {str(e)}")
            return
        
        if selected_school:
            try:
                # Filter data for the selected school
                school_data = df[df['school'] == selected_school]
                
                if school_data.empty:
                    st.warning(f"No data available for {selected_school}.")
                    return
                
                # Check if there are at least two classes to compare
                if len(school_data['group'].unique()) < 1:
                    st.warning(f"At least one class is required for comparison. Found {len(school_data['group'].unique())} classes.")
                    return
                
                # Calculate class comparison data
                try:
                    egra_table, egma_table, class_means = cc.calculate_class_comparison(df, selected_school)
                except Exception as e:
                    st.error(f"Error calculating comparison data: {str(e)}")
                    st.error(traceback.format_exc())
                    return
                
                # EGRA Results
                st.subheader("📖 EGRA Results")
                if egra_table is not None and not egra_table.empty:
                    st.dataframe(egra_table, use_container_width=True)
                else:
                    st.warning("No EGRA data available for comparison.")
                
                egra_indicators = ["clpm", "phoneme", "sound_word", "cwpm", "listening", "orf", "comprehension"]
                try:
                    fig_egra = cc.plot_comparison(class_means, egra_indicators, "EGRA Comparison by class with standards")
                    st.plotly_chart(fig_egra, use_container_width=True)
                except Exception as e:
                    st.error(f"Error creating EGRA chart: {str(e)}")
                    fig_egra = None
                
                # EGMA Results
                st.subheader("🔢 EGMA Results")
                if egma_table is not None and not egma_table.empty:
                    st.dataframe(egma_table, use_container_width=True)
                else:
                    st.warning("No EGMA data available for comparison.")
                
                egma_indicators = ["number_id", "discrimin", "missing_number", "addition", "subtraction", "problems"]
                try:
                    fig_egma = cc.plot_comparison(class_means, egma_indicators, "EGMA Comparison by class with standards")
                    st.plotly_chart(fig_egma, use_container_width=True)
                except Exception as e:
                    st.error(f"Error creating EGMA chart: {str(e)}")
                    fig_egma = None
                
                # Interpretation
                summary_text = None
                llm_summary = None
                
                if class_means is not None and not class_means.empty:
                    try:
                        # Generate interpretations
                        summary_text = interpretation.generate_group_summary(class_means, level='class')
                        prompt = interpretation.create_group_prompt(summary_text)
                        llm_summary = interpretation.generate_llm_message(prompt)
                        
                        # Display interpretations
                        st.subheader("🧠 Class Insights")
                        st.markdown("**Systematic Summary**")
                        st.info(summary_text)
                        st.markdown("**LLM Interpretation**")
                        st.success(llm_summary)
                    except Exception as e:
                        st.error(f"Error generating interpretation: {str(e)}")
                        st.error(traceback.format_exc())

                # Export section
                figures = [fig_egra, fig_egma] 
                st.markdown("### 💾 Export Report")
                if st.button("📝 Generate Report"):
                    try:
                        report_title = f"Class Comparison Report - {selected_school}"
                        word_file = cc.export_comparison_to_word(
                            report_title, 
                            egra_table, 
                            egma_table, 
                            figures,
                            summary_text,
                            llm_summary
                        )
                        now = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"class_comparison_{selected_school.replace(' ', '_')}_{now}.docx"
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
                st.error(f"Unexpected error during class comparison: {str(e)}")
                st.error(traceback.format_exc())
    except Exception as e:
        st.error(f"Critical application error: {str(e)}")
        st.error(traceback.format_exc())
        st.info("Please refresh the page and try again. If the problem persists, contact support.")


if __name__ == '__main__':
    main()