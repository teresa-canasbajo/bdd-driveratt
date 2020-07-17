import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import ..nslr_hmm

# Simulate a dummy recording session
t = np.arange(0, 5, 0.01)
saw = ((t*10)%10)/10.0*10.0 # 10 deg/second sawtooth
horiz_gaze = saw
vert_gaze = -saw
eye = np.vstack(( horiz_gaze, vert_gaze )).T
eye += np.random.randn(*eye.shape)*0.1

# Segment the data and classify the segments in one go using
# the default parameters.
sample_class, segmentation, seg_class = nslr_hmm.classify_gaze(t, eye)

COLORS = {
        nslr_hmm.FIXATION: 'blue',
        nslr_hmm.SACCADE: 'black',
        nslr_hmm.SMOOTH_PURSUIT: 'green',
        nslr_hmm.PSO: 'yellow',
}

plt.plot(t, eye[:,0], '.')
for i, seg in enumerate(segmentation.segments):
    cls = seg_class[i]
    plt.plot(seg.t, np.array(seg.x)[:,0], color=COLORS[cls])

plt.show()
