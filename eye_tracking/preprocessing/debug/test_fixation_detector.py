import os
import sys
from sys import platform
import zmq
import socket

sys.path.append(os.path.abspath("../../lib/pupil_API/pupil_src/shared_modules/"))
sys.path.append(os.path.abspath("../../lib/nslr-hmm/"))

import file_methods as pl_file_methods
import eye_tracking.preprocessing.functions.base_functions as base_functions

from eye_tracking.lib.pupil_API.pupil_src.shared_modules import fixation_detector

hostname = socket.gethostname()

if platform == 'darwin':
    demo_path = '/Users/teresa/Dropbox/Psicologia/PhD/UC BERKELEY/WHITNEY LAB/BDD/DriversAttention/data/3 - TCB - AUT/000 2/'
elif (platform == 'linux' or platform == 'linux2') and hostname != 'teresa-desktop':
    demo_path = '/media/whitney/New Volume/Teresa/bdd-driveratt/demo'


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

events = {}
events['gaze'] = gaze

detector = fixation_detector.Offline_Fixation_Detector(fake_gpool)
a = detector.recent_events(events)

print('done')

