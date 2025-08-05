from fastmcp import FastMCP
from mcp.types import ImageContent
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import base64
import io
from typing import List, Dict, Any, Optional, Union
import json

mcp = FastMCP("Charting")

# Configure matplotlib for better appearance
plt.style.use('default')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['figure.dpi'] = 100

def _create_image_content() -> ImageContent:
    """Convert current matplotlib plot to ImageContent."""
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=150)
    buffer.seek(0)
    plot_data = buffer.getvalue()
    buffer.close()
    plt.close()  # Close the plot to free memory
    
    # Encode as base64 for the ImageContent data field
    encoded = base64.b64encode(plot_data).decode('utf-8')
    return ImageContent(
        type="image", 
        data=encoded, 
        mimeType="image/png"
    )

def _parse_data(data: Union[str, List, Dict]) -> pd.DataFrame:
    """Parse various data formats into a pandas DataFrame."""
    if isinstance(data, str):
        try:
            # Try to parse as JSON
            parsed_data = json.loads(data)
            if isinstance(parsed_data, list):
                return pd.DataFrame(parsed_data)
            elif isinstance(parsed_data, dict):
                return pd.DataFrame.from_dict(parsed_data, orient='index' if all(isinstance(v, (int, float)) for v in parsed_data.values()) else 'columns')
        except json.JSONDecodeError:
            # Try to parse as CSV
            try:
                return pd.read_csv(io.StringIO(data))
            except:
                raise ValueError("Could not parse string data as JSON or CSV")
    elif isinstance(data, list):
        return pd.DataFrame(data)
    elif isinstance(data, dict):
        return pd.DataFrame.from_dict(data, orient='index' if all(isinstance(v, (int, float)) for v in data.values()) else 'columns')
    else:
        raise ValueError("Data must be a string (JSON/CSV), list, or dictionary")

@mcp.tool()
async def create_bar_chart(
    data: Union[str, List, Dict],
    x_column: Optional[str] = None,
    y_column: Optional[str] = None,
    title: str = "Bar Chart",
    x_label: str = "Categories",
    y_label: str = "Values",
    color: str = "steelblue",
    horizontal: bool = False
) -> ImageContent:
    """Create a bar chart from the provided data.
    
    Args:
        data: Data in JSON string, list, or dictionary format
        x_column: Column name for x-axis (if data is DataFrame-like)
        y_column: Column name for y-axis (if data is DataFrame-like)
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label
        color: Bar color
        horizontal: Whether to create horizontal bars
        
    Returns:
        ImageContent with the chart as PNG image
    """
    try:
        df = _parse_data(data)
        
        # Handle different data structures
        if x_column and y_column and x_column in df.columns and y_column in df.columns:
            x_data = df[x_column]
            y_data = df[y_column]
        elif len(df.columns) >= 2:
            x_data = df.iloc[:, 0]
            y_data = df.iloc[:, 1]
        elif len(df.columns) == 1:
            y_data = df.iloc[:, 0]
            x_data = range(len(y_data))
        else:
            raise ValueError("Insufficient data for bar chart")
        
        fig, ax = plt.subplots()
        
        if horizontal:
            ax.barh(x_data, y_data, color=color)
            ax.set_xlabel(y_label)
            ax.set_ylabel(x_label)
        else:
            ax.bar(x_data, y_data, color=color)
            ax.set_xlabel(x_label)
            ax.set_ylabel(y_label)
        
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        
        # Rotate x-axis labels if they're text and not horizontal
        if not horizontal and hasattr(x_data, 'dtype') and x_data.dtype == 'object':
            plt.xticks(rotation=45, ha='right')
        
        plt.tight_layout()
        return _create_image_content()
        
    except Exception as e:
        plt.close()
        raise ValueError(f"Error creating bar chart: {str(e)}")

