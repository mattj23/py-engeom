import numpy

try:
    from matplotlib.pyplot import Axes, Circle
except ImportError:
    pass
else:

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




