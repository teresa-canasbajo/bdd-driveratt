#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd

import os
import logging

##########
# TODO: next functions will need to be looked at before adding them to the respository. Right now i've deleted them so I need
# to uncomment the following imports:

from eye_tracking.preprocessing.functions.et_helper import findFile, gaze_to_pandas
import eye_tracking.preprocessing.functions.et_make_df as make_df

########


import scipy
import scipy.stats


def raw_pl_data(subject='', datapath='/media/whitney/New Volume/Teresa/bdd-driveratt', postfix='raw'):
    # Input:    subjectname, datapath
    # Output:   Returns pupillabs dictionary
    from eye_tracking.lib.pupil_API.pupil_src.shared_modules import file_methods as pl_file_methods

    if subject == '':
        filename = datapath
    else:
        filename = os.path.join(datapath, subject, postfix)
    print(os.path.join(filename, 'pupil_data'))
    # with dict_keys(['notifications', 'pupil_positions', 'gaze_positions'])
    # where each value is a list that contains a dictionary

    if os.path.exists(os.path.join(filename, 'pupil_data')):
        logging.warning('This code only works for data from pupil capture versions greater than 1.17. Please update '
                        'your pupil capture & try again with new data.')

    elif os.path.exists(os.path.join(filename, 'pupil.pldata')):
        print('Newer pupil capture used')
        original_pldata = pl_file_methods.load_pldata_file(datapath, 'pupil')
        notifications = pl_file_methods.load_pldata_file(datapath, 'notify')
        gaze = pl_file_methods.load_pldata_file(datapath, 'gaze')
        print('notifications_assigned')

    return original_pldata, notifications, gaze


# surfaceMap False in et_import for testing purposes
# parsemsg False: not currently working, may be needed in the future if notifications of start/end/etc important
def import_pl(subject='', datapath='/media/whitney/New Volume/Teresa/bdd-driveratt', recalib=True, surfaceMap=False,
              parsemsg=False, pupildetect=None, pupildetect_options=None):
    # Input:    subject:         (str) name
    #           datapath:        (str) location where data is stored
    #           surfaceMap:
    # Output:   Returns 2 dfs (plsamples and plmsgs)

    # get a logger
    logger = logging.getLogger(__name__)

    assert (not surfaceMap, 'Surface detector NOT functional yet. If you want to continue without it, please turn '
                            'surfaceMap to False')
    if surfaceMap:
        logging.warning(
            'Surface detector NOT functional yet. If you want to continue without it, please turn surfaceMap to False')

    if recalib:
        logging.warning(
            'Recalib NOT functional yet. If you want to continue without it, please turn surfaceMap to False')

    if pupildetect:
        # has to be imported first
        import av
        import ctypes
        # not needed for now
        ctypes.cdll.LoadLibrary(
            '/net/store/nbp/users/behinger/projects/etcomp/local/build/build_ceres_working/lib/libceres.so.2')

    if surfaceMap:
        # has to be imported before nbp recalib
        try:
            import functions.pl_surface_forTesting as pl_surface
        except ImportError:
            raise ('Custom Error:Could not import pl_surface')

    assert (type(subject) == str)

    # Get samples df
    # (is still a dictionary here)
    # this works already
    original_pldata, notifications, gaze = raw_pl_data(subject=subject, datapath=datapath)

    # detect pupil positions, not sure if we need:
    if pupildetect is not None:  # can be 2d or 3d
        from eye_tracking.analysis.code.functions.nbp_pupildetect import nbp_pupildetect
        if subject == '':
            filename = datapath
        else:
            filename = os.path.join(datapath, subject, 'raw')

        pupil_positions_0 = nbp_pupildetect(detector_type=pupildetect, eye_id=0, folder=filename,
                                            pupildetect_options=pupildetect_options)
        pupil_positions_1 = nbp_pupildetect(detector_type=pupildetect, eye_id=1, folder=filename,
                                            pupildetect_options=pupildetect_options)
        pupil_positions = pupil_positions_0 + pupil_positions_1
        original_pldata['pupil_positions'] = pupil_positions

    # recalibrate data
    if recalib:
        from debug import debug_nbp_recalib as nbp_recalib
        # added following line to resolve issue: original_pldata not acting as dictionary --> can't call or add keys
        original_pldata = original_pldata._asdict()
        notifications = notifications._asdict()
        if pupildetect is not None:
            original_pldata['gaze_positions'] = nbp_recalib.nbp_recalib(original_pldata, notifications,
                                                                        calibration_mode=pupildetect)
        original_pldata['gaze_positions'] = nbp_recalib.nbp_recalib(original_pldata, notifications)

    # here we are:
    if surfaceMap:
        folder = os.path.join(datapath)  # before it was taking subject, 'raw' as args

        # we have fixed map_surface!
        tracker = pl_surface.map_surface(folder, loadCache=True)  # originally was True
        # now we are working on surface_map_data:
        gaze_on_srf = pl_surface.surface_map_data(tracker, original_pldata['gaze_positions'])
        logger.warning('Original Data Samples: %s on surface: %s', len(original_pldata['gaze_positions']),
                       len(gaze_on_srf))
        original_pldata['gaze_positions'] = gaze_on_srf

    # use pupilhelper func to make samples df (confidence, gx, gy, smpl_time, diameter)
    original_pldata = original_pldata._asdict()
    original_pldata['gaze_positions'] = gaze
    pldata = gaze_to_pandas(original_pldata['gaze_positions'])
    print('pldata', pldata)

    if surfaceMap:
        pldata.gx = pldata.gx * (1920 - 2 * (75 + 18)) + (75 + 18)  # minus white border of marker & marker
        pldata.gy = pldata.gy * (1080 - 2 * (75 + 18)) + (75 + 18)
        logger.debug('Mapped Surface to ScreenSize 1920 & 1080 (minus markers)')
        del tracker

    # sort according to smpl_time
    pldata.sort_values('smpl_time', inplace=True)

    # get the nice samples df
    plsamples = make_df.make_samples_df(pldata)

    notifications = notifications._asdict()

    if parsemsg:
        # Get msgs df      
        # make a list of gridnotes that contain all notifications of original_pldata if they contain 'label'

        gridnotes = [note for note in notifications['data'] if 'topics' in note.keys()]
        # come back and fix !!
        # gridnotes = [note for note in notifications['data'] if 'topics' in note.keys()]
        plmsgs = pd.DataFrame()
        for note in gridnotes:
            msg = parse.parse_message(note)
            if not msg.empty:
                plmsgs = plmsgs.append(msg, ignore_index=True)
        plmsgs = fix_smallgrid_parser(plmsgs)
    else:
        # plmsgs = original_pldata['notifications']
        plmsgs = notifications['data']

    plevents = pd.DataFrame()
    return plsamples, plmsgs, plevents


