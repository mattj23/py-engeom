"""
    This module contains helper functions for working with PyVista.
"""
import numpy
from .geom3 import Mesh

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