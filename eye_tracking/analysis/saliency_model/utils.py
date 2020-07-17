import pandas as pd

def get_fixations_data():
    """Converts detected fixation data into a working Pandas dataframe. 
    Expects data to be located in fixations.csv
    """
    df = pd.read_csv('fixations.csv')
    fixations = []
    prev_start = 0
    for i in range(len(df)):
        row = df.iloc[i]

        # fill in gaps
        if row['start_frame_index'] - prev_start > 0:
            for j in range(prev_start, row['start_frame_index']):
                fixations.append((0,0))
        
        # fill in fixations if high enough confidence
        if row['confidence'] > 0.8:
            for j in range(row['start_frame_index'], row['end_frame_index']):
                fixations.append((row['norm_pos_x'] , row['norm_pos_y']))
        else:
            for j in range(row['start_frame_index'], row['end_frame_index']):
                fixations.append((0, 0))

        prev_start = row['end_frame_index']
    return fixations