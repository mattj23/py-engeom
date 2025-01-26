use engeom;
use pyo3::exceptions::{PyTypeError, PyValueError};
use pyo3::prelude::*;

#[pyclass]
pub struct Plane {
    pub inner: engeom::Plane3,
}

#[pymethods]
impl Plane {
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
            "<engeom::Plane3 normal=({}, {}, {}), d={}>",
            self.inner.normal.x, self.inner.normal.y, self.inner.normal.z, self.inner.d
        )
    }
}
