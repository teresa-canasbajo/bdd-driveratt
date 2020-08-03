from eye_tracking.preprocessing.functions.et_preprocess import preprocess_et
from eye_tracking.preprocessing.functions.detect_events import make_fixations, make_blinks, make_saccades


demo = '/media/whitney/New Volume/Teresa/bdd-driveratt/demo'
manual_demo = '/media/whitney/New Volume/Teresa/bdd-driveratt/manual_demo'
auto_demo = '/media/whitney/New Volume/Teresa/bdd-driveratt/auto_demo'
naive_diff_demo = '/media/whitney/New Volume/Teresa/SD_grant_EM/Naive_Subjects/Subject_AS/000'
diff_demo = '/media/whitney/New Volume/Teresa/SD_grant_EM/003'
diff_demo = '/media/whitney/New Volume/Teresa/000'

data = preprocess_et(subject='', datapath=diff_demo, surfaceMap=True)

print('Preprocessing complete!')
