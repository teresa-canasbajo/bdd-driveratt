
# Preprocessing pipeline
## Installation

1. Clone project and intialize submodules

   ```bash
   git clone https://github.com/teresa-canasbajo/bdd-driveratt
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

We want to acknowledge the work of behinger/etcomp repository (https://github.com/behinger/etcomp) of which we based the organizational structure of the code & output along with a few functions.

```python
from eye_tracking.preprocessing.functions.et_preprocess import preprocess_et
data = preprocess_et(subject='', datapath='/media/whitney/New Volume/Teresa/bdd-driveratt/demo')
```

preprocess_et outputs three dataframes: etsamples, etmsgs, etevents that are saved into your data directory /preprocessed

### Surface detector:

We've created a new implementation of the April tags package. The main maker detector is in manual_detection.py, that runs using the april_tags package: https://github.com/pupil-labs/apriltags

To install: pip install pupil-apriltags

Make sure to update (1) tags & (2) tags_corner_attribute parameters in detect_tags_and_surfaces() to detect surface.
Current version detects 1 surface. 
If there are multiple surfaces, turn off surface detector by making surfaceMap False in import_pl()

Frames annotated with surfaces are saved into you data directory /frames/bounding_box_frames

This code has been built and modified using Pycharm. Note the source root as bdd-driveratt for the paths to work. 
Otherwise you may need to add the paths in another way.
