import os
from eye_tracking.lib.pupil_API.pupil_src.shared_modules import file_methods as pl_file_methods
from eye_tracking.lib.pupil_API.pupil_src.shared_modules import fixation_detector

import msgpack

print(msgpack.version[1])

demo_path = '/Users/teresa/Dropbox/Psicologia/PhD/UC BERKELEY/WHITNEY LAB/BDD/DriversAttention/data/3 - TCB - AUT/000 2/'

# os.chdir(demo_path)
gaze = pl_file_methods.load_pldata_file(demo_path, 'gaze')

print('done')