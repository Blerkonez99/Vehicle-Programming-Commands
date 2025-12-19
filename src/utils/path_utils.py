import os
import sys


def get_base_path() -> str:
    """Return the base path for accessing bundled resources.

    When packaged with PyInstaller, data files are placed alongside the
    executable within the temporary _MEIPASS directory. In development,
    resources live in the repository root.
    """
    if hasattr(sys, "_MEIPASS"):
        return sys._MEIPASS

    return os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))

