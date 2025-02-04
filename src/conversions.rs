//! This module has conversion helpers for numpy arrays and other engeom types

use engeom::{Point2, Point3, Vector2, Vector3};
use numpy::ndarray::{ArrayD, ArrayViewD};
use pyo3::exceptions::PyValueError;
use pyo3::PyResult;

pub fn points_to_array3(points: &[Point3]) -> ArrayD<f64> {
    let mut array = ArrayD::zeros(vec![points.len(), 3]);
    for (i, point) in points.iter().enumerate() {
        array[[i, 0]] = point.x;
        array[[i, 1]] = point.y;
        array[[i, 2]] = point.z;
    }
    array
}

pub fn points_to_array2(points: &[Point2]) -> ArrayD<f64> {
    let mut array = ArrayD::zeros(vec![points.len(), 2]);
    for (i, point) in points.iter().enumerate() {
        array[[i, 0]] = point.x;
        array[[i, 1]] = point.y;
    }
    array
}

pub fn faces_to_array(faces: &[[u32; 3]]) -> ArrayD<u32> {
    let mut array = ArrayD::zeros(vec![faces.len(), 3]);
    for (i, face) in faces.iter().enumerate() {
        array[[i, 0]] = face[0];
        array[[i, 1]] = face[1];
        array[[i, 2]] = face[2];
    }
    array
}


pub fn array_to_faces(array: &ArrayViewD<'_, u32>) -> PyResult<Vec<[u32; 3]>> {
    let shape = array.shape();
    if shape.len() != 2 || shape[1] != 3 {
        return Err(PyValueError::new_err("Expected Nx3 array of faces"));
    }

    Ok(array
        .rows()
        .into_iter()
        .map(|row| [row[0], row[1], row[2]])
        .collect())
}

pub fn array_to_points3(array: &ArrayViewD<'_, f64>) -> PyResult<Vec<Point3>> {
    let shape = array.shape();
    if shape.len() != 2 || shape[1] != 3 {
        return Err(PyValueError::new_err("Expected Nx3 array of points"));
    }

    Ok(array
        .rows()
        .into_iter()
        .map(|row| Point3::new(row[0], row[1], row[2]))
        .collect())
}

pub fn array_to_vectors3(array: &ArrayViewD<'_, f64>) -> PyResult<Vec<Vector3>> {
    let shape = array.shape();
    if shape.len() != 2 || shape[1] != 3 {
        return Err(PyValueError::new_err("Expected Nx3 array of vectors"));
    }

    Ok(array
        .rows()
        .into_iter()
        .map(|row| Vector3::new(row[0], row[1], row[2]))
        .collect())
}

pub fn array_to_points2(array: &ArrayViewD<'_, f64>) -> PyResult<Vec<Point2>> {
    let shape = array.shape();
    if shape.len() != 2 || shape[1] != 2 {
        return Err(PyValueError::new_err("Expected Nx2 array of points"));
    }

    Ok(array
        .rows()
        .into_iter()
        .map(|row| Point2::new(row[0], row[1]))
        .collect())
}

pub fn array_to_vectors2(array: &ArrayViewD<'_, f64>) -> PyResult<Vec<Vector2>> {
    let shape = array.shape();
    if shape.len() != 2 || shape[1] != 2 {
        return Err(PyValueError::new_err("Expected Nx2 array of vectors"));
    }

    Ok(array
        .rows()
        .into_iter()
        .map(|row| Vector2::new(row[0], row[1]))
        .collect())
}