def fix_smallgrid_parser(etmsgs):
    # This fixes the missing separation between smallgrid before and small grid after. During experimental sending
    # both were named identical.
    replaceGrid = pd.Series([k for l in [13 * ['SMALLGRID_BEFORE'], 13 * ['SMALLGRID_AFTER']] * 6 for k in l])
    ix = etmsgs.query('grid_size==13').index
    if len(ix) is not 156:
        raise RuntimeError('we need to have 156 small grid msgs')

    replaceGrid.index = ix
    etmsgs.loc[ix, 'condition'] = replaceGrid

    # this here fixes that all buttonpresses and stop messages etc. were send as GRID and not SMALLGG 
    for blockid in etmsgs.block.dropna().unique():
        if blockid == 0:
            continue
        tmp = etmsgs.query('block==@blockid')
        t_before_start = tmp.query('condition=="DILATION"& exp_event=="stop"').msg_time.values
        t_before_end = tmp.query('condition=="SHAKE"   & exp_event=="stop"').msg_time.values
        t_after_start = tmp.query('condition=="SHAKE"   & exp_event=="stop"').msg_time.values
        t_after_end = tmp.iloc[-1].msg_time

        t_before_start = float(t_before_start)
        t_before_end = float(t_before_end)
        t_after_start = float(t_after_start)
        t_after_end = float(t_after_end)

        ix = tmp.query('condition=="GRID"&msg_time>@t_before_start & msg_time<=@t_before_end').index
        etmsgs.loc[ix, 'condition'] = 'SMALLGRID_BEFORE'

        ix = tmp.query('condition=="GRID"&msg_time>@t_after_start  & msg_time<=@t_after_end').index
        etmsgs.loc[ix, 'condition'] = 'SMALLGRID_AFTER'

    return etmsgs
