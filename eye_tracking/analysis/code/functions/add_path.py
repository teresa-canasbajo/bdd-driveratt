# -*- coding: utf-8 -*-
"""

This function adds the relevant libraries necessary for running the preprocessing pipeline



"""

import os
import sys
import pandas as pd

# may need to update these?
sys.path.append(os.path.abspath("../lib/pupil_new/pupil_src/shared_modules/calibration_routines"))
sys.path.append(os.path.abspath("../lib/pupil_new/pupil_src/shared_modules/"))
# sys.path.append(os.path.abspath("../lib/pupil/pupil_src/player/"))
# sys.path.append(os.path.abspath("../lib/opencv2"))
# sys.path.append(os.path.abspath("../lib/glfw3"))
sys.path.append(os.path.abspath("../"))
sys.path.append(os.path.abspath("../code"))
sys.path.append(os.path.abspath("../lib/nslr-hmm"))
# sys.path.append(os.path.abspath("../lib/pyedfread/lib"))
# sys.path.append(os.path.abspath("../code/functions/fake_pl_loading"))

pd.options.display.max_columns = 30
