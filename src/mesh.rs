use crate::primitives::Plane;
use engeom;
use engeom::common::SplitResult;
use engeom::utility::slice_to_points;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;

#[pyclass]
pub struct Mesh {
    inner: engeom::Mesh,
}

#[pymethods]
impl Mesh {
    #[new]
    fn new(vertices: Vec<[f64; 3]>, triangles: Vec<[u32; 3]>) -> PyResult<Self> {
        let vertices = slice_to_points(&vertices);
        let mesh = engeom::Mesh::new(vertices, triangles, false);
        Ok(Self { inner: mesh })
    }

    fn vertices(&self) -> Vec<[f64; 3]> {
        self.inner
            .vertices()
            .iter()
            .map(|v| v.coords.into())
            .collect()
    }

    fn triangles(&self) -> Vec<[u32; 3]> {
        self.inner.triangles().iter().map(|t| (*t).into()).collect()
    }

    fn __repr__(&self) -> String {
        format!(
            "<engeom::Mesh {} points, {} faces>",
            self.inner.vertices().len(),
            self.inner.triangles().len()
        )
    }

    fn split(&self, plane: &Plane) -> PyResult<(Option<Mesh>, Option<Mesh>)> {
        match self.inner.split(&plane.inner) {
            SplitResult::Pair(mesh1, mesh2) => {
                Ok((Some(Mesh { inner: mesh1 }), Some(Mesh { inner: mesh2 })))
            }
            SplitResult::Negative => Ok((
                Some(Mesh {
                    inner: self.inner.clone(),
                }),
                None,
            )),
            SplitResult::Positive => Ok((
                None,
                Some(Mesh {
                    inner: self.inner.clone(),
                }),
            )),
        }
    }
}
