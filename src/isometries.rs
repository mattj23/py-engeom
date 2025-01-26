use engeom;
use pyo3::exceptions::{PyTypeError, PyValueError};
use pyo3::prelude::*;

#[pyclass]
pub struct Iso2 {
    inner: engeom::Iso2,
}

#[pymethods]
impl Iso2 {
    #[new]
    fn new(x: f64, y: f64, r: f64) -> Self {
        // let t = engeom::Iso2::from_parts(
        //     engeom::Iso2::
        // )
        todo!()
    }
}
