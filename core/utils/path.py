import logging
from pathlib import Path
import sys
import os
import shutil
import tempfile

def resource_path(relative_path: str) -> Path:
    return Path(getattr(sys, '_MEIPASS', Path(__file__).resolve().parent.parent.parent)) / relative_path

def get_nircmd_path() -> Path:
    return resource_path("bin/nircmd.exe")

def get_SoundVolumeView_path() -> Path:
    return resource_path("bin/SoundVolumeView.exe")


def extract_resource_to_temp(relative_path: str) -> Path:
    """Extrae un archivo embebido en PyInstaller a un path temporal accesible."""
    source = Path(getattr(sys, '_MEIPASS', Path('.'))) / relative_path
    target = Path(tempfile.gettempdir()) / Path(relative_path).name

    if not target.exists():
        shutil.copy(source, target)
        logging.info(f"📁 Recurso extraído: {target}")
    return target