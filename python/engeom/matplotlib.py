from typing import List, Iterable, Tuple, Union

import matplotlib.lines
import numpy
from .geom2 import Curve2, Circle2, Aabb2, Point2, Vector2
from .metrology import Length2

PlotCoords = Union[Point2, Vector2, Iterable[float]]
_point = 1.0 / 72.0

try:
    from matplotlib.pyplot import Axes, Circle
    from matplotlib.colors import ListedColormap
except ImportError:
    pass
else:

    class GomColorMap(ListedColormap):
        def __init__(self):
            colors = numpy.array(
                [
                    [1, 0, 160],
                    [1, 0, 255],
                    [0, 254, 255],
                    [0, 160, 0],
                    [0, 254, 0],
                    [255, 255, 0],
                    [255, 128, 0],
                    [255, 1, 0],
                ],
                dtype=numpy.float64,
            )
            colors /= 256.0
            colors = numpy.hstack((colors, numpy.ones((len(colors), 1))))
            super().__init__(colors)
            self.set_under("magenta")
            self.set_over("darkred")


    GOM_CMAP = GomColorMap()


    def add_curve_plots(
            ax: Axes, *curves: Curve2, **kwargs
    ) -> List[List[matplotlib.lines.Line2D]]:
        """
        Plot a list of curves on a Matplotlib Axes object.
        :param ax: a Matplotlib Axes object
        :param curves: a list of Curve2 objects
        :param kwargs: keyword arguments to pass to the plot function
        :return: None
        """
        actors = []
        for curve in curves:
            points = curve.clone_points()
            a = ax.plot(points[:, 0], points[:, 1], **kwargs)
            actors.append(a)
        return actors


    def set_aspect_fill(ax: Axes):
        """
        Set the aspect ratio of a Matplotlib Axes (subplot) object to be 1:1 in x and y, while also having it expand
        to fill all available space.

        In comparison to the set_aspect('equal') method, this method will also expand the plot to prevent the overall
        figure from shrinking.  It does this by manually re-checking the x and y limits and adjusting whichever is the
        limiting value. Essentially, it will honor the larger of the two existing limits which were set before this
        function was called, and will only expand the limits on the other axis to fill the remaining space.

        Call this function after all visual elements have been added to the plot and any manual adjustments to the axis
        limits are performed. If you use fig.tight_layout(), call this function after that.
        :param ax: a Matplotlib Axes object
        :return: None
        """
        x0, x1 = ax.get_xlim()
        y0, y1 = ax.get_ylim()

        bbox = ax.get_window_extent()
        width, height = bbox.width, bbox.height

        x_scale = width / (x1 - x0)
        y_scale = height / (y1 - y0)

        if y_scale > x_scale:
            y_range = y_scale / x_scale * (y1 - y0)
            y_mid = (y0 + y1) / 2
            ax.set_ylim(y_mid - y_range / 2, y_mid + y_range / 2)
        else:
            x_range = x_scale / y_scale * (x1 - x0)
            x_mid = (x0 + x1) / 2
            ax.set_xlim(x_mid - x_range / 2, x_mid + x_range / 2)


    class AxesHelper:
        def __init__(self, ax: Axes, skip_aspect=False, hide_axes=False):
            self.ax = ax
            if not skip_aspect:
                ax.set_aspect("equal", adjustable="datalim")

            if hide_axes:
                ax.axis("off")

        def set_bounds(self, box: Aabb2):
            """
            Set the bounds of a Matplotlib Axes object.
            :param box: an Aabb2 object
            :return: None
            """
            self.ax.set_xlim(box.min.x, box.max.x)
            self.ax.set_ylim(box.min.y, box.max.y)

        def plot_circle(self, *circle: Circle2 | Iterable[float], **kwargs):
            """
            Plot a circle on a Matplotlib Axes object.
            :param circle: a Circle2 object
            :param kwargs: keyword arguments to pass to the plot function
            :return: None
            """
            from matplotlib.pyplot import Circle

            for cdata in circle:
                if isinstance(cdata, Circle2):
                    c = Circle((cdata.center.x, cdata.center.y), cdata.r, **kwargs)
                else:
                    x, y, r, *_ = cdata
                    c = Circle((x, y), r, **kwargs)
                self.ax.add_patch(c)

        def plot_curve(self, curve: Curve2, **kwargs):
            """
            Plot a curve on a Matplotlib Axes object.
            :param curve: a Curve2 object
            :param kwargs: keyword arguments to pass to the plot function
            :return: None
            """
            self.ax.plot(curve.points[:, 0], curve.points[:, 1], **kwargs)

        def plot_length(
                self,
                length: Length2,
                side_shift: float = 0,
                format: str = "{value:.3f}",
                fontsize: int = 10,
        ):
            """
            Plot a Length2 object on a Matplotlib Axes object.
            :param side_shift:
            :param length: a Length2 object
            :return: None
            """
            from matplotlib.pyplot import Line2D

            pad_scale = self._font_height(12) * 1.5
            center = length.center.shift_orthogonal(side_shift)
            leader_a = center.projection(length.a)
            leader_b = center.projection(length.b)

            self.arrow(leader_a - length.direction * pad_scale, leader_a)

            self.arrow(leader_b + length.direction * pad_scale, leader_b)

            result = self.annotate_text_only(
                format.format(value=length.value),
                leader_b + length.direction * pad_scale,
                bbox=dict(boxstyle="round,pad=0.3", ec="black", fc="white"),
                ha="center", va="center",
                fontsize=fontsize,
            )
            print(result)

        def annotate_text_only(self, text: str, pos: PlotCoords, **kwargs):
            """
            Annotate a Matplotlib Axes object with text only.
            :param text: the text to annotate
            :param pos: the position of the annotation
            :param kwargs: keyword arguments to pass to the annotate function
            :return: None
            """
            return self.ax.annotate(text, xy=_tuplefy(pos), **kwargs)

        def arrow(self, start: PlotCoords, end: PlotCoords):
            """
            Plot an arrow on a Matplotlib Axes object.
            :param start: the start point of the arrow
            :param end: the end point of the arrow
            :param kwargs: keyword arguments to pass to the arrow function
            :return: None
            """
            self.ax.annotate("", xy=_tuplefy(end), xytext=_tuplefy(start), arrowprops=dict(arrowstyle="-|>", fc="black"))

        def _font_height(self, font_size: int) -> float:
            """ Get the height of a font in data units. """
            fig_dpi = self.ax.figure.dpi
            font_height_inches = font_size * _point
            font_height_px = font_height_inches * fig_dpi

            px_per_data = self._get_scale()
            return font_height_px / px_per_data

        def _get_scale(self) -> float:
            """ Get the scale of the plot in data units per pixel. """
            x0, x1 = self.ax.get_xlim()
            y0, y1 = self.ax.get_ylim()

            bbox = self.ax.get_window_extent()
            width, height = bbox.width, bbox.height

            # Units are pixels per data unit
            x_scale = width / (x1 - x0)
            y_scale = height / (y1 - y0)

            return min(x_scale, y_scale)


    def _tuplefy(item: PlotCoords) -> Tuple[float, float]:
        if isinstance(item, (Point2, Vector2)):
            return item.x, item.y
        else:
            x, y, *_ = item
            return x, y
