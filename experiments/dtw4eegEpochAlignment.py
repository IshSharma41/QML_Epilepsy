# 7. Dynamic Time Warping (DTW) for EEG Epoch Alignment
from fastdtw import fastdtw
import numpy as np

def dtw_epoch_alignment(epochs, reference_epoch_index=0):
    """Aligns EEG epochs using Dynamic Time Warping (DTW)."""

    aligned_epochs = []
    reference_epoch = epochs.get_data()[reference_epoch_index]

    for epoch in epochs.get_data():
        distances = []
        aligned_epoch = []
        for channel_data in epoch:
            distance, path = fastdtw(reference_epoch[0], channel_data)
            distances.append(distance)
            warped_channel = []
            for i, j in path:
                warped_channel.append(channel_data[j])
            aligned_epoch.append(np.array(aligned_epoch))

    return aligned_epochs

# Details:
# - Function: dtw_epoch_alignment
# - Algorithm: Dynamic Time Warping (DTW).
# - Rationale: Aligns EEG epochs even with temporal variations.
# - Justification: Improves the comparison of time-locked EEG features.
