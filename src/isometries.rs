use crate::conversions::{array_to_points3, array_to_vectors3};
use engeom;
use engeom::geom3::iso3_try_from_array;
use engeom::geom3::Flip3;
use numpy::ndarray::ArrayD;
use numpy::{IntoPyArray, PyArrayDyn, PyReadonlyArrayDyn, PyUntypedArrayMethods};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
