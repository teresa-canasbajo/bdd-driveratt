#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from eye_tracking.lib.pupil.pupil_src.shared_modules import fixation_detector
from eye_tracking.lib.pupil.pupil_src.shared_modules.camera_models import load_intrinsics
from eye_tracking.lib.pupil.pupil_src.shared_modules import file_methods
from . import detect_events
from types import SimpleNamespace
import numpy as np
import os
import collections


def fixation_detection(directory):
    # gaze_data parameter
    gaze = file_methods.load_pldata_file(directory, 'gaze')
    gaze_data = [gp.serialized for gp in gaze.data]

    # capture parameter
    cap = SimpleNamespace()
    cap.frame_size = (1280, 960)
    cap.intrinsics = load_intrinsics('', 'Pupil Cam1 ID2', (1280, 720))
    cap.timestamps = np.load(os.path.join(directory, 'world_timestamps.npy'))

    # define other parameters
    max_dispersion = 1.50
    min_duration = 80
    max_duration = 220
    confidence = 0.6

    print("Detecting fixations...")
    fixations = list(fixation_detector.detect_fixations(cap, gaze_data, np.deg2rad(max_dispersion), min_duration / 1000,
                                                        max_duration / 1000, confidence))

    # filepath for preprocessed folder
    preprocessed_path = os.path.join(directory, 'preprocessed')

    # create new folder if there is none
    if not os.path.exists(preprocessed_path):
        os.makedirs(preprocessed_path)

    fixations_data = []
    fixations_base_data = []
    # extract fixation data to create csv
    for data in fixations[1:-1]:
        # extract fixation base data
        for datum in data[1][0]['base_data']:
            fixations_base_data.append(datum)
        # data[1][0].pop("base_data")
        fixations_data.append(data[1][0])

    # create csv file of fixations
    csv_file = preprocessed_path + '/fixations.csv'
    csv_columns = ['topic', 'norm_pos', 'dispersion', 'method', 'base_data', 'timestamp', 'duration', 'confidence',
                   'gaze_point_3d', 'start_frame_index', 'end_frame_index', 'mid_frame_index', 'id']
    detect_events.event_csv(csv_file, csv_columns, fixations_data)

    return fixations_base_data, fixations_data


def pl_data_fixation(data_lst):
    # initialize variables
    PLData = collections.namedtuple("PLData", ["data", "timestamps", "topics"])
    data_gaze = []
    data_ts_gaze = []
    topics_gaze = []

    # iterate through fixations & extract base_data, timestamp, & topic
    for data in data_lst:
        data_gaze.append(data)
        data_ts_gaze.append(data['timestamp'])
        topics_gaze.append(data['topic'])

    # return PLData object
    pl_fixation = PLData(collections.deque(data_gaze), np.asarray(data_ts_gaze), collections.deque(topics_gaze))
    return pl_fixation

def fixationevent(data, surface):
    # define variables
    # base_data = list(data['base_data'])
    # norm_pos = np.mean([gp["norm_pos"] for gp in base_data], axis=0).tolist()
    start_time = data['timestamp']
    duration = data['duration'] / 1000
    end_time = start_time + duration

    # fixation event creation
    fixation = {"start_time": start_time,
                "duration": data['duration'],
                "end_time": end_time,
                "mean_gx": data['norm_pos'][0],
                "mean_gy": data['norm_pos'][1],
                "dispersion": data['dispersion'],
                "type": data['topic'],
                "surface": surface}

    return fixation
