use crate::bounding::Aabb3;
use crate::common::DeviationMode;
use crate::conversions::{array_to_faces, array_to_points3, faces_to_array, points_to_array3};
use crate::geom3::{Curve3, Iso3, Plane3};
use engeom::common::points::dist;
use engeom::common::SplitResult;
use numpy::ndarray::{Array1, ArrayD};
use numpy::{IntoPyArray, PyArray1, PyArrayDyn, PyReadonlyArrayDyn};
use pyo3::exceptions::{PyIOError, PyValueError};
use pyo3::prelude::*;
use std::path::PathBuf;

#[pyclass]
pub struct Mesh {
    inner: engeom::Mesh,
    points: Option<Py<PyArrayDyn<f64>>>,
    triangles: Option<Py<PyArrayDyn<u32>>>,
}

impl Mesh {
    pub fn get_inner(&self) -> &engeom::Mesh {
        &self.inner
    }

    pub fn from_inner(inner: engeom::Mesh) -> Self {
        Self {
            inner,
            points: None,
            triangles: None,
        }
    }
}

impl Clone for Mesh {
    fn clone(&self) -> Self {
        Self::from_inner(self.inner.clone())
    }
}

#[pymethods]
impl Mesh {
    #[new]
    #[pyo3(signature=(vertices, triangles, merge_duplicates = false, delete_degenerate = false))]
    fn new<'py>(
        vertices: PyReadonlyArrayDyn<'py, f64>,
        triangles: PyReadonlyArrayDyn<'py, u32>,
        merge_duplicates: bool,
        delete_degenerate: bool,
    ) -> PyResult<Self> {
        let vertices = array_to_points3(&vertices.as_array())?;
        let triangles = array_to_faces(&triangles.as_array())?;
        let mesh = engeom::Mesh::new_with_options(
            vertices,
            triangles,
            false,
            merge_duplicates,
            delete_degenerate,
            None,
        )
        .map_err(|e| PyValueError::new_err(e.to_string()))?;

        Ok(Self::from_inner(mesh))
    }

    #[getter]
    fn aabb(&self) -> Aabb3 {
        Aabb3::from_inner(self.inner.aabb())
    }

    #[staticmethod]
    #[pyo3(signature=(path, merge_duplicates = false, delete_degenerate = false))]
    fn load_stl(path: PathBuf, merge_duplicates: bool, delete_degenerate: bool) -> PyResult<Self> {
        let mesh = engeom::io::read_mesh_stl(&path, merge_duplicates, delete_degenerate)
            .map_err(|e| PyIOError::new_err(e.to_string()))?;

        Ok(Self::from_inner(mesh))
    }

    fn transform_by(&mut self, iso: &Iso3) {
        self.inner.transform(iso.get_inner());
    }

    fn append(&mut self, other: &Mesh) -> PyResult<()> {
        self.inner
            .append(&other.inner)
            .map_err(|e| PyValueError::new_err(e.to_string()))
    }

    fn cloned(&self) -> Self {
        self.clone()
    }

    fn write_stl(&self, path: PathBuf) -> PyResult<()> {
        engeom::io::write_mesh_stl(&path, &self.inner)
            .map_err(|e| PyIOError::new_err(e.to_string()))
    }

    #[getter]
    fn points<'py>(&mut self, py: Python<'py>) -> &Bound<'py, PyArrayDyn<f64>> {
        if self.points.is_none() {
            let array = points_to_array3(self.inner.vertices());
            self.points = Some(array.into_pyarray(py).unbind());
        }
        self.points.as_ref().unwrap().bind(py)
    }

    #[getter]
    fn triangles<'py>(&mut self, py: Python<'py>) -> &Bound<'py, PyArrayDyn<u32>> {
        if self.triangles.is_none() {
            let faces = faces_to_array(self.inner.triangles());
            self.triangles = Some(faces.into_pyarray(py).unbind());
        }

        self.triangles.as_ref().unwrap().bind(py)
    }

    fn __repr__(&self) -> String {
        format!(
            "<Mesh {} points, {} faces>",
            self.inner.vertices().len(),
            self.inner.triangles().len()
        )
    }

    fn split(&self, plane: &Plane3) -> PyResult<(Option<Self>, Option<Self>)> {
        match self.inner.split(&plane.inner) {
            SplitResult::Pair(mesh1, mesh2) => {
                Ok((Some(Self::from_inner(mesh1)), Some(Self::from_inner(mesh2))))
            }
            SplitResult::Negative => Ok((Some(self.clone()), None)),
            SplitResult::Positive => Ok((None, Some(self.clone()))),
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
                DeviationMode::Point => dist(&closest.point, point) * normal_dev.signum(),
                DeviationMode::Plane => normal_dev,
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

    #[pyo3(signature=(plane, tol = None))]
    fn section(&self, plane: Plane3, tol: Option<f64>) -> PyResult<Vec<Curve3>> {
        let results = self
            .inner
            .section(plane.get_inner(), tol)
            .map_err(|e| PyValueError::new_err(e.to_string()))?;

        Ok(results.into_iter().map(Curve3::from_inner).collect())
    }
}
