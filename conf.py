import os

ABS_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(ABS_PATH)
DATA_DIR = os.path.join(BASE_DIR, "data")
RUN_DIR = os.path.join(DATA_DIR, "runs")
STORAGE_OUTPUTS = os.path.join(RUN_DIR, 'storage')