# 5. Connectivity Analysis (EEG)
import mne
from mne.connectivity import spectral_connectivity

def eeg_connectivity_analysis(epochs, method='pli', fmin=8, fmax=13):
    """Calculates EEG connectivity using Phase Lag Index (PLI)."""

    freq_bands = [(fmin, fmax)]  # Alpha band example
    con, freqs, times, n_epochs, n_tapers = spectral_connectivity(
        epochs, method=method, mode='fourier', sfreq=epochs.info['sfreq'],
        fmin=fmin, fmax=fmax, faverage=True, verbose=False)

    return con[0]  # Returns the connectivity matrix for the specified frequency band

# Details:
# - Function: eeg_connectivity_analysis
# - Algorithm: Spectral connectivity analysis using Phase Lag Index (PLI).
# - Rationale: Quantifies the interactions between different EEG channels in the frequency domain.
# - Justification: Reveals altered brain network dynamics in neurological disorders.
