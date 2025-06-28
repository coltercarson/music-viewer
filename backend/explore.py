import math
from pathlib import Path
import json
import hashlib
from collections import defaultdict
from plot import check_layout

from prepare_metadata import *

##
base_dir = Path(__file__).resolve().parents[1]
input_json = base_dir / "data" / "json" / "output.json"
output_json = base_dir / "frontend" / "public" / "prepared.json"

main(input_json, output_json)
check_layout()  # Optional: visualize the layout after preparation
