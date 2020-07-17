import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib import animation
import pandas as pd
import numpy as np 
import glob
import json
import ast
import sys
import os
from expand_bounding_box import expand_logo_bb
from manual_detection import print_progress_bar

def draw_box(ymin, xmin, ymax, xmax, img_length, img_width):
    """Overlays a red bounding box over the current plot figure.

    Keyword arguments: 
    ymin -- normalized top edge
    xmin -- normalized left edge
    ymax -- normalized bottom edge
    xmax -- normalized right edge
    img_length -- image length
    img_width -- image width
    """
    ymin = float(ymin) * img_length
    xmin = float(xmin) * img_width
    ymax = float(ymax) * img_length
    xmax = float(xmax) * img_width
    width = (xmax-xmin)
    length = (ymax-ymin)
    return patches.Rectangle((xmin, ymin), width, length, linewidth=1, edgecolor='r', facecolor='none')

def animate_tf(input_dir_path, json_path, animation_filename, threshold):
    """Overlays the detected bounding boxes onto the original subject video.

    Keyword arguments: 
    input_dir_path -- path to directory containing raw video frames
    json_path -- path to output of object_detection.py
    animation_filename -- savepath for generated video
    threshold -- minimum acceptable detection score
    """
    frames = sorted(glob.glob(input_dir_path + '*.png'), key=lambda x: int(x.split('/')[-1].split('.')[0][5:]))
    output_dir_path = input_dir_path + '_animate_tf'
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
    with open(json_path, 'r') as f:
            tf_hub_results = json.load(f)
            total = len(frames)
            print_progress_bar(0, total, prefix='Progress:', suffix='Complete', length=50)
            for i, result in enumerate(tf_hub_results):
                print_progress_bar(i, total, prefix='Progress:', suffix='Complete', length=50)
                fig, ax = plt.subplots(1)
                img = plt.imread(frames[i])
                ax.imshow(img)

                for j in range(len(result['detection_class_entities'])):
                    # billboard filter conditions
                    if (result['detection_class_entities'][j] == 'Billboard' and float(result['detection_scores'][j]) > threshold and 
                      float(result['detection_boxes'][j][2]) - float(result['detection_boxes'][j][0]) < 0.5 and 
                      float(result['detection_boxes'][j][3]) - float(result['detection_boxes'][j][1]) < 0.5):
                        bounding_box = draw_box(*result['detection_boxes'][j], img.shape[0], img.shape[1])
                        ax.add_patch(bounding_box)

                plt.savefig(output_dir_path + frames[i].split('/')[-1])
                plt.close()
    print_progress_bar(total, total, prefix='Progress:', suffix='Complete', length=50)
    animate(output_dir_path, animation_filename)

def animate_tf_smoothed(input_dir_path, csv_path, animation_filename):
    """Overlays the smoothed bounding box detections onto the original subject video.

    Keyword arguments: 
    input_dir_path -- path to directory containing raw video frames
    csv_path -- path to output of identification.py
    animation_filename -- savepath for generated video
    """
    output_dir_path = input_dir_path + '_animate_tf_smoothed'
    if not os.path.exists(output_dir_path):
        os.makedirs(output_dir_path)
    smoothed_bbs = pd.read_csv(csv_path, dtype=object)
    total = len(smoothed_bbs)
    print_progress_bar(0, total, prefix='Progress:', suffix='Complete', length=50)
    for i, row in smoothed_bbs.iterrows():
        print_progress_bar(i, total, prefix='Progress:', suffix='Complete', length=50)
        fig, ax = plt.subplots(1)
        filename = 'frame' + str(row['Frame']) + '.png'
        img = plt.imread(input_dir_path + filename)
        ax.imshow(img)
        boxes = ast.literal_eval(row['Smoothed'])
        for box in boxes:
            bounding_box = draw_box(*box, img.shape[0], img.shape[1])
            ax.add_patch(bounding_box)
        plt.savefig(output_dir_path + filename)
        plt.close()
    print_progress_bar(total, total, prefix='Progress:', suffix='Complete', length=50)
    animate(output_dir_path, animation_filename)

def animate_tf_compare(path_to_frames, output_filename):
    """Animates the original and smoothed bounding box detections
    side by side. Assumes that both animations have already been
    separately generated.

    Keyword arguments: 
    path_to_frames -- path to original raw frames
    output_filename -- savepath for generated animation
    """
    original_path = path_to_frames + '_animate_tf'
    smoothed_path = path_to_frames + '_animate_tf_smoothed'
    fig, ax = plt.subplots(1, 2)
    original_frames = sorted(glob.glob(original_path + '*.png'), key=lambda x: int(x.split('/')[-1].split('.')[0][5:]))
    smoothed_frames = sorted(glob.glob(smoothed_path + '*.png'), key=lambda x: int(x.split('/')[-1].split('.')[0][5:]))

    original_images = [plt.imread(frame) for frame in original_frames]
    smoothed_images = [plt.imread(frame) for frame in smoothed_frames]
    im1 = ax[0].imshow(np.zeros(original_images[0].shape))
    im2 = ax[1].imshow(np.zeros(original_images[0].shape))
    ax[0].set_title('Original')
    ax[1].set_title('Smoothed')
    # plt.tight_layout()

    def init():
        im1.set_data(np.zeros(original_images[0].shape))
        im2.set_data(np.zeros(smoothed_images[0].shape))
        return [im1, im2]

    def animate(i):
        im1.set_data(original_images[i])
        im2.set_data(smoothed_images[i])
        return [im1, im2]

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(original_frames), interval=200, blit=True)
    anim.save(output_filename + '.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()

def animate(frame_path, output_filename):
    """Produces a matplotlib animation using the images in the specified directory.

    Keyword arguments: 
    frame_path -- path to directory containing images to be used
    output_filename -- savepath for generated animation
    """
    fig = plt.figure()
    frames = sorted(glob.glob(frame_path + '*.png'), key=lambda x: int(x.split('/')[-1].split('.')[0][5:]))

    images = [plt.imread(frame) for frame in frames]
    im = plt.imshow(np.zeros(images[0].shape))

    def init():
        im.set_data(np.zeros(images[0].shape))
        return [im]

    def animate(i):
        im.set_data(images[i])
        return [im]

    anim = animation.FuncAnimation(fig, animate, init_func=init, frames=len(frames), interval=20, blit=True)
    anim.save(output_filename + '.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

    plt.show()

args = sys.argv[1:]
assert(len(args) >= 3)
if args[0] == 'tf':
    assert(len(args) >= 6)
    animate_tf(args[1], args[2], args[3], args[4], float(args[5]))
elif args[0] == 'tf_smoothed':
    animate_tf_smoothed(args[1], args[2], args[3], args[4])
elif args[0] == 'tf_compare':
    animate_tf_compare(args[1], args[2], args[3])
# elif args[0] == 'google':
#     animate_google(args[1], args[2], args[3], args[4])
else:
    print("Unknown Command.")
