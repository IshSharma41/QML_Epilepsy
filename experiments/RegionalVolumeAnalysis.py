# 3. Regional Volume Analysis (MRI)
import ants
from nilearn import image, datasets, input_data
import numpy as np

def regional_volume_analysis(mri_file, atlas="harvard_oxford"):
    """Extract regional brain volumes using an atlas."""
    
    img = ants.image_read(mri_file)
    
    if atlas == "harvard_oxford":
        atlas_data = datasets.fetch_atlas_harvard_oxford("cort-maxprob-thr25-2mm")
        atlas_filename = atlas_data.maps
    
    atlas_img = image.load_img(atlas_filename)
    resampled_atlas = image.resample_to_img(atlas_img, image.load_img(img.clone().to_filename()), interpolation=0)
    masker = input_data.NiftiLabelsMasker(resampled_atlas)
    
    regional_volumes = []
    
    data = img.numpy()
    masked_data = masker.fit_transform(image.new_img_like(atlas_img, data))
    regional_volumes = np.sum(masked_data, axis=0)
    return regional_volumes

# Details:
# - Function: regional_volume_analysis
# - Algorithm: Atlas-based regional volume extraction.
# - Rationale: Uses an anatomical atlas to segment brain regions and calculate their volumes.
# - Justification: Provides more focused regional information than voxel-based analysis.
