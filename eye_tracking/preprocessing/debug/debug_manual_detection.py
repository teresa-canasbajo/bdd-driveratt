from eye_tracking.preprocessing.functions.manual_detection import *

# demo = '/media/whitney/New Volume/Teresa/frames'
# demo = '/media/whitney/New Volume/Teresa/SD_grant_EM/003/frames'
demo = '/media/whitney/New Volume/Teresa/SD_grant_EM/003_modified/frames'

# frame, tag_ids = detect_tags(demo)
frame, tag_ids, coordinates_df = detect_tags(demo)
coordinates_df.to_csv(os.path.join(demo, 'coordinates.csv'), index=False)

print('done!')
