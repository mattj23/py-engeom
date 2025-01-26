mod isometries;
mod mesh;
mod primitives;

use pyo3::prelude::*;

/// A Python module implemented in Rust.
#[pymodule]
// #[pyo3(name = "engeom")]
fn py_engeom(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<primitives::Plane>()?;
    m.add_class::<isometries::Iso2>()?;
    m.add_class::<mesh::Mesh>()?;

    Ok(())
}
