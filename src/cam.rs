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
