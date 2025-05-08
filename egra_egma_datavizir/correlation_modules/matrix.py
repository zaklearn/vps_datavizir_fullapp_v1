"""
Module for generating and displaying correlation matrix visualizations.
"""
import streamlit as st
import plotly.figure_factory as ff

def display_correlation_heatmap(corr_matrix, t):
    """
    Display the correlation matrix heatmap.
    
    Args:
        corr_matrix (pandas.DataFrame): Correlation matrix to visualize
        t (dict): Translation dictionary for UI elements
    """
    # Create correlation heatmap
    translated_labels = [t["columns_of_interest"].get(col, col) for col in corr_matrix.columns]
    
    # Use Plotly's figure factory for annotated heatmap
    fig = ff.create_annotated_heatmap(
        z=corr_matrix.values,
        x=translated_labels,
        y=translated_labels,
        annotation_text=corr_matrix.values.round(2),
        colorscale='Viridis',
        showscale=True,
        zmin=-1, zmax=1
    )
    
    # Update layout for better readability
    fig.update_layout(
        height=600,
        xaxis={'side': 'bottom'},
        title=t.get("correlation_heatmap_title", "Correlation Heatmap"),
        xaxis_title=t.get("variables", "Variables"),
        yaxis_title=t.get("variables", "Variables")
    )
    
    # Rotate x-axis labels for better readability
    fig.update_xaxes(tickangle=-45)
    
    st.plotly_chart(fig, use_container_width=True)
