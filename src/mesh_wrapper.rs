use pyo3::prelude::*;
use pyo3::exceptions::PyValueError;

type _Mesh = engeom::geom3::Mesh;

#[pyclass]
pub struct Mesh {
    mesh: _Mesh
}


#[pymethods]
impl Mesh {

    #[staticmethod]
    fn read_stl(path: &str) -> PyResult<Self> {
        let path = std::path::Path::new(path);
        match _Mesh::read_stl(path) {
            Ok(mesh) => Ok(Self { mesh }),
            Err(e) => Err(PyValueError::new_err(e.to_string()))
        }

    }

    // fn vertices(&self) -> Vec<Vec<f64>> {
    //     self.mesh.vertices().iter().map(|v| v.coords.into()).collect()
    // }
    //
    fn faces(&self) -> Vec<[u32; 3]> {
        self.mesh.faces().iter().map(|f| *f).collect()
    }
}