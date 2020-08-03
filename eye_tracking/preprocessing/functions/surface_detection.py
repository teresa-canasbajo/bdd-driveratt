import collections
import collections.abc
import numpy as np
import pandas as pd
import os
import shutil
from .manual_detection import extract_frames, detect_tags_and_surfaces
from .utils import print_progress_bar


# %%
def map_surface(folder, deleteFrames=False):
    # Input:    folder:       (str) datapath & subject pathway where data is stored
    #           deleteFrames: (boolean) True to delete frames directory once surface coordinates extracted (save memory)
    # Output:   Returns surface coordinates dataframes

    # create paths
    video_path = os.path.join(folder, 'world.mp4')
    preprocessed_path = os.path.join(folder, 'preprocessed')
    if not os.path.exists(preprocessed_path):
        os.makedirs(preprocessed_path)

    print('Finding markers & surfaces ...')

    surfaces_path = os.path.join(preprocessed_path, 'surface_coordinates.csv')
    try:
        if not os.path.exists(surfaces_path):
            # create frames directory if none exists
            frames_path = os.path.join(folder, 'frames')
            try:
                if not os.path.exists(frames_path):
                    os.mkdir(frames_path)
                    print("Successfully created the directory %s " % frames_path)
                    extract_frames(video_path, frames_path)
                else:
                    print("Directory %s already exists." % frames_path)
            except OSError:
                print("Creation of the directory %s failed" % frames_path)

            # detect surface coordinates
            tags = [2, 3, 5, 6, 7, 8, 9, 11, 0, 1]
            tags_corner_attribute = [True, False, False, True, False, True, False, False, True, False]
            frame, tag_ids, surfaces_df = detect_tags_and_surfaces(frames_path, createSurfaceFrame=False, tags=tags,
                                                                   tags_corner_attribute=tags_corner_attribute)
            surfaces_df.to_csv(os.path.join(preprocessed_path, 'surface_coordinates.csv'), index=False)
            print('Success! Surfaces detected: %s ' % surfaces_path)

            # delete frames directory if True
            if deleteFrames:
                shutil.rmtree(frames_path)
                print("Directory %s successfully deleted." % frames_path)
        else:
            print("Surfaces already detected: %s " % surfaces_path)

            # create surfaces dataframe from existing csv file
            surfaces_df = pd.read_csv(surfaces_path)
            surfaces_df = surfaces_df.apply(pd.to_numeric, errors='coerce')

    except OSError:
        print("Creation of the pathway %s failed" % surfaces_path)

    return surfaces_df


def surface_map_data(surface, gaze):
    # initialize variables
    PLData = collections.namedtuple("PLData", ["data", "timestamps", "topics"])
    data_gaze = []
    data_ts_gaze = []
    topics_gaze = []

    # extract gaze info
    data_dict = gaze._asdict()
    data = [t for t in data_dict['data']]
    time = [t for t in data_dict['timestamps']]
    topics = [t for t in data_dict['topics']]

    # iterate through gaze data
    i = 0
    n = 0

    while n < len(data):

        # define gaze position
        try:
            pupil1_pos = data[n]['base_data'][1]['norm_pos']
            pupil0_pos = data[n]['base_data'][0]['norm_pos']
            gaze_pos = ((pupil0_pos[0] + pupil1_pos[0]) / 2, (pupil0_pos[1] + pupil1_pos[1]) / 2)
        except IndexError:
            gaze_pos = data[n]['base_data'][0]['norm_pos']

        # match gaze timestamp to surface timestamp
        while (i < (len(surface.timestamp) - 1)) and (time[n] >= surface.timestamp[i + 1]):
            i = i + 1

        #  check whether gaze falls within surface
        tl_x = surface.norm_top_left_x[i]
        bl_x = surface.norm_bottom_left_x[i]
        br_x = surface.norm_bottom_right_x[i]
        tr_x = surface.norm_top_right_x[i]

        left = tl_x if tl_x < bl_x else bl_x
        right = br_x if br_x > tr_x else tr_x

        if (gaze_pos[0] > left) and (gaze_pos[0] < right):
            tl_y = surface.norm_top_left_y[i]
            bl_y = surface.norm_bottom_left_y[i]
            br_y = surface.norm_bottom_right_y[i]
            tr_y = surface.norm_top_right_y[i]

            top = tl_y if tl_y < tr_y else tr_y
            bottom = br_y if br_y > bl_y else bl_y

            if (gaze_pos[1] > top) and (gaze_pos[1] < bottom):
                data_gaze.append(data[n])
                data_ts_gaze.append(time[n])
                topics_gaze.append(topics[n])
        n = n + 1
        print_progress_bar(n, len(data), prefix='Progress:', suffix='Complete', length=50)
    print('success!')

    gaze_on_srf = PLData(collections.deque(data_gaze), np.asarray(data_ts_gaze), collections.deque(topics_gaze))
    return gaze_on_srf


def annotate_surface(etsamples, gaze_on_srf):
    # create df to store index of marked samples
    marked_samples = pd.DataFrame()

    ix_surface = []
    for p in etsamples.smpl_time:
        # check if sample is in surface
        if p in gaze_on_srf.timestamps:
            ix_surface.append(True)
        else:
            ix_surface.append(False)
    ix_surface = pd.Series(ix_surface)
    marked_samples['surface'] = ix_surface

    # concatenate surface column
    marked_samples.index = etsamples.index
    annotated_samples = pd.concat([etsamples, marked_samples], axis=1)

    return annotated_samples
