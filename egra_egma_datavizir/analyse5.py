import streamlit as st
import pandas as pd
import tempfile
import os
from config import translations, egra_columns, egma_columns

# Import modular components
from correlation_modules.matrix import display_correlation_heatmap
from correlation_modules.interactive import display_interactive_analysis
from correlation_modules.significant import display_significant_correlations
from correlation_modules.interpretation import provide_educational_interpretation
from correlation_modules.report import create_correlation_word_report

def show_correlation(df, language):
    """
    Displays correlation analysis between EGRA and EGMA variables with enhanced
    visualizations including scatterplots and regression analysis.
    
    Args:
        df (pandas.DataFrame): The data to analyze
        language (str): Selected language for UI elements (en/fr)
    """
    t = translations[language]  # Get translations for selected language
    
    st.markdown(f"""
    ### {t.get("title_correlation", "Correlation Analysis")}
    
    🔍 **{t.get("correlation_intro", "Objective: Identify relationships between different assessment tasks.")}**
    
    📌 **{t.get("correlation_interpretation", "Interpretation Guide:")}**
    - {t.get("correlation_point1", "A correlation close to 1 indicates a strong positive relationship")}
    - {t.get("correlation_point2", "A correlation close to -1 indicates a strong negative relationship")}
    - {t.get("correlation_point3", "A correlation close to 0 indicates a weak or no relationship")}
    - {t.get("correlation_point4", "Correlations > 0.5 or < -0.5 are considered significant")}
    """)
    
    # Get available assessment columns
    available_egra = [col for col in egra_columns if col in df.columns]
    available_egma = [col for col in egma_columns if col in df.columns]
    available_columns = available_egra + available_egma
    
    if not available_columns:
        st.error(t.get("no_assessment_columns", "No assessment columns found in the data."))
        return
    
    # Allow users to select columns for correlation analysis
    st.subheader(t.get("select_variables", "📋 Select Variables for Correlation Analysis"))
    
    # Create two columns for selection
    col1, col2 = st.columns(2)
    
    with col1:
        selected_egra = st.multiselect(
            t.get("egra_variables", "EGRA Variables:"),
            options=available_egra,
            default=available_egra[:min(3, len(available_egra))],
            format_func=lambda x: t["columns_of_interest"].get(x, x)
        )
    
    with col2:
        selected_egma = st.multiselect(
            t.get("egma_variables", "EGMA Variables:"),
            options=available_egma,
            default=available_egma[:min(3, len(available_egma))],
            format_func=lambda x: t["columns_of_interest"].get(x, x)
        )
    
    selected_columns = selected_egra + selected_egma
    
    if selected_columns:
        try:
            # Calculate correlation matrix
            corr_matrix = df[selected_columns].corr().round(2)
            
            # Find significant correlations
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
            else:
                df_strong = pd.DataFrame(columns=["task1", "task2", "correlation"])
            
            # Create tabs for different analyses
            tab1, tab2, tab3, tab4 = st.tabs([
                t.get("heatmap_tab", "Correlation Matrix"), 
                t.get("interactive_tab", "Interactive Analysis"),
                t.get("significant_tab", "Significant Correlations"),
                t.get("interpretation_tab", "Educational Interpretation")
            ])
            
            # Tab 1: Correlation Matrix
            with tab1:
                display_correlation_heatmap(corr_matrix, t)
            
            # Tab 2: Interactive Correlation Analysis
            with tab2:
                display_interactive_analysis(df, selected_columns, t)
            
            # Tab 3: Significant Correlations
            with tab3:
                display_significant_correlations(df, df_strong, t)
            
            # Tab 4: Educational Interpretation
            with tab4:
                if not df_strong.empty:
                    provide_educational_interpretation(df_strong, t)
                else:
                    st.info(t.get("no_strong_correlation", "No significant correlations (>|0.5|) were found."))
            
            # Export options
            st.subheader(t.get("export_options", "Export Options"))
            col1, col2 = st.columns(2)
            
            # CSV Export
            with col1:
                if not df_strong.empty:
                    # Translate column names for display
                    df_display = df_strong.copy()
                    df_display["task1"] = df_display["task1"].map(lambda x: t["columns_of_interest"].get(x, x))
                    df_display["task2"] = df_display["task2"].map(lambda x: t["columns_of_interest"].get(x, x))
                    
                    # Format column names for display
                    df_display.columns = [
                        t.get("task_1", "Task 1"),
                        t.get("task_2", "Task 2"),
                        t.get("correlation", "Correlation")
                    ]
                    
                    csv = df_display.to_csv(index=False).encode('utf-8-sig')
                    st.download_button(
                        t.get("export_correlation_csv", "📥 Download CSV"),
                        csv,
                        "significant_correlations.csv",
                        "text/csv",
                        key='download-correlation-csv'
                    )
                else:
                    st.info(t.get("no_data_for_export", "No significant correlations to export."))
            
            # Word Export
            with col2:
                if st.button(t.get("export_correlation_word", "📄 Export to Word")):
                    try:
                        doc = create_correlation_word_report(corr_matrix, df_strong, t, df)
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp:
                            doc.save(tmp.name)
                            with open(tmp.name, 'rb') as f:
                                docx = f.read()
                            st.download_button(
                                t.get("download_correlation_word", "📥 Download Word Report"),
                                docx,
                                "correlation_analysis.docx",
                                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
                            )
                        os.unlink(tmp.name)
                    except Exception as e:
                        st.error(f"Error creating Word report: {str(e)}")
        
        except Exception as e:
            st.error(f"Error in correlation analysis: {str(e)}")
    
    else:
        st.warning(t.get("warning_select_variable", "Please select at least one variable to analyze."))
