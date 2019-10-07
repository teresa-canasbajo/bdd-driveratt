from pupil_apriltags import Detector, Detection
from collections import defaultdict
from typing import List, Dict, Tuple, Any
from glob import glob
import numpy as np

import cv2

### Change paths to match yours ###
test_folder_path = '/Users/richardliu/Documents/BDD/bdd-driveratt/eye_tracking/analysis/test' # Change filepath
video_path = '/Users/richardliu/Downloads/world.mp4' # Change filepath
frames_path = '/Users/richardliu/Documents/BDD/bdd-driveratt/eye_tracking/analysis/surfaceTest' # Change filepath (also make sure this directory exists)

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
        # Createa grayscale 2D NumPy array for Detector.detect()
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        if type(img) == np.ndarray:
            # Optional print statement
            print(f'Analyzing file: {img_path}')

            for tag in at_detector.detect(img):
                # Increment frequency
                tag_ids[tag.tag_id] += 1

                # Add to frames in following format - feel free to adjust
                frames.append({
                    'id': tag.tag_id,
                    'centroid': tag.center,
                    'verts': tag.corners
                })

    return frames, tag_ids

# Convert video to frames
extract_frames(video_path, frames_path)

# Detect tags in frames
frames, tag_ids = detect_tags(frames_path)

# Descriptive print statements
tag_count = sum(count for count in tag_ids.values())
print(f'Detected {tag_count} tags in {len(frames)} frames.')
print(f'Found IDs of {list(tag_ids.keys())}.')
