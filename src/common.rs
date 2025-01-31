use engeom::common::DistMode;
use pyo3::prelude::*;

#[pyclass(eq, eq_int)]
#[derive(PartialEq, Copy, Clone, Debug)]
pub enum DeviationMode {
    Point,
    Plane,
}

impl From<DeviationMode> for DistMode {
    fn from(val: DeviationMode) -> Self {
        match val {
            DeviationMode::Point => DistMode::ToPoint,
            DeviationMode::Plane => DistMode::ToPlane,
        }
    }
}

#[pyclass]
#[derive(Copy, Clone, Debug)]
pub enum Resample {
    Count(usize),
    Spacing(f64),
    MaxSpacing(f64),
}

#[pymethods]
impl Resample {
    fn __repr__(&self) -> String {
        match self {
            Resample::Count(count) => format!("Resample.Count({})", count),
            Resample::Spacing(spacing) => format!("Resample.Spacing({})", spacing),
            Resample::MaxSpacing(max_spacing) => {
                format!("Resample.MaxSpacing({})", max_spacing)
            }
        }
    }
}

impl From<Resample> for engeom::common::Resample {
    fn from(val: Resample) -> Self {
        match val {
            Resample::Count(count) => engeom::common::Resample::ByCount(count),
            Resample::Spacing(spacing) => engeom::common::Resample::BySpacing(spacing),
            Resample::MaxSpacing(max_spacing) => {
                engeom::common::Resample::ByMaxSpacing(max_spacing)
            }
        }
    }
}
