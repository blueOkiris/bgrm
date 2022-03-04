/*
 * Author: Dylan Turner
 * Description: Handle OpenCV processing of camera feed
 */

use opencv::{
    core::Mat,
    videoio::VideoCapture,
    prelude::VideoCaptureTrait
};
use clap::ArgMatches;
use pyo3::{
    Python, PyResult, prepare_freethreaded_python,
    types::{
        PyList, PyModule
    }
};

pub struct Cam {
    settings: ArgMatches,
    vid_feed: VideoCapture
}

/*
 * Later we'll import the python to get selfi segmentation:
 * 
 * import sys
 * sys.path.append('/opt/.bgrm/.venv/lib/site-packages/')
 * from cvzone import stackImages
 * from cvzone.SelfiSegmentationModule import SelfiSegmentation
 */

const VIRT_ENV_PATH: &'static str = "/opt/.bgrm/.venv/lib/site-packages/";

impl Cam {
    pub fn new(settings: &ArgMatches) -> Cam {
        let vid_feed = VideoCapture::new(
            settings.value_of("camera").unwrap().parse::<i32>().expect(
                "Invalid '--camera' provided!"
            ), 0
        ).expect("Failed to create video feed!");

        Cam {
            settings: settings.clone(),
            vid_feed
        }
    }

    pub fn get_frame(&mut self, bg_img: &Option<Mat>) -> (Mat, Mat) {
        let mut frame: Mat = Mat::default();
        self.vid_feed.read(&mut frame).expect("Failed to get frame.");

        let no_bg_frame: PyResult<Mat> = if bg_img.is_none() {
            // Just remove background
            let frame_clone = frame.clone();
            prepare_freethreaded_python();
            Python::with_gil(move |py| {
                // Add our virtual env to path
                let sys = py.import("sys")?;
                let path: &PyList = sys.getattr("path")?.extract()?;
                path.append(VIRT_ENV_PATH)?;
                sys.setattr("path", path)?;

                // Use the cvzone library
                let segment_mod: &PyModule =
                    py.import("cvzone.SelfiSegmentationModule")?.extract()?;
                let selfi_segment =
                    segment_mod.getattr("SelfiSegmentation")?;
                selfi_segment.call0()?;

                // Remove the bg with the library
                let arg_list = PyList::new(py, Vec::new());
                arg_list.call_method1("insert", (0, frame));
                selfi_segment.call_method1(
                    "removeBG", arg_list
                )?;

                Ok(frame_clone)
            })
        } else {
            // Replace background
            let frame_clone = frame.clone();
            prepare_freethreaded_python();
            Python::with_gil(move |py| {
                let sys = py.import("sys")?;
                let path = sys.getattr("version")?;

                Ok(frame_clone)
            })
        };
        
        (frame, no_bg_frame.expect("Failed to remove background!"))
    }
}
