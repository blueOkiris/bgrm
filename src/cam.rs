/*
 * Author: Dylan Turner
 * Description: Handle OpenCV processing of camera feed
 */

use opencv::{
    core::Mat,
    videoio::{
        VideoCapture, CAP_ANY, VideoCaptureTraitConst
    }, prelude::{
        VideoCaptureTrait, BackgroundSubtractorMOG2
    }, video::create_background_subtractor_mog2,
    highgui::{
        imshow, wait_key
    }, 
    Result
};
use clap::ArgMatches;

pub struct Cam {
    settings: ArgMatches,
    vid_feed: VideoCapture,
    subtractor: Box<dyn BackgroundSubtractorMOG2>
}

impl Cam {
    pub fn new(settings: &ArgMatches) -> Result<Cam> {
        let vid_feed = VideoCapture::new(
            settings.value_of("camera").unwrap().parse::<i32>().expect(
                "Invalid '--camera' provided!"
            ), CAP_ANY
        )?;
        if !VideoCapture::is_opened(&vid_feed)? {
            panic!("Unable to open camera!");
        }

        let subtractor = create_background_subtractor_mog2(
            1000, settings.value_of("thresh").unwrap().parse::<f64>().expect(
                "Could not parse threshold value!"
            ), true
        )?;

        Ok(Cam {
            settings: settings.clone(),
            vid_feed,
            subtractor: Box::new(subtractor)
        })
    }

    pub fn get_frame(&mut self, bg_img: &Option<Mat>) -> Result<(Mat, Mat)> {
        let mut frame = Mat::default();
        self.vid_feed.read(&mut frame)?;
        let mut no_bg_frame = Mat::default();
        BackgroundSubtractorMOG2::apply(
            self.subtractor.as_mut(), &frame, &mut no_bg_frame, -1.0
        )?;
        if bg_img.is_none() {
            
        }
        
        Ok((frame, no_bg_frame))
    }

    pub fn display(&self, stack_frame: &Mat) -> Result<bool> {
        imshow(self.settings.value_of("title").unwrap(), stack_frame)?;
        // WARNING: Do not optimize. It doesn't work lol
        if wait_key(1)? & 0xFF == b'q'.into() {
            return Ok(false);
        }
        Ok(true)
    }
}
