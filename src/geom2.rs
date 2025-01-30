use crate::conversions::{array_to_points2, array_to_vectors2};
use numpy::ndarray::{Array1, ArrayD};
use numpy::{IntoPyArray, PyArray1, PyArrayDyn, PyReadonlyArrayDyn};
use pyo3::{
    pyclass, pymethods, Bound, FromPyObject, IntoPy, IntoPyObject, PyObject, PyResult, Python,
};

#[derive(FromPyObject)]
enum Vector2OrPoint2 {
    Vector(Vector2),
    Point(Point2),
}

// ================================================================================================
// Vectors
// ================================================================================================

#[pyclass]
#[derive(Clone, Debug)]
pub struct Vector2 {
    inner: engeom::Vector2,
}

impl Vector2 {
    pub fn get_inner(&self) -> &engeom::Vector2 {
        &self.inner
    }

    pub fn from_inner(inner: engeom::Vector2) -> Self {
        Self { inner }
    }
}

#[pymethods]
impl Vector2 {
    #[new]
    fn new(x: f64, y: f64) -> Self {
        Self {
            inner: engeom::Vector2::new(x, y),
        }
    }

    #[getter]
    fn x(&self) -> f64 {
        self.inner.x
    }

    #[getter]
    fn y(&self) -> f64 {
        self.inner.y
    }

    fn as_numpy<'py>(&self, py: Python<'py>) -> Bound<'py, PyArray1<f64>> {
        let mut array = Array1::zeros(2);
        array[0] = self.inner.x;
        array[1] = self.inner.y;
        array.into_pyarray(py)
    }

    fn __neg__(&self) -> Self {
        Self { inner: -self.inner }
    }

    fn __mul__(&self, other: f64) -> Self {
        Self {
            inner: self.inner * other,
        }
    }

    fn __rmul__(&self, other: f64) -> Self {
        Self {
            inner: self.inner * other,
        }
    }

    fn __add__<'py>(&self, py: Python<'py>, other: Vector2OrPoint2) -> PyObject {
        match other {
            Vector2OrPoint2::Vector(other) => {
                let result = self.inner + other.inner;
                Vector2::new(result.x, result.y).into_py(py)
            }
            Vector2OrPoint2::Point(other) => {
                let result = self.inner + other.inner.coords;
                Point2::new(result.x, result.y).into_py(py)
            }
        }
    }

    fn __sub__(&self, other: Vector2) -> Self {
        Self {
            inner: self.inner - other.inner,
        }
    }

    fn __repr__(&self) -> String {
        format!("Vector2({}, {})", self.inner.x, self.inner.y)
    }
}

// ================================================================================================
// Points
// ================================================================================================

#[pyclass]
#[derive(Clone, Debug)]
pub struct Point2 {
    inner: engeom::Point2,
}

impl Point2 {
    pub fn get_inner(&self) -> &engeom::Point2 {
        &self.inner
    }

    pub fn from_inner(inner: engeom::Point2) -> Self {
        Self { inner }
    }
}

#[pymethods]
impl Point2 {
    #[new]
    fn new(x: f64, y: f64) -> Self {
        Self {
            inner: engeom::Point2::new(x, y),
        }
    }

    #[getter]
    fn x(&self) -> f64 {
        self.inner.x
    }

    #[getter]
    fn y(&self) -> f64 {
        self.inner.y
    }

    #[getter]
    fn coords(&self) -> Vector2 {
        Vector2 {
            inner: self.inner.coords,
        }
    }

    fn as_numpy<'py>(&self, py: Python<'py>) -> Bound<'py, PyArray1<f64>> {
        let mut array = Array1::zeros(2);
        array[0] = self.inner.x;
        array[1] = self.inner.y;
        array.into_pyarray(py)
    }

    fn __add__(&self, other: Vector2) -> Self {
        Self {
            inner: self.inner + other.inner,
        }
    }

    fn __sub__<'py>(&self, py: Python<'py>, other: Vector2OrPoint2) -> PyObject {
        match other {
            Vector2OrPoint2::Vector(other) => {
                let result = self.inner - other.inner;
                Point2::new(result.x, result.y).into_py(py)
            }
            Vector2OrPoint2::Point(other) => {
                let result = self.inner - other.inner.coords;
                Vector2::new(result.x, result.y).into_py(py)
            }
        }
    }

    fn __repr__(&self) -> String {
        format!("Point2({}, {})", self.inner.x, self.inner.y)
    }
}

