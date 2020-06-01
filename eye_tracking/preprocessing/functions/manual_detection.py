from pupil_apriltags import Detector, Detection
from collections import defaultdict
from typing import List, Dict, Tuple, Any
from glob import glob
import os
import time
import sys
import numpy as np
import cv2
import pandas as pd


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

def detect_tags_and_surfaces(frames_path: str, tags = [0, 1, 2, 3, 5, 6, 7, 8, 9, 11], aperture=11, visualize=False) -> Tuple[List[List[Dict[str, Any]]], Dict[int, int], pd.DataFrame]:
    """Detect all tags (Apriltags3) & surfaces found in a folder of PNG files and return (1) a list of tag objects
    for preprocessing, (2) a dictionary containing the frequency that each tag ID appeared, (3) a dataframe
    consisting of all surface coordinates associated with each frame
    Args:
        frames_path (str): path to the directory containing PNG images
        tags (int):
        aperture (int):
        visualize (bool):

    Returns:
        frames (List[Dict[str, Any]]): list of objects containing id (int), centroid (np.array[int]) and corners (np.array[int])
        tag_ids (Dict[int, int]): dictionary mapping tag IDs to frequency of tag across all images
        coordinates_df (DataFrame): dataframe that lists the coordinates of the corners & center
    """
    # Initialize variables
    frames = []
    tag_ids = defaultdict(int)
    at_detector = Detector()

    img_n_total = []
    starting_frame = False
    img_n = []
    top_left_corner = []
    top_right_corner = []
    bottom_left_corner = []
    bottom_right_corner = []
    center = []
    norm_top_left_corner_x = []
    norm_top_right_corner_x = []
    norm_bottom_left_corner_x = []
    norm_bottom_right_corner_x = []
    norm_center_x = []
    norm_top_left_corner_y = []
    norm_top_right_corner_y = []
    norm_bottom_left_corner_y = []
    norm_bottom_right_corner_y = []
    norm_center_y = []

    bounding_box_frames_path = frames_path + "/bounding_box_frames"

    # Sort by index in.../frame<index>.png
    all_images = sorted(glob(f'{frames_path}/*.png'), key=lambda f: int(os.path.basename(f)[5:-4]))

    # Deleted last image after out of range error popped up
    # TODO: but not analyzing last 2 frames?
    # print(len(all_images))
    if len(all_images) > 1:
        all_images = all_images[:-1]

    num_images = len(all_images)
    # print_progress_bar(0, num_images, prefix='Progress:', suffix='Complete', length=50)

    # Iterate thru all PNG images in frames_path
    for i, img_path in enumerate(all_images):
        # Create a grayscale 2D NumPy array for Detector.detect()
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        if type(img) == np.ndarray:
            tags_in_framex = []
            for tag in at_detector.detect(img):
                # Increment frequency
                tag_ids[tag.tag_id] += 1
                # r = np.roll(np.float32(img), tag.homography + 1, axis=0)
                # Add to frames in following format - feel free to adjust
                tags_in_framex.append({
                    'id': tag.tag_id,
                    'id_confidence': tag.decision_margin,
                    'soft_id': tag.tag_id,
                    'perimeter': 100, #cv2.arcLength(img, closed=True),
                    'centroid': tag.center,
                    'verts': tag.corners,
                    'frames_since_true_detection': 0
                })

                # {'id': msg, 'id_confidence': id_confidence, 'verts': r.tolist(), 'soft_id': soft_msg,
                #  'perimeter': cv2.arcLength(r, closed=True), 'centroid': centroid.tolist(),
                #  "frames_since_true_detection": 0}
            frames.append(tags_in_framex)

        # all frame numbers
        head, tail = os.path.split(img_path)
        img_n_total.append(int(''.join(list(filter(str.isdigit, tail)))))

        # detect surfaces once the first frame with all tags are identified
        if len(tags_in_framex) == 10:
            starting_frame = True

        if starting_frame:
            # frame number
            img_n.append(int(''.join(list(filter(str.isdigit, tail)))))

            # define surface
            tl, tr, bl, br, c, norm_tl, norm_tr, norm_bl, norm_br, norm_c = surface_coordinates(frames, img_path, tags, bounding_box_frames_path)
            top_left_corner.append(tl)
            top_right_corner.append(tr)
            bottom_left_corner.append(bl)
            bottom_right_corner.append(br)
            center.append(c)
            norm_top_left_corner_x.append(norm_tl[0])
            norm_top_right_corner_x.append(norm_tr[0])
            norm_bottom_left_corner_x.append(norm_bl[0])
            norm_bottom_right_corner_x.append(norm_br[0])
            norm_center_x.append(norm_c[0])
            norm_top_left_corner_y.append(norm_tl[1])
            norm_top_right_corner_y.append(norm_tr[1])
            norm_bottom_left_corner_y.append(norm_bl[1])
            norm_bottom_right_corner_y.append(norm_br[1])
            norm_center_y.append(norm_c[1])

        time.sleep(0.01)
        print_progress_bar(i + 1, num_images, prefix='Progress:', suffix='Complete', length=50)

    # match world timestamps to appropriate frame
    head, tail = os.path.split(frames_path)
    timestamps_path = os.path.join(head, 'world_timestamps.npy')
    a = np.load(timestamps_path)
    t = {'Image': img_n_total, 'Timestamp': a}
    timestamp = []
    for i in img_n:
        x = t['Image'].index(i)
        timestamp.append(t['Timestamp'][x-1])

    # coordinates dataframe output
    bb_coords = {'image': img_n,
                 'timestamp': timestamp,
                 # 'top_left': top_left_corner,
                 # 'bottom_left': bottom_left_corner,
                 # 'bottom_right': bottom_right_corner,
                 # 'top_right': top_right_corner,
                 # 'center': center,
                 'norm_top_left_x': norm_top_left_corner_x,
                 'norm_bottom_left_x': norm_bottom_left_corner_x,
                 'norm_bottom_right_x': norm_bottom_right_corner_x,
                 'norm_top_right_x': norm_top_right_corner_x,
                 'norm_center_x': norm_center_x,
                 'norm_top_left_y': norm_top_left_corner_y,
                 'norm_bottom_left_y': norm_bottom_left_corner_y,
                 'norm_bottom_right_y': norm_bottom_right_corner_y,
                 'norm_top_right_y': norm_top_right_corner_y,
                 'norm_center_y': norm_center_y
                 }
    coordinates_df = pd.DataFrame(bb_coords)
    # coordinates_df.to_csv(os.path.join(frames_path, 'coordinates.csv'), index=False)

    return frames, dict(tag_ids), coordinates_df

