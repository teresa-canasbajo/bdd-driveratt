import sys
import json
import random
import pandas as pd
import numpy as np

from bisect import bisect_left

def main(json_filepath, output_filepath, detection_threshold, smoothing_threshold, fps):
    """Generate a csv file containing all billboard detections per video frame,
    with gaps in the detections smoothed via linear interpolation.

    Keyword arguments:
    json_filepath -- path to output of object_detection.py
    output_filepath -- savepath for generated csv
    detection_threshold -- specifies minimum acceptable detection score
    smoothing_threshold -- specifies maximum time delay between associated billboards when smoothing
    fps -- frame rate of original video
    """
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
        history = [] # each entry corresponds to a billboard instance, its value being its last seen location
        for i, frame in enumerate(frames):
            original_boxes = []
            smoothed_boxes = []
            for j in range(len(frame['detection_class_labels'])):
                if (frame['detection_class_labels'][j] == '87' and float(frame['detection_scores'][j]) >= detection_threshold and 
                  float(frame['detection_boxes'][j][2]) - float(frame['detection_boxes'][j][0]) < 0.5 and 
                  float(frame['detection_boxes'][j][3]) - float(frame['detection_boxes'][j][1]) < 0.5):
                    box = frame['detection_boxes'][j]

                    best_metric = 0
                    most_likely_correspondence = None
                    for h in range(len(history)):
                        prev_box, last_seen = history[h]
                        metric = iou(prev_box, box)
                        time_gap = (i-last_seen)/fps
                        if metric >= 0.4 and time_gap <= smoothing_threshold and metric > best_metric:
                            best_metric = metric
                            most_likely_correspondence = h

                    if most_likely_correspondence is not None:
                        # print(best_metric)
                        prev_box, last_seen = history[most_likely_correspondence]
                        for step in range(1, i-last_seen):
                            t = step/(i-last_seen)
                            inter_ymin = (1-t)*float(prev_box[0]) + t*float(box[0])
                            inter_xmin = (1-t)*float(prev_box[1]) + t*float(box[1])
                            inter_ymax = (1-t)*float(prev_box[2]) + t*float(box[2])
                            inter_xmax = (1-t)*float(prev_box[3]) + t*float(box[3])
                            smoothed[last_seen+step].append([str(inter_ymin), str(inter_xmin), str(inter_ymax), str(inter_xmax)])
                        history[most_likely_correspondence] = (box, i)
                    else:
                        history.append((box, i))
                    original_boxes.append(box)
                    smoothed_boxes.append(box)
            original.append(original_boxes)
            smoothed.append(smoothed_boxes)
            frame_num.append(i)
        columns = ['Frame', 'Original', 'Smoothed']
        df = pd.DataFrame(zip(frame_num, original, smoothed), columns=columns)
        df.to_csv(output_filepath)

def billboard_confidence_stats(frames):
    """Calculates the max, min, and avg confidence
    of the most likely billboard detections.

    Keyword arguments:
    frames -- json object contains all detections per frame
    """
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
    """Returns the confidence of the most likely billboard detection
    if it exists.

    Keyword arguments:
    frame -- TFHub detection result dictionary
    """
    billboard_scores = [float(frame['detection_scores'][i]) for i in range(len(frame['detection_scores'])) if frame['detection_class_entities'][i] == 'Billboard']
    if len(billboard_scores) > 0:
        return billboard_scores[0]
    return 0

def iou(box1, box2):
    """Calculates Intersection over Union of two bounding boxes.

    Keyword arguments:
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

def euclid_center_dist(box1, box2):
    """Calculates the euclidean distance between the centers of two
    bounding boxes.

    Keyword arguments:
    box1 -- first bounding box ordered ymin, xmin, ymax, xmax
    box2 -- second bounding box ordered ymin, xmin, ymax, xmax
    """
    box1 = np.array(box1, dtype=np.float32)
    box2 = np.array(box2, dtype=np.float32)
    center1 = ( (box1[3]-box1[1])/2, (box1[2]-box1[0])/2 )
    center2 = ( (box2[3]-box2[1])/2, (box2[2]-box2[0])/2 )
    return ((center1[0]-center2[0])**2 + (center1[1] - center2[1])**2 )**(1/2)

if __name__ == '__main__':
    args = sys.argv[1:]
    assert(len(args) >= 5)
    main(*args)
