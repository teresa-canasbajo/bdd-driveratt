
# Preprocessing pipeline
## Installation

1. Clone project and intialize submodules

   ```bash
   git clone https://github.com/tere93/bdd-driveratt
   git submodule update --init
   ```

2. Run Make file: generates a virtual environment (bdddriverattenv), runs requirements.pip with all required python packages and requirements for Pupil Labs.

   ```python
   make
   ```

3. You may need to install the following packages with sudo/root privileges:

   `pkg-config`

   `automake`

   `cmake`

   `python3-dev`

   `libglew-dev`

   `xorg-dev libglu1-mesa-dev` <-- needed for libglew

   `libportaudio2` <-- for pyaudio

   `portaudio19-dev` <-- for pyaudio

   `pyaudio`

## Instructions of use

```python
import functions.et_preprocess
from functions.detect_events import make_blinks,make_saccades,make_fixations
data = preprocess_et(subject='', datapath='/media/whitney/New Volume/Teresa/bdd-driveratt/demo', save=True, eventfunctions=(make_blinks, make_saccades, make_fixations))
```

preprocess_et outputs three dataframes: etsamples, etmsgs, etevents that are saved into your data directory /preprocessed
(remember to turn save=True if you want it to be saved)

## In progress

### Surface detector:

 We've created a new implementation of the April tags package. The main maker detector is in manual_detection.py, that runs using the april_tags package: https://github.com/pupil-labs/apriltags

 To install: pip install pupil-apriltags

This code has been built and modified using Pycharm. Please note that you'll need to add the eye_tracking/analysis/lib/pupil/pupil_src as source root for the paths to work. 
Otherwise you may need to add the paths in another way.