from __future__ import annotations

from pathlib import Path
from typing import Tuple, Iterable, List

import numpy
from engeom import DeviationMode, Resample

type Transformable3 = Vector3 | Point3 | Plane3 | Iso3 | SurfacePoint3


class Vector3:
    def __init__(self, x: float, y: float, z: float):
        """

        :param x:
        :param y:
        :param z:
        """
        ...

    @property
    def x(self) -> float:
        ...

    @property
    def y(self) -> float:
        ...

    @property
    def z(self) -> float:
        ...

    def __iter__(self) -> Iterable[float]:
        ...

    def __rmul__(self, other: float) -> Vector3:
        ...

    def __add__(self, other: Vector3 | Point3) -> Vector3 | Point3:
        ...

    def __sub__(self, other: Vector3) -> Vector3:
        ...

    def __neg__(self) -> Vector3:
        ...

    def __mul__(self, x: float) -> Vector3:
        ...

    def as_numpy(self) -> numpy.ndarray[float]:
        """
        Create a numpy array of shape (3,) from the vector.
        """
        ...

    def dot(self, other: Vector3) -> float:
        """
        Calculate the dot product of this vector with another vector.
        :param other: the other vector to calculate the dot product with.
        :return: the dot product of the two vectors.
        """
        ...

    def cross(self, other: Vector3) -> Vector3:
        """
        Calculate the cross product of this vector with another vector.
        :param other: the other vector to calculate the cross product with.
        :return: the cross product of the two vectors.
        """
        ...

    def norm(self) -> float:
        """
        Calculate the norm (length) of the vector.
        :return:
        """

    def normalized(self) -> Vector3:
        """
        Return a normalized version of the vector.
        :return: a new vector that has unit length
        """

    def angle_to(self, other: Vector3) -> float:
        """
        Calculate the smallest angle between this vector and another vector.
        :param other: the other vector to calculate the angle to.
        :return: the angle between the two vectors in radians.
        """
        ...


class Point3:
    def __init__(self, x: float, y: float, z: float):
        """

        :param x:
        :param y:
        :param z:
        """
        ...

    @property
    def x(self) -> float:
        ...

    @property
    def y(self) -> float:
        ...

    @property
    def z(self) -> float:
        ...

    def __iter__(self) -> Iterable[float]:
        ...

    @property
    def coords(self) -> Vector3:
        """
        Get the coordinates of the point as a Vector3 object.
        :return: a Vector3 object
        """
        ...

    def __sub__(self, other: Vector3 | Point3) -> Vector3 | Point3:
        ...

    def __add__(self, other: Vector3) -> Vector3:
        ...

    def as_numpy(self) -> numpy.ndarray[float]:
        """
        Create a numpy array of shape (2,) from the point.
        """
        ...


class SurfacePoint3:
    def __init__(self, x: float, y: float, z: float, nx: float, ny: float, nz: float):
        """

        :param x:
        :param y:
        :param z:
        :param nx:
        :param ny:
        :param nz:
        """
        ...

    @property
    def point(self) -> Point3:
        """
        Get the coordinates of the point as a Point3 object.
        :return: a Point3 object
        """
        ...

    @property
    def normal(self) -> Vector3:
        """
        Get the normal of the point as a Vector3 object.
        :return: a Vector3 object
        """
        ...

    def at_distance(self, distance: float) -> Point3:
        """
        Get the point at a distance along the normal from the surface point.
        :param distance: the distance to move along the normal.
        :return: the point at the distance along the normal.
        """
        ...

    def scalar_projection(self, point: Point3) -> float:
        """
        Calculate the scalar projection of a point onto the axis defined by the surface point position and direction.
        Positive values indicate that the point is in the normal direction from the surface point, while negative values
        indicate that the point is in the opposite direction.

        :param point: the point to calculate the projection of.
        :return: the scalar projection of the point onto the normal.
        """
        ...

    def projection(self, point: Point3) -> Point3:
        """
        Calculate the projection of a point onto the axis defined by the surface point position and direction.

        :param point: the point to calculate the projection of.
        :return: the projection of the point onto the plane.
        """
        ...

    def reversed(self) -> SurfacePoint3:
        """
        Return a new surface point with the normal vector inverted, but the position unchanged.
        :return: a new surface point with the inverted normal vector.
        """
        ...

    def planar_distance(self, point: Point3) -> float:
        """
        Calculate the planar (non-normal) distance between the surface point and a point. This is complementary to the
        scalar projection. A point is projected onto the plane defined by the position and normal of the surface point,
        and the distance between the surface point position and the projected point is returned.  The value will always
        be positive.

        :param point: the point to calculate the distance to.
        :return: the planar distance between the surface point and the point.
        """
        ...

    def get_plane(self) -> Plane3:
        """
        Get the plane defined by the surface point.
        :return: the plane defined by the surface point.
        """
        ...


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

    def __matmul__(self, other: Transformable3) -> Transformable3:
        """
        Multiply another object by the isometry, transforming it and returning a new object of the same type.
        :param other: an object of one of the transformable types
        :return: a new object of the same type as the input object, transformed by the isometry.
        """
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

    def as_numpy(self) -> numpy.ndarray[float]:
        """ Return a copy of the 4x4 matrix representation of the isometry. This is a copy operation. """
        ...

    def flip_around_x(self) -> Iso3:
        """ Return a new isometry that flips the isometry 180° around the x-axis. The origin of the isometry will be
        preserved, but the y and z axes will point in the opposite directions. """
        ...

    def flip_around_y(self) -> Iso3:
        """ Return a new isometry that flips the isometry 180° around the y-axis. The origin of the isometry will be
        preserved, but the x and z axes will point in the opposite directions. """
        ...

    def flip_around_z(self) -> Iso3:
        """ Return a new isometry that flips the isometry 180° around the z-axis. The origin of the isometry will be
        preserved, but the x and y axes will point in the opposite directions. """
        ...


