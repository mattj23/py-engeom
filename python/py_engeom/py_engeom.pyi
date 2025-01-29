from __future__ import annotations
from typing import Any, List, Tuple, Union
from enum import Enum

import numpy


class DeviationMode(Enum):
    Absolute = 0
    Normal = 1


class Iso3:
    """ An isometry (rigid body transformation) in 3D space. """

    def __init__(self, matrix: numpy.ndarray[float]):
        """ Create an isometry from a 4x4 matrix. """
        ...

    @staticmethod
    def identity() -> Iso3:
        """ Return the identity isometry. """
        ...

    @staticmethod
    def from_translation(x: float, y: float, z: float) -> Iso3:
        """ Create an isometry representing a translation. """
        ...

    @staticmethod
    def from_rotation(angle: float, a: float, b: float, c: float) -> Iso3:
        """
        Create an isometry representing a rotation around an axis. The axis will be normalized before the rotation is
        applied.
        :param angle: the angle to rotate by in radians.
        :param a: the x component of the rotation axis.
        :param b: the y component of the rotation axis.
        :param c: the z component of the rotation axis.
        :return: the isometry representing the rotation.
        """
        ...

    def __matmul__(self, other) -> Iso3:
        """ Multiply two isometries together. """
        ...

    def inverse(self) -> Iso3:
        """ Return the inverse of the isometry. """
        ...

    def transform_points(self, points: numpy.ndarray[float]) -> numpy.ndarray[float]:
        """ Transform a set of points by the isometry. This will transform the points by the rotation and translation
        of the isometry.

        :param points: a numpy array of shape (n, 3) containing the points to transform.
        :return: a numpy array of shape (n, 3) containing the transformed points.
        """
        ...

    def transform_vectors(self, vector: numpy.ndarray[float]) -> numpy.ndarray[float]:
        """ Transform a set of vectors by the isometry. This will only transform the direction of the vectors, not
        their magnitude.

        :param vector: a numpy array of shape (n, 3) containing the vectors to transform.
        :return: a numpy array of shape (n, 3) containing the transformed vectors.
        """
        ...

    def clone_matrix(self) -> numpy.ndarray[float]:
        """ Return a copy of the 4x4 matrix representation of the isometry. This is a copy operation. """
        ...


class Plane:
    def __init__(self, a: float, b: float, c: float, d: float):
        ...


class Mesh:
    """
    A class holding an unstructured, 3-dimensional mesh of triangles.
    """

    def __init__(
            self,
            vertices: numpy.ndarray[float],
            triangles: numpy.ndarray[numpy.uint32],
    ):
        """
        Create an engeom mesh from vertices and triangles.  The vertices should be a numpy array of shape (n, 3), while
        the triangles should be a numpy array of shape (m, 3) containing the indices of the vertices that make up each
        triangle. The triangles should be specified in counter-clockwise order when looking at the triangle from the
        front/outside.

        :param vertices: a numpy array of shape (n, 3) containing the vertices of the mesh.
        :param triangles: a numpy array of shape (m, 3) containing the triangles of the mesh, should be uint.
        """
        ...

    @staticmethod
    def load_stl(file_path: str) -> Mesh:
        """
        Load a mesh from an STL file. This will return a new mesh object containing the vertices and triangles from the
        file.

        :param file_path: the path to the STL file to load.
        :return: the mesh object containing the data from the file.
        """
        ...

    def write_stl(self, file_path: str):
        """
        Write the mesh to an STL file. This will write the vertices and triangles of the mesh to the file in binary
        format.

        :param file_path: the path to the STL file to write.
        """
        ...

    def clone(self) -> Mesh:
        """
        Will return a copy of the mesh. This is a copy of the data, so modifying the returned mesh will not modify the
        original mesh.

        :return:
        """

    def append(self, other: Mesh):
        """
        Append another mesh to this mesh. This will add the vertices and triangles from the other mesh to this mesh,
        changing this one and leaving the other one unmodified.

        :param other: the mesh to append to this mesh, will not be modified in this operation
        """
        ...

    def clone_vertices(self) -> numpy.ndarray[float]:
        """
        Will return a copy of the vertices of the mesh as a numpy array. If the mesh has not been modified, this will
        be the same as the original vertices. This is a copy of the data, so modifying the returned array will not
        modify the mesh.
        :return:
        """
        ...

    def clone_triangles(self) -> numpy.ndarray[numpy.uint32]:
        """
        Will return a copy of the triangles of the mesh as a numpy array. If the mesh has not been modified, this will
        be the same as the original triangles. This is a copy of the data, so modifying the returned array will not
        modify the mesh.

        :return:
        """
        ...

    def split(self, plane: Plane) -> Tuple[Mesh | None, Mesh | None]:
        """
        Split the mesh by a plane. The plane will divide the mesh into two possible parts and return them as two new
        objects.  If the part lies entirely on one side of the plane, the other part will be None.
        :param plane: the plane to split the mesh by.
        :return: a tuple of two optional meshes, the first being that on the negative side of the plane, the second being
        that on the positive side of the plane.
        """
        ...

    def deviation(self, points: numpy.ndarray[float], mode: DeviationMode) -> numpy.ndarray[float]:
        """
        Calculate the deviation between a set of points and their respective closest points on the mesh surface. The
        deviation can be calculated in two modes: absolute and normal. In the absolute mode, the deviation is the
        linear distance between the point and the closest point on the mesh. In the normal mode, the deviation is the
        distance along the normal of the closest point on the mesh.  In both cases, the deviation will be positive if
        the point is outside the surface and negative if the point is inside the surface.

        :param points: a numpy array of shape (n, 3) containing the points to calculate the deviation for.
        :param mode: the mode to calculate the deviation in.
        :return: a numpy array of shape (n,) containing the deviation for each point.
        """
        ...
