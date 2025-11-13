import sys
from pathlib import Path

# Ensure project root is on sys.path so `_supporting` and `src` imports work.
ROOT = Path(__file__).resolve().parent
root_str = str(ROOT)

if root_str not in sys.path:
    sys.path.insert(0, root_str)
