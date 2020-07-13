#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 18 14:57:55 2018

@author: kgross

GET nice DATAFRAMES


"""

import numpy as np
from numpy import pi
from . import et_helper as helper


# %% MAKE SAMPLES

def make_samples_df(etsamples):
    # why do we have gx_vel, gy_vel column?
    fields_to_keep = {'smpl_time', 'gx', 'gy', 'confidence', 'pa', 'type', 'diameter', 'surface'}

    fields_to_fillin = fields_to_keep - set(etsamples.columns)
    fields_to_copy = fields_to_keep - fields_to_fillin

    etsamples_reduced = etsamples.loc[:, fields_to_copy]

    for fieldname in fields_to_fillin:
        # error: cannot set a frame with no defined index and a scalar
        etsamples_reduced.loc[:, fieldname] = np.nan

    return etsamples_reduced


def make_events_df(etevents):
    # why do we have an rms, end_point column?
    fields_to_keep = {'surface', 'start_gx', 'start_gy', 'end_gx', 'end_gy', 'end_time', 'start_time', 'type',
                      'amplitude', 'duration', 'dispersion', 'peak_velocity', 'mean_gx', 'mean_gy'}

    fields_to_fill_in = fields_to_keep - set(etevents.columns)
    fields_to_copy = fields_to_keep - fields_to_fill_in

    etevents_reduced = etevents.loc[:, fields_to_copy]

    for fieldname in fields_to_fill_in:
        etevents_reduced.loc[:, fieldname] = np.nan

    return etevents_reduced




# %% Make df for LARGE GRID condition


def calc_3d_angle_points(x_0, y_0, x_1, y_1):
    # calculate the spherical angle between 2 points We add pi/2 so that (0°,0°,1), and (0°,90°,1) have a distance of
    # 90° instead of 0. (we take the "y" axis as the "0°,0°")
    #
    vec1 = helper.sph2cart(x_0 / 360 * 2 * pi + pi / 2, y_0 / 360 * 2 * pi + pi / 2)
    vec2 = helper.sph2cart(x_1 / 360 * 2 * pi + pi / 2, y_1 / 360 * 2 * pi + pi / 2)

    # pupillabs : precision = np.sqrt(np.mean(np.rad2deg(np.arccos(succesive_distances.clip(-1., 1.))) ** 2))
    cosdistance = np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))
    angle = np.arccos(np.clip(cosdistance, -1., 1.))
    angle = angle * 360 / (2 * pi)  # radian to degree

    return angle





