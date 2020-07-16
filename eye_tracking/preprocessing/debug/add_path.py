# -*- coding: utf-8 -*-
"""

This function adds the relevant libraries necessary for running the preprocessing pipeline



"""

import os
import sys
import pandas as pd


def add_path():
    print('Adding relevant files...')
    sys.path.append(os.path.abspath('../../lib/pupil/pupil_src/shared_modules/calibration_routines'))
    sys.path.append(os.path.abspath("../../lib/pupil/pupil_src/shared_modules/"))
    sys.path.append(os.path.abspath("../"))
    sys.path.append(os.path.abspath("../functions"))
    sys.path.append(os.path.abspath("../../lib/nslr_hmm/"))

    pd.options.display.max_columns = 30
    print('Done.')