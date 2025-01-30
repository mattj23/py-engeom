use crate::conversions::{array_to_points3, array_to_vectors3};
use engeom;
use engeom::geom3::iso3_try_from_array;
use engeom::geom3::Flip3;
use numpy::ndarray::ArrayD;
use numpy::{IntoPyArray, PyArrayDyn, PyReadonlyArrayDyn, PyUntypedArrayMethods};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

#[pyclass]
pub struct Iso2 {
    inner: engeom::Iso2,
}

#[pymethods]
impl Iso2 {
    #[new]
    fn new(x: f64, y: f64, r: f64) -> Self {
        let inner = engeom::Iso2::translation(x, y) * engeom::Iso2::rotation(r);
        Self { inner }
    }

    #[staticmethod]
    fn identity() -> Self {
        Self {
            inner: engeom::Iso2::identity(),
        }
    }
}

#[pyclass]
pub struct Iso3 {
    inner: engeom::Iso3,
}

impl Iso3 {
    pub fn get_inner(&self) -> &engeom::Iso3 {
        &self.inner
    }

    pub fn from_inner(inner: engeom::Iso3) -> Self {
        Self { inner }
    }
}

#[pymethods]
impl Iso3 {
    fn __repr__(&self) -> String {
        format!(
            "<Iso3 t=[{}, {}, {}] r=[{}, {}, {}, {}]>",
            self.inner.translation.x,
            self.inner.translation.y,
            self.inner.translation.z,
            self.inner.rotation.i,
            self.inner.rotation.j,
            self.inner.rotation.k,
            self.inner.rotation.w,
        )
    }

    #[new]
    fn new<'py>(matrix: PyReadonlyArrayDyn<'py, f64>) -> PyResult<Self> {
        if matrix.shape().len() != 2 || matrix.shape()[0] != 4 || matrix.shape()[1] != 4 {
            return Err(PyValueError::new_err("Expected 4x4 matrix"));
        }

        let mut array = [0.0; 16];
        for (i, value) in matrix.as_array().iter().enumerate() {
            array[i] = *value;
        }

        let inner = iso3_try_from_array(&array)
            .map_err(|e| PyValueError::new_err(format!("Error creating Iso3: {}", e)))?;

        Ok(Self { inner })
    }

    #[staticmethod]
    fn from_translation(x: f64, y: f64, z: f64) -> Self {
        Self {
            inner: engeom::Iso3::translation(x, y, z),
        }
    }

    #[staticmethod]
    fn from_rotation(angle: f64, a: f64, b: f64, c: f64) -> Self {
        let axis = engeom::UnitVec3::new_normalize(engeom::Vector3::new(a, b, c));
        let rot_vec = axis.into_inner() * angle;

        Self {
            inner: engeom::Iso3::rotation(rot_vec),
        }
    }

    fn __matmul__(&self, other: &Self) -> Self {
        Self {
            inner: self.inner * other.inner,
        }
    }

    fn inverse(&self) -> Self {
        Self {
            inner: self.inner.inverse(),
        }
    }

    fn clone_matrix<'py>(&self, py: Python<'py>) -> Bound<'py, PyArrayDyn<f64>> {
        let mut result = ArrayD::zeros(vec![4, 4]);
        let m = self.inner.to_matrix();
        // TODO: In a rush, fix this later
        result[[0, 0]] = m.m11;
        result[[0, 1]] = m.m12;
        result[[0, 2]] = m.m13;
        result[[0, 3]] = m.m14;
        result[[1, 0]] = m.m21;
        result[[1, 1]] = m.m22;
        result[[1, 2]] = m.m23;
        result[[1, 3]] = m.m24;
        result[[2, 0]] = m.m31;
        result[[2, 1]] = m.m32;
        result[[2, 2]] = m.m33;
        result[[2, 3]] = m.m34;
        result[[3, 0]] = m.m41;
        result[[3, 1]] = m.m42;
        result[[3, 2]] = m.m43;
        result[[3, 3]] = m.m44;
        result.into_pyarray(py)
    }

    #[staticmethod]
    fn identity() -> Self {
        Self {
            inner: engeom::Iso3::identity(),
        }
    }

    fn flip_around_x(&self) -> Self {
        Self {
            inner: self.inner.flip_around_x(),
        }
    }

    fn flip_around_y(&self) -> Self {
        Self {
            inner: self.inner.flip_around_y(),
        }
    }

    fn flip_around_z(&self) -> Self {
        Self {
            inner: self.inner.flip_around_z(),
        }
    }

    fn transform_points<'py>(
        &self,
        py: Python<'py>,
        points: PyReadonlyArrayDyn<'py, f64>,
    ) -> PyResult<Bound<'py, PyArrayDyn<f64>>> {
        let points = array_to_points3(&points.as_array())?;
        let mut result = ArrayD::zeros(vec![points.len(), 3]);

        for (i, point) in points.iter().enumerate() {
            let transformed = self.inner * point;
            result[[i, 0]] = transformed.x;
            result[[i, 1]] = transformed.y;
            result[[i, 2]] = transformed.z;
        }

        Ok(result.into_pyarray(py))
    }

    fn transform_vectors<'py>(
        &self,
        py: Python<'py>,
        vectors: PyReadonlyArrayDyn<'py, f64>,
    ) -> PyResult<Bound<'py, PyArrayDyn<f64>>> {
        let vectors = array_to_vectors3(&vectors.as_array())?;
        let mut result = ArrayD::zeros(vec![vectors.len(), 3]);

        for (i, vector) in vectors.iter().enumerate() {
            let transformed = self.inner * vector;
            result[[i, 0]] = transformed.x;
            result[[i, 1]] = transformed.y;
            result[[i, 2]] = transformed.z;
        }

        Ok(result.into_pyarray(py))
    }
}
