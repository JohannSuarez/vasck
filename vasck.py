#!/usr/bin/python3
'''
The main module of the vasck package.
'''
import os
import argparse
import shutil
import cv2

from modules.vid2jpg import frame_extract
from modules.colorizer import BColors as fontc


def folders_manager():
    '''
    Manages the folders required
    for the operations. If they're there, folders are cleaned.
    If not, the folders are created.
    '''
    if not os.path.isdir("jpeg_images"):
        print(
            fontc.YELLOW + "Creating folder: jpeg_images. This will contain \
            the jpegs to be converted to ASCII" +
            fontc.ENDC)
        os.mkdir("jpeg_images")
    else:
        print("jpeg_images directory found. Clearing contents..")
        shutil.rmtree('jpeg_images/')
        os.mkdir("jpeg_images")


def main():
    '''
    The main function.

    Resposibilities:
        - Check that the inputs are valid.
        - Call upon the modules jpg2ascii.py and vid2jpg.py
        -
    '''

    # What are the arguments?
    # Input video, size percentage compared to original video.
    # Third argument will be for background.
    # If not provided, text will be white against black background.

    # Once the input is determined to be valid
    # Create a directory called jpeg_images
    # Use vid2jpg.py's function to start conversion.

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "vid_input",
        help="Any video as input (avi or mp4)")
    parser.add_argument(
        "vsize_perc",
        help="The output GIF's size (in percentage) relative to \
        the orginal input. (i.e. 40 will make the gif) forty percent \
        of the original video size). \
        \nPut 100 for default size.")
    parser.add_argument(
        "background",
        help="An optional background for the text that will be used \
        against the text, to give the font color.\
        \nPut 0 for white text and black background.")

    user_input = parser.parse_args()

    folders_manager()

    jpeg_images_count = frame_extract(
        user_input.vid_input, "jpeg_images")

    print(
        fontc.CYAN +
        "Jpeg images counted: " +
        fontc.ENDC +
        str(jpeg_images_count))


if __name__ == "__main__":
    main()
