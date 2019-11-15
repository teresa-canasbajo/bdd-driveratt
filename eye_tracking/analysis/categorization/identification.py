import json
import random
import pandas as pd

from bisect import bisect_left

def main():
    with open('./frames.json', 'r') as f:
        items = ['Tree', 'Vehicle', 'Billboard', 'Person']
        frames = json.load(f)
        fixations = [(random.uniform(0, 1), random.uniform(0, 1)) for _ in frames]
        # print('Frame  \tFixation     \tObjects')
        data = []
        for i, frame in enumerate(frames):
            # print(f'{i}   \t({"%.3f" % x}, {"%.3f" % y})\t{identify(x, y, frames[i])}')
            x, y = fixations[i]
            objects = identify(x, y, frame)
            boxes = [objects.get(item, None) for item in items]
            data.append([i, "(%.3f,  %.3f)" % (x, y)] + boxes)
        columns = ['Frame', 'Fixation'] + items
        df = pd.DataFrame(data, columns=columns)
        df.to_csv(r'./fixations.csv')

def identify(x, y, frame):
    min_confidence = 0.2
    scores = [float(s) for s in frame['detection_scores'][::-1]]
    cutoff = len(scores) - bisect_left(scores, min_confidence)
    print('Cut: ', cutoff)
    boxes = frame['detection_boxes'][:cutoff]
    entities = frame['detection_class_entities'][:cutoff]

    def inside_box(box):
        ymin, xmin, ymax, xmax = map(lambda s: float(s), box)
        return xmin <= x <= xmax and ymin <= y <= ymax

    # Return all entities that satisfy inside_box condition
    return {entities[j]: boxes[j] for j, box in enumerate(boxes[::-1]) if inside_box(box)}

if __name__ == '__main__':
    main()
