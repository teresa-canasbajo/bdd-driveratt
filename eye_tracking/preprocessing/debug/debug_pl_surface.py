#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 11:41:34 2018

@author: behinger
"""
import collections

import functions.add_path
from functions.manual_detection import extract_frames, detect_tags, print_progress_bar
import numpy as np
import time
import pickle  # to save & restore variable
from glob import glob
import cv2
import os
from surface_tracker import surface_tracker_offline

from surface_tracker import surface_tracker_online
import av  # important to load this library before pupil-library! (even though we dont use it...)

from IPython.core.debugger import set_trace

from queue import Empty as QueueEmptyException

from camera_models import load_intrinsics
from player_methods import correlate_data

from video_capture import fake_backend


# %%

def map_surface(folder):
    # 1. create class with info about the folder
    fake_gpool = fake_gpool_surface(folder)

    tracker_online = surface_tracker_online.Surface_Tracker_Online(fake_gpool)

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

    # first create events dictionary, then call tracker_online.recent_events(events)
    # loop through all frames and images
    # then pass the correct markers into the on_add_surface_click()

    for i, img_path in enumerate(all_images):
        # Create a grayscale 2D NumPy array for Detector.detect()

        # An event has information about a particular frame, like the shape, np.array of the img, etc.
        # pupil lab folks say this is initiated by each step in gui, but we create our own separate in define_events

        events = define_event(i, all_images, fake_gpool)

        # In recent_event we detect markers in the frame, and if there is a surface it updates its location
        tracker_online.recent_events(events)

        print_progress_bar(i + 1, num_images, prefix='Progress:', suffix='Complete', length=50)

        # a surface is defined by at least 4 markers.
        # TODO: we need to predefine surfaces!!
        if len(tracker_online.markers) >= 4:
            tracker_online.on_add_surface_click()

    print('success!')


def fake_gpool_surface(folder=None):
    if not folder:
        raise ('we need the folder else we cannot load timestamps and surfaces etc.')
    surface_dir = os.path.join(folder, 'surface')
    if not os.path.exists(surface_dir):
        os.makedirs(surface_dir)

    fake_gpool = gen_fakepool(folder)
    fake_gpool.surfaces = []
    fake_gpool.rec_dir = surface_dir
    fake_gpool.timestamps = np.load(os.path.join(folder, 'world_timestamps.npy'))
    fake_gpool.capture.source_path = os.path.join(folder, 'world.mp4')
    fake_gpool.capture.intrinsics = load_intrinsics('', 'Pupil Cam1 ID2', (1280, 720))
    fake_gpool.seek_control = global_container()
    fake_gpool.seek_control.trim_left = 0
    fake_gpool.seek_control.trim_right = 0
    fake_gpool.timeline = global_container()
    return fake_gpool


def define_event(idx, all_images, fake_gpool):
    img_path = all_images[idx]
    # read image:
    img = cv2.imread(img_path)

    # timestamp is stored in fake_gpool
    timestamp = fake_gpool.timestamps[idx]
    index = idx
    events = {'frame': fake_backend.Frame(timestamp, img, index)}
    return events
