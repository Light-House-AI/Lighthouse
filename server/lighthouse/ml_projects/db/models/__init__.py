"""
Contains database models.
"""

from os.path import dirname, basename, isfile, join
import glob


def load_all_models():
    """Imports all models."""

    files = glob.glob(join(dirname(__file__), "*.py"))
    modules = [
        basename(f)[:-3] for f in files
        if isfile(f) and not f.endswith('__init__.py')
    ]

    for module in modules:
        __import__("models." + module)
