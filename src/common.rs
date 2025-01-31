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

#[pyclass]
#[derive(Copy, Clone, Debug)]
pub enum Resample {
    ByCount(usize),
    BySpacing(f64),
    ByMaxSpacing(f64),
}

#[pymethods]
impl Resample {
    fn __repr__(&self) -> String {
        match self {
            Resample::ByCount(count) => format!("Resample.ByCount({})", count),
            Resample::BySpacing(spacing) => format!("Resample.BySpacing({})", spacing),
            Resample::ByMaxSpacing(max_spacing) => {
                format!("Resample.ByMaxSpacing({})", max_spacing)
            }
        }
    }
}

impl Into<engeom::common::Resample> for Resample {
    fn into(self) -> engeom::common::Resample {
        match self {
            Resample::ByCount(count) => engeom::common::Resample::ByCount(count),
            Resample::BySpacing(spacing) => engeom::common::Resample::BySpacing(spacing),
            Resample::ByMaxSpacing(max_spacing) => {
                engeom::common::Resample::ByMaxSpacing(max_spacing)
            }
        }
    }
}
