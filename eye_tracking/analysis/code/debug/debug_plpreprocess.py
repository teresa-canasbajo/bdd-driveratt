from debug.debug_pl_surface import *
from functions.et_preprocess import *
import functions.add_path as add_path

from sys import platform

if platform == 'darwin':
    super_best = '~/Dropbox/demos/super_best'
elif platform == 'linux' or platform == 'linux2':
    super_best = '/home/whitney/Teresa/demos/super_best'
    original = '/media/whitney/New Volume/Teresa/bdd-driveratt/VP1/raw'

# surfaceMap False in et_import for testing purposes
# data = preprocess_et(subject='', datapath=super_best, save=True, eventfunctions=(make_blinks,make_saccades,make_fixations))

# preprocess_et does not take et anymore


test = map_surface(super_best)

print('done!')