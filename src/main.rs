/*
 * Author: Dylan Turner
 * Description: Load modules and start application
 */

mod settings;
mod cam;

use opencv::{
    imgproc::{
        resize
    }, imgcodecs::{
        imread
    }, prelude::MatTraitConst,
    core::{
        copy_make_border, Size_, BORDER_CONSTANT, Mat, Range, VecN
    }
};
use clap::ArgMatches;
use crate::settings::settings;

fn main() {
    let settings = settings();

    // Set a background image if one was provided
    let mut bg_img = None;
    if settings.value_of("bg").unwrap() != String::from("") {
        bg_img = Some(get_correctly_sized_bg(&settings.clone()))
    }

    //let cam = Camera::from_settings(&settings.clone());
    //TODO: let virt_cam = open /dev/video10 for writing BINARILY
    //format_virt_cam(&settings.clone(), virt_cam)

    loop {
        //let (frame, mut no_bg_frame) = cam.get_frame(&settings.clone());
        /*
        // Reapply background, but blurred, if blur enabled
        if settings.blur {
            let rmvd_bg = frame - no_bg_frame;
            let blurred = gaussian_blur(rmvd_bg, (77, 77), 21);
            no_bg_frame += blurred;
        }*/

        // Write to virtual camera
        //virt_cam.write(cvt_color(no_bg_frame, COLOR_BGR2YUV_I420)

        // Display
        //let stack_frame = cam.stack_frames(frame, no_bg_frame)
        /*if !cam.display(stack_frame)
            break;
        }*/
    }
}

fn get_correctly_sized_bg(settings: &ArgMatches) -> Mat {
    let mut bg_img = imread(settings.value_of("bg").unwrap(), 0).expect(
        "Invalid '--bg' provided!"
    );

    // Get width and height from cli
    let screen_height_str = settings.value_of("height").unwrap();
    let screen_height = screen_height_str.parse::<u32>().expect(
        "Invalid '--height' provided. Reason: Not an unsigned integer!"
    );
    let screen_width_str = settings.value_of("width").unwrap();
    let screen_width = screen_width_str.parse::<u32>().expect(
        "Invalid '--width' provided. Reason: Not an unsigned integer!"
    );

    // Scale to match y and be centered
    let (bg_height, bg_width) = (bg_img.rows(), bg_img.cols());
    let aspect = bg_width as f32 / bg_height as f32;
    let new_width = (screen_height as f32 * aspect) as i32;
    resize(
        &bg_img.clone(), &mut bg_img.clone(),
        Size_::new(new_width, screen_height as i32),
        0.0, 0.0, 0
    ).expect(
        "Failed to resize background image to meet specs!"
    );

    // Scale down
    let mut start_x = 0;
    if new_width > screen_width as i32 {
        start_x = (new_width - screen_width as i32) / 2;
        let end_x = new_width - start_x;
        bg_img = bg_img
            .row_range(&Range::new(0, screen_height as i32).unwrap()).expect(
                "Failed to format bg image to correct height!"
            ).col_range(&Range::new(start_x, end_x).unwrap()).expect(
                "Failed to format bg image to correct width!"
            );
    } else {
        let padding = (screen_width as i32 - new_width) / 2;
        copy_make_border(
            &bg_img.clone(), &mut bg_img.clone(),
            0, 0, padding, padding, BORDER_CONSTANT,
            VecN::new(0.0, 0.0, 0.0, 0.0)
        ).expect("Failed to add border to bg image!");
    }

    bg_img
}
