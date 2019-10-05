from pupil_apriltags import Detector, Detection
from collections import defaultdict
from glob import glob

import cv2

frames = []
tag_ids = defaultdict(int)
tag_count = 0
at_detector = Detector()

video_path = ''

def extract_frames(video_path, frames_path):
    video = cv2.VideoCapture(video_path)
    count = 0
    success = 1

    while success:
        success, frame = video.read()
        cv2.imwrite(f"{frames_path}/frame{count}.png", frame)
        count += 1

test_folder_path = '/Users/richardliu/Documents/BDD/bdd-driveratt/eye_tracking/analysis/test'
frames_path = '/Users/richardliu/Documents/BDD/bdd-driveratt/eye_tracking/analysis/surface2frames'

for img_path in glob(f'{test_folder_path}/*.png'):
    img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
    tags = at_detector.detect(img, estimate_tag_pose=False, camera_params=None, tag_size=None)
    tag_count += len(tags)
    for tag in tags:
        tag_ids[tag.tag_id] += 1
        frames.append({
            'id': tag.tag_id,
            'centroid': tag.center,
            'verts': tag.corners
        })
        

# Helper function
# def load_image_into_numpy_array(image):
#     print(image)
#     (im_width, im_height) = image.size
#     return np.array(image.getdata()).reshape(
#         (im_height, im_width, 3)).astype(np.uint8)

print(f'Detected {tag_count} tags in {len(frames)} frames.')
print(f'Found IDs of f{tag_ids.keys()}')
