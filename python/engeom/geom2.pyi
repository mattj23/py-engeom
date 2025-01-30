from __future__ import annotations
import numpy


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
