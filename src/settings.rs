/*
 * Author: Dylan Turner
 * Description: Keep app settings in one place
 */

use clap::{
    Arg, Command, ArgMatches,
    crate_version
};

pub fn settings() -> ArgMatches {
    Command::new("bgrm")
        .version(crate_version!())
        .author("Dylan Turner <dylantdmt@gmail.com>")
        .about("WebCam background removal")
        .arg(
            Arg::new("title")
                .short('t')
                .long("title")
                .takes_value(true)
                .help("Title of popup window")
                .default_value("Feeds")
        )
        .arg(
            Arg::new("start_x")
                .short('x')
                .long("start_x")
                .takes_value(true)
                .help("Horizontal start position of the window")
                .default_value("1000")
        )
        .arg(
            Arg::new("start_y")
                .short('y')
                .long("start_y")
                .takes_value(true)
                .help("Vertical start position of the window")
                .default_value("300")
        )
        .arg(
            Arg::new("camera")
                .short('c')
                .long("camera")
                .takes_value(true)
                .help("Input camera that will have its background removed")
                .default_value("0")
        )
        .arg(
            Arg::new("width")
                .short('w')
                .long("width")
                .takes_value(true)
                .help("Width of camera output.")
                .default_value("1280")
        )
        .arg(
            Arg::new("height")
                .short('H')
                .long("height")
                .takes_value(true)
                .help("Height of camera output")
                .default_value("960")
        )
        .arg(
            Arg::new("thresh")
                .short('T')
                .long("thresh")
                .takes_value(true)
                .help("Threshold for how strong the background removal is")
                .default_value(".4")
        )
        .arg(
            Arg::new("scale")
                .short('s')
                .long("scale")
                .takes_value(true)
                .help("How much larger/smaller the window is than camera size")
                .default_value(".5")
        )
        .arg(
            Arg::new("bg")
                .short('b')
                .long("bg")
                .takes_value(true)
                .help("Image to replace background with")
                .default_value("")
        )
        .arg(
            Arg::new("blur")
                .long("blur")
                .takes_value(false)
                .help("Optionally blur the background instead")
        )
        .arg(
            Arg::new("disable_window")
                .long("disable_window")
                .takes_value(false)
                .help("Don't show a popup window")
        ).arg(
            Arg::new("no_modprobe")
                .long("no_modprobe")
                .takes_value(false)
                .help("Don't call modprobe")
        ).get_matches()
}
