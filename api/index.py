import os
import sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PARENT_DIR = os.path.dirname(CURRENT_DIR)

for p in [PARENT_DIR, CURRENT_DIR, os.getcwd()]:
    if p and p not in sys.path:
        sys.path.insert(0, p)

from main import app
