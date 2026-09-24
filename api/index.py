import sys
import os

# Tambahkan parent directory ke sys.path agar semua modul (config, database, dll) dapat di-import
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from app import app