class SvdBasis3:
    """
    A class representing a basis in 3D space. This class is created from a set of points and will calculate the best
    fitting basis for the points using a singular value decomposition.
    """

    def __init__(
            self,
            points: numpy.ndarray[float],
            weights: numpy.ndarray[float] | None = None
    ):
        """
        Create a basis from a set of points. The basis will be calculated using a singular value decomposition of the
        points.

        :param points: a numpy array of shape (n, 3) containing the points to calculate the basis from.
        :param weights: a numpy array of shape (n,) containing the weights of the points. If None, all points will be
        weighted equally.
        """
        ...

    def to_iso3(self) -> Iso3:
        """
        Produce an isometry which will transform from the world space to the basis space.

        For example, if the basis is created from a set of points that lie in an arbitrary plane, transforming the
        original points by this isometry will move the points such that all points lie on the XY plane.
        :return: the isometry that transforms from the world space to the basis space.
        """
        ...

    def largest(self) -> numpy.ndarray[float]:
        """
        Return the largest normalized basis vector.
        :return: a numpy array of shape (3,) containing the largest basis vector.
        """
        ...

    def smallest(self) -> numpy.ndarray[float]:
        """
        Return the smallest normalized basis vector.
        :return: a numpy array of shape (3,) containing the smallest basis vector.
        """
        ...

    def basis_variances(self) -> numpy.ndarray[float]:
        """
        Return the variances of the basis vectors.
        :return: a numpy array of shape (3,) containing the variances of the basis vectors.
        """
        ...

    def basis_stdevs(self) -> numpy.ndarray[float]:
        """
        Return the standard deviations of the basis vectors.
        :return: a numpy array of shape (3,) containing the standard deviations of the basis vectors.
        """
        ...

    def rank(self, tol: float) -> int:
        """
        Retrieve the rank of the decomposition by counting the number of singular values that are
        greater than the provided tolerance.  A rank of 0 indicates that all singular values are
        less than the tolerance, and thus the point set is essentially a single point. A rank of 1
        indicates that the point set is essentially a line. A rank of 2 indicates that the point
        set exists roughly in a plane.  The maximum rank is 3, which indicates that the point set
        cannot be reduced to a lower dimension.

        The singular values do not directly have a clear physical meaning. They are square roots of
        the variance multiplied by the number of points used to compute the basis.  Thus, they can
        be interpreted in relation to each other, and when they are very small.

        This method should be used either when you know roughly what a cutoff tolerance for the
        problem you're working on should be, or when you know the cutoff value should be very
        small.  Otherwise, consider examining the standard deviations of the basis vectors
        instead, as they will be easier to interpret (`basis_stdevs()`).
        :param tol: the tolerance to use when determining the rank.
        :return: the rank of the decomposition.
        """
        ...


