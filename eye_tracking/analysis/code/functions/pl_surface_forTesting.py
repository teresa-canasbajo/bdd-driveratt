#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 20 11:41:34 2018

@author: behinger
"""
import collections

import functions.add_path
from functions.manual_detection import extract_frames, detect_tags
import numpy as np
import time

import os
import av  # important to load this library before pupil-library! (even though we dont use it...)

from eye_tracking.analysis.lib.pupil.pupil_src.shared_modules import offline_surface_tracker

from eye_tracking.analysis.lib.pupil.pupil_src.shared_modules.offline_reference_surface import Offline_Reference_Surface
from IPython.core.debugger import set_trace

from functions.pl_recalib import gen_fakepool
from functions.pl_recalib import global_container
from queue import Empty as QueueEmptyException

from eye_tracking.analysis.lib.pupil.pupil_src.shared_modules.camera_models import load_intrinsics
from eye_tracking.analysis.lib.pupil.pupil_src.shared_modules.player_methods import correlate_data


# %%

def map_surface(folder, loadCache=True, loadSurface=True):
    # if you want to redo it, put loadCache to false

    # How a surface in pupil labs works (took me many days to figure that out...)
    #  1. detect all markers in tracker (this starts its own slave process)
    #  2. add some markers to a surface via build_correspondence
    #  3. for all markers detect the surface (init_cache)
    #  4. add the surface to the tracker
    #  5. map the observed pupil data to the surface (done in surface_map_data)

    fake_gpool = fake_gpool_surface(folder)

    # Step 1.
    print('Starting Tracker - WARNING: ROBUST_DETECTION IS CURRENTLY FALSE')
    # TODO Decide robust detection (not really sure what it does)
    tracker = offline_surface_tracker.Offline_Surface_Tracker(fake_gpool, min_marker_perimeter=30,
                                                              robust_detection=False)
    # line 50 is the error line found when debugging for the new videos recorded although when I comment out still running?!
        # so looks like it's actually tracker variable creation in line 47
    # offline_surface_tracker.py: where "No surfaces defined" comment came  -- lines 70-71 seem problematic possibly?
    tracker.timeline = None

    if loadSurface and len(tracker.surfaces) == 1 and tracker.surfaces[0].defined:
        print('Surface already defined, loadSurface=TRUE, thus returning tracker')
        tracker.cleanup()
        return tracker
    # Remove the cache if we do not need it
    if not loadCache:
        tracker.invalidate_marker_cache()

    start = time.time()

    print('Finding Markers')
    # This does what offline_surface_tracker.update_marker_cache() does (except the update surface, we dont need it), 
    # but in addition gives us feedback & has a stopping criterion
    while True:
        if (time.time() - start) > 1:
            start = time.time()
            visited_list = [False if x is False else True for x in tracker.cache]
            percent_visited = np.mean(np.asarray(visited_list))
            print(percent_visited)

            if percent_visited == 1:
                # save stuff and stop the process
                tracker.cleanup()
                break
        # try:
        #     idx, c_m = tracker.cache_queue.get(timeout=5)  # TODO check this for object detection IDS?
        # except QueueEmptyException:
        #     print('inside except')
        #     time.sleep(1)
        #
        #     print('Nothing to do, waiting...')
        #     continue
        # tracker.cache.update(idx, c_m)
        #
        # if tracker.cacher_run.value is False:
        #     tracker.recalculate()
        # Create video path
        video_path = folder + "/world.mp4"
        # Create frame path using OS package
        # Define the name of the directory to be created
        frames_path = folder + "/frames"
        try:
            os.mkdir(frames_path)
        except OSError:
            print("Creation of the directory %s failed" % frames_path)
        else:
            print("Successfully created the directory %s " % frames_path)
        extract_frames(video_path, frames_path)
        tracker.cache, _ = detect_tags(frames_path)

    # Step 2.    
    # add a single surface
    print('Adding a surface')
    surface = Offline_Reference_Surface(tracker.g_pool)

    # Original text:
    # First define the markers that should be used for the surface
    # find a frame where there are 16 markers and all of them have high confidence

    # Teresa: our surfaces are defined now by four markers, so we are going define that as a variable here, in case
    # that changes

    numMarkers = 4
    minConfidence = 0.000002  # just to be able to use the test video, cause I didn't calibrate so
    # confidence is usually around 0
    # TODO change minConfidence

    #     # have you found more than four markers? (four markers make 1 surface)
    #     # then check if those four belong to one surface.
    #     # if they do, then put them in the usable markers, then name them surface A, B or C.
    #     # if not then move forward
    #     # TODO: write criterion function for defining markers as surfaces, needs to be flexible for multiple surfaces or only one
    #     # TODO: figure out how the markers are ID'd.
    #     # TODO: figure out how the markers verts are created and what they mean.
    #     # TODO: how to detect half screens? like A and C.

    # array of arrays: each element represents the frame & within the frame element, tracker.cache stored if screen id'd
    screens_per_frame = screen_detection(tracker, numMarkers, minConfidence)

    # Step 3 This dissables pupil-labs functionality. They ask for 90 frames with the markers. but because we know
    # there will be 16 markers, we dont need it (toitoitoi)
    print('Defining & Finding Surface')
    surface.required_build_up = 1
    # iterating through all the frames
    for frame in screens_per_frame:
        # checking if frame has any screens
        if len(frame) > 0:
            for screen in frame:
                surface.build_correspondence(screen, 0.3, 0.7)
    if not surface.defined:
        raise ('Oh oh trouble ahead. The surface was not defined')
    surface.init_cache(tracker.cache, 0.3, 0.7)

    # Step 4
    tracker.surfaces = [surface]

    print('Saving Surface')
    tracker.save_surface_definitions_to_file()

    print('Changing Permissions to Group Read')

    def file_permissions_groupreadwrite(path):
        try:
            os.chmod(path, 0o770)
            for root, dirs, _ in os.walk(path):
                for d in dirs:
                    try:
                        os.chmod(os.path.join(root, d), 0o770)
                    except PermissionError:
                        print('permission in subfolder denied')
                        pass

        except PermissionError:
            print('permission in surface folder denied')
            pass

    file_permissions_groupreadwrite(fake_gpool.rec_dir)

    return tracker


def fake_gpool_surface(folder=None):
    if not folder:
        raise ('we need the folder else we cannot load timestamps and surfaces etc.')
    surface_dir = os.path.join(folder, '../', 'surface')
    if not os.path.exists(surface_dir):
        os.makedirs(surface_dir)

    fake_gpool = gen_fakepool()
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


def list_to_stream(gaze_list):
    import msgpack
    gaze_serialized = [msgpack.packb(gaze, use_bin_type=True) for gaze in gaze_list]
    return gaze_serialized


def surface_map_data(tracker, data):
    # if not (type(data) == list):
    # can also be lib.pupil.pupil_src.shared_modules.player_methods.Bisector
    #    raise 'Did you forget to select what data? I expected a list here'
    # data = list_to_stream(data)
    # get the gaze positions in world-camera units

    import eye_tracking.analysis.lib.pupil.pupil_src.shared_modules.player_methods as player_methods

    tmp = data
    if hasattr(player_methods, 'Bisector'):
        # pupil labs starting from v1.8 needs the data as a Bisector
        tmp = player_methods.Bisector(data, [p['timestamp'] for p in data])

    fake_gpool = tracker.g_pool
    fake_gpool.gaze_positions = tmp
    fake_gpool.gaze_positions_by_frame = correlate_data(data, fake_gpool.timestamps)

    if not (len(tracker.surfaces) == 1):
        raise ('expected only a single surface!')
    # And finally calculate the positions 
    gaze_on_srf = tracker.surfaces[0].gaze_on_srf_in_section()

    return gaze_on_srf


def screen_detection(tracker, numMarkers, minConfidence):
    """Identifies 1+ screens for each frame.
        Args:
            tracker: tracker variable
            numMarkers: min number of markers that define 1 screen
            minConfidence: min id confidence level checker
        """
    screenA = [0, 1, 2, 3]
    screenB = [4, 5, 6, 7]
    screenC = [8, 9, 10, 11]
    screenUnknownDemo = [8, 12, 21, 0, 19, 20, 4, 23]
    screens = [screenUnknownDemo, screenA, screenB, screenC]

    screens_per_frame = []
    ix = 0
    while ix < len(tracker.cache):
        screens_per_frame.append([])
        # loops through possible screen options to find if present
        for s in screens:
            usable_markers = []
            if len(tracker.cache[ix]) >= numMarkers:  # verifying min number of markers that define 1 screen
                for m in tracker.cache[ix]:
                    # verifying if id associated with screen & meets mim confidence lev reqs
                    if (m['id'] in s) & (m['id_confidence'] >= minConfidence):
                        usable_markers.append(m['id'])
                if len(usable_markers) >= numMarkers:  # verifying if # of id in this frame is enough to define 1 screen
                    # appending frame each time a screen appears
                    screens_per_frame[ix].append(tracker.cache[ix])
        ix += 1
    return screens_per_frame

