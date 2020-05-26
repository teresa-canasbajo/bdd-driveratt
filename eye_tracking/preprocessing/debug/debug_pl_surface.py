#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 11:41:34 2018

@author: behinger
"""
# import collections

# import functions.add_path
from eye_tracking.preprocessing.functions.manual_detection import extract_frames, detect_tags, print_progress_bar
import numpy as np
# import time
# import pickle  # to save & restore variable
from glob import glob
import cv2
import os

from eye_tracking.lib.pupil_API.pupil_src.shared_modules.surface_tracker import surface_tracker_online, surface_tracker_offline
# import av  # important to load this library before pupil-library! (even though we dont use it...)

# from IPython.core.debugger import set_trace

# from queue import Empty as QueueEmptyException

from eye_tracking.lib.pupil_API.pupil_src.shared_modules.camera_models import load_intrinsics
from eye_tracking.lib.pupil_API.pupil_src.shared_modules.player_methods import correlate_data

from eye_tracking.lib.pupil_API.pupil_src.shared_modules.video_capture import fake_backend
from eye_tracking.preprocessing.functions.base_functions import gen_fakepool, global_container

# %%
def map_surface(folder, markers_per_screen):
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
    # bad images cuz they don't have actual surface
    # all_images = all_images[24720:24984]
    # all_images = all_images[793:966]

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
        # seems like surfaces are already defined in recent_events - not sure, but all markers in 1 frame seem to be stated as 1 surface
        # TODO: we need to predefine surfaces!!
        if len(tracker_online.markers) >= markers_per_screen:
            size = len(tracker_online.markers)
            while size >= markers_per_screen:
                # how do we know which markers are associated with this surface?
                tracker_online.on_add_surface_click()
                size -= markers_per_screen

    print('success!')

    return tracker_online


def fake_gpool_surface(folder=None):
    if not folder:
        raise ('we need the folder else we cannot load timestamps and surfaces etc.')
    surface_dir = os.path.join(folder, 'surface')
    if not os.path.exists(surface_dir):
        os.makedirs(surface_dir)

    fake_gpool = gen_fakepool(folder, surface_dir)
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


def surface_map_data(tracker, data):
    import eye_tracking.lib.pupil_API.pupil_src.shared_modules.player_methods as player_methods
    import eye_tracking.lib.pupil_API.pupil_src.shared_modules.surface_tracker.surface as surface

    tmp = data
    if hasattr(player_methods, 'Bisector'):
        # pupil labs starting from v1.8 needs the data as a Bisector
        data_dict = data._asdict()
        data = [t for t in data_dict['data']]
        time = [t for t in data_dict['timestamps']]
        tmp = player_methods.Bisector(data, time)

    fake_gpool = tracker.g_pool
    fake_gpool.gaze_positions = tmp
    fake_gpool.gaze_positions_by_frame = correlate_data(data, list(fake_gpool.timestamps))

    # if not (len(tracker.surfaces) == 1):
    #     raise 'expected only a single surface!'
    # And finally calculate the positions
    # gaze_on_srf = tracker.surfaces[0].gaze_on_srf_in_section()

    # gaze_on_srf = fake_gpool.gaze_positions_by_frame
    # trying the following -- gaze_on_srf_in_section() seems to be from prev API
    # gaze_on_srf = tracker.surfaces[0].update_gaze_history()
    # check out map_gaze_and_fixation_events under surface - surface api
    # also surface_tracker file see code below
    # for surface in self.surfaces:
    #     if surface.detected:
    #         gaze_on_surf = surface.map_gaze_and_fixation_events(
    #             gaze_events, self.camera_model
    #         )


    return gaze_on_srf
