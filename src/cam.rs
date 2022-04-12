/*
 * Author: Dylan Turner
 * Description: Handle OpenCV processing of camera feed
 */

use opencv::{
    core::Mat,
    videoio::{
        VideoCapture, CAP_ANY, VideoCaptureTraitConst
    }, prelude::{
        VideoCaptureTrait
    }, highgui::{
        imshow, wait_key
    }, 
    Result
};
use clap::ArgMatches;

pub struct Cam {
    settings: ArgMatches,
    vid_feed: VideoCapture
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

        Ok(Cam {
            settings: settings.clone(),
            vid_feed
        })
    }

    pub fn get_frame(&mut self, bg_img: &Option<Mat>) -> Result<(Mat, Mat)> {
        let mut frame = Mat::default();
        self.vid_feed.read(&mut frame)?;
        let mut no_bg_frame = Mat::default();

        // TODO: Rm bg

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