class Plane3:
    """
    A class representing a plane in 3D space. The plane is represented by a unit normal vector and a distance from the
    origin along the normal vector.
    """

    def __init__(self, a: float, b: float, c: float, d: float):
        """
        Create a plane from the equation ax + by + cz + d = 0.
        :param a: the x value of the unit normal vector.
        :param b: the y value of the unit normal vector.
        :param c: the z value of the unit normal vector.
        :param d: the distance from the origin along the normal vector.
        """
        ...

    def inverted_normal(self) -> Plane3:
        """
        Return a new plane with the normal vector inverted.
        :return: a new plane with the inverted normal vector.
        """
        ...

    def signed_distance_to_point(self, point: Point3) -> float:
        """
        Calculate the signed distance from the plane to a point. The distance will be positive if the point is on the
        same side of the plane as the normal vector, and negative if the point is on the opposite side.
        :param point: the point to calculate the distance to.
        :return: the signed distance from the plane to the point.
        """
        ...

    def project_point(self, point: Point3) -> Point3:
        """
        Project a point onto the plane. The projected point will be the closest point on the plane to the input point.
        :param point: the point to project.
        :return: the projected point.
        """
        ...


class Mesh:
    """
    A class holding an unstructured, 3-dimensional mesh of triangles.
    """

    def __init__(
            self,
            vertices: numpy.ndarray[float],
            triangles: numpy.ndarray[numpy.uint32],
            merge_duplicates: bool | None = None,
            delete_degenerate: bool | None = None
    ):
        """
        Create an engeom mesh from vertices and triangles.  The vertices should be a numpy array of shape (n, 3), while
        the triangles should be a numpy array of shape (m, 3) containing the indices of the vertices that make up each
        triangle. The triangles should be specified in counter-clockwise order when looking at the triangle from the
        front/outside.

        :param vertices: a numpy array of shape (n, 3) containing the vertices of the mesh.
        :param triangles: a numpy array of shape (m, 3) containing the triangles of the mesh, should be uint.
        :param merge_duplicates: merge duplicate vertices and triangles. If None, the default behavior is to do nothing
        :param delete_degenerate: delete degenerate triangles. If None, the default behavior is to do nothing
        """
        ...

    @staticmethod
    def load_stl(path: str | Path, merge_duplicates: bool | None = None, delete_degenerate: bool | None = None) -> Mesh:
        """
        Load a mesh from an STL file. This will return a new mesh object containing the vertices and triangles from the
        file.  Optional parameters can be used to control the behavior of the loader when handling duplicate vertices/
        triangles and degenerate triangles.

        :param path: the path to the STL file to load.
        :param merge_duplicates: merge duplicate vertices and triangles. If None, the default behavior is to do nothing
        :param delete_degenerate: delete degenerate triangles. If None, the default behavior is to do nothing
        :return: the mesh object containing the data from the file.
        """
        ...

    def write_stl(self, path: str | Path):
        """
        Write the mesh to an STL file. This will write the vertices and triangles of the mesh to the file in binary
        format.

        :param path: the path to the STL file to write.
        """
        ...

    def clone(self) -> Mesh:
        """
        Will return a copy of the mesh. This is a copy of the data, so modifying the returned mesh will not modify the
        original mesh.

        :return:
        """

    def transform_by(self, iso: Iso3):
        """
        Transforms the vertices of the mesh by an isometry. This will modify the mesh in place.  Any copies made of
        the vertices will no longer match the mesh after this operation.
        :param iso: the isometry to transform the mesh by.
        :return: None
        """
        ...

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
        :return: a numpy array of shape (n, 3) containing the vertices of the mesh.
        """
        ...

    def clone_triangles(self) -> numpy.ndarray[numpy.uint32]:
        """
        Will return a copy of the triangles of the mesh as a numpy array. If the mesh has not been modified, this will
        be the same as the original triangles. This is a copy of the data, so modifying the returned array will not
        modify the mesh.

        :return: a numpy array of shape (m, 3) containing the triangles of the mesh.
        """
        ...

    def split(self, plane: Plane3) -> Tuple[Mesh | None, Mesh | None]:
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

    def sample_poisson(self, radius: float) -> numpy.ndarray[float]:
        """
        Sample the surface of the mesh using a Poisson disk sampling algorithm. This will return a numpy array of points
        and their normals that are approximately evenly distributed across the surface of the mesh. The radius parameter
        controls the minimum distance between points.

        Internally, this algorithm will first re-sample each triangle of the mesh with a dense array of points at a
        maximum distance of radius/2, before applying a random poisson disk sampling algorithm to thin the resampled
        points. This means that the output points are not based on the mesh vertices, so large triangles will not be
        under-represented and small triangles will not be over-represented.

        :param radius: the minimum distance between points.
        :return: a numpy array of shape (n, 6) containing the sampled points.
        """
        ...

    def section(self, plane: Plane3, tol: float | None = None) -> List[Curve3]:
        """
        Calculate and return the intersection curves between the mesh and a plane.

        :param plane:
        :param tol:
        :return:
        """
        ...


class CurveStation3:
    """
    A class representing a station along a curve in 3D space. The station is represented by a point on the curve, a
    tangent (direction) vector, and a length along the curve.
    """

    @property
    def point(self) -> Point3:
        """ The 3d position in space on the curve. """
        ...

    @property
    def direction(self) -> Vector3:
        """ The tangent (direction) vector of the curve at the station. """
        ...

    @property
    def direction_point(self) -> SurfacePoint3:
        """
        A `SurfacePoint3` object representing the point on the curve and the curve's tangent/direction vector.
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


