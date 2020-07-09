#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

import logging

##########

import eye_tracking.preprocessing.functions.et_make_df as make_df
from eye_tracking.lib.pupil_API.pupil_src.shared_modules import file_methods as pl_file_methods
import eye_tracking.preprocessing.functions.et_parse as parse
from eye_tracking.preprocessing.functions.pl_detect_fixations import *
from eye_tracking.preprocessing.functions.et_helper import gaze_to_pandas
import eye_tracking.preprocessing.functions.pl_surface as pl_surface

########

def raw_pl_data(subject='', datapath='/media/whitney/New Volume/Teresa/bdd-driveratt', postfix='raw'):
    # Input:    subjectname, datapath
    # Output:   Returns pupillabs dictionary

    if subject == '':
        filename = datapath
    else:
        filename = os.path.join(datapath, subject, postfix)
    print(os.path.join(filename, 'pupil_data'))
    # with dict_keys(['annotations', 'pupil_positions', 'gaze_positions'])
    # where each value is a list that contains a dictionary

    if os.path.exists(os.path.join(filename, 'pupil_data')):
        logging.warning('This code only works for data from pupil capture versions greater than 1.17. Please update '
                        'your pupil capture & try again with new data.')

    elif os.path.exists(os.path.join(filename, 'pupil.pldata')):
        original_pldata = pl_file_methods.load_pldata_file(datapath, 'pupil')
        annotations = pl_file_methods.load_pldata_file(datapath, 'annotation')
        gaze = pl_file_methods.load_pldata_file(datapath, 'gaze')
        print('notifications_assigned')

    return original_pldata, annotations, gaze


def import_pl(subject='', datapath='/media/whitney/New Volume/Teresa/bdd-driveratt', surfaceMap=True, parsemsg=True):
    # Input:    subject:         (str) name
    #           datapath:        (str) location where data is stored
    #           surfaceMap:
    # Output:   Returns 2 dfs (plsamples and plmsgs)

    assert (not surfaceMap, 'If you want to continue without surface detector, please turn '
                            'surfaceMap to False')
    if surfaceMap:
        logging.warning(
            'If you want to continue without surface detector, please turn surfaceMap to False')

    # Get samples df
    # (is still a dictionary here)
    original_pldata, annotations, gaze = raw_pl_data(subject=subject, datapath=datapath)

    # use pupilhelper func to make samples df (confidence, gx, gy, smpl_time, diameter)
    pldata = gaze_to_pandas(gaze)

    if surfaceMap:
        folder = os.path.join(datapath)  # before it was taking subject, 'raw' as args

        # define surface coordinates per frame
        surfaces_df = pl_surface.map_surface(folder)

        # extract gaze data that falls within surface
        print('Detecting gaze on surface ...')
        gaze_on_srf = pl_surface.surface_map_data(surfaces_df, gaze)

        # mark which samples fall within the surface
        pldata = pl_surface.annotate_surface(pldata, gaze_on_srf)

    print('pldata', pldata)

    # sort according to smpl_time
    pldata.sort_values('smpl_time', inplace=True)

    # get the nice samples df
    plsamples = make_df.make_samples_df(pldata)

    if parsemsg:
        annotations = annotations._asdict()
        # Get msgs df
        annot_msg = [annot for annot in annotations['data']]
        plmsgs = pd.DataFrame()
        for note in annot_msg:
            msg = parse.parse_message(note)
            if not msg.empty:
                plmsgs = plmsgs.append(msg, ignore_index=True)
    else:
        plmsgs = annotations['data']

    plevents = pd.DataFrame()
    return plsamples, plmsgs, plevents, surfaceMap
