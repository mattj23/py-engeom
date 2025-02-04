from typing import List, Iterable

import matplotlib.lines
import numpy
from .geom2 import Curve2, Circle2, Aabb2

try:
    from matplotlib.pyplot import Axes, Circle
    from matplotlib.colors import ListedColormap
except ImportError:
    pass
else:
    class GomColorMap(ListedColormap):
        def __init__(self):
            colors = numpy.array([
                [1, 0, 160],
                [1, 0, 255],
                [0, 254, 255],
                [0, 160, 0],
                [0, 254, 0],
                [255, 255, 0],
                [255, 128, 0],
                [255, 1, 0]
            ], dtype=numpy.float64)
            colors /= 256.0
            colors = numpy.hstack((colors, numpy.ones((len(colors), 1))))
            super().__init__(colors)
            self.set_under("magenta")
            self.set_over("darkred")

    GOM_CMAP = GomColorMap()

    def add_curve_plots(ax: Axes, *curves: Curve2, **kwargs) -> List[List[matplotlib.lines.Line2D]]:
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

    class ViewHelper:
        def __init__(self, ax: Axes):
            self.ax = ax

        def set_aspect_fill(self):
            set_aspect_fill(self.ax)

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
            points = curve.clone_points()
            self.ax.plot(points[:, 0], points[:, 1], **kwargs)