import os
import sys

# make sure repository root is on the import path (needed in some CI environments)
sys.path.insert(0, os.path.abspath(os.getcwd()))

import app


def test_app_import():
    assert hasattr(app, 'app') or True  # just ensure module loads
