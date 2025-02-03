use crate::geom2::{Circle2, Curve2, Point2};
use pyo3::{pyclass, pyfunction, pymethods, IntoPyObject, PyResult};
use pyo3::exceptions::PyValueError;
// ================================================================================================
// Inscribed Circle
// ================================================================================================

#[pyclass]
#[derive(Clone)]
pub struct InscribedCircle {
    inner: engeom::airfoil::InscribedCircle,
}

impl InscribedCircle {
    pub fn get_inner(&self) -> &engeom::airfoil::InscribedCircle {
        &self.inner
    }

    pub fn from_inner(inner: engeom::airfoil::InscribedCircle) -> Self {
        Self { inner }
    }
}

#[pymethods]
impl InscribedCircle {

    #[getter]
    fn circle(&self) -> Circle2 {
        Circle2::from_inner(self.inner.circle.clone())
    }

    #[getter]
    fn contact_a(&self) -> Point2 {
        Point2::from_inner(self.inner.upper.clone())
    }

    #[getter]
    fn contact_b(&self) -> Point2 {
        Point2::from_inner(self.inner.lower.clone())
    }
}

// ================================================================================================
// Functions
// ================================================================================================

#[pyfunction]
pub fn compute_inscribed_circles(
    section: Curve2,
    refine_tol: f64,
) -> PyResult<Vec<InscribedCircle>> {
    let sec = section.get_inner();
    let hull = sec.make_hull()
        .ok_or(PyValueError::new_err("Failed to make convex hull"))?;

    let circles = engeom::airfoil::extract_camber_line(sec, &hull, Some(refine_tol))
        .map_err(|e| PyValueError::new_err(e.to_string()))?;

    let result = circles.into_iter()
        .map(|c| InscribedCircle::from_inner(c))
        .collect();

    Ok(result)
}
