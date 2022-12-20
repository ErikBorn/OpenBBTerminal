from io import BytesIO
from pathlib import Path
from typing import List, Union

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import plotly.tools as tls
import requests
from PIL import Image
from plotly.subplots import make_subplots

from openbb_terminal.qt_app.config import openbb_styles as theme


# pylint: disable=R0913
class PlotlyFigureHelper:
    """Helper class for creating Plotly figures"""

    def __init__(self, fig: go.Figure, is_subplots: bool = False):
        self.fig = fig
        self.is_subplots = is_subplots
        self._set_theme()

    def _set_theme(self):
        """Set theme for the figure"""
        self.fig.update_layout(**theme.PLOTLY_THEME)

    def set_title(self, title: str, **kwargs):
        """Set the title of the figure"""
        self.fig.update_layout(title=title, **kwargs)

    @classmethod
    def create(
        cls,
        title: str = None,
        xaxis: dict = None,
        yaxis: dict = None,
        xaxis_title: str = None,
        yaxis_title: str = None,
        xaxis_range: List[Union[float, int]] = None,
        **kwargs,
    ):
        """Create a new Plotly figure"""
        fig = go.Figure()
        fig.update_layout(
            title=title,
            xaxis_title=xaxis_title,
            yaxis_title=yaxis_title,
            xaxis_range=xaxis_range,
            **kwargs,
        )
        if xaxis:
            fig.update_xaxes(xaxis)
        if yaxis:
            fig.update_yaxes(yaxis)

        return cls(fig)

    @classmethod
    def create_subplots(
        cls,
        rows: int = None,
        cols: int = None,
        shared_xaxes: bool = True,
        vertical_spacing: float = None,
        horizontal_spacing: float = None,
        subplot_titles: tuple = None,
        row_width: List[Union[float, int]] = None,
        specs: List[List[dict]] = None,
        **kwargs,
    ):
        """Create a new Plotly figure with subplots"""
        fig = make_subplots(
            rows=rows,
            cols=cols,
            shared_xaxes=shared_xaxes,
            vertical_spacing=vertical_spacing,
            horizontal_spacing=horizontal_spacing,
            subplot_titles=subplot_titles,
            row_width=row_width,
            specs=specs,
            **kwargs,
        )
        return cls(fig, is_subplots=True)

    def update_layout(
        self,
        **kwargs,
    ):
        """Update the layout of the figure"""
        self.fig.update_layout(**kwargs)

    def add_scatter(
        self,
        x: Union[List, np.ndarray],
        y: Union[List, np.ndarray],
        name: str,
        mode: str = "lines",
        row: int = None,
        col: int = None,
        secondary_y: bool = None,
        **kwargs,
    ):
        """Add a scatter trace to the figure"""
        self.fig.add_trace(
            go.Scatter(x=x, y=y, name=name, mode=mode, **kwargs),
            row=row,
            col=col,
            secondary_y=secondary_y,
        )

    def add_hline(
        self,
        y: Union[int, float],
        row: int = None,
        col: int = None,
        secondary_y: bool = None,
        **kwargs,
    ):
        """Add a horizontal line to the figure"""
        self.fig.add_hline(y=y, row=row, col=col, secondary_y=secondary_y, **kwargs)

    def add_vline(
        self,
        x: Union[int, float],
        row: int = None,
        col: int = None,
        secondary_y: bool = None,
        **kwargs,
    ):
        """Add a vertical line to the figure"""
        self.fig.add_vline(x=x, row=row, col=col, secondary_y=secondary_y, **kwargs)

    def add_annotation(
        self,
        x: Union[int, float],
        y: Union[int, float],
        text: str,
        row: int = None,
        col: int = None,
        secondary_y: bool = None,
        **kwargs,
    ):
        """Add an annotation to the figure"""
        self.fig.add_annotation(
            x=x, y=y, text=text, row=row, col=col, secondary_y=secondary_y, **kwargs
        )

    def add_bar(
        self,
        x: Union[List, np.ndarray],
        y: Union[List, np.ndarray],
        name: str,
        row: int = None,
        col: int = None,
        secondary_y: bool = None,
        **kwargs,
    ):
        """Add a bar trace to the figure"""
        self.fig.add_trace(
            go.Bar(x=x, y=y, name=name, **kwargs),
            row=row,
            col=col,
            secondary_y=secondary_y,
        )

    def add_candlestick(
        self,
        x: Union[List, np.ndarray],
        open_: Union[List, np.ndarray],
        high: Union[List, np.ndarray],
        low: Union[List, np.ndarray],
        close: Union[List, np.ndarray],
        name: str,
        row: int = None,
        col: int = None,
        secondary_y: bool = None,
        **kwargs,
    ):
        """Add a candlestick trace to the figure"""
        increasing_dict = (
            kwargs.pop("increasing", None) or theme.PLT_CANDLESTICKS["increasing"]
        )
        decreasing_dict = (
            kwargs.pop("decreasing", None) or theme.PLT_CANDLESTICKS["decreasing"]
        )

        self.fig.add_trace(
            go.Candlestick(
                x=x,
                open=open_,
                high=high,
                low=low,
                close=close,
                name=name,
                increasing=increasing_dict,
                decreasing=decreasing_dict,
                **kwargs,
            ),
            row=row,
            col=col,
            secondary_y=secondary_y,
        )

    def add_volume(
        self,
        x: Union[List, np.ndarray],
        y: Union[List, np.ndarray],
        name: str,
        row: int = None,
        col: int = None,
        secondary_y: bool = None,
        **kwargs,
    ):
        """Add a volume trace to the figure"""
        self.fig.add_trace(
            go.Bar(x=x, y=y, name=name, **kwargs),
            row=row,
            col=col,
            secondary_y=secondary_y,
        )

    def add_text(
        self,
        x: Union[int, float],
        y: Union[int, float],
        text: str,
        xref: str = "x",
        yref: str = "y",
        **kwargs,
    ):
        """Add text to the figure"""
        if "showarrow" not in kwargs:
            kwargs["showarrow"] = False

        self.fig.add_annotation(
            dict(xref=xref, yref=yref, x=x, y=y, text=text, **kwargs)
        )

    def add_image(
        self,
        x: Union[int, float],
        y: Union[int, float],
        sizex: Union[int, float],
        sizey: Union[int, float],
        source: str,
        xref: str = "x",
        yref: str = "y",
        **kwargs,
    ):
        """Add an image to the plot"""
        if source.startswith("http"):
            image = Image.open(BytesIO(requests.get(source).content))
        else:
            image = Image.open(Path(source).resolve())

        self.fig.add_layout_image(
            dict(
                source=image,
                xref=xref,
                yref=yref,
                x=x,
                y=y,
                sizex=sizex,
                sizey=sizey,
                **kwargs,
            )
        )
        image.close()

    def add_table(self, header: List[str], cells: List[List], name: str, **kwargs):
        """Add a table to the figure"""
        self.fig.add_trace(
            go.Table(
                header=dict(values=header),
                cells=dict(values=cells),
                name=name,
                **kwargs,
            )
        )

    def add_mesh3d(
        self,
        name: str,
        x: Union[List, np.ndarray],
        y: Union[List, np.ndarray],
        z: Union[List, np.ndarray],
        i: Union[List, np.ndarray] = None,
        j: Union[List, np.ndarray] = None,
        k: Union[List, np.ndarray] = None,
        **kwargs,
    ):
        """Add a 3D mesh to the figure"""
        self.fig.add_trace(go.Mesh3d(x=x, y=y, z=z, i=i, j=j, k=k, name=name, **kwargs))

    @classmethod
    def convert_to_plotly(cls, fig: plt.Figure):
        """Converts a matplotlib figure to a plotly figure"""
        plotly_dict = tls.mpl_to_plotly(fig)

        plotly_dict["layout"]["showlegend"] = True
        fig = go.Figure(plotly_dict)

        return cls(fig)

    def show(self, **kwargs):
        """Show the figure"""
        self.fig.show(**kwargs)

    def json(self, **kwargs):
        """Return the figure as a JSON string"""
        return self.fig.to_json(**kwargs)