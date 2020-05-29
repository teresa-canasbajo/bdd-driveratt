#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

import os
import logging

##########
# TODO: next functions will need to be looked at before adding them to the respository. Right now i've deleted them so I need
# to uncomment the following imports:

from eye_tracking.preprocessing.functions.et_helper import gaze_to_pandas
import eye_tracking.preprocessing.functions.et_make_df as make_df
from eye_tracking.lib.pupil_API.pupil_src.shared_modules import file_methods as pl_file_methods
import eye_tracking.preprocessing.functions.et_parse as parse

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


# surfaceMap False in et_import for testing purposes
def import_pl(subject='', datapath='/media/whitney/New Volume/Teresa/bdd-driveratt', surfaceMap=False, parsemsg=True, markers_per_screen = 4):
    # Input:    subject:         (str) name
    #           datapath:        (str) location where data is stored
    #           surfaceMap:
    # Output:   Returns 2 dfs (plsamples and plmsgs)

    # get a logger
    logger = logging.getLogger(__name__)

    assert (not surfaceMap, 'If you want to continue without surface detector, please turn '
                            'surfaceMap to False')
    if surfaceMap:
        logging.warning(
            'If you want to continue without surface detector, please turn surfaceMap to False')

    if surfaceMap:
        import eye_tracking.preprocessing.functions.pl_surface as pl_surface

    # Get samples df
    # (is still a dictionary here)
    original_pldata, annotations, gaze = raw_pl_data(subject=subject, datapath=datapath)

    # use pupilhelper func to make samples df (confidence, gx, gy, smpl_time, diameter)
    original_pldata = original_pldata._asdict()
    original_pldata['gaze_positions'] = gaze
    # pldata = gaze_to_pandas(original_pldata['gaze_positions'])
    # print('pldata', pldata)

    if surfaceMap:
        folder = os.path.join(datapath)  # before it was taking subject, 'raw' as args

        # define surface coordinates per frame
        surfaces_df = pl_surface.map_surface(folder, markers_per_screen=markers_per_screen)#, loadCache=True)  # originally was True

        gaze_on_srf = pl_surface.surface_map_data(surfaces_df, gaze)
        logger.warning('Original Data Samples: %s on surface: %s', len(original_pldata['gaze_positions']),
                       len(gaze_on_srf))
        original_pldata['gaze_positions'] = gaze_on_srf

    # use pupilhelper func to make samples df (confidence, gx, gy, smpl_time, diameter)
    pldata = gaze_to_pandas(original_pldata['gaze_positions'])
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
    return plsamples, plmsgs, plevents
