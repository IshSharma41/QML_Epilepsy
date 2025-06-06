# 6. Surface-Based Morphometry (MRI)
import subprocess
import os

def freesurfer_surface_morphometry(mri_file, subject_id, freesurfer_subjects_dir):
    """Performs surface-based morphometry using FreeSurfer."""

    subject_dir = os.path.join(freesurfer_subjects_dir, subject_id)
    os.makedirs(subject_dir, exist_ok=True)

    # FreeSurfer recon-all command
    recon_command = [
        'recon-all',
        '-i', mri_file,
        '-s', subject_id,
        '-all',
        '-sd', freesurfer_subjects_dir
    ]

    try:
        subprocess.run(recon_command, check=True)
        return subject_dir #return the directory where the freesurfer output is located.

    except subprocess.CalledProcessError as e:
        print(f"FreeSurfer processing failed: {e}")
        return None

# Details:
# - Function: freesurfer_surface_morphometry
# - Algorithm: FreeSurfer's recon-all pipeline.
# - Rationale: Performs detailed cortical surface reconstruction and measures cortical thickness, surface area, etc.
# - Justification: Captures subtle changes in cortical structure that might be missed by voxel-based methods.
