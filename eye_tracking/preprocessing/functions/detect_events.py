#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os
from . import detect_fixations
from . import surface_detection as pl_surface
from . import detect_saccades as saccades
from . import detect_blinks
from eye_tracking.lib.pupil.pupil_src.shared_modules import file_methods


# unnecessary et in parameter but linked to next function which also is unnecessary
# unecessary subject, datapath, surfaceMap in parameter
def make_saccades(etsamples, etevents, subject, datapath, surfaceMap, engbert_lambda=5):
    saccadeevents = saccades.detect_saccades_engbert_mergenthaler(etsamples, etevents,
                                                                  engbert_lambda=engbert_lambda)

    # select only interesting columns: keep only the raw
    keepcolumns = [s for s in saccadeevents.columns if "raw" in s]
    saccadeevents = saccadeevents[keepcolumns]

    # remove the part of the string that says raw in order to be consistent
    newname = [s.replace('raw_', '') for s in saccadeevents.columns if "raw" in s]

    saccadeevents = saccadeevents.rename(columns=dict(zip(keepcolumns, newname)))

    # add the type
    saccadeevents['type'] = 'saccade'

    # concatenate to original event df
    etevents = pd.concat([etevents, saccadeevents], axis=0, sort=False)

    return etsamples, etevents


# unnecessary et in parameter
def make_fixations(etsamples, etevents, subject, datapath, surfaceMap):
    # detect fixations calling pupil lab's api
    directory = os.path.join(datapath, subject)
    fixations_base_data, fixations_data = detect_fixations.fixation_detection(directory)
    # reformat into PLData object
    fixations = detect_fixations.pl_data_fixation(fixations_base_data)

    if surfaceMap:
        # create surfaces dataframe from existing csv file
        preprocessed_path = os.path.join(datapath, subject, 'preprocessed')
        surfaces_df = pd.read_csv(preprocessed_path + '/surface_coordinates.csv')
        surfaces_df = surfaces_df.apply(pd.to_numeric, errors='coerce')

        # extract fixation data that falls within surface
        print('Detecting fixation on surface ...')
        fixation_gaze_on_srf = pl_surface.surface_map_data(surfaces_df, fixations)
        fixations = fixation_gaze_on_srf

    # variable to classify which fixations fall in surface, if applicable
    fixation_match_check = fixations.data

    fixationevents = []
    i = 0
    # iterate through original fixation data
    for data in fixations_data:
        start_time = data['timestamp']

        # match fixation timestamp to surface timestamp, if applicable
        while (i < len(fixation_match_check) - 1) and (start_time > fixation_match_check[i + 1]['timestamp']):
            i = i + 1

        # match fixation timestamp to surface timestamp, if applicable (pt 2)
        if start_time >= fixation_match_check[i]['timestamp']:
            surface = "unknown" if not surfaceMap else True
        else:
            surface = "unknown" if not surfaceMap else False
        fixation = detect_fixations.fixationevent(data, surface)
        fixationevents.append(fixation)

    # convert into pandas df
    fixationevents = pd.DataFrame(fixationevents)

    # concatenate to original event df
    etevents = pd.concat([etevents, fixationevents], axis=0, sort=False)

    print("Done ... detecting fixations")

    return etsamples, etevents


# unecessary et, surfaceMap in parameter
def make_blinks(etsamples, etevents, subject, datapath, surfaceMap):
    print('Detecting blinks ...')
    directory = os.path.join(datapath, subject)
    pupil_positions = file_methods.load_pldata_file(directory, 'pupil')
    blinks = detect_blinks.Offline_Blink_Detection.recalculate(detect_blinks.Offline_Blink_Detection, pupil_positions,
                                                               directory)

    # filepath for preprocessed folder
    preprocessed_path = os.path.join(datapath, subject, 'preprocessed')

    # create new folder if there is none
    if not os.path.exists(preprocessed_path):
        os.makedirs(preprocessed_path)

    # create csv file of blinks
    csv_file = preprocessed_path + '/blinks.csv'
    csv_columns = ['topic', 'start_timestamp', 'id', 'end_timestamp', 'timestamp', 'duration', 'base_data',
                   'filter_response', 'confidence', 'start_frame_index', 'end_frame_index', 'index']
    event_csv(csv_file, csv_columns, blinks.data)

    # iterate through blink data to append to events
    blinkevents = []
    for data in list(blinks.data):
        blink = {"start_time": data['start_timestamp'],
                 "duration": data['duration'],
                 "end_time": data['end_timestamp'],
                 "type": data['topic']}
        blinkevents.append(blink)

    # convert into pandas df
    blinkevents = pd.DataFrame(blinkevents)

    # etevents is empty
    etevents = pd.concat([etevents, blinkevents], axis=0, sort=False)

    print("Done ... detecting blinks")

    return etsamples, etevents


def event_csv(filepath, csv_columns, eventdata):
    try:
        import csv
        with open(filepath, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, csv_columns)
            writer.writeheader()
            for data in list(eventdata):
                writer.writerow(data)
    except IOError:
        print("I/O error")
