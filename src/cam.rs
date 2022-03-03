/*
 * Author: Dylan Turner
 * Description: Handle OpenCV processing of camera feed
 */

use opencv::{
    videoio::VideoCapture
};
use clap::ArgMatches;

struct Cam {
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
}
