#!/usr/bin/python3
'''
The main module of the vasck package.
'''
import os
import argparse
import shutil
import subprocess

from modules.vid2jpg import frame_extract
from modules.colors import BColors as fontc
from modules.ascii2png import text_image


def cleanup():
    '''
    Removes all the files required during the operation.
    Leaves behind the final output.
    '''

    shutil.rmtree("jpeg_images")
    shutil.rmtree("ascii")


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

    if not os.path.isdir("ascii_pngs"):
        print(
            fontc.YELLOW + "Creating folder: ascii_pngs. This will contain \
            the jpegs to be converted to ASCII" +
            fontc.ENDC)
        os.mkdir("ascii_pngs")
    else:
        print("ascii_pngs directory found. Clearing contents..")
        shutil.rmtree('ascii_pngs/')
        os.mkdir("ascii_pngs")


def main():
    '''
    The main function.

    Resposibilities:
        - Check that the inputs are valid.
        - Call upon the modules jpg2ascii.py and vid2jpg.py
    '''

    # First argument will be vid input
    # Second argument will be for background.
    # If not provided, text will be white against black background.

    # Once the input is determined to be valid
    # Create a directory called jpeg_images
    # Use vid2jpg.py's function to start conversion.

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "vid_input",
        help="Any video as input (avi or mp4)")
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

    subprocess.run("modules/jpg2ascii.sh")

    for txt_file in range(jpeg_images_count):
        # text images retuns an image, and its second
        # parameter is for the font.
        # You have to save it from here.
        image = text_image('ascii/'+str(txt_file)+'.txt',
                           'tests/anonymous.ttf')

        print("Saving " + str(txt_file)+'.png ..')
        image.save('ascii_pngs/'+str(txt_file)+'.png')

    print("Cleaning...")
    cleanup()


if __name__ == "__main__":
    main()
