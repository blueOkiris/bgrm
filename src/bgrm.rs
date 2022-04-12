/*
 * Author: Dylan Turner
 * Description: The actual "removal" functions. Covert data to python, call, and then get it bacl
 */

use opencv::{
    core::Mat,
    prelude::{
        MatTrait, MatTraitConstManual, MatTraitConst
    }
};
use pyo3::{
    PyResult, Python, PyAny, PyModule
};

// We need to get the opencv matrices into a numpy pyarray
//fn mat_to_numpy(mat: &Mat) -> arr

fn mat_to_arr(mat: &Mat) -> Vec<Vec<u8>> {
    let (width, height) = (mat.size().unwrap().width, mat.size().unwrap().height);
    let channels = mat.channels();
    let frame_data = mat.data();

    let mut data = Vec::new();
    for y in 0..height {
        let mut row = Vec::new();
        for x in 0..width*channels {
            unsafe {
                row.push(*(frame_data.add((y * width * channels + x) as usize)));
            }
        }
        data.push(row);
    }
    data
}

fn py_remove_bg(img: &Vec<Vec<u8>>) -> PyResult<Vec<Vec<u8>>> {
    static SEGMENTOR: Option<PyAny> = None;

    Python::with_gil(|py| {
        let rm_bg_func = PyModule::from_code(
r#"
def remove_bg(img):
"#

        Ok(Vec::new())
    })
}

pub fn remove_bg(frame: &Mat) -> Mat {
    let raw = mat_to_arr(frame);
    let raw_rm = py_remove_bg(&raw).expect("Unable to remove background.");

    frame.clone()
}
