import os
from pathlib import Path

path = Path(os.getcwd())
project_root = path.parent.parent

ROOT_DIR = project_root
DATA_DIR = path.joinpath(ROOT_DIR, 'data')
DB_DIR = path.joinpath(ROOT_DIR, 'db')
