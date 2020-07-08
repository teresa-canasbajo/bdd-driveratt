#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 8 16:42:55 2018


"""
import eye_tracking.preprocessing.functions.detect_saccades as saccades
import pandas as pd
from eye_tracking.preprocessing.functions.pl_detect_fixations import *

# parses SR research EDF data files into pandas df


# from sklearn.metrics import mean_squared_error

# %% PL Events df

# unnecessary et in parameter but linked to next function which also is unnecessary
# unecessary datapath, surfaceMap in parameter
def make_saccades(etsamples, etevents, datapath, surfaceMap, engbert_lambda=5):
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
def make_fixations(etsamples, etevents, datapath, surfaceMap):
    # detect fixations calling pupil lab's api
    fixations_base_data, fixations_data = detect_fixations(datapath)
    # reformat into PLData object
    fixations = pl_data_fixation(fixations_base_data)

    if surfaceMap:
        import eye_tracking.preprocessing.functions.pl_surface as pl_surface

        # create surfaces dataframe from existing csv file
        frames_path = datapath + "/frames"
        surfaces_df = pd.read_csv(frames_path + '/surface_coordinates.csv')
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
        # define variables
        base_data = list(data['base_data'])
        start_time = base_data[0]["timestamp"]

        # match fixation timestamp to surface timestamp, if applicable
        while ((i < len(fixation_match_check) - 1) and (start_time > fixation_match_check[i + 1]['timestamp'])):
            i = i + 1

        # match fixation timestamp to surface timestamp, if applicable (pt 2)
        if start_time >= fixation_match_check[i]['timestamp']:
            if not surfaceMap:
                surface = "unknown"
            else:
                surface = True
            fixation = fixationevent(data, surface)
        else:
            if not surfaceMap:
                surface = "unknown"
            else:
                surface = False
            fixation = fixationevent(data, surface)
        fixationevents.append(fixation)

    # convert into pandas df
    fixationevents = pd.DataFrame(fixationevents)

    # concatenate to original event df
    etevents = pd.concat([etevents, fixationevents], axis=0, sort=False)

    print("Done ... detecting fixations")

    return etsamples, etevents

# # unecessary surfaceMap in parameter
def make_blinks(etsamples, etevents, datapath, surfaceMap):
    from eye_tracking.lib.pupil_API.pupil_src.shared_modules import file_methods
    from eye_tracking.preprocessing.functions import pl_blink_detection

    print('Detecting blinks ...')
    pupil_positions = file_methods.load_pldata_file(datapath, 'pupil')
    blinks = pl_blink_detection.Offline_Blink_Detection.recalculate(pl_blink_detection.Offline_Blink_Detection, pupil_positions, datapath)

    # filepath for preprocessed folder
    preprocessed_path = os.path.join(datapath, 'preprocessed')

    # create new folder if there is none
    if not os.path.exists(preprocessed_path):
        os.makedirs(preprocessed_path)

    # create csv file of fixations
    csv_file = preprocessed_path + '/blinks.csv'
    csv_columns = ['topic', 'start_timestamp', 'id', 'end_timestamp', 'timestamp', 'duration', 'base_data',
                   'filter_response', 'confidence', 'start_frame_index', 'end_frame_index', 'index']
    try:
        import csv
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, csv_columns)
            writer.writeheader()
            for data in list(blinks.data):
                writer.writerow(data)
    except IOError:
        print("I/O error")

    blinkevents = []
    # iterate through blink data
    for data in list(blinks.data):
        blink = {"start_time": data['start_timestamp'], "duration": data['duration'], "end_time": data['end_timestamp'], "type": data['topic']}
        blinkevents.append(blink)

    # convert into pandas df
    blinkevents = pd.DataFrame(blinkevents)

    # etevents is empty
    etevents = pd.concat([etevents, blinkevents], axis=0, sort=False)

    print("Done ... detecting blinks")

    return etsamples, etevents
