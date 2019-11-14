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
import pickle # to save & restore variable
from glob import glob
import cv2
import os
from pupil_new.pupil_src.shared_modules.surface_tracker import surface_tracker_offline
from pupil_new.pupil_src.shared_modules.surface_tracker import surface

from pupil_new.pupil_src.shared_modules.surface_tracker import surface_tracker_online
import av  # important to load this library before pupil-library! (even though we dont use it...)

from eye_tracking.analysis.lib.pupil.pupil_src.shared_modules import offline_surface_tracker

from eye_tracking.analysis.lib.pupil.pupil_src.shared_modules.offline_reference_surface import Offline_Reference_Surface
from IPython.core.debugger import set_trace


from debug.debug_pl_recalib_new import gen_fakepool
from debug.debug_pl_recalib_new import global_container
from queue import Empty as QueueEmptyException

from eye_tracking.analysis.lib.pupil_new.pupil_src.shared_modules.camera_models import load_intrinsics
from eye_tracking.analysis.lib.pupil.pupil_src.shared_modules.player_methods import correlate_data


# %%

def map_surface(folder):
    # 1. create class with info about the folder
    fake_gpool = fake_gpool_surface(folder)

    tracker = surface_tracker_offline.Surface_Tracker_Offline(fake_gpool)
    tracker_online = surface_tracker_online.Surface_Tracker_Online(fake_gpool)
#    surface_test = surface.Surface() # parenthesis!
    tracker_subclass = tracker.Surface_Class()

    tracker_detector = tracker.marker_detector


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
    print('Finding Markers\n')

    print_progress_bar(0, num_images, prefix='Progress:', suffix='Complete', length=50)

    # for i, img_path in enumerate(all_images):
    #     # Create a grayscale 2D NumPy array for Detector.detect()
    #     img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    #
    #     if type(img) == np.ndarray:
    #         tracker.marker_cache[i] = tracker.marker_detector.detect_markers(img, i)
    #     print_progress_bar(i + 1, num_images, prefix='Progress:', suffix='Complete', length=50)

    print('Add Surface')
    all_locations = []

    # first create events dictionary, then call tracker_online.recent_events(events)
    # loop through all frames and images
    for i, img_path in enumerate(all_images):
        # Create a grayscale 2D NumPy array for Detector.detect()
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        # pupil labs folks say we only need the frame key to work, but we may need to add more, like video info
        events = {'frame': img} # this creates the dictionary
        tracker_online.recent_events(events)
        # now img contains image and i contains frame idx

        print_progress_bar(i + 1, num_images, prefix='Progress:', suffix='Complete', length=50)


    # This is almost working but we're trying recent_events()
    # surface_location = []
    #
    # for frame in range(num_images):
    #
    #     if len(tracker.marker_cache[frame]) >= 4: # if is not empty
    #         surface_location.append(tracker_subclass.update_location(
    #             frame,
    #             tracker.marker_cache,
    #             tracker.camera_model))
    #


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

print('done!')