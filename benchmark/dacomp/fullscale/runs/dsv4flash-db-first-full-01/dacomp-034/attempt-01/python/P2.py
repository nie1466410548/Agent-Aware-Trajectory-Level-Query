import pandas as pd
import numpy as np
from scipy import stats
import os
print("CWD:", os.getcwd())
print("Files in results:", os.listdir('results') if os.path.isdir('results') else 'no results dir')
# Try to find the file
for f in os.listdir('results'):
    print(f)