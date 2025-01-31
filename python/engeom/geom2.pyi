from __future__ import annotations
import numpy
from typing import Iterable, Tuple

from engeom.engeom import Resample

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

    def __init__(
            self,
            points: numpy.ndarray[float],
            weights: numpy.ndarray[float] | None = None
    ):
        """

        :param points:
        :param weights:
        """
        ...


class CurveStation2:
    """
    A class representing a station along a curve in 3D space. The station is represented by a point on the curve, a
    tangent (direction) vector, and a length along the curve.
    """

    @property
    def point(self) -> Point2:
        """ The 2d position in space on the curve. """
        ...

    @property
    def direction(self) -> Vector2:
        """ The tangent (direction) vector of the curve at the station. """
        ...

    @property
    def normal(self) -> Vector2:
        """ The normal vector of the curve at the station. """
        ...

    @property
    def direction_point(self) -> SurfacePoint2:
        """
        A `SurfacePoint2` object representing the point on the curve and the curve's tangent/direction vector.
        """
        ...

    @property
    def surface_point(self) -> SurfacePoint2:
        """
        A `SurfacePoint2` object representing the point on the curve and the curve's normal vector.
        """
        ...

    @property
    def index(self) -> int:
        """ The index of the previous vertex on the curve, at or before the station. """
        ...

    @property
    def length_along(self) -> float:
        """ The length along the curve from the start of the curve to the station. """
        ...


