# actions/audio/device_control_nircmd.py

import subprocess
import logging
from pathlib import Path

from core.utils.path import get_nircmd_path

# Ruta absoluta al ejecutable de nircmd
NIRCMD_PATH = get_nircmd_path()

# Cache simple
_cached_output_volume = None
_cached_input_volume = None


def set_input_volume(volume_percent: int):
    """
    Ajusta el volumen del micrófono predeterminado (default recording device).
    :param volume_percent: Valor de volumen entre 0 y 100.
    """
    global _cached_input_volume

    level = int((volume_percent / 100.0) * 65535)

    if _cached_input_volume == level:
        logging.debug(f"🎙 Volumen de micrófono ya está en {volume_percent}%, se omite.")
        return

    logging.info(f"🎙 Ajustando micrófono a {volume_percent}% → {level}")
    subprocess.call([str(NIRCMD_PATH), "setsysvolume", str(level), "default_record"])

    _cached_input_volume = level


def set_output_volume(device_name: str, raw_value: int):
    """
    Ajusta el volumen general de salida (no por aplicación).
    :param device_name: Nombre del dispositivo (no usado por nircmd directamente).
    :param raw_value: Valor MIDI (0–127).
    """
    global _cached_output_volume

    level = int((raw_value / 127.0) * 65535)

    if _cached_output_volume == level:
        logging.debug(f"🔊 Volumen ya está en {raw_value}/127, se omite.")
        return

    logging.info(f"🔊 Ajustando salida a {raw_value}/127 → {level}")
    subprocess.call([str(NIRCMD_PATH), "setsysvolume", str(level)])

    _cached_output_volume = level
