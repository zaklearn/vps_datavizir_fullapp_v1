import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import numpy as np
import pandas as pd
from scipy import stats
import tempfile
import os
from pathlib import Path

# Define standard color schemes that are colorblind-friendly
# Based on ColorBrewer and IBM Design Library
COLOR_SCHEMES = {
    "categorical": ["#4E79A7", "#F28E2B", "#76B7B2", "#59A14F", "#EDC948", "#B07AA1", "#FF9DA7", "#9C755F", "#BAB0AC"],
    "sequential_blue": ["#DEEBF7", "#9ECAE1", "#4292C6", "#2171B5", "#08306B"],
    "sequential_green": ["#E5F5E0", "#A1D99B", "#41AB5D", "#238B45", "#005A32"],
    "sequential_orange": ["#FEEDDE", "#FDBE85", "#FD8D3C", "#E6550D", "#A63603"],
    "diverging": ["#2171B5", "#6BAED6", "#BDD7E7", "#EBEBEB", "#F7B799", "#E6550D", "#A63603"],
    "binary": ["#4E79A7", "#F28E2B"]  # For binary comparisons (e.g., gender)
}

class VisualizationUtilities:
    """Utility class for creating standardized, publication-quality visualizations."""
    
    def __init__(self, language="en"):
        """
        Initialize the visualization utilities with language setting.
        
        Args:
            language (str): Language for labels and titles ("en" or "fr")
        """
        self.language = language
        self.translations = {
            "en": {
                "mean": "Mean",
                "median": "Median",
                "score": "Score",
                "frequency": "Frequency",
                "variable": "Variable",
                "group": "Group",
                "count": "Count",
                "value": "Value",
                "correlation": "Correlation",
                "distribution": "Distribution of {}",
                "comparison": "{} by {}",
                "save_failed": "Failed to save visualization",
                "normal_curve": "Normal Distribution Curve",
                "trend_line": "Trend Line"
            },
            "fr": {
                "mean": "Moyenne",
                "median": "Médiane",
                "score": "Score",
                "frequency": "Fréquence",
                "variable": "Variable",
                "group": "Groupe",
                "count": "Nombre",
                "value": "Valeur",
                "correlation": "Corrélation",
                "distribution": "Distribution de {}",
                "comparison": "{} par {}",
                "save_failed": "Échec de l'enregistrement de la visualisation",
                "normal_curve": "Courbe de Distribution Normale",
                "trend_line": "Ligne de Tendance"
            }
        }
    
    def _get_text(self, key, default=""):
        """Get translated text for the current language."""
        return self.translations.get(self.language, {}).get(key, default)
    
    def _apply_standard_layout(self, fig, title, xaxis_title=None, yaxis_title=None):
        """Apply standard layout settings to a figure."""
        # Set title
        fig.update_layout(
            title={
                "text": title,
                "font": {"size": 18, "family": "Arial", "color": "#333333"},
                "x": 0.5,  # Center title
                "xanchor": "center"
            },
            # Set standard font family for all text
            font={"family": "Arial", "size": 12, "color": "#333333"},
            # Set background color and margins
            paper_bgcolor="white",
            plot_bgcolor="#F8F9FA",
            margin={"t": 80, "b": 80, "l": 80, "r": 80},
            # Enable responsive sizing
            autosize=True
        )
        
        # Set axis titles if provided
        if xaxis_title:
            fig.update_xaxes(
                title_text=xaxis_title,
                title_font={"size": 14, "family": "Arial"},
                gridcolor="#DCDCDC",
                showline=True,
                linecolor="#333333",
                linewidth=1
            )
        
        if yaxis_title:
            fig.update_yaxes(
                title_text=yaxis_title,
                title_font={"size": 14, "family": "Arial"},
                gridcolor="#DCDCDC",
                showline=True,
                linecolor="#333333",
                linewidth=1
            )
        
        # Add subtle grid lines
        fig.update_layout(
            xaxis={"showgrid": True, "gridwidth": 1, "gridcolor": "#DCDCDC"},
            yaxis={"showgrid": True, "gridwidth": 1, "gridcolor": "#DCDCDC"}
        )
        
        # Improve legend
        fig.update_layout(
            legend={
                "orientation": "h",
                "yanchor": "bottom",
                "y": -0.2,
                "xanchor": "center",
                "x": 0.5,
                "font": {"size": 12, "family": "Arial"}
            }
        )
        
        return fig
    
    def create_bar_chart(self, data, x, y, color=None, title=None, xaxis_title=None, yaxis_title=None, 
                         error_y=None, barmode="group", color_scheme="categorical"):
        """
        Create a publication-quality bar chart.
        
        Args:
            data (pd.DataFrame): DataFrame containing the data
            x (str): Column name for x-axis
            y (str): Column name for y-axis
            color (str, optional): Column name for color grouping
            title (str, optional): Chart title
            xaxis_title (str, optional): X-axis title
            yaxis_title (str, optional): Y-axis title
            error_y (str, optional): Column name for error bars
            barmode (str, optional): Bar mode ("group" or "stack")
            color_scheme (str, optional): Color scheme to use
            
        Returns:
            plotly.graph_objects.Figure: Bar chart
        """
        # Set default titles if not provided
        if title is None:
            title = self._get_text("comparison").format(y, x)
        if xaxis_title is None:
            xaxis_title = self._get_text("group")
        if yaxis_title is None:
            yaxis_title = self._get_text("value")
        
        # Create bar chart
        fig = px.bar(
            data,
            x=x,
            y=y,
            color=color,
            barmode=barmode,
            color_discrete_sequence=COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["categorical"]),
            title=title,
            error_y=error_y,
            labels={
                x: xaxis_title,
                y: yaxis_title,
                color: self._get_text("group") if color else None
            }
        )
        
        # Apply standard layout
        fig = self._apply_standard_layout(fig, title, xaxis_title, yaxis_title)
        
        # Adjust for readability
        if len(data[x].unique()) > 5:
            fig.update_layout(xaxis_tickangle=-45)
        
        # Add value labels on bars
        fig.update_traces(texttemplate='%{y:.2f}', textposition='outside')
        
        return fig
    
    def create_box_plot(self, data, x, y, color=None, title=None, xaxis_title=None, yaxis_title=None, 
                       points="outliers", notched=False, color_scheme="categorical"):
        """
        Create a publication-quality box plot.
        
        Args:
            data (pd.DataFrame): DataFrame containing the data
            x (str): Column name for x-axis (groups)
            y (str): Column name for y-axis (values)
            color (str, optional): Column name for color grouping
            title (str, optional): Chart title
            xaxis_title (str, optional): X-axis title
            yaxis_title (str, optional): Y-axis title
            points (str, optional): How to show points ("all", "outliers", "suspectedoutliers", False)
            notched (bool, optional): Whether to show notched box plots
            color_scheme (str, optional): Color scheme to use
            
        Returns:
            plotly.graph_objects.Figure: Box plot
        """
        # Set default titles if not provided
        if title is None:
            title = self._get_text("distribution").format(y)
        if xaxis_title is None:
            xaxis_title = self._get_text("group")
        if yaxis_title is None:
            yaxis_title = self._get_text("score")
        
        # Create box plot
        fig = px.box(
            data,
            x=x,
            y=y,
            color=color,
            notched=notched,
            points=points,
            color_discrete_sequence=COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["categorical"]),
            title=title,
            labels={
                x: xaxis_title,
                y: yaxis_title,
                color: self._get_text("group") if color else None
            }
        )
        
        # Apply standard layout
        fig = self._apply_standard_layout(fig, title, xaxis_title, yaxis_title)
        
        # Add mean markers
        if x and y:
            # Calculate means for each group
            means = data.groupby(x)[y].mean().reset_index()
            
            # Add mean markers
            fig.add_trace(go.Scatter(
                x=means[x],
                y=means[y],
                mode='markers',
                marker=dict(
                    symbol='diamond',
                    size=10,
                    color='black',
                    line=dict(color='white', width=1)
                ),
                name=self._get_text("mean")
            ))
        
        return fig
    
    def create_histogram(self, data, x, title=None, xaxis_title=None, yaxis_title=None, bins=None, 
                        show_normal=True, show_kde=False, color_scheme="sequential_blue"):
        """
        Create a publication-quality histogram, optionally with normal curve overlay.
        
        Args:
            data (pd.DataFrame or pd.Series): DataFrame or Series containing the data
            x (str or pd.Series): Column name or pandas Series
            title (str, optional): Chart title
            xaxis_title (str, optional): X-axis title
            yaxis_title (str, optional): Y-axis title
            bins (int, optional): Number of bins
            show_normal (bool, optional): Whether to show a normal distribution curve
            show_kde (bool, optional): Whether to show a kernel density estimate
            color_scheme (str, optional): Color scheme to use
            
        Returns:
            plotly.graph_objects.Figure: Histogram
        """
        # Handle both DataFrame column and Series inputs
        if isinstance(data, pd.DataFrame) and isinstance(x, str):
            series = data[x]
            var_name = x
        elif isinstance(x, pd.Series):
            series = x
            var_name = x.name if x.name else "Value"
        else:
            series = pd.Series(x)
            var_name = "Value"
        
        # Detect NaN values and handle them
        series = series.dropna()
        if len(series) == 0:
            # Create empty figure with a note if no data
            fig = go.Figure()
            fig.add_annotation(
                text="No data available for histogram",
                xref="paper", yref="paper",
                x=0.5, y=0.5,
                showarrow=False,
                font=dict(size=14)
            )
            return fig
        
        # Set default titles if not provided
        if title is None:
            title = self._get_text("distribution").format(var_name)
        if xaxis_title is None:
            xaxis_title = var_name
        if yaxis_title is None:
            yaxis_title = self._get_text("frequency")
        
        # Calculate optimal number of bins if not specified
        if bins is None:
            bins = min(max(int(np.sqrt(len(series))), 5), 50)  # Between 5 and 50 bins
        
        # Create histogram
        fig = px.histogram(
            series,
            nbins=bins,
            opacity=0.8,
            color_discrete_sequence=[COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["sequential_blue"])[2]],
            title=title,
            labels={"value": xaxis_title, "count": yaxis_title}
        )
        
        # Apply standard layout
        fig = self._apply_standard_layout(fig, title, xaxis_title, yaxis_title)
        
        # Add normal distribution curve if requested
        if show_normal and len(series) > 2:
            mean = series.mean()
            std = series.std()
            
            # Create x values for the normal distribution curve
            x_min = series.min()
            x_max = series.max()
            x_range = x_max - x_min
            x_normal = np.linspace(x_min - 0.1 * x_range, x_max + 0.1 * x_range, 100)
            
            # Calculate normal distribution values
            y_normal = stats.norm.pdf(x_normal, mean, std)
            
            # Scale to match histogram height
            hist_values, _ = np.histogram(series, bins=bins)
            scaling_factor = max(hist_values) / max(y_normal) if max(y_normal) > 0 else 1
            y_normal = y_normal * scaling_factor
            
            # Add normal curve
            fig.add_trace(go.Scatter(
                x=x_normal,
                y=y_normal,
                mode='lines',
                line=dict(color='red', width=2, dash='dash'),
                name=self._get_text("normal_curve")
            ))
        
        # Add KDE if requested
        if show_kde and len(series) > 2:
            kde_x = np.linspace(series.min(), series.max(), 100)
            kde = stats.gaussian_kde(series)
            kde_y = kde(kde_x)
            
            # Scale to match histogram height
            hist_values, _ = np.histogram(series, bins=bins)
            scaling_factor = max(hist_values) / max(kde_y) if max(kde_y) > 0 else 1
            kde_y = kde_y * scaling_factor
            
            # Add KDE curve
            fig.add_trace(go.Scatter(
                x=kde_x,
                y=kde_y,
                mode='lines',
                line=dict(color='blue', width=2),
                name='KDE'
            ))
        
        return fig
    
    def create_correlation_heatmap(self, data, columns=None, title=None, 
                                  colorscale="RdBu_r", zmin=-1, zmax=1, text_auto=True):
        """
        Create a publication-quality correlation heatmap.
        
        Args:
            data (pd.DataFrame): DataFrame containing the data
            columns (list, optional): List of columns to include in correlation
            title (str, optional): Chart title
            colorscale (str, optional): Colorscale to use
            zmin (float, optional): Minimum value for color scale
            zmax (float, optional): Maximum value for color scale
            text_auto (bool, optional): Whether to show text values automatically
            
        Returns:
            plotly.graph_objects.Figure: Correlation heatmap
        """
        # Filter columns if specified
        if columns is not None:
            df = data[columns].copy()
        else:
            df = data.copy()
        
        # Calculate correlation matrix
        corr_matrix = df.corr().round(2)
        
        # Set default title if not provided
        if title is None:
            title = self._get_text("correlation")
        
        # Create heatmap using figure_factory for annotated heatmap
        fig = ff.create_annotated_heatmap(
            z=corr_matrix.values,
            x=list(corr_matrix.columns),
            y=list(corr_matrix.index),
            annotation_text=corr_matrix.values.round(2) if text_auto else None,
            colorscale=colorscale,
            showscale=True,
            zmin=zmin,
            zmax=zmax
        )
        
        # Update layout for better appearance
        fig.update_layout(
            title={
                "text": title,
                "font": {"size": 18, "family": "Arial", "color": "#333333"},
                "x": 0.5
            },
            autosize=True,
            height=600,
            xaxis={"side": "bottom"}
        )
        
        # Improve font and annotations
        fig.update_annotations(font={"size": 10, "family": "Arial", "color": "black"})
        
        # Add color bar title
        fig.update_layout(
            coloraxis_colorbar={
                "title": self._get_text("correlation"),
                "titlefont": {"size": 12, "family": "Arial"}
            }
        )
        
        return fig
    
    def create_scatter_plot(self, data, x, y, color=None, size=None, title=None, xaxis_title=None, 
                           yaxis_title=None, add_trendline=True, color_scheme="categorical"):
        """
        Create a publication-quality scatter plot with optional trend line.
        
        Args:
            data (pd.DataFrame): DataFrame containing the data
            x (str): Column name for x-axis
            y (str): Column name for y-axis
            color (str, optional): Column name for color grouping
            size (str, optional): Column name for point size
            title (str, optional): Chart title
            xaxis_title (str, optional): X-axis title
            yaxis_title (str, optional): Y-axis title
            add_trendline (bool, optional): Whether to add a trend line
            color_scheme (str, optional): Color scheme to use
            
        Returns:
            plotly.graph_objects.Figure: Scatter plot
        """
        # Set default titles if not provided
        if title is None:
            title = f"{y} vs {x}"
        if xaxis_title is None:
            xaxis_title = x
        if yaxis_title is None:
            yaxis_title = y
        
        # Create scatter plot
        fig = px.scatter(
            data,
            x=x,
            y=y,
            color=color,
            size=size,
            color_discrete_sequence=COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["categorical"]),
            title=title,
            labels={
                x: xaxis_title,
                y: yaxis_title,
                color: self._get_text("group") if color else None,
                size: self._get_text("value") if size else None
            },
            trendline="ols" if add_trendline and not color else None
        )
        
        # If we have color groups and want a trendline, we need to add trendlines separately for each group
        if add_trendline and color:
            for i, group in enumerate(data[color].unique()):
                group_data = data[data[color] == group]
                
                # Skip if too few points
                if len(group_data) < 2:
                    continue
                
                # Fit OLS model
                x_values = group_data[x]
                y_values = group_data[y]
                
                # Skip if data contains NaN
                if x_values.isna().any() or y_values.isna().any():
                    continue
                
                # Create numpy arrays for trendline
                x_array = np.array(x_values)
                y_array = np.array(y_values)
                
                try:
                    # Fit OLS line
                    slope, intercept, r_value, p_value, std_err = stats.linregress(x_array, y_array)
                    x_range = np.linspace(x_array.min(), x_array.max(), 100)
                    y_range = intercept + slope * x_range
                    
                    # Add trendline
                    current_color = COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["categorical"])[i % len(COLOR_SCHEMES.get(color_scheme, COLOR_SCHEMES["categorical"]))]
                    fig.add_trace(go.Scatter(
                        x=x_range,
                        y=y_range,
                        mode='lines',
                        line=dict(color=current_color, width=2, dash='dash'),
                        name=f"{group} {self._get_text('trend_line')}"
                    ))
                except:
                    # Skip if regression fails
                    continue
        
        # Apply standard layout
        fig = self._apply_standard_layout(fig, title, xaxis_title, yaxis_title)
        
        return fig
    
    def save_figure(self, fig, filename, format="png", width=800, height=600, scale=2):
        """
        Save a figure to disk in specified format.
        
        Args:
            fig (plotly.graph_objects.Figure): Figure to save
            filename (str): Output filename
            format (str, optional): Output format (png, jpg, svg, pdf)
            width (int, optional): Image width in pixels
            height (int, optional): Image height in pixels
            scale (int, optional): Scale factor for resolution
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Create directory if it doesn't exist
            directory = os.path.dirname(filename)
            if directory and not os.path.exists(directory):
                os.makedirs(directory)
            
            # Save figure
            fig.write_image(filename, format=format, width=width, height=height, scale=scale)
            return True
        except Exception as e:
            print(f"{self._get_text('save_failed')}: {str(e)}")
            return False
    
    def fig_to_bytes(self, fig, format="png", width=800, height=600, scale=2):
        """
        Convert a figure to bytes for embedding in documents.
        
        Args:
            fig (plotly.graph_objects.Figure): Figure to convert
            format (str, optional): Output format (png, jpg, svg, pdf)
            width (int, optional): Image width in pixels
            height (int, optional): Image height in pixels
            scale (int, optional): Scale factor for resolution
            
        Returns:
            bytes: Image bytes if successful, None otherwise
        """
        try:
            return fig.to_image(format=format, width=width, height=height, scale=scale)
        except Exception as e:
            print(f"{self._get_text('save_failed')}: {str(e)}")
            return None


# Example usage:
# 
# # Create visualization utilities
# viz = VisualizationUtilities(language="en")
# 
# # Create and display a bar chart
# df = pd.DataFrame({
#     "Group": ["A", "B", "C", "A", "B", "C"],
#     "Category": ["X", "X", "X", "Y", "Y", "Y"],
#     "Value": [10, 15, 13, 12, 18, 16]
# })
# 
# fig = viz.create_bar_chart(
#     data=df,
#     x="Group",
#     y="Value",
#     color="Category",
#     title="Value by Group and Category"
# )
# 
# # Display in Streamlit
# st.plotly_chart(fig, use_container_width=True)
# 
# # Save the figure
# viz.save_figure(fig, "bar_chart.png")