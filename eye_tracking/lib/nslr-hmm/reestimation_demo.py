# Demonstrates usage of parameter reestimation methods with
# synthetic data. The provided reestimation is not recommended for real data analysis;
# is is known to converge to bad results, likely due to somewhat errorenous assumptions
# of the hidden markov model formulation.
#
# If estimating the transition and observation models simultaneously is enabled, the
# reestimation will often fail with an exception when any of the class gets a zero probability.
# This tends to happen often with bad convergences, which happen often.
#
# The reestimation code is given for reference and study. It's not very well tested
# and may contain errors. Bug reports and fixes are very welcome.

import numpy as np
import matplotlib.pyplot as plt
import scipy.signal
import nslr_hmm

# Generate simulated recording sessions. Note
# that these are not representative of real
# eye movements and will give very bad estimates.
sessions = []
for i in range(10):
    t = np.arange(0, 30, 0.01)
    saw = ((t*10)%10)/10.0*10.0 # 10 deg/second sawtooth
    eye = np.vstack(( saw, -saw )).T
    eye += np.random.randn(*eye.shape)*0.1
    
    # The logic for handling outliers in the classification
    # and reestimation is probably broken, and this should
    # probably always be None.
    outlier_idx = None

    sessions.append((t, eye, outlier_idx))


# Extract classification features from the sessions
session_features = nslr_hmm.dataset_features(sessions)

# Select the estimation method. The Viterbi one uses a robust observation
# matrix estimation, which is less likely to totally fail. The Viterbi method
# is not theoretically as sound as the Baum-Welch method.

#reestimate_observations = nslr_hmm.reestimate_observations_viterbi_robust
reestimate_observations = nslr_hmm.reestimate_observations_baum_welch

# Estimate new parameters based on the data
transition_probs, observation_model = reestimate_observations(session_features,
        # Setting either of these False can avoid
        # failure due to a class getting zero probability.
        estimate_transition_model=False,
        estimate_observation_model=True,
        # Enable to show an animated plot of the observation model estimation
        plot_process=True,
        )

# Classify one session using the new model(s)
t, eye, outliers = sessions[0]
sample_class, segmentation, seg_class = nslr_hmm.classify_gaze(t, eye, outliers=outliers,
        transition_probs=transition_probs,
        observation_model=observation_model)

# Plot the resulting classification
plt.figure()
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
