import pytest
import json
import base64
from fastmcp import FastMCP, Client
from mcp.types import ImageContent
from src.app import mcp
import pandas as pd
import io
from PIL import Image

# Configure pytest to use asyncio
pytest_plugins = ('pytest_asyncio',)


@pytest.fixture
def mcp_server():
    """Fixture that returns the existing mcp server from app.py"""
    return mcp


@pytest.fixture
def sample_data():
    """Fixture providing sample data for testing charts"""
    return {
        "simple_dict": {"A": 10, "B": 20, "C": 15, "D": 25},
        "list_of_dicts": [
            {"category": "A", "value": 10},
            {"category": "B", "value": 20},
            {"category": "C", "value": 15},
            {"category": "D", "value": 25}
        ],
        "json_string": '{"A": 10, "B": 20, "C": 15, "D": 25}',
        "csv_string": "category,value\nA,10\nB,20\nC,15\nD,25",
        "numeric_list": [1, 4, 2, 8, 5, 7, 3, 6],
        "pie_data": {"Product A": 30, "Product B": 25, "Product C": 20, "Product D": 25}
    }


def decode_base64_image(base64_string: str) -> Image.Image:
    """Helper function to decode base64 image string"""
    # Remove data URL prefix if present
    if base64_string.startswith("data:image/png;base64,"):
        base64_string = base64_string.split(",")[1]
    
    image_data = base64.b64decode(base64_string)
    return Image.open(io.BytesIO(image_data))


def validate_image_content(result) -> Image.Image:
    """Helper function to validate ImageContent result and return PIL Image"""
    # The result should be an ImageContent object
    result = result[0]
    assert isinstance(result, ImageContent)
    assert result.type == "image"
    assert result.mimeType == "image/png"
    assert result.data is not None
    
    # Decode and validate the image
    img = decode_base64_image(result.data)
    assert img.format == "PNG"
    return img


class TestBarChart:
    async def test_bar_chart_with_dict(self, mcp_server, sample_data):
        """Test bar chart creation with dictionary data"""
        async with Client(mcp_server) as client:
            result = await client.call_tool("create_bar_chart", {
                "data": sample_data["simple_dict"],
                "title": "Test Bar Chart",
                "x_label": "Categories",
                "y_label": "Values"
            })
            validate_image_content(result)

    async def test_bar_chart_with_json_string(self, mcp_server, sample_data):
        """Test bar chart creation with JSON string data"""
        async with Client(mcp_server) as client:
            result = await client.call_tool("create_bar_chart", {
                "data": sample_data["json_string"],
                "color": "red",
                "horizontal": False
            })
            
            validate_image_content(result)

    async def test_bar_chart_horizontal(self, mcp_server, sample_data):
        """Test horizontal bar chart creation"""
        async with Client(mcp_server) as client:
            result = await client.call_tool("create_bar_chart", {
                "data": sample_data["list_of_dicts"],
                "x_column": "category",
                "y_column": "value",
                "horizontal": True,
                "color": "green"
            })
            
            validate_image_content(result)

    async def test_bar_chart_with_csv_string(self, mcp_server, sample_data):
        """Test bar chart creation with CSV string data"""
        async with Client(mcp_server) as client:
            result = await client.call_tool("create_bar_chart", {
                "data": sample_data["csv_string"],
                "x_column": "category",
                "y_column": "value"
            })
            
            validate_image_content(result)


class TestLineChart:
    async def test_line_chart_with_dict(self, mcp_server, sample_data):
        """Test line chart creation with dictionary data"""
        async with Client(mcp_server) as client:
            result = await client.call_tool("create_line_chart", {
                "data": sample_data["simple_dict"],
                "title": "Test Line Chart",
                "color": "blue",
                "line_style": "-",
                "marker": "o"
            })
            
            validate_image_content(result)

    async def test_line_chart_with_list_of_dicts(self, mcp_server, sample_data):
        """Test line chart creation with list of dictionaries"""
        async with Client(mcp_server) as client:
            result = await client.call_tool("create_line_chart", {
                "data": sample_data["list_of_dicts"],
                "x_column": "category",
                "y_column": "value",
                "color": "red",
                "line_style": "--",
                "marker": "s"
            })
            
            validate_image_content(result)

    async def test_line_chart_styling_options(self, mcp_server, sample_data):
        """Test line chart with different styling options"""
        async with Client(mcp_server) as client:
            result = await client.call_tool("create_line_chart", {
                "data": sample_data["numeric_list"],
                "title": "Styled Line Chart",
                "x_label": "Index",
                "y_label": "Value",
                "color": "purple",
                "line_style": "-.",
                "marker": "^"
            })
            
            validate_image_content(result)


class TestHistogram:
    async def test_histogram_with_numeric_list(self, mcp_server, sample_data):
        """Test histogram creation with numeric list"""
        async with Client(mcp_server) as client:
            result = await client.call_tool("create_histogram", {
                "data": sample_data["numeric_list"],
                "bins": 5,
                "title": "Test Histogram",
                "color": "skyblue",
                "alpha": 0.7
            })
            
            validate_image_content(result)

    async def test_histogram_with_dataframe_column(self, mcp_server, sample_data):
        """Test histogram creation specifying a column"""
        async with Client(mcp_server) as client:
            result = await client.call_tool("create_histogram", {
                "data": sample_data["list_of_dicts"],
                "column": "value",
                "bins": 10,
                "color": "orange",
                "alpha": 0.8
            })
            
            validate_image_content(result)

    async def test_histogram_custom_bins(self, mcp_server, sample_data):
        """Test histogram with custom number of bins"""
        async with Client(mcp_server) as client:
            result = await client.call_tool("create_histogram", {
                "data": sample_data["numeric_list"],
                "bins": 3,
                "title": "Custom Bins Histogram",
                "x_label": "Value Range",
                "y_label": "Count"
            })
            
            validate_image_content(result)


