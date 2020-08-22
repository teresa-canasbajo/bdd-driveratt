#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import os
import logging

##########

from . import et_make_df as make_df
from . import et_parse as parse
from . import surface_detection as pl_surface
from .et_helper import gaze_to_pandas
from eye_tracking.lib.pupil.pupil_src.shared_modules import file_methods as pl_file_methods

########

def raw_pl_data(subject='', datapath='/media/whitney/New Volume/Teresa/bdd-driveratt'):
    # Input:    subjectname, datapath
    # Output:   Returns pupillabs dictionary

    if subject == '':
        datapath = datapath
    else:
        datapath = os.path.join(datapath, subject)

    original_pldata = pl_file_methods.load_pldata_file(datapath, 'pupil')
    annotations = pl_file_methods.load_pldata_file(datapath, 'annotation')
    gaze = pl_file_methods.load_pldata_file(datapath, 'gaze')

    # 'annotation', 'pupil_positions', 'gaze_positions' with dict_keys(['data', 'timestamps', 'topics'])
    # 'annotation' data_dict_keys(['topic', 'label', 'timestamp', 'duration'])
    # 'pupil' data_dict_keys(['circle_3d', 'confidence', 'timestamp', 'diameter_3d', 'ellipse', 'location',
    #                           'diameter', 'sphere', 'projected_sphere', 'model_confidence', 'model_id',
    #                           'model_birth_timestamp', 'theta', 'phi', 'norm_pos', 'topic', 'id', 'method'])
    # 'gaze' data_dict_keys(['topic', 'eye_centers_3d', 'gaze_normals_3d', 'gaze_point_3d', 'confidence',
    #                           'timestamp', 'base_data', 'norm_pos'])

    return original_pldata, annotations, gaze


def import_pl(subject='', datapath='/media/whitney/New Volume/Teresa/bdd-driveratt', surfaceMap=True, parsemsg=True):
    # Input:    subject:         (str) name
    #           datapath:        (str) location where data is stored
    #           surfaceMap:      (boolean) extract surface info for mapping purposes
    #           parsemsg:        (boolean)
    # Output:   Returns 2 dfs (plsamples and plmsgs)

    if surfaceMap:
        logging.warning(
            'Make sure detect_tags_and_surfaces() arguments, (1) tags and (2) tags_corner_attribute, are correctly '
            'defined in surface_detection.py. If you want to continue without surface detector, please turn '
            'surfaceMap to False.')

    # Get samples df
    # (is still a dictionary here)
    original_pldata, annotations, gaze = raw_pl_data(subject=subject, datapath=datapath)

    # use pupilhelper func to make samples df (confidence, gx, gy, smpl_time, diameter)
    pldata = gaze_to_pandas(gaze)

    if surfaceMap:
        folder = os.path.join(datapath, subject)  # before it was taking subject, 'raw' as args

        # define surface coordinates per frame
        surfaces_df = pl_surface.map_surface(folder)

        # extract gaze data that falls within surface
        print('Detecting gaze on surface ...')
        gaze_on_srf = pl_surface.surface_map_data(surfaces_df, gaze)

        # mark which samples fall within the surface
        pldata = pl_surface.annotate_surface(pldata, gaze_on_srf)

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