// ================================================================================================
// Transformations
// ================================================================================================

#[derive(FromPyObject)]
enum Transformable2 {
    Iso(Iso2),
    Vec(Vector2),
    Pnt(Point2),
}

#[pyclass]
#[derive(Clone, Debug)]
pub struct Iso2 {
    inner: engeom::Iso2,
}

impl Iso2 {
    pub fn get_inner(&self) -> &engeom::Iso2 {
        &self.inner
    }

    pub fn from_inner(inner: engeom::Iso2) -> Self {
        Self { inner }
    }
}

#[pymethods]
impl Iso2 {
    #[new]
    fn new(tx: f64, ty: f64, r: f64) -> Self {
        let inner = engeom::Iso2::translation(tx, ty) * engeom::Iso2::rotation(r);
        Self { inner }
    }

    #[staticmethod]
    fn identity() -> Self {
        Self {
            inner: engeom::Iso2::identity(),
        }
    }

    fn inverse(&self) -> Self {
        Self {
            inner: self.inner.inverse(),
        }
    }

    fn __repr__(&self) -> String {
        format!(
            "Iso2({}, {}, {})",
            self.inner.translation.x,
            self.inner.translation.y,
            self.inner.rotation.angle()
        )
    }

    fn __matmul__<'py>(&self, py: Python<'py>, other: Transformable2) -> PyObject {
        match other {
            Transformable2::Iso(other) => Iso2::from_inner(self.inner * other.inner).into_py(py),
            Transformable2::Vec(other) => Vector2::from_inner(self.inner * other.inner).into_py(py),
            Transformable2::Pnt(other) => Point2::from_inner(self.inner * other.inner).into_py(py),
        }
    }

    fn as_numpy<'py>(&self, py: Python<'py>) -> Bound<'py, PyArrayDyn<f64>> {
        let mut result = ArrayD::zeros(vec![3, 3]);
        let m = self.inner.to_matrix();
        result[[0, 0]] = m.m11;
        result[[0, 1]] = m.m12;
        result[[0, 2]] = m.m13;
        result[[1, 0]] = m.m21;
        result[[1, 1]] = m.m22;
        result[[1, 2]] = m.m23;
        result[[2, 0]] = m.m31;
        result[[2, 1]] = m.m32;
        result[[2, 2]] = m.m33;
        result.into_pyarray(py)
    }

    fn transform_points<'py>(
        &self,
        py: Python<'py>,
        points: PyReadonlyArrayDyn<'py, f64>,
    ) -> PyResult<Bound<'py, PyArrayDyn<f64>>> {
        let points = array_to_points2(&points.as_array())?;
        let transformed = points.iter().map(|p| self.inner * p).collect::<Vec<_>>();
        let mut result = ArrayD::zeros(vec![transformed.len(), 2]);
        for (i, point) in transformed.iter().enumerate() {
            result[[i, 0]] = point.x;
            result[[i, 1]] = point.y;
        }
        Ok(result.into_pyarray(py))
    }

    fn transform_vectors<'py>(
        &self,
        py: Python<'py>,
        vectors: PyReadonlyArrayDyn<'py, f64>,
    ) -> PyResult<Bound<'py, PyArrayDyn<f64>>> {
        let vectors = array_to_vectors2(&vectors.as_array())?;
        let transformed = vectors.iter().map(|v| self.inner * v).collect::<Vec<_>>();
        let mut result = ArrayD::zeros(vec![transformed.len(), 2]);
        for (i, vector) in transformed.iter().enumerate() {
            result[[i, 0]] = vector.x;
            result[[i, 1]] = vector.y;
        }
        Ok(result.into_pyarray(py))
    }
}
