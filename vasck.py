#!/usr/bin/python3
'''
The main module of the vasck package.
'''
import os
import argparse
import shutil
import subprocess
import cv2

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


def png2mp4(vidin):
    '''
    Function that converts the sequence of pngs to mp4's.
    '''

    # Get FPS of inputted bw video.
    cap = cv2.VideoCapture(vidin)
    fps = cap.get(cv2.CAP_PROP_FPS)

    image_folder = 'ascii_pngs'
    video_name = 'final_output.avi'

    # Preparing all variables required to write a video using the f_out frames.
    images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
    frame = cv2.imread(os.path.join(image_folder, images[0]))
    height, width, layers = frame.shape
    video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(
        *'XVID'), fps, (width, height))

    # The list is initially unsorted, this is to fix that.
    images = sorted(images, key=lambda x: int(x[0:-4]))

    for image in images:
        video.write(cv2.imread(os.path.join(image_folder, image)))

    cv2.destroyAllWindows()
    video.release()


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
        help="Any video as input (avi, mp4, or webm)")
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

        i = "Saving " + str(txt_file) + '.png..'
        print(i, end='\r')
        image.save('ascii_pngs/'+str(txt_file)+'.png')

    print()
    print("Cleaning...")
    cleanup()

    print("Creating video...")
    png2mp4(user_input.vid_input)


if __name__ == "__main__":
    main()
