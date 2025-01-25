import pytest
import py_engeom


def test_sum_as_string():
    assert py_engeom.sum_as_string(1, 1) == "2"
