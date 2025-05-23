import logging
from pathlib import Path
import sys
import os
import shutil
import tempfile


def resource_path(relative_path: str) -> Path:
    """
    Devuelve la ruta absoluta a un recurso, manejando tanto entornos de desarrollo como entornos empaquetados con PyInstaller.

    Argumentos:
        relative_path (str): La ruta relativa al archivo de recurso.

    Retorna:
        Path: La ruta absoluta al recurso.

    Notas:
        - Si se ejecuta como un paquete de PyInstaller, utiliza la carpeta temporal almacenada en sys._MEIPASS.
        - De lo contrario, resuelve la ruta relativa a la raíz del proyecto.
    """
    return (
        Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent.parent))
        / relative_path
    )


def get_nircmd_path() -> Path:
    """
    Extrae el recurso 'nircmd.exe' del directorio 'bin' a una ubicación temporal y retorna su ruta.

    Retorna:
        Path: Ruta en el sistema de archivos al ejecutable extraído 'nircmd.exe'.
    """
    path = extract_resource_to_temp("bin/nircmd.exe")
    logging.info(f"🧪 nircmd extraído a: {path}")
    return path


def get_SoundVolumeView_path() -> Path:
    """
    Extrae el recurso 'SoundVolumeView.exe' a un directorio temporal y retorna su ruta.

    Retorna:
        Path: Ruta en el sistema de archivos al ejecutable extraído 'SoundVolumeView.exe'.
    """
    path = extract_resource_to_temp("bin/SoundVolumeView.exe")
    logging.info(f"🧪 SoundVolumeView extraído a: {path}")
    return path


def get_soundEqualizer_path() -> Path:
    """
    Extrae el recurso 'drum.wav' a un directorio temporal y retorna su ruta.

    Retorna:
        Path: Ruta en el sistema de archivos al ejecutable extraído 'drum.wav'.
    """
    path = extract_resource_to_temp("core/utils/percu.wav")
    logging.info(f"🧪 drum extraído a: {path}")
    return path


def extract_resource_to_temp(relative_path: str) -> Path:
    """
    Extrae un archivo de recurso desde el directorio empaquetado de la aplicación (por ejemplo, al usar PyInstaller)
    al directorio temporal del sistema.
    Argumentos:
        relative_path (str): Ruta relativa al archivo de recurso dentro del directorio de la aplicación.
    Retorna:
        Path: Ruta al archivo de recurso extraído en el directorio temporal.
    Notas:
        - Si el recurso ya ha sido extraído al directorio temporal, no se copiará nuevamente.
        - Registra un mensaje informativo cuando el recurso es extraído.
    """

    source = Path(getattr(sys, "_MEIPASS", Path("."))) / relative_path
    target = Path(tempfile.gettempdir()) / Path(relative_path).name

    if not target.exists():
        shutil.copy(source, target)
        logging.info(f"📁 Recurso extraído: {target}")
    return target
