from eye_tracking.preprocessing.debug.debug_pl_surface import *
from eye_tracking.preprocessing.functions.et_preprocess import *

from sys import platform
import socket

hostname = socket.gethostname()

if platform == 'darwin':
    super_best = '~/Dropbox/demos/super_best'
elif (platform == 'linux' or platform == 'linux2') and hostname != 'teresa-desktop':
    super_best = '/home/whitney/Teresa/demos/super_best'
    original = '/media/whitney/New Volume/Teresa/bdd-driveratt/VP1/raw'
elif platform == 'linux' and hostname == 'teresa-desktop':
    super_best = '/home/teresa//Documents/demos/super_best'

demo = '/media/whitney/New Volume/Teresa/bdd-driveratt/demo'

# surfaceMap False in et_import for testing purposes
data = preprocess_et(subject='', datapath=demo, save=True, eventfunctions=(make_blinks, make_saccades, make_fixations))

print('done!')