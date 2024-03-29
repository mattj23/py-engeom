mod mesh_wrapper;
use pyo3::prelude::*;
use mesh_wrapper::Mesh;

#[pymodule]
fn pyengeom(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<Mesh>()?;

    Ok(())
}
