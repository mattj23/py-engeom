use engeom::common::DistMode;
use pyo3::prelude::*;

#[pyclass]
#[derive(Copy, Clone, Debug)]
pub enum DeviationMode {
    Absolute,
    Normal,
}

impl Into<DistMode> for DeviationMode {
    fn into(self) -> DistMode {
        match self {
            DeviationMode::Absolute => DistMode::ToPoint,
            DeviationMode::Normal => DistMode::ToPlane,
        }
    }
}