class Curve2:
    """
    A class representing a curve in 2D space. The curve is defined by a set of vertices and the line segments between
    them. In two dimensions, the curve also has the concepts of closed/open, surface direction, and hull.

    """

    def __init__(
            self,
            vertices: numpy.ndarray,
            normals: numpy.ndarray | None = None,
            tol: float | None = None,
            force_closed: bool = False,
            hull_ccw: bool = False,
    ):
        """
        Create a 2d curve from a set of vertices and some additional options.

        It's important to note that in 2d, a curve has a concept of a normal direction, built from the concept of
        inside/outside defined through the winding order of the vertices. This extra information can allow a 2d curve
        to model a manifold surface.

        There are three ways to specify the winding order of the vertices:
        1. Control it manually by passing the vertices array with the rows already organized so that an exterior surface
        is counter-clockwise.
        2. If the vertices represent an exterior shape, pass `hull_ccw=True` to have the constructor automatically
        check the winding order and reverse it if point ordering in the convex hull does not match ordering in the
        original array.
        3. Pass a `normals` array the same size as the `vertices` array, where the normals are non-zero vectors pointed
        in the "outside" direction at each point. The constructor will reverse the winding if the majority of normals
        do not point in the same direction as the winding.

        :param vertices: a numpy array of shape (N, 2) representing the vertices of the curve.
        :param normals: an optional numpy array of shape (N, 2) representing the normals of the curve associated with
        each vertex.
        :param tol: a tolerance value for the curve. If not provided, a default value of 1e-6 is used. This is the
        distance at which two points are considered to be the same.
        :param force_closed: If True, the curve will be closed even if the first and last points are not the same, which
        will be done by adding a new point at the end of the array that is the same as the first point.
        :param hull_ccw: If True, the constructor will check the winding order of the vertices and reverse it if the
        convex hull of the points is not in the same order as the original array. This will do nothing if the `normals`
        parameter is provided.
        """
        ...

    def length(self) -> float:
        """
        Get the length of the curve.
        :return: the length of the curve.
        """
        ...

    def at_front(self) -> CurveStation2:
        """
        Get the station at the front of the curve.
        :return: the station at the front of the curve.
        """
        ...

    def at_back(self) -> CurveStation2:
        """
        Get the station at the back of the curve.
        :return: the station at the back of the curve.
        """
        ...

    def at_length(self, length: float) -> CurveStation2:
        """
        Get the station at a given length along the curve. Will throw a ValueError if the length is less than zero or
        greater than the length of the curve.
        :param length: the length along the curve.
        :return: the station at the given length.
        """
        ...

    def at_fraction(self, fraction: float) -> CurveStation2:
        """
        Get the station at a given fraction of the length of the curve. Will throw a ValueError if the fraction is less
        than zero or greater than one.
        :param fraction: the fraction of the length of the curve.
        :return: the station at the given fraction.
        """
        ...

    def at_closest_to_point(self, point: Point2) -> CurveStation2:
        """
        Get the station on the curve that is closest to a given point.
        :param point: the point to find the closest station to.
        :return: the station on the curve that is closest to the given point.
        """
        ...

    @property
    def is_closed(self) -> bool:
        """
        Check if the curve is closed.
        :return: True if the curve is closed, False otherwise.
        """
        ...

    def trim_front(self, length: float) -> Curve2:
        """
        Remove the front of the curve by a given length and return a new curve.
        :param length: the length to trim from the front of the curve.
        :return: a new curve with the front trimmed by the given length.
        """
        ...

    def trim_back(self, length: float) -> Curve2:
        """
        Remove the back of the curve by a given length and return a new curve.
        :param length: the length to trim from the back of the curve.
        :return: a new curve with the back trimmed by the given length.
        """
        ...

    def between_lengths(self, l0: float, l1: float) -> Curve2:
        """
        Attempt to get a new curve cut between two lengths along the curve. If the lengths are not valid, a ValueError
        will be thrown.

        If the curve is closed, the lengths will be wrapped around the curve. If the curve is not closed, the value
        of `l0` must be less than `l1`. In either case, the lengths must be within the bounds of the curve.

        :param l0: the start length.
        :param l1: the end length.
        :return: a new curve between the two lengths.
        """
        ...

    def between_lengths_by_control(self, a: float, b: float, control: float) -> Curve2:
        """
        Attempt to get a new curve cut between two lengths along the curve, with a control point that will be used to
        determine which side of the curve to keep. This is primarily helpful on closed curves when you can find a length
        (usually via use of the `at_closest_to_point` method) that is on the side of the curve you want to keep.

        If the lengths are not valid, a ValueError will be thrown.

        :param a: the first length along the curve to cut
        :param b: the second length along the curve to cut
        :param control: a length along the curve that is on a point in the portion of the result that you want to keep
        :return: a new curve between the two lengths
        """

    def reversed(self) -> Curve2:
        """
        Reverse the curve and return a new curve.
        :return: a new curve with the vertices in reverse order.
        """
        ...

    def make_hull(self) -> numpy.ndarray[float]:
        """
        Get the vertices of a convex hull of the curve, in counter-clockwise order.
        :return: a numpy array of shape (N, 2) representing the convex hull of the curve.
        """
        ...

    def max_point_in_direction(self, direction: Vector2) -> Tuple[int, Point2]:
        """
        Find the point on the curve that is furthest in a given direction.
        :param direction: the direction to find the furthest point in.
        :return: a tuple of the index of the point and the point itself.
        """
        ...

    def max_distance_in_direction(self, surf_point: SurfacePoint2) -> float:
        """
        Find the maximum scalar projection of all vertices of the curve onto a surface point.
        :param surf_point: the direction to find the furthest point in.
        :return: the maximum scalar projection of all vertices of the curve onto a surface point.
        """
        ...

    def clone_points(self) -> numpy.ndarray[float]:
        """
        Clone the points of the curve.
        :return: a numpy array of shape (N, 2) representing the points of the curve.
        """
        ...

    def simplify(self, tol: float) -> Curve2:
        """
        Simplify the curve using the Ramer-Douglas-Peucker algorithm.
        :param tol: the tolerance to use for simplification.
        :return: a new curve with the simplified points.
        """
        ...

    def resample(self, resample: Resample) -> Curve2:
        """
        Resample the curve using the given resampling method. The resampling method can be one of the following:

        - `Resample.ByCount(count: int)`: resample the curve to have the given number of points.
        - `Resample.BySpacing(distance: float)`: resample the curve to have points spaced by the given distance.
        - `Resample.ByMaxSpacing(distance: float)`: resample the curve to have points spaced by a maximum distance.

        :param resample: the resampling method to use.
        :return: a new curve object with the resampled vertices.
        """
        ...

    def transformed_by(self, transform: Iso2) -> Curve2:
        """
        Transform the curve by the given transform and return a new curve.
        :param transform: the transform to apply to the curve.
        :return: a new curve object with the transformed vertices.
        """
        ...
