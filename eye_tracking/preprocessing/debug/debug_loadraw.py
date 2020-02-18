from functions.et_import import import_pl
from functions.et_import import raw_pl_data
from functions.et_helper import findFile, gaze_to_pandas
import pandas
path = '/home/whitney/Teresa/demos/surfaceANDcalibration_3screens'

# etsamples, etmsgs, etevents = import_pl(datapath=path, surfaceMap=False)
original_pldata = raw_pl_data(datapath=path)

# pretty sure the gaze_to_pandas can handle this without having to reformat the original_pldata through the rest of
# the preprocessing pipeline. Not sure how yet, so this will output the error that there it cannot read data.
# it's meant to read gaze, pupil positions, surface positions, etc, like after preprocessing.

# not working
pldata = gaze_to_pandas(original_pldata['data'])

print('done')

