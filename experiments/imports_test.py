

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# test_import.py
from src.preprocessing_modules.modules import mri_harmonization
print("Success!")
