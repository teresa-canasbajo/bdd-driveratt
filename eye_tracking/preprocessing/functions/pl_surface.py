#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 11:41:34 2018

@author: behinger
"""
import collections
import collections.abc
from eye_tracking.preprocessing.functions.manual_detection import extract_frames, print_progress_bar, detect_tags_and_surfaces

import numpy as np
import pandas as pd

from glob import glob
import os


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

    print('Finding markers & surfaces ...')

    bounding_box_frames_path = frames_path + "/bounding_box_frames"
    try:
        if not os.path.exists(bounding_box_frames_path):
            os.mkdir(bounding_box_frames_path)
            print("Successfully created the directory %s " % bounding_box_frames_path)

            print_progress_bar(0, len(all_images), prefix='Progress:', suffix='Complete', length=50)

            # detect surface coordinates
            frame, tag_ids, surfaces_df = detect_tags_and_surfaces(frames_path)
            surfaces_df.to_csv(os.path.join(frames_path, 'surface_coordinates.csv'), index=False)
            print('success!\n')
        else:
            print("Directory %s already exists." % bounding_box_frames_path)

            # create surfaces dataframe from existing csv file
            surfaces_df = pd.read_csv(frames_path + '/surface_coordinates.csv')
            surfaces_df = surfaces_df.apply(pd.to_numeric, errors='coerce')

    except OSError:
        print("Creation of the directory %s failed" % bounding_box_frames_path)

    return surfaces_df


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
        if (gaze_pos[0] > surface.norm_top_left_x[i]) and (gaze_pos[0] < surface.norm_bottom_right_x[i]):
            if (gaze_pos[1] > surface.norm_top_left_y[i]) and (gaze_pos[1] < surface.norm_bottom_right_y[i]):
                data_gaze.append(data[n])
                data_ts_gaze.append(time[n])
                topics_gaze.append(topics[n])
        n = n + 1
        print_progress_bar(n, len(data), prefix='Progress:', suffix='Complete', length=50)
    print('success!\n')

    gaze_on_srf = PLData(collections.deque(data_gaze), np.asarray(data_ts_gaze), collections.deque(topics_gaze))
    return gaze_on_srf
