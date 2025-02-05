use crate::geom2::{Point2, Vector2};
use crate::geom3::{Point3, Vector3};
use parry2d_f64::bounding_volume::BoundingVolume;
use pyo3::{pyclass, pymethods};

// ================================================================================================
// Aabb2
// ================================================================================================

#[pyclass]
#[derive(Clone, Debug)]
pub struct Aabb2 {
    inner: engeom::geom2::Aabb2,
}

impl Aabb2 {
    pub fn get_inner(&self) -> &engeom::geom2::Aabb2 {
        &self.inner
    }

    pub fn from_inner(inner: engeom::geom2::Aabb2) -> Self {
        Self { inner }
    }
}

#[pymethods]
impl Aabb2 {
    #[new]
    fn new(x_min: f64, y_min: f64, x_max: f64, y_max: f64) -> Self {
        Self {
            inner: engeom::geom2::Aabb2::new(
                engeom::Point2::new(x_min, y_min),
                engeom::Point2::new(x_max, y_max),
            ),
        }
    }

    #[staticmethod]
    #[pyo3(signature=(x, y, w, h=None))]
    fn at_point(x: f64, y: f64, w: f64, h: Option<f64>) -> Self {
        let h = h.unwrap_or(w) / 2.0;
        let w = w / 2.0;
        let p = engeom::Point2::new(x, y);
        let v = engeom::Vector2::new(w, h);

        Self {
            inner: engeom::geom2::Aabb2::new(p - v, p + v),
        }
    }

    fn __repr__(&self) -> String {
        format!(
            "Aabb2({}, {}, {}, {})",
            self.inner.mins.x, self.inner.mins.y, self.inner.maxs.x, self.inner.maxs.y,
        )
    }

    #[getter]
    fn min(&self) -> Point2 {
        Point2::from_inner(self.inner.mins)
    }

    #[getter]
    fn max(&self) -> Point2 {
        Point2::from_inner(self.inner.maxs)
    }

    #[getter]
    fn center(&self) -> Point2 {
        Point2::from_inner(self.inner.center())
    }

    #[getter]
    fn extent(&self) -> Vector2 {
        Vector2::from_inner(self.inner.extents())
    }

    fn expand(&self, d: f64) -> Self {
        Aabb2::from_inner(self.inner.loosened(d))
    }

    fn shrink(&self, d: f64) -> Self {
        Aabb2::from_inner(self.inner.tightened(d))
    }
}

// ================================================================================================
// Aabb3
// ================================================================================================

#[pyclass]
#[derive(Clone, Debug)]
pub struct Aabb3 {
    inner: engeom::geom3::Aabb3,
}

impl Aabb3 {
    pub fn get_inner(&self) -> &engeom::geom3::Aabb3 {
        &self.inner
    }

    pub fn from_inner(inner: engeom::geom3::Aabb3) -> Self {
        Self { inner }
    }
}

#[pymethods]
impl Aabb3 {
    #[new]
    fn new(x_min: f64, y_min: f64, z_min: f64, x_max: f64, y_max: f64, z_max: f64) -> Self {
        Self {
            inner: engeom::geom3::Aabb3::new(
                engeom::Point3::new(x_min, y_min, z_min),
                engeom::Point3::new(x_max, y_max, z_max),
            ),
        }
    }

    fn __repr__(&self) -> String {
        format!(
            "Aabb3({}, {}, {}, {}, {}, {})",
            self.inner.mins.x,
            self.inner.mins.y,
            self.inner.mins.z,
            self.inner.maxs.x,
            self.inner.maxs.y,
            self.inner.maxs.z
        )
    }

    #[getter]
    fn min(&self) -> Point3 {
        Point3::from_inner(self.inner.mins)
    }

    #[getter]
    fn max(&self) -> Point3 {
        Point3::from_inner(self.inner.maxs)
    }

    #[getter]
    fn center(&self) -> Point3 {
        Point3::from_inner(self.inner.center())
    }

    #[getter]
    fn extent(&self) -> Vector3 {
        Vector3::from_inner(self.inner.extents())
    }
}
