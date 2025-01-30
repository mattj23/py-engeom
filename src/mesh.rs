use crate::common::DeviationMode;
use crate::conversions::{array_to_faces, array_to_points3};
use engeom;
use engeom::common::points::dist;
use engeom::common::SplitResult;
use numpy::ndarray::{Array1, ArrayD};
use numpy::{IntoPyArray, PyArray1, PyArrayDyn, PyReadonlyArrayDyn, PyUntypedArrayMethods};
use pyo3::exceptions::{PyIOError, PyValueError};
use pyo3::prelude::*;
use std::path::{Path, PathBuf};
use crate::geom3::{Iso3, Plane3};

#[pyclass]
pub struct Mesh {
    inner: engeom::Mesh,
}

impl Mesh {
    pub fn get_inner(&self) -> &engeom::Mesh {
        &self.inner
    }
}

#[pymethods]
impl Mesh {
    #[new]
    fn new<'py>(
        vertices: PyReadonlyArrayDyn<'py, f64>,
        triangles: PyReadonlyArrayDyn<'py, u32>,
    ) -> PyResult<Self> {
        let vertices = array_to_points3(&vertices.as_array())?;
        let triangles = array_to_faces(&triangles.as_array())?;
        let mesh = engeom::Mesh::new(vertices, triangles, false);
        Ok(Self { inner: mesh })
    }

    #[staticmethod]
    fn load_stl(path: PathBuf) -> PyResult<Self> {
        let mesh =
            engeom::io::read_mesh_stl(&path).map_err(|e| PyIOError::new_err(e.to_string()))?;
        Ok(Self { inner: mesh })
    }

    fn transform_by(&mut self, iso: &Iso3) {
        self.inner.transform(iso.get_inner());
    }

    fn append(&mut self, other: &Mesh) -> PyResult<()> {
        self.inner
            .append(&other.inner)
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    fn clone(&self) -> Self {
        Self {
            inner: self.inner.clone(),
        }
    }

    fn write_stl(&self, path: PathBuf) -> PyResult<()> {
        engeom::io::write_mesh_stl(&path, &self.inner)
            .map_err(|e| PyIOError::new_err(e.to_string()))
    }

    fn clone_vertices<'py>(&self, py: Python<'py>) -> Bound<'py, PyArrayDyn<f64>> {
        let mut result = ArrayD::zeros(vec![self.inner.vertices().len(), 3]);
        for (i, point) in self.inner.vertices().iter().enumerate() {
            result[[i, 0]] = point.x;
            result[[i, 1]] = point.y;
            result[[i, 2]] = point.z;
        }
        result.into_pyarray(py)
    }

    fn clone_triangles<'py>(&self, py: Python<'py>) -> Bound<'py, PyArrayDyn<u32>> {
        let mut result = ArrayD::zeros(vec![self.inner.triangles().len(), 3]);
        for (i, triangle) in self.inner.triangles().iter().enumerate() {
            result[[i, 0]] = triangle[0];
            result[[i, 1]] = triangle[1];
            result[[i, 2]] = triangle[2];
        }

        result.into_pyarray(py)
    }

    fn __repr__(&self) -> String {
        format!(
            "<Mesh {} points, {} faces>",
            self.inner.vertices().len(),
            self.inner.triangles().len()
        )
    }

    fn split(&self, plane: &Plane3) -> PyResult<(Option<Mesh>, Option<Mesh>)> {
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

    fn deviation<'py>(
        &self,
        py: Python<'py>,
        points: PyReadonlyArrayDyn<'py, f64>,
        mode: DeviationMode,
    ) -> PyResult<Bound<'py, PyArray1<f64>>> {
        let points = array_to_points3(&points.as_array())?;
        let mut result = Array1::zeros(points.len());

        for (i, point) in points.iter().enumerate() {
            let closest = self.inner.surf_closest_to(point);
            let normal_dev = closest.scalar_projection(point);

            result[i] = match mode {
                // Copy the sign of the normal deviation
                DeviationMode::Absolute => dist(&closest.point, point) * normal_dev.signum(),
                DeviationMode::Normal => normal_dev,
            }
        }

        Ok(result.into_pyarray(py))
    }

    fn sample_poisson<'py>(&self, py: Python<'py>, radius: f64) -> Bound<'py, PyArrayDyn<f64>> {
        let sps = self.inner.sample_poisson(radius);
        let mut result = ArrayD::zeros(vec![sps.len(), 6]);
        for (i, sp) in sps.iter().enumerate() {
            result[[i, 0]] = sp.point.x;
            result[[i, 1]] = sp.point.y;
            result[[i, 2]] = sp.point.z;
            result[[i, 3]] = sp.normal.x;
            result[[i, 4]] = sp.normal.y;
            result[[i, 5]] = sp.normal.z;
        }
        result.into_pyarray(py)
    }
}
