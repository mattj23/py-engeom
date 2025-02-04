use crate::geom2::{Circle2, Curve2, Point2};
use engeom::airfoil::EdgeLocation;
use numpy::ndarray::ArrayD;
use numpy::{IntoPyArray, PyArrayDyn};
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use pyo3::IntoPyObjectExt;

// ================================================================================================
// Orientation Methods
// ================================================================================================
#[pyclass]
#[derive(Clone, Copy, Debug)]
pub enum MclOrient {
    TmaxFwd {},
    DirFwd { x: f64, y: f64 },
}

#[pymethods]
impl MclOrient {
    fn __repr__(&self) -> String {
        match self {
            MclOrient::TmaxFwd {} => "MclOrient.TmaxFwd".to_string(),
            MclOrient::DirFwd { x, y } => format!("MclOrient.DirFwd({}, {})", x, y),
        }
    }
}

impl From<MclOrient> for Box<dyn engeom::airfoil::CamberOrientation> {
    fn from(value: MclOrient) -> Self {
        match value {
            MclOrient::TmaxFwd {} => engeom::airfoil::TMaxFwd::make(),
            MclOrient::DirFwd { x, y } => {
                engeom::airfoil::DirectionFwd::make(engeom::Vector2::new(x, y))
            }
        }
    }
}

// ================================================================================================
// Edge Extraction Methods
// ================================================================================================
#[pyclass]
#[derive(Clone, Copy, Debug)]
pub enum EdgeFind {
    Open {},
    OpenIntersect { max_iter: usize },
    Intersect {},
    RansacRadius { in_tol: f64, n: usize },
}

#[pymethods]
impl EdgeFind {
    fn __repr__(&self) -> String {
        match self {
            EdgeFind::Open {} => "EdgeFind.Open".to_string(),
            EdgeFind::OpenIntersect { max_iter } => format!("EdgeFind.OpenIntersect({})", max_iter),
            EdgeFind::Intersect {} => "EdgeFind.Intersect".to_string(),
            EdgeFind::RansacRadius { in_tol, n } => {
                format!("EdgeFind.RansacRadius({}, {})", in_tol, n)
            }
        }
    }
}

impl From<EdgeFind> for Box<dyn EdgeLocation> {
    fn from(value: EdgeFind) -> Self {
        use engeom::airfoil;

        match value {
            EdgeFind::Open {} => airfoil::OpenEdge::make(),
            EdgeFind::OpenIntersect { max_iter } => airfoil::OpenIntersectGap::make(max_iter),
            EdgeFind::Intersect {} => airfoil::IntersectEdge::make(),
            EdgeFind::RansacRadius { in_tol, n } => airfoil::RansacRadiusEdge::make(in_tol, n),
        }
    }
}

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
// Airfoil geometry result
// ================================================================================================
#[pyclass]
pub struct AirfoilGeometry {
    inner: engeom::airfoil::AirfoilGeometry,
    camber: Option<Py<Curve2>>,
    circle_array: Option<Py<PyArrayDyn<f64>>>,
}

impl AirfoilGeometry {
    pub fn get_inner(&self) -> &engeom::airfoil::AirfoilGeometry {
        &self.inner
    }

    pub fn from_inner(inner: engeom::airfoil::AirfoilGeometry) -> Self {
        Self { inner, camber: None, circle_array: None }
    }
}

impl Clone for AirfoilGeometry {
    fn clone(&self) -> Self {
        Self::from_inner(self.inner.clone())
    }
}

#[pymethods]
impl AirfoilGeometry {
    #[getter]
    fn camber<'py>(&mut self, py: Python<'py>) -> &Bound<'py, Curve2> {
        if self.camber.is_none() {
            let camber = Curve2::from_inner(self.inner.camber.clone());
            self.camber = Some(Py::new(py, camber).unwrap());
        }
        self.camber.as_ref().unwrap().bind(py)
    }

    #[getter]
    fn circle_array<'py>(&mut self, py: Python<'py>) -> &Bound<'py, PyArrayDyn<f64>> {
        if self.circle_array.is_none() {
            let mut result = ArrayD::zeros(vec![self.inner.stations.len(), 3]);
            for (i, c) in self.inner.stations.iter().enumerate() {
                result[[i, 0]] = c.circle.center.x;
                result[[i, 1]] = c.circle.center.y;
                result[[i, 2]] = c.circle.r();
            }
            self.circle_array = Some(result.into_pyarray(py).unbind());
        }
        self.circle_array.as_ref().unwrap().bind(py)
    }
}

// ================================================================================================
// Functions
// ================================================================================================
#[pyfunction]
pub fn compute_airfoil_geometry(
    section: Curve2,
    refine_tol: f64,
    orient: MclOrient,
    leading: EdgeFind,
    trailing: EdgeFind,
) -> PyResult<AirfoilGeometry> {
    // Construct the parameters
    let params =
        engeom::airfoil::AfParams::new(refine_tol, orient.into(), leading.into(), trailing.into());

    let result = engeom::airfoil::analyze_airfoil_geometry(section.get_inner(), &params)
        .map_err(|e| PyValueError::new_err(e.to_string()))?;

    Ok(AirfoilGeometry::from_inner(result))
}

#[pyfunction]
pub fn compute_inscribed_circles(
    section: Curve2,
    refine_tol: f64,
) -> PyResult<Vec<InscribedCircle>> {
    let sec = section.get_inner();
    let hull = sec
        .make_hull()
        .ok_or(PyValueError::new_err("Failed to make convex hull"))?;

    let circles = engeom::airfoil::extract_camber_line(sec, &hull, Some(refine_tol))
        .map_err(|e| PyValueError::new_err(e.to_string()))?;

    let result = circles
        .into_iter()
        .map(|c| InscribedCircle::from_inner(c))
        .collect();

    Ok(result)
}
