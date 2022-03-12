/*
 * Author: Dylan Turner
 * Description: Handle OpenCV processing of camera feed
 */

use opencv::{
    core::Mat,
    videoio::VideoCapture,
    prelude::{
        VideoCaptureTrait, BackgroundSubtractor, BackgroundSubtractorGMG
    }, bgsegm::create_background_subtractor_gmg
};
use clap::ArgMatches;

pub struct Cam {
    settings: ArgMatches,
    vid_feed: VideoCapture,
    subtractor: Box<dyn BackgroundSubtractorGMG>
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
            0, 0
        ).expect("Failed to create video feed!");

        let mut subtractor = create_background_subtractor_gmg(
            30, settings.value_of("thresh").unwrap().parse::<f64>().expect(
                "Could not parse threshold value!"
            )
        ).expect("Failed to create background subtracter!");

        Cam {
            settings: settings.clone(),
            vid_feed,
            subtractor: Box::new(subtractor)
        }
    }

    pub fn get_frame(&mut self, bg_img: &Option<Mat>) -> (Mat, Mat) {
        let mut frame = Mat::default();
        self.vid_feed.read(&mut frame).expect("Failed to get frame.");
        let mut no_bg_frame = Mat::default();
        /*self.subtractor.apply(&frame, &mut no_bg_frame, -1.0).expect(
            "Failed to remove background!"
        );*/
        if bg_img.is_none() {
            
        }
        
        (frame, no_bg_frame)
    }
}
