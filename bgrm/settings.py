# Author: Dylan Turner
# Description: Keep app settings in one place

from typing import Tuple
from dataclasses import dataclass
from argparse import ArgumentParser
from subprocess import run, PIPE

@dataclass
class AppSettings:
    virt_dev: int
    camera: int
    screen_width: int
    screen_height: int
    view_scale: float
    rm_thresh: float
    fill_color: Tuple[float, float, float]
    bg_img: str
    blur: bool
    disable_win: bool
    file_mode: bool
    input_file: str
    output_file: str
    fps: int

    @staticmethod
    def from_cli():
        virt_dev = pull_virt_dev()
        args = cli_args()

        # Convert fill color from string to tuple
        fill_col = args.color.split(',')
        if len(fill_col) != 3:
            print('Failed to parse fill color argument \'' + args.color + '\'')
            raise SettingsError
        fill_col = tuple([ float(e) for e in fill_col ])

        return AppSettings(
            virt_dev, args.camera, args.width, args.height, args.scale,
            args.thresh, fill_col, args.bg, args.blur, args.disable_window,
            args.file_mode, args.input, args.output, args.fps
        )

# Get video settings from command line
def pull_virt_dev():
    shell_result = run(
        [ 'ls', '/sys/devices/virtual/video4linux' ],
        stderr = PIPE, stdout = PIPE, text = True
    )
    raw_devs = shell_result.stdout.split('\n')
    raw_devs = list(filter(lambda elem: elem != '', raw_devs))
    
    devs = [ int(vid_str.replace('video', '')) for vid_str in raw_devs ]

    if len(devs) < 1:
        print('Failed to find virtual device! Do you have v4l2loopback set up?')
        raise SettingsError

    return devs[0]

def cli_args():
    parser = ArgumentParser()

    # Set up arguments
    parser.add_argument(
        '-c', '--camera', type = int, default = 0,
        help = 'ID of camera device to use for input'
    )
    parser.add_argument(
        '-b', '--bg', type = str, default = '',
        help = 'Background image'
    )
    parser.add_argument(
        '-T', '--thresh', type = float, default = 0.4,
        help = 'Background removal threshold'
    )
    parser.add_argument(
        '-w', '--width', type = int, default = 1280,
        help = 'Width of camera input'
    )
    parser.add_argument(
        '-H', '--height', type = int, default = 960,
        help = 'Height of camera input'
    )

    # Extra options
    parser.add_argument(
        '--blur', help = 'Blur background (overrides --bg)',
        action = 'store_true'
    )
    parser.add_argument(
        '--disable_window', help = 'Disable feedback window',
        action = 'store_true'
    )
    parser.add_argument(
        '-C', '--color', type = str, default = '0,0,0',
        help = 'List of R, G, B to replace background with',
    )

    # File versions
    parser.add_argument(
        '--file_mode',
        help = 'Remove the background from video files instead of cameras (overrides --camera)',
        action = 'store_true'
    )
    parser.add_argument(
        '-i', '--input', type = str, default = '',
        help = 'Only used with file mode. Input file to remove background',
    )
    parser.add_argument(
        '-o', '--output', type = str, default = '',
        help = 'Only used with file mode. Output file to store removed background feed.'
    )
    parser.add_argument(
        '-f', '--fps', type = int, default = 30,
        help = 'Only used with file mode. Output file fps'
    )

    # Mostly useless window options
    parser.add_argument(
        '-s', '--scale', type = float, default = 0.5,
        help = 'Scale factor from camera size to window.'
    )

    return parser.parse_args()

