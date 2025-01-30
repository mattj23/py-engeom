use crate::conversions::array_to_points3;
use crate::geom3::Iso3;
use numpy::ndarray::Array1;
use numpy::{IntoPyArray, PyArray1, PyArrayMethods, PyReadonlyArray1, PyReadonlyArrayDyn};
use pyo3::exceptions::{PyIOError, PyValueError};
use pyo3::prelude::*;

#[pyclass]
pub struct SvdBasis2 {
    inner: engeom::SvdBasis2,
}

impl SvdBasis2 {
    pub fn get_inner(&self) -> &engeom::SvdBasis2 {
        &self.inner
    }
}

#[pymethods]
impl SvdBasis2 {}

#[pyclass]
pub struct SvdBasis3 {
    inner: engeom::SvdBasis3,
}

impl SvdBasis3 {
    pub fn get_inner(&self) -> &engeom::SvdBasis3 {
        &self.inner
    }
}

#[pymethods]
impl SvdBasis3 {
    #[new]
    pub fn new<'py>(
        points: PyReadonlyArrayDyn<'py, f64>,
        weights: Option<PyReadonlyArray1<'py, f64>>,
    ) -> PyResult<Self> {
        let points = array_to_points3(&points.as_array())?;

        // TODO: Is there some way to pass it back as a reference?
        let basis = match weights {
            Some(weights) => engeom::SvdBasis3::from_points(
                &points,
                Some(&weights.as_array().as_slice().unwrap()),
            ),
            None => engeom::SvdBasis3::from_points(&points, None),
        };

        Ok(Self { inner: basis })
    }

    fn rank(&self, tol: f64) -> usize {
        self.inner.rank(tol)
    }

    fn largest<'py>(&self, py: Python<'py>) -> Bound<'py, PyArray1<f64>> {
        let mut result = Array1::zeros(3);
        let largest = self.inner.largest();

        result[0] = largest[0];
        result[1] = largest[1];
        result[2] = largest[2];

        result.into_pyarray(py)
    }

    fn smallest<'py>(&self, py: Python<'py>) -> Bound<'py, PyArray1<f64>> {
        let mut result = Array1::zeros(3);
        let smallest = self.inner.smallest();

        result[0] = smallest[0];
        result[1] = smallest[1];
        result[2] = smallest[2];

        result.into_pyarray(py)
    }

    fn basis_variances<'py>(&self, py: Python<'py>) -> Bound<'py, PyArray1<f64>> {
        let mut result = Array1::zeros(3);
        let variances = self.inner.basis_variances();

        result[0] = variances[0];
        result[1] = variances[1];
        result[2] = variances[2];

        result.into_pyarray(py)
    }

    fn basis_stdevs<'py>(&self, py: Python<'py>) -> Bound<'py, PyArray1<f64>> {
        let mut result = Array1::zeros(3);
        let stdevs = self.inner.basis_stdevs();

        result[0] = stdevs[0];
        result[1] = stdevs[1];
        result[2] = stdevs[2];

        result.into_pyarray(py)
    }

    fn to_iso3(&self) -> Iso3 {
        Iso3::from_inner((&self.inner).into())
    }
}