#function that gets what attribute is of the dictionary generated by detect tags a user needs
#for instance, I needed the centers of each tag and the corners to crop the image, so this function acquires tgem from the
#return call of detect tags
def attribute(frame, feature):
    qr_codes = frame
    attributes = []
    for i in range(len(qr_codes)):
        qr_code = qr_codes[i]
        attributes.append(qr_code[feature])
    return attributes

def coordinates(frame, tag):
    for f in frame:
        id = attribute(f, 'id')

        # extrapolate coordinates from prev coordinates if it doesn't exist
        while len(id) < len(tag):
            id.append('None')

        # attains the corners for each of the QR codes in the frame; not sorted in any order
        corners = attribute(f, 'verts')
        # bottom left corners[x][0]
        # bottom right corners[x][1]
        # top right corners[x][2]
        # top left corners[x][3]

        centers = attribute(f, 'centroid')

        # coordinates to create the rectangle
        if tag[0] in id:
            i = id.index(tag[0])
            top_left = corners[i][3]
        if tag[5] in id:
            i = id.index(tag[5])
            bottom_right = corners[i][1]

        # coordinates to create the horizontal line
        if tag[1] in id:
            i = id.index(tag[1])
            left = centers[i]
        if tag[6] in id:
            i = id.index(tag[6])
            right = centers[i]

        # coordinates to create the vertical line
        if tag[3] in id:
            i = id.index(tag[3])
            bottom_center_left = centers[i]
        if tag[4] in id:
            i = id.index(tag[4])
            bottom_center_right = centers[i]
        if tag[8] in id:
            i = id.index(tag[8])
            top_center_right = centers[i]
        if tag[9] in id:
            i = id.index(tag[9])
            top_center_left = centers[i]

        # other tags
        if tag[2] in id:
            i = id.index(tag[2])
            bottom_left = corners[i][0]
        if tag[7] in id:
            i = id.index(tag[7])
            top_right = corners[i][2]

        # coordinates = [top_left, left, bottom_left, bottom_center_left, bottom_center_right,
        #                 bottom_right, right, top_right, top_center_right, top_center_left]

    return top_left, left, bottom_center_left, bottom_left, bottom_center_right, bottom_right, right, top_right, top_center_right, top_center_left

