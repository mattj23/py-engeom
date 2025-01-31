"""
    Tests of simple objects in geom2 module.
"""
import pytest
import numpy
from engeom.geom2 import Vector2, Point2, SurfacePoint2, Iso2


# Test that a vector plus a vector is a vector.
def test_vector_plus_vector():
    v1 = Vector2(1, 2)
    v2 = Vector2(3, 4)
    v3 = v1 + v2
    assert isinstance(v3, Vector2)


def test_vector_plus_point():
    v = Vector2(1, 2)
    p = Point2(3, 4)
    result = v + p
    assert isinstance(result, Point2)


# Test that a point plus a vector is a point.
def test_point_plus_vector():
    p = Point2(1, 2)
    v = Vector2(3, 4)
    result = p + v
    assert isinstance(result, Point2)


# Test that a point minus a point is a vector.
def test_point_minus_point():
    p1 = Point2(1, 2)
    p2 = Point2(3, 4)
    result = p1 - p2
    assert isinstance(result, Vector2)


# Test that a point minus a vector is a point.
def test_point_minus_vector():
    p = Point2(3, 4)
    v = Vector2(1, 2)
    result = p - v
    assert isinstance(result, Point2)


# Test that a vector minus a vector is a vector.
def test_vector_minus_vector():
    v1 = Vector2(3, 4)
    v2 = Vector2(1, 2)
    result = v1 - v2
    assert isinstance(result, Vector2)


# Test that an Iso2 matmul by a vector returns a vector.
def test_iso2_matmul_vector():
    iso = Iso2(1, 2, 0.5)
    v = Vector2(3, 4)
    result = iso @ v
    assert isinstance(result, Vector2)


# Test that an Iso2 matmul by a point returns a point.
def test_iso2_matmul_point():
    iso = Iso2(1, 2, 0.5)
    p = Point2(3, 4)
    result = iso @ p
    assert isinstance(result, Point2)


# Test that an Iso2 matmul by a surface point returns a surface point.
def test_iso2_matmul_surfacepoint():
    iso = Iso2(1, 2, 0.5)
    sp = SurfacePoint2(3, 4, 1, 0)
    result = iso @ sp
    assert isinstance(result, SurfacePoint2)


# Test that an Iso2 matmul by another Iso2 returns an Iso2.
def test_iso2_matmul_iso2():
    iso1 = Iso2(1, 2, 0.5)
    iso2 = Iso2(3, 4, 0.5)
    result = iso1 @ iso2
    assert isinstance(result, Iso2)
