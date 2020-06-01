#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 11:41:34 2018

@author: behinger
"""
import collections
import collections.abc
from eye_tracking.preprocessing.functions.manual_detection import extract_frames, detect_tags, print_progress_bar

import numpy as np

from glob import glob
import cv2
import os

from eye_tracking.lib.pupil_API.pupil_src.shared_modules.video_capture import fake_backend

# %%
def map_surface(folder):
    if True:
        video_path = folder + "/world.mp4"
        # Create frame path using OS package
        # Define the name of the directory to be created
        frames_path = folder + "/frames"
        try:
            if not os.path.exists(frames_path):
                os.mkdir(frames_path)
                print("Successfully created the directory %s " % frames_path)
                extract_frames(video_path, frames_path)
            else:
                print("Directory %s already exists." % frames_path)
        except OSError:
            print("Creation of the directory %s failed" % frames_path)
    # Sort by index in.../frame<index>.png
    all_images = sorted(glob(f'{frames_path}/*.png'), key=lambda f: int(os.path.basename(f)[5:-4]))
    all_images = all_images[:-1]

    num_images = len(all_images)

    print('Finding Markers & Surfaces\n')

    print_progress_bar(0, num_images, prefix='Progress:', suffix='Complete', length=50)

    # detect surface coordinates
    frame, tag_ids, surfaces_df = detect_tags(frames_path)
    surfaces_df.to_csv(os.path.join(frames_path, 'surface_coordinates.csv'), index=False)

    print('success!\n')

    return surfaces_df


def define_event(idx, all_images, fake_gpool):
    img_path = all_images[idx]
    # read image:
    img = cv2.imread(img_path)

    # timestamp is stored in fake_gpool
    timestamp = fake_gpool.timestamps[idx]
    index = idx
    events = {'frame': fake_backend.Frame(timestamp, img, index)}
    return events


def surface_map_data(surface, gaze):
    # initialize variables
    PLData = collections.namedtuple("PLData", ["data", "timestamps", "topics"])
    data_gaze = []
    data_ts_gaze = []
    topics_gaze = []

    # extract gaze info
    data_dict = gaze._asdict()
    data = [t for t in data_dict['data']]
    time = [t for t in data_dict['timestamps']]
    topics = [t for t in data_dict['topics']]

    print('Detecting gaze on surface\n')

    # iterate through gaze data
    i = 0
    n = 0
    while n < len(data):
        # define gaze position
        try:
            pupil1_pos = data[n]['base_data'][1]['norm_pos']
            pupil0_pos = data[n]['base_data'][0]['norm_pos']
            gaze_pos = ((pupil0_pos[0] + pupil1_pos[0]) / 2, (pupil0_pos[1] + pupil1_pos[1]) / 2)
        except IndexError:
            gaze_pos = data[n]['base_data'][0]['norm_pos']

        # match gaze timestamp to surface timestamp
        while (i < (len(surface.timestamp)-1)) and (time[n] >= surface.timestamp[i+1]):
            i = i + 1

        #  check whether gaze falls within surface
        if (gaze_pos[0] > surface.norm_top_left[i][0]) and (gaze_pos[0] < surface.norm_bottom_right[i][0]):
            if (gaze_pos[1] > surface.norm_top_left[i][1]) and (gaze_pos[1] < surface.norm_bottom_right[i][1]):
                data_gaze.append(data[n])
                data_ts_gaze.append(time[n])
                topics_gaze.append(topics[n])
        n = n + 1
        print_progress_bar(n, len(data), prefix='Progress:', suffix='Complete', length=50)
    print('success!\n')

    gaze_on_srf = PLData(collections.deque(data_gaze), np.asarray(data_ts_gaze), collections.deque(topics_gaze))
    return gaze_on_srf
