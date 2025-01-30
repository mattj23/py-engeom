mod common;
mod conversions;
mod isometries;
mod mesh;
mod primitives;
pub mod alignments;
mod svd_basis;

use numpy::{IntoPyArray, PyUntypedArrayMethods};
use pyo3::prelude::*;

/// Engeom is a library for geometric operations in 2D and 3D space.
#[pymodule(name="engeom")]
fn py_engeom<'py>(py: Python<'py>, m: &Bound<'_, PyModule>) -> PyResult<()> {

    // Isometries
    m.add_class::<isometries::Iso2>()?;
    m.add_class::<isometries::Iso3>()?;

    // Common features and primitives
    m.add_class::<common::DeviationMode>()?;
    m.add_class::<primitives::Plane>()?;

    // SVD Basis
    m.add_class::<svd_basis::SvdBasis2>()?;
    m.add_class::<svd_basis::SvdBasis3>()?;

    // Mesh, curves, other complex geometries
    m.add_class::<mesh::Mesh>()?;

    // Alignment submodule
    register_align_module(py, m)?;

    Ok(())
}


fn register_align_module<'py>(py: Python<'py>, parent_module: &Bound<'_, PyModule>) -> PyResult<()> {
    let mut child = PyModule::new(parent_module.py(), "align")?;

    child.add_function(wrap_pyfunction!(alignments::points_to_mesh, &child)?)?;

    parent_module.add_submodule(&child)

    // py.import("sys")?.getattr("modules")?.setattr("py_engeom.align", child)
}