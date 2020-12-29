#!/usr/bin/python3
'''
This module does the conversion
of ASCII text files into images

Credits to original authors KobeJohn for the text_image function:
https://stackoverflow.com/users/377366/kobejohn

'''

import PIL
import PIL.Image
import PIL.ImageFont
import PIL.ImageOps
import PIL.ImageDraw
import cv2
import numpy as np

PIXEL_ON = 255  # PIL color to use for "on"
PIXEL_OFF = 0  # PIL color to use for "off"


def text_image(text_path, font_path=None):
    '''Convert text file to a grayscale image with black characters on a white background.

    arguments:
    text_path - the content of this file will be converted to an image
    font_path - path to a font file (for example impact.ttf)
    '''
    grayscale = 'L'
    # parse the file into lines
    with open(text_path) as text_file:  # can throw FileNotFoundError
        lines = tuple(l.rstrip() for l in text_file.readlines())

    # choose a font (you can see more detail in my library on github)
    large_font = 20  # get better resolution with larger size
    # Courier New. works in windows.
    font_path = font_path or '../tests/anonymous.ttf'
    try:
        font = PIL.ImageFont.truetype(font_path, size=large_font)
    except IOError:
        font = PIL.ImageFont.load_default()
        print('Could not use chosen font. Using default.')

    # make the background image based on the combination of font and lines
    # convert points to pixels
    def pt2px(pt): return int(round(pt * 96.0 / 72))
    max_width_line = max(lines, key=lambda s: font.getsize(s)[0])
    # max height is adjusted down because it's too large visually for spacing
    test_string = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    max_height = pt2px(font.getsize(test_string)[1])
    max_width = pt2px(font.getsize(max_width_line)[0])
    height = max_height * len(lines)  # perfect or a little oversized
    width = int(round(max_width + 40))  # a little oversized
    image = PIL.Image.new(grayscale, (width, height), color=PIXEL_OFF)
    draw = PIL.ImageDraw.Draw(image)

    # draw each line of text
    vertical_position = 5
    horizontal_position = 5
    line_spacing = int(round(max_height * 0.8))  # reduced spacing seems better
    for line in lines:
        draw.text((horizontal_position, vertical_position),
                  line, fill=PIXEL_ON, font=font)
        vertical_position += line_spacing

    # crop the text

    c_box = PIL.ImageOps.invert(image).getbbox()
    image = image.crop(c_box)

    return image


def main():
    '''
    A main function if moduled is called alone.
    '''
    image = text_image('../tests/hello_world.txt')
    image.show()
    image.save('../tests/hello_world.png')


if __name__ == '__main__':
    main()
