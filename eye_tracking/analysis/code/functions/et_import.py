#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import numpy as np
import pandas as pd

import os
import logging

##########
# TODO: next functions will need to be looked at before adding them to the respository. Right now i've deleted them so I need
# to uncomment the following imports:

from functions.et_helper import findFile, gaze_to_pandas
#import functions.et_parse as parse
import functions.et_make_df as make_df
import functions.et_helper as helper


########


import scipy
import scipy.stats


# %% PUPILLABS
def pl_fix_timelag(pl):
    # fixes the pupillabs latency lag (which can be super large!!)

    t_cam = np.asarray(
        [p['recent_frame_timestamp'] for p in pl['notifications'] if p['subject'] == 'trigger'])  # camera time
    t_msg = np.asarray([p['timestamp'] for p in pl['notifications'] if p['subject'] == 'trigger'])  # msg time

    # slope, intercept, r_value, p_value, std_err  = scipy.stats.linregress(t_msg,t_cam) # predict camera time based on msg time
    slope, intercept, low, high = scipy.stats.theilslopes(t_cam, t_msg)
    logger = logging.getLogger(__name__)
    logger.warning("fixing lag (at t=0) of :%.2fms, slope of %.7f (in a perfect world this is 0ms & 1.0)" % (
    intercept * 1000, slope))
    # fill it back in
    # gonna do it with a for-loop because other stuff is too voodo or not readable for me

    # Use this code (and change t_cam and t_msg above) if you want everything in computer time timestamps
    # for ix,m in enumerate(pl['gaze_positions']):
    #    pl['gaze_positions'][ix]['timestamp'] = pl['gaze_positions'][ix]['timestamp']  * slope + intercept   
    #    for ix2,m2 in enumerate(pl['gaze_positions'][ix]['pupil_positions']):
    #            pl['gaze_positions'][ix]['pupil_positions']['timestamp'] = pl['gaze_positions'][ix]['pupil_positions']['timestamp']  * slope + intercept
    # for ix,m in enumerate(pl['gaze_positions']):
    #     pl['pupil_positions'][ix]['timestamp'] = pl['pupil_positions'][ix]['timestamp']  * slope + intercept# + 0.045 # the 45ms  are the pupillabs defined delay between camera image & timestamp3   

    # this code is to get notifications into sample time stamp. But for now we 
    for ix, m in enumerate(pl['notifications']):
        pl['notifications'][ix]['timestamp'] = pl['notifications'][ix][
                                                   'timestamp'] * slope + intercept + 0.045  # the 45ms  are the pupillabs defined delay between camera image & timestamp3

    return (pl)


def raw_pl_data(subject='', datapath='/media/whitney/New Volume/Teresa/bdd-driveratt', postfix='raw'):
    # Input:    subjectname, datapath
    # Output:   Returns pupillabs dictionary
    from pupil_new.pupil_src.shared_modules import file_methods as pl_file_methods

    if subject == '':
        filename = datapath
    else:
        filename = os.path.join(datapath, subject, postfix)
    print(os.path.join(filename, 'pupil_data'))
    # with dict_keys(['notifications', 'pupil_positions', 'gaze_positions'])
    # where each value is a list that contains a dictionary

    # IMPORTANT: the file to use depends on which version of Pupil labs you used to record.
    # if old version, your data will be in pupil_data
    # if newer version, your data will be in pupil.pldata


    if os.path.exists(os.path.join(filename, 'pupil_data')):
        print('Old pupil capture used')
        version = 'old'
        original_pldata = pl_file_methods.load_object(os.path.join(filename, 'pupil_data'))
        notifications = []
    elif os.path.exists(os.path.join(filename, 'pupil.pldata')):
        print('Newer pupil capture used')
        version = 'new'
        original_pldata = pl_file_methods.load_pldata_file(datapath, 'pupil')
        notifications = pl_file_methods.load_pldata_file(datapath, 'notify')
        gaze = pl_file_methods.load_pldata_file(datapath, 'gaze')

        print('notifications_assigned')

    # original_pldata = pl_file_methods.Incremental_Legacy_Pupil_Data_Loader(os.path.join(filename,'pupil_data'))
    # 'notification'
    # dict_keys(['record', 'subject', 'timestamp', 'label', 'duration'])

    # 'pupil_positions'
    # dict_keys(['diameter', 'confidence', 'method', 'norm_pos', 'timestamp', 'id', 'topic', 'ellipse'])

    # 'gaze_positions'
    # dict_keys(['base_data', 'timestamp', 'topic', 'confidence', 'norm_pos'])
    # where 'base_data' has a dict within a list
    # dict_keys(['diameter', 'confidence', 'method', 'norm_pos', 'timestamp', 'id', 'topic', 'ellipse'])
    # where 'normpos' is a list (with horizon. and vert. component)

    # Fix the (possible) timelag of pupillabs camera vs. computer time

    return original_pldata, notifications, version, gaze

# surfaceMap False in et_import for testing purposes
def import_pl(subject='', datapath='/media/whitney/New Volume/Teresa/bdd-driveratt', recalib=True, surfaceMap=False,
              parsemsg=True, fixTimeLag=True, px2deg=True, pupildetect=None,
              pupildetect_options=None):
    # Input:    subject:         (str) name
    #           datapath:        (str) location where data is stored
    #           surfaceMap:
    # Output:   Returns 2 dfs (plsamples and plmsgs)

    # get a logger
    logger = logging.getLogger(__name__)
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
    original_pldata, notifications, version, gaze = raw_pl_data(subject=subject, datapath=datapath)

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
        recalib = True

    # recalibrate data
    if recalib:
        from debug import debug_nbp_recalib as nbp_recalib
        # added following line to resolve issue: original_pldata not acting as dictionary --> can't call or add keys
        if version == 'new':
            original_pldata = original_pldata._asdict()
            notifications = notifications._asdict()
        if pupildetect is not None:
            original_pldata['gaze_positions'] = nbp_recalib.nbp_recalib(original_pldata, notifications, calibration_mode=pupildetect)
        original_pldata['gaze_positions'] = nbp_recalib.nbp_recalib(original_pldata, notifications, version)

    # Fix timing Pupillabs cameras ,have their own timestamps & clock. The msgs are clocked via computertime.
    # Sometimes computertime&cameratime show drift (~40% of cases). We fix this here
    if fixTimeLag:
        original_pldata = pl_fix_timelag(original_pldata)

    # here we are:
    if surfaceMap:
        folder = os.path.join(datapath) # before it was taking subject, 'raw' as args

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
    plsamples = make_df.make_samples_df(pldata, px2deg=px2deg)

    notifications = notifications._asdict()
    if parsemsg:
        # Get msgs df      
        # make a list of gridnotes that contain all notifications of original_pldata if they contain 'label'

        gridnotes = [note for note in notifications['data'] if 'topics' in note.keys()]
        # come back and fix !!
        #gridnotes = [note for note in notifications['data'] if 'topics' in note.keys()]
        plmsgs = pd.DataFrame()
        for note in gridnotes:
            msg = parse.parse_message(note)
            if not msg.empty:
                plmsgs = plmsgs.append(msg, ignore_index=True)
        plmsgs = fix_smallgrid_parser(plmsgs)
    else:
        #plmsgs = original_pldata['notifications']
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
