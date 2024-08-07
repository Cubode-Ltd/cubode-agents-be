from abc import ABC, abstractmethod
import json

#tool function
def run_check(is_possible):

    return is_possible

def create_bar_chart(hash, filename, title, subtitle, column_category, column_values, aggregation, xlabel, ylabel, colorspace, show_background):
    """Create a web component for a bar chart"""

    component = f"<cb-echart-barplot class='active' hash='{hash}' filename='{filename}' chart-title='{title}' chart-subtitle='{subtitle}' chart-x-axis-label='{xlabel}' chart-y-axis-label='{ylabel}' chart-show-background='{show_background}' series-column-category-0='{column_category}' series-column-values-0='{column_values}' series-aggregation-0='{aggregation}' series-colorspace-0='{colorspace}'></cb-echart-barplot>"

    return json.dumps({"response": component})

def create_line_chart(hash, filename, title, subtitle, column_category, column_values, aggregation, xlabel, ylabel, colorspace, show_zoom, line_color, line_type, line_style):
    """Create a web component for a line chart"""

    component = f"<cb-echart-lineplot class='active' hash='{hash}' filename='{filename}' chart-title='{title}' chart-subtitle='{subtitle}' chart-x-axis-label='{xlabel}' chart-y-axis-label='{ylabel}' chart-show-zoom='{show_zoom}' series-column-category-0='{column_category}' series-column-values-0='{column_values}' series-aggregation-0='{aggregation}' series-colorspace-marker-0='{colorspace}' series-color-line-0='{line_color}' series-line-type-0='{line_type}' series-line-style-0='{line_style}'></cb-echart-lineplot>"

    return json.dumps({"response": component})

def create_scatter_chart(hash, filename, title, subtitle, column_xaxis, column_yaxis, xlabel, ylabel, colorspace, show_zoom):
    """Create a web component for a scatter chart"""
    
    component = f"<cb-echart-scatterplot class='active' hash='{hash}' filename='{filename}' chart-title='{title}' chart-subtitle='{subtitle}' chart-x-axis-label='{xlabel}' chart-y-axis-label='{ylabel}' chart-show-zoom='{show_zoom}' series-column-x-axis-0='{column_xaxis}' series-column-y-axis-0='{column_yaxis}' series-colorspace-0='{colorspace}'></cb-echart-scatterplot>"

    return json.dumps({"response": component})

def create_pie_chart(hash, filename, title, subtitle, column_category, column_values, aggregation, pie_type, colorspace):
        """Create a web component for a pie chart"""

        component = f"<cb-echart-pieplot class='active' hash='{hash}' filename='{filename}' chart-title='{title}' chart-subtitle='{subtitle}' chart-pie-type='{pie_type}' series-column-category-0='{column_category}' series-column-values-0='{column_values}' series-aggregation-0='{aggregation}' series-colorspace-0='{colorspace}'></cb-echart-pieplot>"

        return json.dumps({"response": component})

# Tool classes & stragies
class ToolStrategy(ABC):
    @abstractmethod
    def execute(self, hash: str, filename: str, args: dict):
        pass

class ToolContext:
    def __init__(self, strategy: ToolStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ToolStrategy):
        self._strategy = strategy

    def execute_strategy(self, hash: str, filename: str, args: dict):
        return self._strategy.execute(hash, filename, args)

class BarChartTool(ToolStrategy):
    """Class to create a bar chart tool

    Args:
        ToolStrategy (ToolStrategy): _description_
    """
    def execute(self, hash: str, filename: str, args: dict):
        return create_bar_chart(
            hash=hash,
            filename=filename,
            title=args.get("title"),
            subtitle=args.get("subtitle"),
            column_category=args.get("column_category"),
            column_values=args.get("column_values"),
            aggregation=args.get("aggregation"),
            colorspace=args.get("colorspace"),
            xlabel=args.get("xlabel"),
            ylabel=args.get("ylabel"),
            show_background=args.get("show_background")
        )

class LineChartTool(ToolStrategy):
    """Class to create a line chart tool

    Args:
        ToolStrategy (ToolStrategy): _description_
    """

    def execute(self, hash: str, filename: str, args: dict):
        return create_line_chart(
            hash=hash,
            filename=filename,
            title=args.get("title"),
            subtitle=args.get("subtitle"),
            column_category=args.get("column_category"),
            column_values=args.get("column_values"),
            aggregation=args.get("aggregation"),
            colorspace=args.get("colorspace"),
            xlabel=args.get("xlabel"),
            ylabel=args.get("ylabel"),
            show_zoom=args.get("show_zoom"),
            line_color=args.get("line_color"),
            line_type=args.get("line_type"),
            line_style=args.get("line_style")
        )
    
class ScatterChartTool(ToolStrategy):
    """Class to create a scatter chart tool

    Args:
        ToolStrategy (ToolStrategy): _description_
    """

    def execute(self, hash: str, filename: str, args: dict):
        return create_scatter_chart(
            hash=hash,
            filename=filename,
            title=args.get("title"),
            subtitle=args.get("subtitle"),
            column_xaxis=args.get("column_xaxis"),
            column_yaxis=args.get("column_yaxis"),
            colorspace=args.get("colorspace"),
            xlabel=args.get("xlabel"),
            ylabel=args.get("ylabel"),
            show_zoom=args.get("show_zoom"),
        )

class PieChartTool(ToolStrategy):
    """Class to create a pie chart tool

    Args:
        ToolStrategy (ToolStrategy): _description_
    """

    def execute(self, hash: str, filename: str, args: dict):
        return create_pie_chart(
            hash=hash,
            filename=filename,
            title=args.get("title"),
            subtitle=args.get("subtitle"),
            column_category=args.get("column_category"),
            column_values=args.get("column_values"),
            aggregation=args.get("aggregation"),
            pie_type=args.get("pie_type"),
            colorspace=args.get("colorspace"),
        )