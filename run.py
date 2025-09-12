import os
import sys

# Ensure src/ is on sys.path for src-layout projects
ROOT = os.path.dirname(__file__)
SRC = os.path.join(ROOT, "src")
if SRC not in sys.path:
    sys.path.insert(0, SRC)

from authbot import run  # noqa: E402

if __name__ == "__main__":
    run()