def surface_coordinates(frame, img_path, tag, bounding_box_frames_path):

    top_left, left, bottom_center_left, bottom_left, bottom_center_right, bottom_right, right, top_right, top_center_right, top_center_left = coordinates(frame, tag)

    tl = tuple(top_left.astype(int))
    tr = tuple(top_right.astype(int))
    br = tuple(bottom_right.astype(int))
    bl = tuple(bottom_left.astype(int))
    l = tuple(left.astype(int))
    r = tuple(right.astype(int))

    bottom_midpoint = (((bottom_center_right[0] + bottom_center_left[0]) / 2).astype(int),
                       ((bottom_center_right[1] + bottom_center_left[1]) / 2).astype(int))
    top_midpoint = (((top_center_right[0] + top_center_left[0]) / 2).astype(int),
                    ((top_center_right[1] + top_center_left[1]) / 2).astype(int))

    center = intersection([l, r], [bottom_midpoint, top_midpoint])

    img = cv2.imread(img_path, cv2.IMREAD_COLOR)

    # for normalization calculations
    height = img.shape[0]
    width = img.shape[1]
    norm_tl = normalize(tl, width, height)
    norm_tr = normalize(tr, width, height)
    norm_bl = normalize(bl, width, height)
    norm_br = normalize(br, width, height)
    norm_center = normalize(center, width, height)

    red = (0, 0, 255)
    thickness = 2

    cv2.rectangle(img, tl, br, red, thickness) # rectangle

    cv2.line(img, l, r, red, thickness) # horizontal line
    cv2.line(img, bottom_midpoint, top_midpoint, red, thickness) # vertical line
    cv2.circle(img, center, 2, (0, 255, 255), 8)  # point in the center of the screen

    head, tail = os.path.split(img_path)
    cv2.imwrite(bounding_box_frames_path + "/" + tail, img)

    return tl, tr, bl, br, center, norm_tl, norm_tr, norm_bl, norm_br, norm_center

def normalize(coord, width, height):
    x = coord[0]/width
    y = coord[1]/height
    return (x, y)

def intersection(L1, L2):
    xdiff = (L1[0][0] - L1[1][0], L2[0][0] - L2[1][0])
    ydiff = (L1[0][1] - L1[1][1], L2[0][1] - L2[1][1])

    def det(a, b):
        return a[0] * b[1] - a[1] * b[0]

    div = det(xdiff, ydiff)
    if div != 0:
        d = (det(*L1), det(*L2))
        x = det(d, xdiff) / div
        y = det(d, ydiff) / div
        return int(x), int(y)
    else:
        return False


def print_progress_bar (iteration, total, prefix ='', suffix ='', decimals = 1, length = 100, fill ='█', printEnd ="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    sys.stdout.write('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix))
    # Print New Line on Complete
    if iteration == total:
        print()