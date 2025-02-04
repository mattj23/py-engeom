"""
This module contains helper functions for working with PyVista.
"""

from __future__ import annotations

from typing import List

import numpy
from pyvista import ColorLike

from .geom3 import Mesh, Curve3

try:
    import pyvista
except ImportError:
    pass
else:

    class PlotterHelper:
        def __init__(self, plotter: pyvista.Plotter):
            self.plotter = plotter

        def add_curves(
            self,
            *curves: Curve3,
            color: ColorLike = "w",
            width: float = 5.0,
            label: str | None = None,
            name: str | None = None,
        ) -> List[pyvista.vtkActor]:
            """

            :param curves:
            :param color:
            :param width:
            :param label:
            :param name:
            :return:
            """
            result_list = []
            for curve in curves:
                added = self.plotter.add_lines(
                    curve.points,
                    connected=True,
                    color=color,
                    width=width,
                    label=label,
                    name=name,
                )
                result_list.append(added)

            return result_list

        def add_mesh(self, mesh: Mesh, **kwargs) -> pyvista.vtkActor:
            """

            :param mesh:
            :return:
            """
            prefix = numpy.ones((mesh.triangles.shape[0], 1), dtype=mesh.triangles.dtype)
            faces = numpy.hstack((prefix * 3, mesh.triangles))
            data = pyvista.PolyData(mesh.points, faces)
            return self.plotter.add_mesh(data, **kwargs)
