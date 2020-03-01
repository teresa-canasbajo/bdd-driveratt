import os
import sys
from sys import platform
import zmq
import socket

sys.path.append(os.path.abspath("../../lib/pupil_API/pupil_src/shared_modules/"))
sys.path.append(os.path.abspath("../../lib/nslr-hmm/"))
sys.path.append(os.path.abspath("../"))

import file_methods as pl_file_methods
import eye_tracking.preprocessing.functions.base_functions as base_functions
import aid_fixation
from eye_tracking.lib.pupil_API.pupil_src.shared_modules import fixation_detector
from eye_tracking.preprocessing.debug import fixation_detector_api

class global_container():
    pass

hostname = socket.gethostname()

if platform == 'darwin':
    demo_path = '/Users/teresa/Dropbox/Psicologia/PhD/UC BERKELEY/WHITNEY LAB/BDD/DriversAttention/data/3 - TCB - AUT/000 2/'
elif (platform == 'linux' or platform == 'linux2') and hostname != 'teresa-desktop':
    demo_path = '/media/whitney/New Volume/Teresa/bdd-driveratt/demo'
elif platform == 'linux' and hostname == 'teresa-desktop':
    demo_path = '/home/teresa//Documents/demos/TCB_auto'



# os.chdir(demo_path)
gaze = pl_file_methods.load_pldata_file(demo_path, 'gaze')

fake_gpool = base_functions.fake_gpool_surface(demo_path)

# zmq_ctx = zmq.Context()
# ipc_socket = zmq_tools.Msg_Dispatcher(zmq_ctx, ipc_push_url)
#
ctx = zmq.Context.instance()
ipc_pub = ctx.socket(zmq.PUB)
fake_gpool.ipc_pub = ipc_pub
#zmq.Context.instance(zmq.PUB)



detector = fixation_detector_api.Offline_Fixation_Detector(fake_gpool)

# define parameters
param = global_container()
param.max_dispersion = detector.max_dispersion
param.min_duration = detector.min_duration
param.max_duration = detector.max_duration
param.min_data_confidence = 0.8


# call detector
# for i in range(len(gaze.data)):
#     print('Iteration: ' + str(i))
fixations = list(fixation_detector_api.detect_fixations(fake_gpool.capture, gaze.data,
                                                    param.max_dispersion, param.min_duration,
                                                    param.max_duration, param.min_data_confidence))

# for gaze_per_frame in gaze.data:
all_images = aid_fixation.get_frames(demo_path)

for i, img_path in enumerate(all_images):
    events = aid_fixation.define_event(i, all_images, fake_gpool)
    events['gaze'] = gaze.data[i]
    a = detector.recent_events(events)

print('done')

