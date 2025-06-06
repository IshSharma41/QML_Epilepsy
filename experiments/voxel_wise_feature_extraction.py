# 4. Voxel-wise Feature Extraction (PET)
from nilearn import image, input_data
import numpy as np

def voxel_wise_feature_extraction(pet_file, mask_file):
    """Extracts voxel wise features from a pet image."""

    pet_img = image.load_img(pet_file)
    mask_img = image.load_img(mask_file)

    masker = input_data.NiftiMasker(mask_img)
    masked_data = masker.fit_transform(pet_img)

    return masked_data

# Details:
# - Function: voxel_wise_feature_extraction
# - Algorithm: Mask-based voxel extraction.
# - Rationale: Reduces the amount of pet data by only extracting data from within a mask.
# - Justification: Reduces computational load, and focuses the data on a specific region.
