from __future__ import annotations
import numpy
from typing import Iterable

type Transformable2 = Vector2 | Point2 | Iso2 | SurfacePoint2


class Vector2:
    def __init__(self, x: float, y: float):
        """

        :param x:
        :param y:
        """
        ...

    @property
    def x(self) -> float:
        ...

    @property
    def y(self) -> float:
        ...

    def __iter__(self) -> Iterable[float]:
        ...

    def __rmul__(self, other: float) -> Vector2:
        ...

    def __add__(self, other: Vector2 | Point2) -> Vector2 | Point2:
        ...

    def __sub__(self, other: Vector2) -> Vector2:
        ...

    def __neg__(self) -> Vector2:
        ...

    def __mul__(self, x: float) -> Vector2:
        ...

    def as_numpy(self) -> numpy.ndarray[float]:
        """
        Create a numpy array of shape (2,) from the vector.
        """
        ...

    def dot(self, other: Vector2) -> float:
        """
        Compute the dot product of two vectors.
        """
        ...

    def cross(self, other: Vector2) -> float:
        """
        Compute the cross product of two vectors.
        """
        ...

    def norm(self) -> float:
        """
        Compute the norm of the vector.
        """
        ...

    def normalized(self) -> Vector2:
        """
        Return a normalized version of the vector.
        """
        ...

    def angle_to(self, other: Vector2) -> float:
        """
        Compute the smallest angle between two vectors and return it in radians.
        """
        ...


class Point2:
    def __init__(self, x: float, y: float):
        """

        :param x:
        :param y:
        """
        ...

    @property
    def x(self) -> float:
        ...

    @property
    def y(self) -> float:
        ...

    def __iter__(self) -> Iterable[float]:
        ...

    @property
    def coords(self) -> Vector2:
        """
        Get the coordinates of the point as a Vector2 object.
        :return: a Vector2 object
        """
        ...

    def __sub__(self, other: Vector2 | Point2) -> Vector2 | Point2:
        ...

    def __add__(self, other: Vector2) -> Vector2:
        ...

    def as_numpy(self) -> numpy.ndarray[float]:
        """
        Create a numpy array of shape (2,) from the point.
        """
        ...


class SurfacePoint2:
    def __init__(self, x: float, y: float, nx: float, ny: float):
        """

        :param x:
        :param y:
        :param nx:
        :param ny:
        """
        ...

    @property
    def point(self) -> Point2:
        """
        Get the coordinates of the point as a Point2 object.
        :return: a Point2 object
        """
        ...

    @property
    def normal(self) -> Vector2:
        """
        Get the normal of the point as a Vector2 object.
        :return: a Vector2 object
        """
        ...

    def at_distance(self, distance: float) -> Point2:
        """
        Get the point at a distance along the normal from the surface point.
        :param distance: the distance to move along the normal.
        :return: the point at the distance along the normal.
        """
        ...

    def scalar_projection(self, point: Point2) -> float:
        """
        Calculate the scalar projection of a point onto the axis defined by the surface point position and direction.
        Positive values indicate that the point is in the normal direction from the surface point, while negative values
        indicate that the point is in the opposite direction.

        :param point: the point to calculate the projection of.
        :return: the scalar projection of the point onto the normal.
        """
        ...

    def projection(self, point: Point2) -> Point2:
        """
        Calculate the projection of a point onto the axis defined by the surface point position and direction.

        :param point: the point to calculate the projection of.
        :return: the projection of the point onto the plane.
        """
        ...

    def reversed(self) -> SurfacePoint2:
        """
        Return a new surface point with the normal vector inverted, but the position unchanged.
        :return: a new surface point with the inverted normal vector.
        """
        ...

    def planar_distance(self, point: Point2) -> float:
        """
        Calculate the planar (non-normal) distance between the surface point and a point. This is complementary to the
        scalar projection. A point is projected onto the plane defined by the position and normal of the surface point,
        and the distance between the surface point position and the projected point is returned.  The value will always
        be positive.

        :param point: the point to calculate the distance to.
        :return: the planar distance between the surface point and the point.
        """
        ...


class Iso2:
    def __init__(self, tx: float, ty: float, r: float):
        """

        :param tx:
        :param ty:
        :param r:
        """
        ...

    @staticmethod
    def identity() -> Iso2:
        """
        Create the identity isometry.
        """
        ...

    def __matmul__(self, other: Iso2 | Vector2 | Point2) -> Iso2 | Vector2 | Point2:
        ...

    def inverse(self) -> Iso2:
        """
        Get the inverse of the isometry.
        """
        ...

    def as_numpy(self) -> numpy.ndarray[float]:
        """
        Create a numpy array of shape (3, 3) from the isometry.
        """
        ...

    def transform_points(self, points: numpy.ndarray[float]) -> numpy.ndarray[float]:
        """
        Transform an array of points using the isometry.
        :param points: a numpy array of shape (N, 2)
        :return: a numpy array of shape (N, 2)
        """
        ...

    def transform_vectors(self, vectors: numpy.ndarray[float]) -> numpy.ndarray[float]:
        """
        Transform an array of vectors using the isometry. The translation part of the isometry is ignored.
        :param vectors:
        :return:
        """
        ...


class SvdBasis2:

    def __init__(self, points: numpy.ndarray[float], weights: numpy.ndarray[float] | None):
        """

        :param points:
        :param weights:
        """
        ...
