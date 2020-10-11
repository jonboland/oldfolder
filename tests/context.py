from pathlib import Path
import sys

# Enables oldfolder module imports when running tests
context = Path.cwd().parent / "oldfolder"
sys.path.insert(0, str(context))
