from typing import List

import numpy
from enum import Enum

from .geom2 import Circle2, Curve2, Point2, SurfacePoint2, Arc2
from .metrology import Length2

type MclOrientEnum = MclOrient.TmaxFwd | MclOrient.DirFwd
type FaceOrientEnum = FaceOrient.Detect | FaceOrient.UpperDir
type EdgeFindEnum = EdgeFind.Open | EdgeFind.OpenIntersect | EdgeFind.Intersect | EdgeFind.RansacRadius
type EdgeTypeEnum = EdgeType | Arc2
type AfGageEnum = AfGage.OnCamber | AfGage.Radius

class EdgeType(Enum):
    Open=0
    Closed=1

class AfGage:
    """
    A class representing a measurement for locating a position on an airfoil cross-section.
    """
    class OnCamber:
        def __init__(self, d: float):
            """
            A gaging method that measures a distance along the mean camber line. A positive distance will be from the
            leading edge towards the trailing edge, and a negative distance will be from the trailing edge towards the
            leading edge.
            :param d: the distance along the mean camber line to find the position
            """
            ...

    class Radius:
        def __init__(self, r: float):
            """
            A gaging method that measures by intersection with a circle of a given radius centered on either the
            leading or trailing edge point.  A positive radius indicates that the circle is located on the leading edge
            while a negative radius indicates that the circle is located on the trailing edge.
            :param r: the radius of the circle to find the position
            """
            ...

class FaceOrient:
    """
    An enumeration of the possible ways to orient the upper/lower (suction/pressure, convex/concave) faces of an
    airfoil cross-section.
    """

    class Detect:
        """
        In an airfoil with an MCL that exhibits curvature, this will attempt to detect which direction the camber line
        curves and thus identify convex/concave. This will fail if the MCL is straight.
        """
        ...

    class UpperDir:
        """
        This method will orient the faces based on a vector direction provided by the user.
        """

        def __init__(self, x: float, y: float):
            """
            Create a new upper direction parameter. The x and y arguments are components of a direction vector which
            should distinguish the upper (pressure side, convex) face of the airfoil. At the center of the mean camber
            line, an intersection in this direction will be taken with each of the two faces. The intersection that
            is further in the direction of this vector will be considered the upper face of the airfoil, and the other
            will be considered the lower face.

            :param x: the x component of the upper direction vector
            :param y: the y component of the upper direction vector
            """
            ...


class MclOrient:
    """
    An enumeration of the possible ways to orient (to identify which side is the leading edge and which side is the
    trailing edge) the mean camber line of an airfoil.
    """

    class TmaxFwd:
        """
        This method will take advantage of the fact that for most typical subsonic airfoils the maximum thickness point
        is closer to the leading edge than the trailing edge.
        """
        ...

    class DirFwd:
        """
        This method will orient the airfoil based on a vector direction provided by the user.
        """

        def __init__(self, x: float, y: float):
            """
            Create a new forward direction parameter. The x and y arguments are components of a direction vector which
            should distinguish the forward (leading edge) direction of the airfoil. The position of the first and last
            inscribed circle will be projected onto this vector, and the larger result (the one that is more in the
            direction of this vector) will be considered the leading edge of the airfoil.

            For instance, if you know that the airfoil is oriented so that the leading edge will have a smaller x value
            than the trailing edge, `DirFwd(-1, 0)` will correctly orient the airfoil.
            :param x: the x component of the forward direction vector
            :param y: the y component of the forward direction vector
            """
            ...


class EdgeFind:
    """
    An enumeration of the possible techniques to find the leading and/or trailing edge geometry of an airfoil.
    """

    class Open:
        """
        This algorithm will not attempt to find edge geometry, and will simply leave the inscribed circles for the side
        as they are. Use this if you know that the airfoil cross-section is open/incomplete on this side, and you don't
        care to extend the MCL any further.
        """
        ...

    class OpenIntersect:
        def __init__(self, max_iter: int):
            """
            This algorithm will attempt to find the edge geometry by intersecting the end of the inscribed circles
            camber curve with the open gap in the airfoil cross-section, then refining the end of the MCL with more
            inscribed circles until the location of the end converges to within 1/100th of the general refinement
            tolerance.

            If the maximum number of iterations is reached before convergence, the method will throw an error instead.

            :param max_iter: the maximum number of iterations to attempt to find the edge geometry
            """
            ...

    class Intersect:
        """
        This algorithm will simply intersect the end of the inscribed circles camber curve with the airfoil
        cross-section. This is the fastest method with the least amount of assumptions, and makes sense for airfoil
        edges where you know the mean camber line has very low curvature in the vicinity of the edge.
        """
        ...

    class RansacRadius:
        def __init__(self, in_tol: float, n: int = 500):
            """
            This algorithm uses RANSAC (Random Sample Consensus) to find a constant radius leading edge circle that
            fits the greatest number of points leftover at the edge within the tolerance `in_tol`.

            The method will try `n` different combinations of three points picked at random from the remaining points
            at the edge, construct a circle, and then count the number of points within `in_tol` distance of the circle
            perimeter. The circle with the most points within tolerance will be considered the last inscribed circle.

            The MCL will be extended to this final circle, and then intersected with the airfoil cross-section to find
            the final edge point.

            :param in_tol: the max distance from the circle perimeter for a point to be considered a RANSAC inlier
            :param n: The number of RANSAC iterations to perform
            """
            ...


