#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  8 16:42:55 2018


"""
import eye_tracking.preprocessing.functions.detect_saccades as saccades
import pandas as pd
import numpy as np
import os
import logging
from eye_tracking.preprocessing.functions.pl_detect_fixations import detect_fixations, pl_data_fixation

# parses SR research EDF data files into pandas df
from eye_tracking.preprocessing.functions.pl_detect_blinks import pl_detect_blinks


# from sklearn.metrics import mean_squared_error

# %% PL Events df

# unecessary datapath, surfaceMap in parameter
def make_blinks(etsamples, etevents, datapath, surfaceMap):
    # get a logger
    logger = logging.getLogger(__name__)

    logger.debug('Detecting Pupillabs Blinks')

    # add Blink information to pldata
    etsamples = pl_detect_blinks(etsamples)
    etsamples['blink_id'] = (1 * (etsamples['is_blink'] == 1)) * (
            (1 * (etsamples['is_blink'] == 1)).diff() == 1).cumsum()

    blinkevents = pl_make_blink_events(etsamples)
    etsamples = etsamples.drop('is_blink', axis=1)

    # etevents is empty
    etevents = pd.concat([etevents, blinkevents], axis=0, sort=False)

    return etsamples, etevents


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
        norm_pos = np.mean([gp["norm_pos"] for gp in base_data], axis=0).tolist()
        start_time = base_data[0]["timestamp"]
        duration = (base_data[-1]["timestamp"] - base_data[0]["timestamp"]) * 1000
        end_time = start_time + duration

        # match fixation timestamp to surface timestamp, if applicable
        while ((i < len(fixation_match_check) - 1) and (start_time > fixation_match_check[i + 1]['timestamp'])):
            i = i + 1

        # match fixation timestamp to surface timestamp, if applicable (pt 2)
        if start_time >= fixation_match_check[i]['timestamp']:
            fixation = {"start_time": start_time,
                        "duration": data['duration'],
                        "end_time": end_time,
                        "start_gx": norm_pos[0],
                        "start_gy": norm_pos[1],
                        "mean_gx": data['norm_pos'][0],
                        "mean_gy": data['norm_pos'][1],
                        "dispersion": data['dispersion'],
                        "type": 'fixation'}
            fixationevents.append(fixation)

    # convert into pandas df
    fixationevents = pd.DataFrame(fixationevents)

    # concatenate to original event df
    etevents = pd.concat([etevents, fixationevents], axis=0, sort=False)

    print("Done ... detecting fixations")

    return etsamples, etevents


# %%

def pl_make_blink_events(pl_extended_samples):
    # detects Blink events for pupillabs

    assert ('is_blink' in pl_extended_samples)
    assert ('blink_id' in pl_extended_samples)

    # init lists to store info
    blink_id = []
    start = []
    end = []
    # is_blink = []
    event_type = []

    # for each sample look at the blink_id
    for int_blink_id in pl_extended_samples.blink_id.unique():
        # if it is a blink (then the id is not zero)
        if int_blink_id != 0:
            # take all samples that the current unique blink_id
            query = 'blink_id == ' + str(int_blink_id)
            blink_samples = pl_extended_samples.query(query)

            # append infos from queried samples to lists 
            # is_blink.append(True)
            blink_id.append(int_blink_id)
            # blink starts with first marked sample
            start.append(blink_samples.iloc[0]['smpl_time'])
            # blink ends with last marked sample
            end.append(blink_samples.iloc[-1]['smpl_time'])
            event_type.append("blink")

    # create df and store collected infos there
    pl_blink_events = pd.DataFrame({'blink_id': blink_id, 'start_time': start, 'end_time': end, 'type': event_type})

    return pl_blink_events