class Curve3:
    """
    A class representing a polyline in 3D space. The curve is represented by a set of vertices and the segments
    between them.
    """

    def __init__(self, vertices: numpy.ndarray):
        """
        Create a curve from a set of vertices. The vertices should be a numpy array of shape (n, 3).

        :param vertices: a numpy array of shape (n, 3) containing the vertices of the curve.
        """
        ...

    def clone(self) -> Curve3:
        """
        Will return a copy of the curve. This is a copy of the data, so modifying the returned curve will not modify
        the original curve.

        :return: a copy of the curve.
        """
        ...

    def length(self) -> float:
        """
        Return the total length of the curve in the units of the vertices.

        :return: the length of the curve.
        """
        ...

    def clone_vertices(self) -> numpy.ndarray[float]:
        """
        Will return a copy of the vertices of the curve as a numpy array. If the curve has not been modified, this will
        be the same as the original vertices. This is a copy of the data, so modifying the returned array will not
        modify the curve.

        :return: a numpy array of shape (n, 3) containing the vertices of the curve.
        """
        ...

    def at_length(self, length: float) -> CurveStation3:
        """
        Return a station along the curve at the given length. The length is measured from the start of the curve to the
        station. If the length is greater than the length of the curve or less than 0, an error will be raised.

        :param length: the length along the curve to return the station at.
        :return: a `CurveStation3` object representing the station along the curve.
        """
        ...

    def at_fraction(self, fraction: float) -> CurveStation3:
        """
        Return a station along the curve at the given fraction of the length of the curve. If the fraction is greater
        than 1 or less than 0, an error will be raised.

        :param fraction: the fraction of the length of the curve to return the station at.
        :return: a `CurveStation3` object representing the station along the curve.
        """
        ...

    def at_closest_to_point(self, point: Point3) -> CurveStation3:
        """
        Return a station along the curve at the closest point to the given point. The station will be the point on the
        curve that is closest to the given point.

        :param point: the point to find the closest station to.
        :return: a `CurveStation3` object representing the station along the curve.
        """
        ...

    def at_front(self) -> CurveStation3:
        """
        Return a station at the front of the curve. This is equivalent to calling `at_length(0)`.

        :return: a `CurveStation3` object representing the station at the front of the curve.
        """
        ...

    def at_back(self) -> CurveStation3:
        """
        Return a station at the back of the curve. This is equivalent to calling `at_length(length)`.

        :return: a `CurveStation3` object representing the station at the back of the curve.
        """
        ...

    def resample(self, resample: Resample) -> Curve3:
        """
        Resample the curve using the given resampling method. The resampling method can be one of the following:

        - `Resample.ByCount(count: int)`: resample the curve to have the given number of points.
        - `Resample.BySpacing(distance: float)`: resample the curve to have points spaced by the given distance.
        - `Resample.ByMaxSpacing(distance: float)`: resample the curve to have points spaced by a maximum distance.

        :param resample: the resampling method to use.
        :return: a new curve object with the resampled vertices.
        """
        ...

    def simplify(self, tolerance: float) -> Curve3:
        """
        Simplify the curve using the Ramer-Douglas-Peucker algorithm. This will remove vertices from the curve that are
        within the given tolerance of the line between the previous and next vertices.

        :param tolerance: the tolerance to use when simplifying the curve.
        :return: a new curve object with the simplified vertices.
        """
        ...

    def transformed_by(self, iso: Iso3) -> Curve3:
        """
        Transform the curve by an isometry. This will return a new curve object with the transformed vertices.

        :param iso: the isometry to transform the curve by.
        :return: a new curve object with the transformed vertices.
        """
        ...
