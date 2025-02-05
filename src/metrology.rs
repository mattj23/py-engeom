use crate::geom2::{Point2, SurfacePoint2, Vector2};
use engeom::metrology::Dimension;
use engeom::UnitVec2;
use pyo3::prelude::*;

#[pyclass]
pub struct Length2 {
    inner: engeom::metrology::Length2,
}

impl Length2 {
    pub fn get_inner(&self) -> &engeom::metrology::Length2 {
        &self.inner
    }

    pub fn from_inner(inner: engeom::metrology::Length2) -> Self {
        Self { inner }
    }
}

#[pymethods]
impl Length2 {
    #[new]
    #[pyo3(signature=(a, b, direction = None))]
    pub fn new(a: Point2, b: Point2, direction: Option<Vector2>) -> Self {
        let d = direction.map(|v| UnitVec2::new_normalize(*v.get_inner()));
        Self::from_inner(engeom::metrology::Length2::new(
            *a.get_inner(),
            *b.get_inner(),
            d,
        ))
    }

    #[getter]
    pub fn value(&self) -> f64 {
        self.inner.value()
    }

    #[getter]
    pub fn a(&self) -> Point2 {
        Point2::from_inner(self.inner.a)
    }

    #[getter]
    pub fn b(&self) -> Point2 {
        Point2::from_inner(self.inner.b)
    }

    #[getter]
    pub fn direction(&self) -> Vector2 {
        Vector2::from_inner(self.inner.direction.into_inner())
    }

    #[getter]
    pub fn center(&self) -> SurfacePoint2 {
        SurfacePoint2::from_inner(self.inner.center())
    }

    fn reversed(&self) -> Self {
        Self::from_inner(self.inner.reversed())
    }
}
