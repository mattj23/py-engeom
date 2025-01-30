pub mod alignments;
mod common;
mod conversions;
mod geom2;
mod geom3;
mod isometries;
mod mesh;
mod primitives;
mod svd_basis;

use numpy::{IntoPyArray, PyUntypedArrayMethods};
use pyo3::prelude::*;

/// Geometry in 2D space.
fn register_geom2<'py>(py: Python<'py>, parent_module: &Bound<'_, PyModule>) -> PyResult<()> {
    let mut child = PyModule::new(parent_module.py(), "_geom2")?;
    child.add_class::<geom2::Iso2>()?;
    child.add_class::<geom2::Vector2>()?;
    child.add_class::<geom2::Point2>()?;

    child.add_class::<svd_basis::SvdBasis2>()?;
    parent_module.add_submodule(&child)
}

/// Geometry in 3D space.
fn register_geom3<'py>(py: Python<'py>, parent_module: &Bound<'_, PyModule>) -> PyResult<()> {
    let mut child = PyModule::new(parent_module.py(), "_geom3")?;

    // Primitive geometry types
    child.add_class::<geom3::Iso3>()?;
    child.add_class::<geom3::Vector3>()?;
    child.add_class::<geom3::Point3>()?;
    child.add_class::<geom3::Plane3>()?;

    // Mesh, curves, other complex geometries
    child.add_class::<mesh::Mesh>()?;

    child.add_class::<svd_basis::SvdBasis3>()?;

    parent_module.add_submodule(&child)
}

/// Engeom is a library for geometric operations in 2D and 3D space.
#[pymodule(name = "engeom")]
fn py_engeom<'py>(py: Python<'py>, m: &Bound<'_, PyModule>) -> PyResult<()> {
    // 2D geometry submodule
    register_geom2(py, m)?;

    // 3D geometry submodule
    register_geom3(py, m)?;

    // Alignment submodule
    register_align_module(py, m)?;

    // Common features and primitives
    m.add_class::<common::DeviationMode>()?;

    Ok(())
}

fn register_align_module<'py>(
    py: Python<'py>,
    parent_module: &Bound<'_, PyModule>,
) -> PyResult<()> {
    let mut child = PyModule::new(parent_module.py(), "_align")?;
    child.add_function(wrap_pyfunction!(alignments::points_to_mesh, &child)?)?;
    parent_module.add_submodule(&child)
}
