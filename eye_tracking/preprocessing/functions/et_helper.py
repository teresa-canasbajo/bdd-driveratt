#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import os
import numpy as np
from numpy import pi, cos, sin
import pandas as pd
import logging


# %% put PUPIL LABS data into PANDAS DF


def gaze_to_pandas(gaze):
    # Input: gaze data as dictionary
    # Output: pandas dataframe with gx, gy, confidence, smpl_time pupillabsdata, diameter and (calculated) pupil area (pa)
    import pandas as pd

    list_diam = []
    list_pa = []
    gaze = gaze.data # filter only for data
    for idx, p in enumerate(gaze):

        if p:
            if 'surface' in gaze[0]['topic']:
                # we have a surface mapped dictionary. We have to get the real base_data
                # the schachtelung is: surfacemapped => base_data World Mapped => base_data pupil
                p_basedata = p['base_data']['base_data']
            else:
                p_basedata = p['base_data']

            # take the mean over all pupil-diameters
            diam = 0
            pa = 0
            for idx_bd, bd in enumerate(p_basedata):
                pa = convert_diam_to_pa(bd['ellipse']['axes'][0], bd['ellipse']['axes'][1])
                diam = diam + bd['diameter']
            diam = diam / (idx_bd + 1)

            list_diam.append(diam)
            list_pa.append(pa)

    df = pd.DataFrame({'gx': [p['norm_pos'][0] for p in gaze if p],
                       'gy': [p['norm_pos'][1] for p in gaze if p],
                       'confidence': [p['confidence'] for p in gaze if p],
                       'smpl_time': [p['timestamp'] for p in gaze if p],
                       'diameter': list_diam,
                       'pa': list_pa
                       })
    return df


def convert_diam_to_pa(axes1, axes2):
    return math.pi * float(axes1) * float(axes2) * 0.25


# %% adding information to dfs


def add_events_to_samples(etsamples, etevents):
    # Calls append_eventtype_to_sample for each event
    logger = logging.getLogger(__name__)

    etevents_type = etevents.type.unique()
    # classify fixation first, so blink & saccade can override as necessary
    if 'fixations' in etevents_type:
        index = np.where(etevents_type=='fixations')[0][0]
        while index != 0:
            etevents_type = np.roll(etevents_type, 1)
            index = np.where(etevents_type == 'fixations')[0][0]

    logger.info(etevents_type)
    for evt in etevents_type:
        etsamples = append_eventtype_to_sample(etsamples, etevents, eventtype=evt)

    return (etsamples)


def append_eventtype_to_sample(etsamples, etevents, eventtype, timemargin=None):
    # get a logger
    logger = logging.getLogger(__name__)

    logger.debug('Appending eventtype: %s to samples', eventtype)
    if timemargin is None:
        logger.info('Taking Default value for timemargin (0s)')
        timemargin = [0, 0]

    # get index of the rows that have that eventtype
    ix_event = etevents['type'] == eventtype

    # get list of start and end indeces in the etsamples df
    eventstart = etevents.loc[ix_event, 'start_time'] + float(timemargin[0])
    eventend = etevents.loc[ix_event, 'end_time'] + float(timemargin[1])

    flat_ranges = eventtime_to_sampletime(etsamples, eventstart, eventend)
    # all etsamples with ix in ranges , will the eventype in the column type
    if len(flat_ranges) > 0:
        etsamples.loc[etsamples.index[flat_ranges], 'type'] = eventtype

    return etsamples


def eventtime_to_sampletime(etsamples, eventstart, eventend):
    # due to timemargin strange effects can occur and we need to clip
    mintime = etsamples.smpl_time.iloc[0]
    maxtime = etsamples.smpl_time.iloc[-1]
    eventstart.loc[eventstart < mintime] = mintime
    eventstart.loc[eventstart > maxtime] = maxtime
    eventend.loc[eventend < mintime] = mintime
    eventend.loc[eventend > maxtime] = maxtime

    if len(eventstart) != len(eventend):
        raise ValueError

    startix = np.searchsorted(etsamples.smpl_time, eventstart)
    endix = np.searchsorted(etsamples.smpl_time, eventend)

    # print('%i events of %s found'%(len(startix),eventtype))
    # make a list of ranges to have all indices in between the startix and endix
    ranges = [list(range(s, e)) for s, e in zip(startix, endix)]
    flat_ranges = [item for sublist in ranges for item in sublist]

    flat_ranges = np.intersect1d(flat_ranges, range(etsamples.shape[0]))
    return flat_ranges


