from typing import List

from .geom2 import Circle2, Curve2, Point2, SurfacePoint2

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