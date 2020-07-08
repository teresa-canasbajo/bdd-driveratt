from eye_tracking.preprocessing.functions.et_preprocess import *

from sys import platform
import socket

hostname = socket.gethostname()

if platform == 'darwin':
    super_best = '~/Dropbox/demos/super_best'
elif (platform == 'linux' or platform == 'linux2') and hostname != 'teresa-desktop':
    super_best = '/home/whitney/Teresa/demos/super_best'
    original = '/media/whitney/New Volume/Teresa/bdd-driveratt/VP1/raw'
    demo = '/media/whitney/New Volume/Teresa/bdd-driveratt/demo'
    # diff_demo = '/media/whitney/New Volume/Teresa/SD_grant_EM/Eye_Recordings/Subject1/001'
    diff_demo = '/media/whitney/New Volume/Teresa/SD_grant_EM/Eye_Recordings/Subject4/000'
elif platform == 'linux' and hostname == 'teresa-desktop':
    super_best = '/home/teresa//Documents/demos/super_best'
    diff_demo = '/home/teresa//Documents/demos/super_best'

demo = '/media/whitney/New Volume/Teresa/bdd-driveratt/demo'
manual_demo = '/media/whitney/New Volume/Teresa/bdd-driveratt/manual_demo'
auto_demo = '/media/whitney/New Volume/Teresa/bdd-driveratt/auto_demo'
# diff_demo = '/media/whitney/New Volume/Teresa/SD_grant_EM/Eye_Recordings/Subject4/000'
naive_diff_demo = '/media/whitney/New Volume/Teresa/SD_grant_EM/Naive_Subjects/Subject_AS/000'
diff_demo = '/media/whitney/New Volume/Teresa/SD_grant_EM/003'
# diff_demo = '/media/whitney/New Volume/Teresa/SD_grant_EM/003_modified'
diff_demo = '/media/whitney/New Volume/Teresa/000'

data = preprocess_et(subject='', datapath=diff_demo, save=True, eventfunctions=(make_blinks, make_saccades, make_fixations))

print('done!')
