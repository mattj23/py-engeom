use pyo3::prelude::*;

#[pyclass]
#[derive(Copy, Clone, Debug)]
pub enum DeviationMode {
    Absolute,
    Normal,
}
