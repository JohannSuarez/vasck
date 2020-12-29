'''
The module that colors frames.
Color data is grabbed from low-res picture.
Then blended over the low-res black and white picture.
'''

import argparse
import numpy as np
from PIL import Image, ImageEnhance
from skimage import color


class BColors:
    '''
    Color constants. This should be moved elsewhere.
    '''

    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    PURPLE = "\033[1;35m"
    YELLOW = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'



