# 1. Adaptive Artifact Rejection (EEG)
import mne
import numpy as np

def adaptive_artifact_rejection(epochs, window_size=5, threshold_factor=3):
    """Adaptive artifact rejection based on local signal statistics."""
    
    epochs_data = epochs.get_data()
    rejected_epochs = []
    
    for epoch_idx, epoch in enumerate(epochs_data):
        for channel_data in epoch:
            windowed_stds = []
            for i in range(0, len(channel_data), window_size):
                window = channel_data[i:i + window_size]
                if len(window) > 0:
                    windowed_stds.append(np.std(window))
            
            if windowed_stds:
                global_std = np.mean(windowed_stds)
                threshold = global_std * threshold_factor
                if np.any(np.abs(channel_data) > threshold):
                    rejected_epochs.append(epoch_idx)
                    break #reject epoch if any channel has artifacts.
    
    return epochs.drop(rejected_epochs)

# Details:
# - Function: adaptive_artifact_rejection
# - Algorithm: Adaptive thresholding based on local standard deviations.
# - Rationale: Uses a sliding window to calculate local standard deviations, then rejects epochs that exceed a threshold relative to the mean standard deviation.
# - Justification: More robust to varying signal-to-noise ratios compared to fixed thresholds.
