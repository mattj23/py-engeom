use pyo3::prelude::*;
use numpy::ndarray::{Array1, ArrayD};
use numpy::{IntoPyArray, PyArray1, PyArrayDyn, PyReadonlyArrayDyn, PyUntypedArrayMethods};
use pyo3::exceptions::PyValueError;
use crate::common::DeviationMode;
use crate::conversions::array_to_points3;
use crate::isometries::Iso3;
use crate::mesh::Mesh;


#[pyfunction]
pub fn points_to_mesh<'py>(
    points: PyReadonlyArrayDyn<'py, f64>,
    mesh: &Mesh,
    initial: &Iso3,
    mode: DeviationMode,
) -> PyResult<Iso3> {
    let points = array_to_points3(&points.as_array())?;

    let result = engeom::geom3::align3::points_to_mesh(
        &points,
        mesh.get_inner(),
        initial.get_inner(),
        mode.into(),
    );

    match result {
        Ok(align) => Ok(Iso3::from_inner(align.transform().clone())),
        Err(e) => Err(PyValueError::new_err(e.to_string())),
    }
}