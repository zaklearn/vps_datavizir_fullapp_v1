"""
Module for displaying significant correlations and visualizations.
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy import stats
from config import egra_columns, egma_columns

def display_significant_correlations(df, df_strong, t):
    """
    Display significant correlations and visualizations.
    
    Args:
        df (pandas.DataFrame): Original data
        df_strong (pandas.DataFrame): DataFrame with significant correlations
        t (dict): Translation dictionary for UI elements
    """
    if df_strong.empty:
        st.info(t.get("no_strong_correlation", "No significant correlations (>|0.5|) were found."))
        return
    
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
    
    # Display strong correlations table
    st.subheader(t.get("strong_correlations", "📋 Significant Correlations (>|0.5|)"))
    st.dataframe(df_display, use_container_width=True)
    
    # Pairwise Scatterplot Matrix for Strongest Correlations
    if len(df_strong) >= 2:
        display_strongest_scatterplots(df, df_strong, t)
    
    # Visualize significant correlations as a network
    if len(df_strong) >= 3:  # Only show if we have enough relationships
        display_correlation_network(df_strong, t)

def display_strongest_scatterplots(df, df_strong, t):
    """
    Display scatterplots for the strongest correlations.
    
    Args:
        df (pandas.DataFrame): Original data
        df_strong (pandas.DataFrame): DataFrame with significant correlations
        t (dict): Translation dictionary for UI elements
    """
    st.subheader(t.get("strong_correlation_scatterplots", "📊 Strongest Correlation Scatterplots"))
    
    # Get the top N strongest correlations
    top_n = min(6, len(df_strong))  # Limit to top 6
    strongest_pairs = []
    
    # Collect variable pairs with strongest correlations
    for i in range(top_n):
        var1 = df_strong.iloc[i]["task1"]
        var2 = df_strong.iloc[i]["task2"]
        corr_value = df_strong.iloc[i]["correlation"]
        strongest_pairs.append((var1, var2, corr_value))
    
    # Create scatterplots for strongest correlations
    for i in range(0, len(strongest_pairs), 2):  # Display 2 plots per row
        cols = st.columns(2)
        
        # First plot in row
        if i < len(strongest_pairs):
            var1, var2, corr = strongest_pairs[i]
            with cols[0]:
                create_correlation_scatterplot(df, var1, var2, corr, t)
        
        # Second plot in row
        if i + 1 < len(strongest_pairs):
            var1, var2, corr = strongest_pairs[i + 1]
            with cols[1]:
                create_correlation_scatterplot(df, var1, var2, corr, t)

def create_correlation_scatterplot(df, var1, var2, corr_value, t):
    """
    Create a scatterplot with regression line for a pair of variables.
    
    Args:
        df (pd.DataFrame): DataFrame with the data
        var1 (str): First variable name
        var2 (str): Second variable name
        corr_value (float): Correlation value
        t (dict): Translation dictionary for UI elements
    """
    # Translate variable names
    var1_name = t["columns_of_interest"].get(var1, var1)
    var2_name = t["columns_of_interest"].get(var2, var2)
    
    # Create scatter plot with regression line
    fig = px.scatter(
        df,
        x=var1,
        y=var2,
        trendline="ols",
        labels={
            var1: var1_name,
            var2: var2_name
        },
        title=f"{var2_name} vs {var1_name} (r = {corr_value:.2f})"
    )
    
    # Update layout
    fig.update_layout(height=350)
    
    # Display plot
    st.plotly_chart(fig, use_container_width=True)
    
    # Calculate and display regression equation
    try:
        # Calculate linear regression
        valid_data = df[[var1, var2]].dropna()
        slope, intercept, r_value, p_value, std_err = stats.linregress(
            valid_data[var1], valid_data[var2]
        )
        r_squared = r_value ** 2
        
        equation = f"y = {slope:.3f}x + {intercept:.3f} (R² = {r_squared:.3f})"
        st.caption(equation)
    except:
        pass

def display_correlation_network(df_strong, t):
    """
    Display a network visualization of significant correlations.
    
    Args:
        df_strong (pandas.DataFrame): DataFrame with significant correlations
        t (dict): Translation dictionary for UI elements
    """
    st.subheader(t.get("correlation_network", "🔄 Correlation Network"))
    
    # Prepare data for network visualization
    network_nodes = set()
    for _, row in df_strong.iterrows():
        network_nodes.add(row["task1"])
        network_nodes.add(row["task2"])
    
    # Create network edges data
    edge_data = []
    for _, row in df_strong.iterrows():
        edge_data.append({
            "source": t["columns_of_interest"].get(row["task1"], row["task1"]),
            "target": t["columns_of_interest"].get(row["task2"], row["task2"]),
            "correlation": row["correlation"],
            "width": abs(row["correlation"]) * 5,  # Scale line width by correlation strength
            "color": "positive" if row["correlation"] > 0 else "negative"
        })
    
    # Create network nodes data
    node_data = []
    for node in network_nodes:
        # Determine if node is EGRA or EGMA
        node_type = "EGRA" if node in egra_columns else "EGMA"
        node_data.append({
            "name": t["columns_of_interest"].get(node, node),
            "type": node_type,
            "id": node
        })
    
    # Convert data for visualization
    edges_df = pd.DataFrame(edge_data)
    nodes_df = pd.DataFrame(node_data)
    
    # Display explanation for the network graph
    st.info(t.get("network_explanation", "This network shows significant relationships between skills. Line thickness represents correlation strength, blue lines show positive correlations, and red lines show negative correlations."))
    
    # Generate custom network visualization using Plotly
    try:
        create_network_visualization(nodes_df, edges_df, t)
    except Exception as e:
        st.error(f"Error creating network visualization: {str(e)}")

def create_network_visualization(nodes_df, edges_df, t):
    """
    Create a network visualization of correlations.
    
    Args:
        nodes_df (pandas.DataFrame): DataFrame with node data
        edges_df (pandas.DataFrame): DataFrame with edge data
        t (dict): Translation dictionary for UI elements
    """
    # Create a scatter plot for nodes
    fig = px.scatter(
        nodes_df, 
        title=t.get("correlation_network_title", "Relationships Between Skills"),
        color="type",
        color_discrete_map={"EGRA": "#19D3F3", "EGMA": "#FFA15A"}
    )
    
    # Plot in 2D space
    pos = {}
    n = len(nodes_df)
    radius = 1
    for i, row in nodes_df.iterrows():
        angle = 2 * np.pi * i / n
        pos[row["name"]] = (radius * np.cos(angle), radius * np.sin(angle))
    
    # Create scatter plot for nodes
    node_x = [pos[name][0] for name in nodes_df["name"]]
    node_y = [pos[name][1] for name in nodes_df["name"]]
    
    fig = px.scatter(
        x=node_x, 
        y=node_y,
        text=nodes_df["name"],
        color=nodes_df["type"],
        color_discrete_map={"EGRA": "#19D3F3", "EGMA": "#FFA15A"},
        title=t.get("correlation_network_title", "Relationships Between Skills")
    )
    
    # Add edges (lines between nodes)
    for _, edge in edges_df.iterrows():
        fig.add_shape(
            type="line",
            x0=pos[edge["source"]][0],
            y0=pos[edge["source"]][1],
            x1=pos[edge["target"]][0],
            y1=pos[edge["target"]][1],
            line=dict(
                color="blue" if edge["color"] == "positive" else "red", 
                width=edge["width"]
            )
        )
    
    # Add node labels
    for name, position in pos.items():
        fig.add_annotation(
            x=position[0],
            y=position[1],
            text=name,
            showarrow=False,
            font=dict(size=10)
        )
    
    # Update layout for better visualization
    fig.update_layout(
        showlegend=True,
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        height=500,
        legend=dict(title=t.get("skill_type", "Skill Type"))
    )
    
    st.plotly_chart(fig, use_container_width=True)
