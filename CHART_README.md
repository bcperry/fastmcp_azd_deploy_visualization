# FastMCP Data Visualization Server

A powerful MCP (Model Context Protocol) server that generates various types of charts and returns them as base64-encoded PNG images. Perfect for LLMs that need to create visualizations from data.

## Features

### Supported Chart Types
- **Bar Charts** (vertical and horizontal)
- **Line Charts** (for trends and time series)
- **Histograms** (for data distribution)
- **Pie Charts** (for proportional data)

### Key Capabilities
- **Flexible Data Input**: Accepts JSON strings, Python dictionaries, lists, and CSV strings
- **Base64 Output**: Returns charts as base64-encoded PNG images for easy transmission
- **Customization**: Extensive customization options for colors, labels, titles, and styling
- **Error Handling**: Robust validation and error messages
- **Memory Efficient**: Automatically cleans up matplotlib resources

## Installation

```bash
# Install dependencies using uv
uv sync

# Or install manually
pip install fastapi fastmcp matplotlib pandas numpy Pillow
```

## Usage

### Starting the Server

```bash
cd src
uv run python app.py
```

The server will start on `http://0.0.0.0:8000/mcp`

### Available MCP Tools

#### 1. `create_bar_chart`
Creates vertical or horizontal bar charts.

**Parameters:**
- `data`: Data in JSON string, list, or dictionary format
- `x_column`: Column name for x-axis (optional)
- `y_column`: Column name for y-axis (optional)
- `title`: Chart title (default: "Bar Chart")
- `x_label`: X-axis label (default: "Categories")
- `y_label`: Y-axis label (default: "Values")
- `color`: Bar color (default: "steelblue")
- `horizontal`: Create horizontal bars (default: false)

**Example:**
```json
{
  "data": "{\"categories\": [\"Q1\", \"Q2\", \"Q3\", \"Q4\"], \"sales\": [1000, 1500, 1200, 1800]}",
  "x_column": "categories",
  "y_column": "sales",
  "title": "Quarterly Sales",
  "color": "steelblue"
}
```

#### 2. `create_line_chart`
Creates line charts for trends and time series data.

**Parameters:**
- `data`: Data in JSON string, list, or dictionary format
- `x_column`: Column name for x-axis (optional)
- `y_column`: Column name for y-axis (optional)
- `title`: Chart title (default: "Line Chart")
- `x_label`: X-axis label (default: "X Values")
- `y_label`: Y-axis label (default: "Y Values")
- `color`: Line color (default: "blue")
- `line_style`: Line style - '-', '--', '-.', ':' (default: "-")
- `marker`: Marker style - 'o', 's', '^', etc. (default: "o")

**Example:**
```json
{
  "data": "{\"months\": [\"Jan\", \"Feb\", \"Mar\", \"Apr\"], \"temperature\": [32, 35, 45, 55]}",
  "x_column": "months",
  "y_column": "temperature",
  "title": "Monthly Temperature",
  "color": "red"
}
```

#### 3. `create_histogram`
Creates histograms for data distribution visualization.

**Parameters:**
- `data`: Data in JSON string, list, or dictionary format
- `column`: Column name to plot (optional)
- `bins`: Number of bins (default: 30)
- `title`: Chart title (default: "Histogram")
- `x_label`: X-axis label (default: "Values")
- `y_label`: Y-axis label (default: "Frequency")
- `color`: Bar color (default: "skyblue")
- `alpha`: Transparency level 0-1 (default: 0.7)

**Example:**
```json
{
  "data": "[1, 2, 2, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 5]",
  "bins": 10,
  "title": "Data Distribution",
  "color": "lightgreen"
}
```

#### 4. `create_pie_chart`
Creates pie charts for proportional data.

**Parameters:**
- `data`: Data in JSON string, list, or dictionary format
- `labels_column`: Column name for labels (optional)
- `values_column`: Column name for values (optional)
- `title`: Chart title (default: "Pie Chart")
- `colors`: List of colors for pie slices (optional)
- `autopct`: Format string for percentages (default: "%1.1f%%")
- `startangle`: Starting angle for the pie chart (default: 90)

**Example:**
```json
{
  "data": "{\"labels\": [\"Desktop\", \"Mobile\", \"Tablet\"], \"values\": [45, 30, 25]}",
  "labels_column": "labels",
  "values_column": "values",
  "title": "Device Usage"
}
```

## Data Input Formats

The server accepts data in multiple flexible formats:

### 1. JSON String
```json
"{\"x\": [1, 2, 3], \"y\": [10, 20, 30]}"
```

### 2. Python Dictionary
```python
{"categories": ["A", "B", "C"], "values": [10, 20, 30]}
```

### 3. Python List (for simple numerical data)
```python
[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
```

### 4. CSV String
```
"category,value\nA,10\nB,20\nC,30"
```

## Output Format

All charts are returned as base64-encoded PNG images with the format:
```
data:image/png;base64,<encoded_image_data>
```

This format can be:
- Directly embedded in HTML `<img>` tags
- Decoded and saved as PNG files
- Transmitted efficiently over MCP
- Displayed in various client applications

## Error Handling

The server provides comprehensive error handling:
- Data format validation
- Column existence checking
- Value type validation
- Matplotlib resource cleanup
- Descriptive error messages

## Testing

Run the test script to see usage examples:

```bash
uv run python test_charts.py
```

## Azure Deployment

This server is configured for Azure deployment using Azure Developer CLI (azd):
- Bicep infrastructure templates included
- Container app deployment ready
- Environment configuration included

```bash
azd up
```

## Architecture

- **FastMCP**: Provides the MCP server framework
- **Matplotlib**: Core plotting library with Agg backend for server use
- **Pandas**: Data manipulation and parsing
- **NumPy**: Numerical operations
- **Pillow**: Image processing support
- **Base64**: Image encoding for transmission

## License

This project is licensed under the MIT License.