class InscribedCircle:
    @property
    def circle(self) -> Circle2: ...

    @property
    def contact_a(self) -> Point2:
        """
        A contact point of the inscribed circle with one side of the airfoil cross-section. Inscribed circles computed
        together will have a consistent meaning of `a` and `b` sides, but which is the upper or lower surface will
        depend on the ordering of the circles and the coordinate system of the airfoil.
        """
        ...

    @property
    def contact_b(self) -> Point2:
        """
        The other contact point of the inscribed circle with the airfoil cross-section. Inscribed circles computed
        together will have a consistent meaning of `a` and `b` sides, but which is the upper or lower surface will
        depend on the ordering of the circles and the coordinate system of the airfoil.
        """
        ...


class EdgeResult:
    """
    Represents the results of an edge detection algorithm
    """

    @property
    def point(self) -> Point2:
        """
        The point on the airfoil cross-section that was detected as the edge.
        """
        ...

    @property
    def geometry(self):
        ...


class AirfoilGeometry:
    """
    The result of an airfoil geometry computation.
    """

    @staticmethod
    def from_analyze(
            section: Curve2,
            refine_tol: float,
            camber_orient: MclOrientEnum,
            leading: EdgeFindEnum,
            trailing: EdgeFindEnum,
            face_orient: FaceOrientEnum,
    ) -> AirfoilGeometry:
        ...

    @property
    def leading(self) -> EdgeResult | None:
        """
        The result of the leading edge detection algorithm.
        """
        ...

    @property
    def trailing(self) -> EdgeResult | None:
        """
        The result of the trailing edge detection algorithm.
        """
        ...

    @property
    def camber(self) -> Curve2:
        """
        The mean camber line of the airfoil cross-section. The curve will be oriented so that the first point is at
        the leading edge of the airfoil and the last point is at the trailing edge.
        :return:
        """
        ...

    @property
    def upper(self) -> Curve2 | None:
        """
        The curve representing the upper (suction, convex) side of the airfoil cross-section. The curve will be oriented
        in the same winding direction as the original section, so the first point may be at either the leading or
        trailing edge based on the airfoil geometry and the coordinate system.

        :return: A Curve2, or None if there was an issue detecting the leading or trailing edge.
        """
        ...

    @property
    def lower(self) -> Curve2 | None:
        """
        The curve representing the lower (pressure, concave) side of the airfoil cross-section. The curve will be
        oriented in the same winding direction as the original section, so the first point may be at either the leading
        or trailing edge based on the airfoil geometry and the coordinate system.

        :return: A Curve2, or None if there was an issue detecting the leading or trailing edge.
        """
        ...

    @property
    def circle_array(self) -> numpy.ndarray[float]:
        """
        Returns the list of inscribed circles as a numpy array of shape (N, 3) where N is the number of inscribed
        circles. The first two columns are the x and y coordinates of the circle center, and the third column is the
        radius of the circle.
        """
        ...

    def get_thickness(self, gage: AfGageEnum) -> Length2:
        """
        Get the thickness dimension of the airfoil cross-section.
        :param gage: the gaging method to use
        :return:
        """
        ...

    def get_tmax(self) -> Length2:
        """
        Get the maximum thickness dimension of the airfoil cross-section.
        :return:
        """
        ...

    def get_tmax_circle(self) -> Circle2:
        """
        Get the circle representing the maximum thickness dimension of the airfoil cross-section.
        :return:
        """
        ...


def compute_inscribed_circles(section: Curve2, refine_tol: float) -> List[InscribedCircle]:
    """
    Compute the unambiguous inscribed circles of an airfoil cross-section.

    The cross-section is represented by a curve in the x-y plane. The curve does not need to be closed, but the points
    should be oriented in a counter-clockwise direction and should only contain data from the outer surface of the
    airfoil (internal features/points should not be part of the data).

    The method used to compute these circles is:

    1. We calculate the convex hull of the points in the section and find the longest distance between any two points.
    2. At the center of the longest distance line, we draw a perpendicular line and look for exactly two intersections
       with the section. We assume that one of these is on the upper surface of the airfoil and the other is on the
       lower, though it does not matter which is which.
    3. We fit the maximum inscribed circle whose center is constrained to the line between these two points. The
       location and radius of this circle is refined until it converges to within 1/100th of `refine_tol`.
    4. The inscribed circle has two contact points with the section. The line between these contact points is a good
       approximation of the direction orthogonal to the mean camber line near the circle.  We create a parallel line
       to this one, advancing from the circle center by 1/4 of the circle radius, and looking for exactly two
       intersections with the section.  If we fail, we try again with a slightly less aggressive advancement until we
       either succeed or give up.
    5. We fit the maximum inscribed circle whose center is constrained to the new line, and refine it as in step 3.
    6. We recursively fit inscribed circles between this new circle and the previous one until the error between the
       position and radius of any circle is less than `refine_tol` from the linear interpolation between its next and
       previous neighbors.
    7. We repeat the process from step 4 until the distance between the center of the most recent circle and the
       farthest point in the direction of the next advancement is less than 1/4 of the radius of the most recent
       circle. This terminates the process before we get too close to the leading or trailing edge of the airfoil.
    8. We repeat the process from step 3, but this time in the opposite direction from the first circle. This will
       give us the inscribed circles on the other side of the airfoil.

    When finished, we have a list of inscribed circles from the unambiguous regions (not too close to the leading or
    trailing edges) of the airfoil cross-section. The circles are ordered from one side of the airfoil to the other,
    but the order may be *either* from the leading to the trailing edge *or* vice versa.

    :param section: the curve representing the airfoil cross-section.
    :param refine_tol: a tolerance used when refining the inscribed circles, see description for details.
    :return: a list of inscribed circle objects whose order is contiguous but may be in either direction
    """
    ...
