"""
Module for interactive correlation analysis with scatter plots and statistics.
"""
import streamlit as st
import plotly.express as px
import numpy as np
from scipy import stats

def display_interactive_analysis(df, selected_columns, t):
    """
    Display interactive correlation analysis with scatter plots and statistics.
    
    Args:
        df (pandas.DataFrame): The data to analyze
        selected_columns (list): List of columns to include in analysis
        t (dict): Translation dictionary for UI elements
    """
    # Create two columns for x and y variable selection
    scatter_col1, scatter_col2 = st.columns(2)
    
    with scatter_col1:
        x_var = st.selectbox(
            t.get("x_variable", "X Variable:"),
            options=selected_columns,
            format_func=lambda x: t["columns_of_interest"].get(x, x)
        )
    
    with scatter_col2:
        y_var = st.selectbox(
            t.get("y_variable", "Y Variable:"),
            options=[c for c in selected_columns if c != x_var],
            format_func=lambda x: t["columns_of_interest"].get(x, x),
            index=min(1, len(selected_columns)-1) if len(selected_columns) > 1 else 0
        )
    
    # Create color group option
    color_var = st.selectbox(
        t.get("color_by", "Color by (optional):"),
        options=[None] + [c for c in df.columns if c not in [x_var, y_var] and df[c].nunique() < 10],
        format_func=lambda x: t.get("none_selected", "None") if x is None else x
    )
    
    # Create scatter plot
    scatter_col1, scatter_col2 = st.columns([2, 1])
    
    with scatter_col1:
        create_scatter_plot(df, x_var, y_var, color_var, t)
    
    with scatter_col2:
        display_correlation_statistics(df, x_var, y_var, t)

def create_scatter_plot(df, x_var, y_var, color_var, t):
    """
    Create a scatter plot with optional grouping and regression lines.
    
    Args:
        df (pandas.DataFrame): The data to analyze
        x_var (str): X-axis variable name
        y_var (str): Y-axis variable name
        color_var (str or None): Variable for color grouping
        t (dict): Translation dictionary for UI elements
    """
    # Create the scatter plot with regression line
    scatter_fig = px.scatter(
        df,
        x=x_var,
        y=y_var,
        color=color_var,
        trendline="ols" if color_var is None else None,
        labels={
            x_var: t["columns_of_interest"].get(x_var, x_var),
            y_var: t["columns_of_interest"].get(y_var, y_var),
            color_var: color_var if color_var else ""
        },
        title=f"{t['columns_of_interest'].get(y_var, y_var)} vs {t['columns_of_interest'].get(x_var, x_var)}"
    )
    
    # If color variable is selected, add trendline for each category
    if color_var is not None:
        for i, group in enumerate(df[color_var].unique()):
            group_df = df[df[color_var] == group]
            if len(group_df) > 2:  # Need at least 3 points for regression
                try:
                    # Calculate trendline
                    slope, intercept, r_value, p_value, std_err = stats.linregress(
                        group_df[x_var].dropna(), 
                        group_df[y_var].dropna()
                    )
                    # Create range of x values
                    x_range = np.linspace(df[x_var].min(), df[x_var].max(), 100)
                    y_range = intercept + slope * x_range
                    
                    # Add trendline as a scatter plot with line
                    scatter_fig.add_scatter(
                        x=x_range, 
                        y=y_range, 
                        mode='lines', 
                        name=f"{group} trendline",
                        line=dict(dash='dash')
                    )
                except:
                    # Skip if regression fails
                    pass
    
    st.plotly_chart(scatter_fig, use_container_width=True)

def display_correlation_statistics(df, x_var, y_var, t):
    """
    Display detailed correlation statistics for the selected variables.
    
    Args:
        df (pandas.DataFrame): The data to analyze
        x_var (str): X-axis variable name
        y_var (str): Y-axis variable name
        t (dict): Translation dictionary for UI elements
    """
    # Calculate correlation statistics
    st.write("#### " + t.get("correlation_stats", "Correlation Statistics"))
    
    # Filter out NaN values
    valid_data = df[[x_var, y_var]].dropna()
    n_valid = len(valid_data)
    
    # Display sample size
    st.write(f"**{t.get('sample_size', 'Sample Size')}:** {n_valid}")
    
    if n_valid < 3:
        st.warning(t.get("insufficient_data", "Insufficient data for correlation analysis."))
        return
    
    # Calculate Pearson correlation
    pearson_r, pearson_p = stats.pearsonr(valid_data[x_var], valid_data[y_var])
    
    # Display Pearson correlation
    st.write(f"**{t.get('pearson_correlation', 'Pearson Correlation')}:**")
    st.write(f"r = {pearson_r:.3f}")
    st.write(f"p-value = {pearson_p:.4f}")
    
    # Interpret p-value
    if pearson_p < 0.001:
        st.write(f"**{t.get('significance', 'Significance')}:** p < 0.001 (***)")
    elif pearson_p < 0.01:
        st.write(f"**{t.get('significance', 'Significance')}:** p < 0.01 (**)")
    elif pearson_p < 0.05:
        st.write(f"**{t.get('significance', 'Significance')}:** p < 0.05 (*)")
    else:
        st.write(f"**{t.get('significance', 'Significance')}:** {t.get('not_significant', 'Not significant')}")
    
    # Interpret strength
    if abs(pearson_r) >= 0.7:
        strength = t.get("very_strong", "Very strong")
    elif abs(pearson_r) >= 0.5:
        strength = t.get("strong", "Strong")
    elif abs(pearson_r) >= 0.3:
        strength = t.get("moderate", "Moderate")
    elif abs(pearson_r) >= 0.1:
        strength = t.get("weak", "Weak")
    else:
        strength = t.get("very_weak", "Very weak or none")
    
    direction = t.get("positive", "positive") if pearson_r > 0 else t.get("negative", "negative")
    st.write(f"**{t.get('strength', 'Strength')}:** {strength} {direction}")
    
    # Calculate Spearman correlation (rank correlation)
    spearman_r, spearman_p = stats.spearmanr(valid_data[x_var], valid_data[y_var])
    
    # Display Spearman correlation
    st.write(f"**{t.get('spearman_correlation', 'Spearman Rank Correlation')}:**")
    st.write(f"rho = {spearman_r:.3f}")
    st.write(f"p-value = {spearman_p:.4f}")
    
    # Calculate linear regression
    try:
        # Calculate linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            valid_data[x_var], valid_data[y_var]
        )
        r_squared = r_value ** 2
        
        # Display regression statistics
        st.write("**" + t.get("linear_regression", "Linear Regression") + ":**")
        st.write(f"y = {slope:.3f}x + {intercept:.3f}")
        st.write(f"R² = {r_squared:.3f}")
        st.write(f"{t.get('slope_p', 'Slope p-value')} = {p_value:.4f}")
    except:
        st.write(t.get("regression_error", "Could not calculate linear regression"))