@mcp.tool()
async def create_line_chart(
    data: Union[str, List, Dict],
    x_column: Optional[str] = None,
    y_column: Optional[str] = None,
    title: str = "Line Chart",
    x_label: str = "X Values",
    y_label: str = "Y Values",
    color: str = "blue",
    line_style: str = "-",
    marker: str = "o"
) -> ImageContent:
    """Create a line chart from the provided data.
    
    Args:
        data: Data in JSON string, list, or dictionary format
        x_column: Column name for x-axis (if data is DataFrame-like)
        y_column: Column name for y-axis (if data is DataFrame-like)
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label
        color: Line color
        line_style: Line style ('-', '--', '-.', ':')
        marker: Marker style ('o', 's', '^', etc.)
        
    Returns:
        ImageContent with the chart as PNG image
    """
    try:
        df = _parse_data(data)
        
        # Handle different data structures
        if x_column and y_column and x_column in df.columns and y_column in df.columns:
            x_data = df[x_column]
            y_data = df[y_column]
        elif len(df.columns) >= 2:
            x_data = df.iloc[:, 0]
            y_data = df.iloc[:, 1]
        elif len(df.columns) == 1:
            y_data = df.iloc[:, 0]
            x_data = range(len(y_data))
        else:
            raise ValueError("Insufficient data for line chart")
        
        fig, ax = plt.subplots()
        ax.plot(x_data, y_data, color=color, linestyle=line_style, marker=marker, markersize=6)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return _create_image_content()
        
    except Exception as e:
        plt.close()
        raise ValueError(f"Error creating line chart: {str(e)}")

@mcp.tool()
async def create_histogram(
    data: Union[str, List, Dict],
    column: Optional[str] = None,
    bins: int = 30,
    title: str = "Histogram",
    x_label: str = "Values",
    y_label: str = "Frequency",
    color: str = "skyblue",
    alpha: float = 0.7
) -> ImageContent:
    """Create a histogram from the provided data.
    
    Args:
        data: Data in JSON string, list, or dictionary format
        column: Column name to plot (if data is DataFrame-like)
        bins: Number of bins for the histogram
        title: Chart title
        x_label: X-axis label
        y_label: Y-axis label
        color: Bar color
        alpha: Transparency level (0-1)
        
    Returns:
        ImageContent with the chart as PNG image
    """
    try:
        df = _parse_data(data)
        
        # Select data to plot
        if column and column in df.columns:
            plot_data = df[column]
        elif len(df.columns) >= 1:
            plot_data = df.iloc[:, 0]
        else:
            raise ValueError("No data available for histogram")
        
        # Remove NaN values
        plot_data = plot_data.dropna()
        
        fig, ax = plt.subplots()
        ax.hist(plot_data, bins=bins, color=color, alpha=alpha, edgecolor='black', linewidth=0.5)
        ax.set_xlabel(x_label)
        ax.set_ylabel(y_label)
        ax.set_title(title)
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        return _create_image_content()
        
    except Exception as e:
        plt.close()
        raise ValueError(f"Error creating histogram: {str(e)}")

@mcp.tool()
async def create_pie_chart(
    data: Union[str, List, Dict],
    labels_column: Optional[str] = None,
    values_column: Optional[str] = None,
    title: str = "Pie Chart",
    colors: Optional[List[str]] = None,
    autopct: str = "%1.1f%%",
    startangle: int = 90
) -> ImageContent:
    """Create a pie chart from the provided data.
    
    Args:
        data: Data in JSON string, list, or dictionary format
        labels_column: Column name for labels (if data is DataFrame-like)
        values_column: Column name for values (if data is DataFrame-like)
        title: Chart title
        colors: List of colors for pie slices
        autopct: Format string for percentages
        startangle: Starting angle for the pie chart
        
    Returns:
        ImageContent with the chart as PNG image
    """
    try:
        df = _parse_data(data)
        
        # Handle different data structures
        if labels_column and values_column and labels_column in df.columns and values_column in df.columns:
            labels = df[labels_column]
            values = df[values_column]
        elif len(df.columns) >= 2:
            labels = df.iloc[:, 0]
            values = df.iloc[:, 1]
        elif len(df.columns) == 1 and df.index.name:
            labels = df.index
            values = df.iloc[:, 0]
        else:
            # If only values are provided, create generic labels
            values = df.iloc[:, 0] if len(df.columns) >= 1 else df.iloc[:, 0]
            labels = [f"Category {i+1}" for i in range(len(values))]
        
        # Remove zero or negative values
        mask = values > 0
        if isinstance(labels, pd.Series):
            labels = labels[mask]
        else:
            # For list-like labels, filter based on mask
            labels = [labels[i] for i in range(len(labels)) if mask.iloc[i]]
        values = values[mask]
        
        if len(values) == 0:
            raise ValueError("No positive values found for pie chart")
        
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(
            values, 
            labels=labels, 
            colors=colors,
            autopct=autopct,
            startangle=startangle,
            textprops={'fontsize': 10}
        )
        
        ax.set_title(title)
        
        plt.tight_layout()
        return _create_image_content()
        
    except Exception as e:
        plt.close()
        raise ValueError(f"Error creating pie chart: {str(e)}")

if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8001)

