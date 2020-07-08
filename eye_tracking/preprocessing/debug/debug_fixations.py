import pandas as pd
import numpy as np
import builtins
import os
from eye_tracking.preprocessing.debug.debug_fixations_helper import *
from eye_tracking.preprocessing.functions.manual_detection import *

println = builtins.print

preprocessed_path = '/media/whitney/New Volume/Teresa/000/preprocessed/fixations.csv'
export_path = '/media/whitney/New Volume/Teresa/000/exports/002/fixations.csv'
# preprocessed_path = '/media/whitney/New Volume/Teresa/SD_grant_EM/003/preprocessed/fixations.csv'
# export_path = '/media/whitney/New Volume/Teresa/SD_grant_EM/003/exports/008/fixations.csv'

# compare_fixations_df = compare_fixations(export_path, preprocessed_path)

folder = '/media/whitney/New Volume/Teresa/000'
frames_path = folder + '/frames'
fixation_frames_path = frames_path + '/fixations'
video_path = folder + "/world.mp4"

fixation_video(frames_path, preprocessed_path, 'preprocessed')
fixation_video(frames_path, export_path, 'export')

folder = '/media/whitney/New Volume/Teresa/SD_grant_EM/003'
frames_path = folder + '/frames'
preprocessed_path = '/media/whitney/New Volume/Teresa/SD_grant_EM/003/preprocessed/fixations.csv'
export_path = '/media/whitney/New Volume/Teresa/SD_grant_EM/003/exports/008/fixations.csv'

fixation_video(frames_path, preprocessed_path, 'preprocessed')
fixation_video(frames_path, export_path, 'export')

# create fixation video
# remaining_img(frames_path, frames_path + '/preprocessed_fixations')
# create_video(frames_path + '/preprocessed_fixations', 'preprocessed')
# remaining_img(frames_path, frames_path + '/export_fixations')
# create_video(frames_path + '/export_fixations', 'export')


# surfaces_df = pd.read_csv(frames_path + '/surface_coordinates.csv')
# surfaces_df = surfaces_df.apply(pd.to_numeric, errors='coerce')





# if not os.path.exists(fixation_frames_path):
#     os.mkdir(fixation_frames_path)
#     println("Successfully created the directory %s " % fixation_frames_path)
#     fixation_video(frames_path, '/media/whitney/New Volume/Teresa/SD_grant_EM/003/preprocessed/fixations.csv')
# # else:
# #     println("Directory %s already exists." % fixation_frames_path)
# #     fixation_video(frames_path, coord_df)

# x_corr_coeff = np.corrcoef(coord_df.exports_x, coord_df.preprocessed_x)
# y_corr_coeff = np.corrcoef(coord_df.exports_y, coord_df.preprocessed_y)
#
# println('x corr coeff')
# println(x_corr_coeff)
# println('y corr coeff')
# println(y_corr_coeff)

