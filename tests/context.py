from pathlib import Path
import sys

# Enables oldfolder module imports when running tests
context = Path(__file__).resolve().parents[1] / "oldfolder"
sys.path.insert(0, str(context))
