from pupil_apriltags import Detector, Detection
from collections import defaultdict
from typing import List, Dict, Tuple, Any
from glob import glob
import numpy as np
import os

import cv2

# Define path folder
# test path 1 from 10/7 simulator recording - not all tags are id b/c lighting
# path = "/home/whitney/Teresa/demos/surfaceTestUpdatedTags/001"
# test path 2 from 10/7 simulator recording - not all tags are id b/c lighting
# path = "/home/whitney/Teresa/demos/surfaceTestUpdatedTags/002"
# test path 3 from prev recording at desk with reflection - all tags id success
# path = '/home/whitney/Teresa/bdd-driveratt/eye_tracking/analysis'
# test path to id tags
# path = '/home/whitney/Teresa/demos/idtags/013'
# test path 4 from 10/8 recording at lab
path = '/home/whitney/Teresa/demos/surfaceTestUpdatedTagsLab/014'

# Create video path
video_path = path + "/world.mp4"
# Create frame path using OS package
# Define the name of the directory to be created
frames_path = path + "/frames"
try:
    os.mkdir(frames_path)
except OSError:
    print("Creation of the directory %s failed" % frames_path)
else:
    print("Successfully created the directory %s " % frames_path)


def extract_frames(video_path: str, frames_path: str) -> None:
    """Convert a video (mp4 or similar) into a series of individual PNG frames.
    Make sure to create a directory to store the frames before running this function.
    Args:
        video_path (str): filepath to the video being converted
        frames_path (str): filepath to the target directory that will contain the extract frames
    """
    video = cv2.VideoCapture(video_path)
    count = 0
    success = 1

    # Basically just using OpenCV's tools
    while success:
        success, frame = video.read()
        cv2.imwrite(f'{frames_path}/frame{count}.png', frame)
        count += 1

    # Optional print statement
    print(f'Extracted {count} frames from {video_path}.')


def detect_tags(frames_path: str) -> Tuple[List[Dict[str, Any]], Dict[int, int]]:
    """Detect all tags (Apriltags3) found in a folder of PNG files and return (1) a list of tag objects
    for preprocessing and (2) a dictionary containing the frequency that each tag ID appeared
    Args:
        frames_path (str): path to the directory containing PNG images

    Returns:
        frames (List[Dict[str, Any]]): list of objects containing id (int), centroid (np.array[int]) and corners (np.array[int])
        tag_ds (Dict[int, int]): dictionary mapping tag IDs to frequency of tag across all images
    """
    # Initialize variables
    frames = []
    tag_ids = defaultdict(int)
    at_detector = Detector()

    # Iterate thru all PNG images in frames_path
    for img_path in glob(f'{frames_path}/*.png'):
        # Create a grayscale 2D NumPy array for Detector.detect()
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        if type(img) == np.ndarray:
            # Optional print statement
            print(f'Analyzing file: {img_path}')

            tags_in_framex = []
            for tag in at_detector.detect(img):
                # Increment frequency
                tag_ids[tag.tag_id] += 1

                # Add to frames in following format - feel free to adjust
                tags_in_framex.append({
                    'id': tag.tag_id,
                    'centroid': tag.center,
                    'verts': tag.corners
                })
            frames.append(tags_in_framex)

    return frames, tag_ids


# Convert video to frames
extract_frames(video_path, frames_path)

# Detect tags in frames
frames, tag_ids = detect_tags(frames_path)

# Descriptive print statements
tag_count = sum(count for count in tag_ids.values())
print(f'Detected {tag_count} tags in {len(frames)} frames.')
print(f'Found IDs of {list(tag_ids.keys())}.')

