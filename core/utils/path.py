import logging
from pathlib import Path
import sys
import os
import shutil
import tempfile


def resource_path(relative_path: str) -> Path:
    return (
        Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent.parent))
        / relative_path
    )


def get_nircmd_path() -> Path:
    path = extract_resource_to_temp("bin/nircmd.exe")
    logging.info(f"🧪 nircmd extraído a: {path}")
    return path


def get_SoundVolumeView_path() -> Path:
    path = extract_resource_to_temp("bin/SoundVolumeView.exe")
    logging.info(f"🧪 SoundVolumeView extraído a: {path}")
    return path


def extract_resource_to_temp(relative_path: str) -> Path:
    source = Path(getattr(sys, "_MEIPASS", Path("."))) / relative_path
    target = Path(tempfile.gettempdir()) / Path(relative_path).name

    if not target.exists():
        shutil.copy(source, target)
        logging.info(f"📁 Recurso extraído: {target}")
    return target
