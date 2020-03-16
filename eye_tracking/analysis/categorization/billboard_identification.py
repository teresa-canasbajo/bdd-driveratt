import sys
import json
import random
import pandas as pd
import numpy as np

from bisect import bisect_left

def main(json_filepath, output_filepath, detection_threshold, smoothing_threshold, fps):
    fps = int(fps)
    detection_threshold = float(detection_threshold)
    smoothing_threshold = float(smoothing_threshold)
    with open(json_filepath, 'r') as f:
        frames = json.load(f)
        avg_conf, max_conf, min_conf = billboard_confidence_stats(frames)
        print("Average billboard confidence: %f" % avg_conf)
        print("Max billboard confidence: %f" % max_conf)
        print("Min billboard confidence: %f" % min_conf)

        smoothed = []
        original = []
        frame_num = []
        n = len(frames)
        last_billboard_detection = 0
        for i, frame in enumerate(frames):
            original_boxes = []
            smoothed_boxes = []
            for j in range(len(frame['detection_class_labels'])):
                if (frame['detection_class_labels'][j] == '87' and float(frame['detection_scores'][j]) >= detection_threshold and 
                  float(frame['detection_boxes'][j][2]) - float(frame['detection_boxes'][j][0]) < 0.5 and 
                  float(frame['detection_boxes'][j][3]) - float(frame['detection_boxes'][j][1]) < 0.5):
                    box = frame['detection_boxes'][j]
                    n = i-last_billboard_detection
                    # interpolate if this next detection is within a half second window
                    if n > 1 and n/fps <= smoothing_threshold:
                        for prev_bb in smoothed[last_billboard_detection]:
                            if iou(prev_bb, box) >= 0.5:
                                for j in range(1, n):
                                    t = j/n
                                    inter_ymin = (1-t)*float(prev_bb[0]) + t*float(box[0])
                                    inter_xmin = (1-t)*float(prev_bb[1]) + t*float(box[1])
                                    inter_ymax = (1-t)*float(prev_bb[2]) + t*float(box[2])
                                    inter_xmax = (1-t)*float(prev_bb[3]) + t*float(box[3])
                                    if len(smoothed[-(n-j)]) > 0:
                                        print("oops")
                                        return
                                    smoothed[-(n-j)].append([str(inter_ymin), str(inter_xmin), str(inter_ymax), str(inter_xmax)])
                    original_boxes.append(box)
                    smoothed_boxes.append(box)
                    last_billboard_detection = i
            original.append(original_boxes)
            smoothed.append(smoothed_boxes)
            frame_num.append(i)
        columns = ['Frame', 'Original', 'Smoothed']
        df = pd.DataFrame(zip(frame_num, original, smoothed), columns=columns)
        df.to_csv(output_filepath)

def billboard_confidence_stats(frames):
    cumulative_sum = 0
    frames_with_billboards = 0
    max_conf = float("-inf")
    min_conf = float("inf")
    for i, frame in enumerate(frames):
        bc = billboard_confidence(frame)
        if bc != 0:
            cumulative_sum += bc
            frames_with_billboards += 1

            max_conf = max(max_conf, bc)
            min_conf = min(min_conf, bc)
    return cumulative_sum/frames_with_billboards, max_conf, min_conf

def billboard_confidence(frame):
    billboard_scores = [float(frame['detection_scores'][i]) for i in range(len(frame['detection_scores'])) if frame['detection_class_entities'][i] == 'Billboard']
    if len(billboard_scores) > 0:
        return billboard_scores[0]
    return 0

def iou(box1, box2):
    """Calculates Intersection over Union of two bounding boxes.

    Keyword arugments:
    box1 -- first bounding box ordered ymin, xmin, ymax, xmax
    box2 -- second bounding box ordered ymin, xmin, ymax, xmax
    """
    box1 = np.array(box1, dtype=np.float32)
    box2 = np.array(box2, dtype=np.float32)
    x_left = max(box1[1], box2[1])
    y_top = max(box1[0], box2[0])
    x_right = min(box1[3], box2[3])
    y_bot = min(box1[2], box2[2])

    if x_right < x_left or y_bot < y_top:
        return 0.0

    intersection = (x_right-x_left) * (y_bot - y_top)
    area1 = (box1[3]-box1[1]) * (box1[2]-box1[0])
    area2 = (box2[3]-box2[1]) * (box2[2]-box2[0])
    iou = intersection/ (area1 + area2 - intersection)

    assert iou <= 1.0
    assert iou >= 0.0
    return iou

def identify(x, y, frame):
    """Identifies all potential entities that the user was fixated on during a
    keyframe of the simulation based on highest confidence bounding boxes.

    Keyword arguments:
    x -- relative path to config file (float)
    y -- number of test iterations (float)
    frame -- tensorflow_hub detector output; comes sorted in descending order by scores (dict)
    """
    min_confidence = 0.2 #TODO: should this be specified more empiraclly? or maybe set it super low only for billboard class?
    scores = [float(s) for s in frame['detection_scores'][::-1]]
    cutoff = len(scores) - bisect_left(scores, min_confidence) 
    print('Cut: ', cutoff)
    boxes = frame['detection_boxes'][:cutoff]
    entities = frame['detection_class_entities'][:cutoff]

    def inside_box(box):
        ymin, xmin, ymax, xmax = map(lambda s: float(s), box)
        return xmin <= x <= xmax and ymin <= y <= ymax

    return {entities[j]: boxes[j] for j, box in enumerate(boxes[::-1]) if inside_box(box)}
    

if __name__ == '__main__':
    args = sys.argv[1:]
    assert(len(args) >= 5)
    main(*args)
