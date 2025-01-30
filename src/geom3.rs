use crate::conversions::{
    array_to_points2, array_to_points3, array_to_vectors2, array_to_vectors3,
};
use engeom::geom3::{iso3_try_from_array, Flip3};
use numpy::ndarray::{Array1, ArrayD};
use numpy::{IntoPyArray, PyArray1, PyArrayDyn, PyReadonlyArrayDyn, PyUntypedArrayMethods};
use pyo3::exceptions::PyValueError;
use pyo3::{
    pyclass, pymethods, Bound, FromPyObject, IntoPy, IntoPyObject, PyObject, PyResult, Python,
};

#[derive(FromPyObject)]
enum Vector3OrPoint3 {
    Vector(Vector3),
    Point(Point3),
}

// ================================================================================================
// Vectors
// ================================================================================================

#[pyclass]
#[derive(Clone, Debug)]
pub struct Vector3 {
    inner: engeom::Vector3,
}

impl Vector3 {
    pub fn get_inner(&self) -> &engeom::Vector3 {
        &self.inner
    }

    pub fn from_inner(inner: engeom::Vector3) -> Self {
        Self { inner }
    }
}

#[pymethods]
impl Vector3 {
    #[new]
    fn new(x: f64, y: f64, z: f64) -> Self {
        Self {
            inner: engeom::Vector3::new(x, y, z),
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
    fn z(&self) -> f64 {
        self.inner.z
    }

    fn as_numpy<'py>(&self, py: Python<'py>) -> Bound<'py, PyArray1<f64>> {
        let mut array = Array1::zeros(3);
        array[0] = self.inner.x;
        array[1] = self.inner.y;
        array[2] = self.inner.z;
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

    fn __add__<'py>(&self, py: Python<'py>, other: Vector3OrPoint3) -> PyObject {
        match other {
            Vector3OrPoint3::Vector(other) => {
                Vector3::from_inner(self.inner + other.inner).into_py(py)
            }
            Vector3OrPoint3::Point(other) => {
                Point3::from_inner((self.inner + other.inner.coords).into()).into_py(py)
            }
        }
    }

    fn __sub__(&self, other: Vector3) -> Self {
        Self::from_inner(self.inner - other.inner)
    }

    fn __repr__(&self) -> String {
        format!(
            "Vector3({}, {}, {})",
            self.inner.x, self.inner.y, self.inner.z
        )
    }
}

// ================================================================================================
// Points
// ================================================================================================

#[pyclass]
#[derive(Clone, Debug)]
pub struct Point3 {
    inner: engeom::Point3,
}

impl Point3 {
    pub fn get_inner(&self) -> &engeom::Point3 {
        &self.inner
    }

    pub fn from_inner(inner: engeom::Point3) -> Self {
        Self { inner }
    }
}

#[pymethods]
impl Point3 {
    #[new]
    fn new(x: f64, y: f64, z: f64) -> Self {
        Self {
            inner: engeom::Point3::new(x, y, z),
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
    fn z(&self) -> f64 {
        self.inner.z
    }

    #[getter]
    fn coords(&self) -> Vector3 {
        Vector3 {
            inner: self.inner.coords,
        }
    }

    fn as_numpy<'py>(&self, py: Python<'py>) -> Bound<'py, PyArray1<f64>> {
        let mut array = Array1::zeros(3);
        array[0] = self.inner.x;
        array[1] = self.inner.y;
        array[2] = self.inner.z;
        array.into_pyarray(py)
    }

    fn __add__(&self, other: Vector3) -> Self {
        Self::from_inner(self.inner + other.inner)
    }

    fn __sub__<'py>(&self, py: Python<'py>, other: Vector3OrPoint3) -> PyObject {
        match other {
            Vector3OrPoint3::Vector(other) => {
                Point3::from_inner(self.inner - other.inner).into_py(py)
            }
            Vector3OrPoint3::Point(other) => {
                Vector3::from_inner(self.inner - other.inner).into_py(py)
            }
        }
    }

    fn __repr__(&self) -> String {
        format!(
            "Point3({}, {}, {})",
            self.inner.x, self.inner.y, self.inner.z
        )
    }
}

// ================================================================================================
// Plane
// ================================================================================================
#[pyclass]
#[derive(Clone, Debug)]
pub struct Plane3 {
    pub inner: engeom::Plane3,
}

impl Plane3 {
    pub fn get_inner(&self) -> &engeom::Plane3 {
        &self.inner
    }

    pub fn from_inner(inner: engeom::Plane3) -> Self {
        Self { inner }
    }
}

#[pymethods]
impl Plane3 {
    #[new]
    fn new(a: f64, b: f64, c: f64, d: f64) -> PyResult<Self> {
        let v = engeom::Vector3::new(a, b, c);
        let normal = engeom::UnitVec3::try_new(v, 1.0e-6)
            .ok_or(PyValueError::new_err("Invalid normal vector"))?;

        Ok(Self {
            inner: engeom::Plane3::new(normal, d),
        })
    }

    fn __repr__(&self) -> String {
        format!(
            "Plane3({}, {}, {}, {})",
            self.inner.normal.x, self.inner.normal.y, self.inner.normal.z, self.inner.d
        )
    }

    // fn transform_by(&self, iso: Iso3) -> Self {
    //     Self::from_inner(self.inner.transform_by(iso.get_inner()))
    // }

    fn inverted_normal(&self) -> Self {
        Self::from_inner(self.inner.inverted_normal())
    }

    fn signed_distance_to_point(&self, point: Point3) -> f64 {
        self.inner.signed_distance_to_point(point.get_inner())
    }

    fn project_point(&self, point: Point3) -> Point3 {
        Point3::from_inner(self.inner.project_point(point.get_inner()))
    }
}

// ================================================================================================
// Transformations
// ================================================================================================

#[derive(FromPyObject)]
enum Transformable3 {
    Iso(Iso3),
    Vec(Vector3),
    Pnt(Point3),
    Plane(Plane3),
}

#[pyclass]
#[derive(Clone, Debug)]
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

    fn inverse(&self) -> Self {
        Self {
            inner: self.inner.inverse(),
        }
    }

    fn __matmul__<'py>(&self, py: Python<'py>, other: Transformable3) -> PyObject {
        match other {
            Transformable3::Iso(other) => Iso3::from_inner(self.inner * other.inner).into_py(py),
            Transformable3::Vec(other) => Vector3::from_inner(self.inner * other.inner).into_py(py),
            Transformable3::Pnt(other) => Point3::from_inner(self.inner * other.inner).into_py(py),
            Transformable3::Plane(other) => {
                Plane3::from_inner(other.inner.transform_by(&self.inner)).into_py(py)
            }
        }
    }

    fn as_numpy<'py>(&self, py: Python<'py>) -> Bound<'py, PyArrayDyn<f64>> {
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