class TestPieChart:
    async def test_pie_chart_with_dict(self, mcp_server, sample_data):
        """Test pie chart creation with dictionary data"""
        async with Client(mcp_server) as client:
            result = await client.call_tool("create_pie_chart", {
                "data": sample_data["pie_data"],
                "title": "Test Pie Chart",
                "autopct": "%1.1f%%",
                "startangle": 90
            })
            
            validate_image_content(result)

    async def test_pie_chart_with_list_of_dicts(self, mcp_server, sample_data):
        """Test pie chart creation with list of dictionaries"""
        async with Client(mcp_server) as client:
            result = await client.call_tool("create_pie_chart", {
                "data": sample_data["list_of_dicts"],
                "labels_column": "category",
                "values_column": "value",
                "title": "Sales Distribution",
                "autopct": "%1.2f%%"
            })
            
            validate_image_content(result)

    async def test_pie_chart_with_colors(self, mcp_server, sample_data):
        """Test pie chart with custom colors"""
        colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"]
        async with Client(mcp_server) as client:
            result = await client.call_tool("create_pie_chart", {
                "data": sample_data["pie_data"],
                "title": "Colored Pie Chart",
                "colors": colors,
                "startangle": 45
            })
            
            validate_image_content(result)


class TestErrorHandling:
    async def test_bar_chart_invalid_data(self, mcp_server):
        """Test bar chart error handling with invalid data"""
        async with Client(mcp_server) as client:
            with pytest.raises(Exception):
                await client.call_tool("create_bar_chart", {
                    "data": None,
                    "title": "Should Fail"
                })

    async def test_line_chart_empty_data(self, mcp_server):
        """Test line chart error handling with empty data"""
        async with Client(mcp_server) as client:
            with pytest.raises(Exception):
                await client.call_tool("create_line_chart", {
                    "data": {},
                    "title": "Empty Data"
                })

    async def test_histogram_non_numeric_data(self, mcp_server):
        """Test histogram error handling with non-numeric data"""
        async with Client(mcp_server) as client:
            with pytest.raises(Exception):
                await client.call_tool("create_histogram", {
                    "data": {"A": "text", "B": "more text"},
                    "title": "Non-numeric Data"
                })

    async def test_pie_chart_negative_values(self, mcp_server):
        """Test pie chart with negative values (should filter them out)"""
        async with Client(mcp_server) as client:
            result = await client.call_tool("create_pie_chart", {
                "data": {"A": 10, "B": -5, "C": 15},
                "title": "Mixed Values"
            })
            
            # Should succeed by filtering out negative values
            validate_image_content(result)


class TestDataParsing:
    async def test_json_string_parsing(self, mcp_server):
        """Test parsing of JSON string data"""
        json_data = '{"x": [1, 2, 3, 4], "y": [10, 20, 15, 25]}'
        async with Client(mcp_server) as client:
            result = await client.call_tool("create_line_chart", {
                "data": json_data,
                "x_column": "x",
                "y_column": "y"
            })
            
            validate_image_content(result)

    async def test_csv_string_parsing(self, mcp_server):
        """Test parsing of CSV string data"""
        csv_data = "month,sales\nJan,100\nFeb,150\nMar,120\nApr,180"
        async with Client(mcp_server) as client:
            result = await client.call_tool("create_bar_chart", {
                "data": csv_data,
                "x_column": "month",
                "y_column": "sales",
                "title": "Monthly Sales"
            })
            
            validate_image_content(result)

    async def test_list_data_parsing(self, mcp_server):
        """Test parsing of list data"""
        list_data = [10, 20, 15, 25, 30]
        async with Client(mcp_server) as client:
            result = await client.call_tool("create_histogram", {
                "data": list_data,
                "bins": 5,
                "title": "List Data Histogram"
            })
            
            validate_image_content(result)


class TestChartCustomization:
    async def test_chart_titles_and_labels(self, mcp_server, sample_data):
        """Test chart customization with titles and labels"""
        async with Client(mcp_server) as client:
            result = await client.call_tool("create_bar_chart", {
                "data": sample_data["simple_dict"],
                "title": "Custom Title",
                "x_label": "Custom X Label",
                "y_label": "Custom Y Label"
            })
            
            validate_image_content(result)

    async def test_color_customization(self, mcp_server, sample_data):
        """Test color customization across different chart types"""
        colors_to_test = ["red", "green", "blue", "#FF5733", "purple"]
        
        for color in colors_to_test:
            async with Client(mcp_server) as client:
                result = await client.call_tool("create_bar_chart", {
                    "data": sample_data["simple_dict"],
                    "color": color,
                    "title": f"Chart with {color} color"
                })
                
                validate_image_content(result)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
