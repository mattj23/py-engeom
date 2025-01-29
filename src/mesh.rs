use crate::primitives::Plane;
use engeom;
use engeom::common::points::dist;
use engeom::common::SplitResult;
use engeom::utility::slice_to_points;
use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use crate::common::DeviationMode;

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

    fn deviation(&self, points: Vec<[f64; 3]>, mode: DeviationMode) -> PyResult<Vec<f64>> {
        let points = slice_to_points(&points);
        let mut result = Vec::new();

        for point in points.iter() {
            let closest = self.inner.surf_closest_to(point);
            result.push(match mode {
                DeviationMode::Absolute => dist(&closest.point, point),
                DeviationMode::Normal => closest.scalar_projection(point),
            })
        }

        Ok(result)
    }

}