# %% everything related to VISUAL DEGREES

def px2deg(px, orientation, mm_per_px=0.276, distance=600):
    # VD
    # "gx_px - gx_px-midpoint"
    # subtract center of our BENQ

    if orientation == 'horizontal':
        center_x = 1920 / 2
        px = px - center_x

    elif orientation == 'vertical':
        center_y = 1080 / 2
        px = px - center_y
    else:
        raise ('unknown option')
    deg = np.arctan2(px * mm_per_px, distance) * 180 / np.pi

    return deg


def sph2cart(theta_sph, phi_sph, rho_sph=1):
    xyz_sph = np.asarray([rho_sph * sin(theta_sph) * cos(phi_sph),
                          rho_sph * sin(theta_sph) * sin(phi_sph),
                          rho_sph * cos(theta_sph)])

    return xyz_sph


# %% LOAD & SAVE & FIND file

def load_file(subject, datapath='/media/whitney/New Volume/Teresa/bdd-driveratt', outputprefix='', cleaned=True):
    # filepath for preprocessed folder
    preprocessed_path = os.path.join(datapath, subject, 'preprocessed')
    et = outputprefix + 'pl'
    try:
        if cleaned:
            filename_samples = str(et) + '_cleaned_samples.csv'
        else:
            filename_samples = str(et) + '_samples.csv'
        filename_msgs = str(et) + '_msgs.csv'
        filename_events = str(et) + '_events.csv'

        etsamples = pd.read_csv(os.path.join(preprocessed_path, filename_samples))
        etmsgs = pd.read_csv(os.path.join(preprocessed_path, filename_msgs))
        etevents = pd.read_csv(os.path.join(preprocessed_path, filename_events))

    except FileNotFoundError as e:
        print(e)
        raise e

    return etsamples, etmsgs, etevents


def save_file(data, subject, datapath, outputprefix=''):
    # filepath for preprocessed folder
    preprocessed_path = os.path.join(datapath, subject, 'preprocessed')

    # create new folder if there is none
    if not os.path.exists(preprocessed_path):
        os.makedirs(preprocessed_path)

    et = outputprefix + 'pl'
    # dump data in csv
    filename_samples = str(et) + '_samples.csv'
    filename_cleaned_samples = str(et) + '_cleaned_samples.csv'
    filename_msgs = str(et) + '_msgs.csv'
    filename_events = str(et) + '_events.csv'
    filename_timestamps = str(et) + '_timestamps.csv'

    # make separate csv file for every df 
    data[0].to_csv(os.path.join(preprocessed_path, filename_samples), index=False)
    data[1].to_csv(os.path.join(preprocessed_path, filename_cleaned_samples), index=False)
    data[2].to_csv(os.path.join(preprocessed_path, filename_msgs), index=False)
    data[3].to_csv(os.path.join(preprocessed_path, filename_events), index=False)

    # save timestamps as csv
    timestamps_path = os.path.join(datapath, subject, 'world_timestamps.npy')
    a = np.load(timestamps_path)
    df_timestamps = pd.DataFrame(a)
    df_timestamps.to_csv(os.path.join(preprocessed_path, filename_timestamps), index=False)


# %% Tic Toc Matlab equivalent to time things
import time


def TicTocGenerator():
    # Generator that returns time differences
    ti = 0  # initial time
    tf = time.time()  # final time
    while True:
        ti = tf
        tf = time.time()
        yield tf - ti  # returns the time difference


TicToc = TicTocGenerator()  # create an instance of the TicTocGen generator


# This will be the main function through which we define both tic() and toc()
def toc(tempBool=True):
    # Prints the time difference yielded by generator instance TicToc
    tempTimeInterval = next(TicToc)
    if tempBool:
        print("Elapsed time: %f seconds.\n" % tempTimeInterval)




# define 20% winsorized means


def mad(arr):
    """ Median Absolute Deviation: a "Robust" version of standard deviation.
        Indices variabililty of the sample.
        https://en.wikipedia.org/wiki/Median_absolute_deviation 
    """
    arr = np.ma.array(arr).compressed()  # should be faster to not use masked arrays.
    med = np.median(arr)
    return np.median(np.abs(arr - med))
