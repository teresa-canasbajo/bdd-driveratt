from eye_tracking.preprocessing.functions.manual_detection import *
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
import cv2

# demo = '/home/whitney/Downloads/frame7473.png'
demo = '/media/whitney/New Volume/Teresa/frames'

frame, corners, tag_ids = detect_tags(demo)

print('done!')
