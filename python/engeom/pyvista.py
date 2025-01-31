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

    def mesh_polydata(mesh: Mesh) -> pyvista.PolyData:
        """
        Creates a PyVista PolyData object from a Mesh object.
        :param mesh: a Mesh object
        :return: a PyVista PolyData object
        """

        if pyvista is None:
            raise ImportError("PyVista is not installed.")

        vertices = mesh.clone_vertices()
        faces = mesh.clone_triangles()
        faces = numpy.hstack((numpy.ones((faces.shape[0], 1), dtype=faces.dtype) * 3, faces))
        return pyvista.PolyData(vertices, faces)


    def add_curves_to_plotter(
            plotter: pyvista.Plotter,
            curves: List[Curve3],
            color: ColorLike = 'w',
            width: float = 5.0,
            label: str | None = None,
            name: str | None = None,
    ) -> List[pyvista.vtkActor]:
        """
        Adds curves to a PyVista plotter.
        :param plotter:
        :param curves:
        :param color:
        :param width:
        :param label:
        :param name:
        :return:
        """

        if pyvista is None:
            raise ImportError("PyVista is not installed.")

        result_list = []
        for curve in curves:
            v = curve.clone_vertices()
            added = plotter.add_lines(v, connected=True, color=color, width=width, label=label, name=name)
            result_list.append(added)

        return result_list
