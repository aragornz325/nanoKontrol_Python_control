import subprocess
import logging
from pathlib import Path

from core.utils.path import get_SoundVolumeView_path

SOUNDVOL_PATH = get_SoundVolumeView_path()
_volume_cache = {}
_mute_cache = {}

def _run_command(args):
    try:
        result = subprocess.run(
            [str(SOUNDVOL_PATH)] + args,
            capture_output=True,
            text=True,
        )
        return result.returncode, result.stdout.strip()
    except Exception as e:
        logging.error(f"💥 Error ejecutando SoundVolumeView: {e}")
        return -1, ""

def set_volume(name: str, volume_percent: int):
    volume = max(0, min(volume_percent, 100))
    if _volume_cache.get(name) == volume:
        logging.debug(f"🔁 Volumen de '{name}' ya está en {volume}%, se omite.")
        return

    code, _ = _run_command(["/SetVolume", name, str(volume)])
    if code == 0:
        _volume_cache[name] = volume
        logging.info(f"🔊 Volumen de '{name}' seteado a {volume}%")
    else:
        logging.warning(f"❌ No se pudo cambiar volumen de '{name}'")

def get_volume(name: str) -> int | None:
    code, _ = _run_command(["/GetPercent", name])
    if code != 0:
        logging.warning(f"❌ No se pudo obtener volumen de '{name}'")
        return None
    return code // 10  # Devuelve el % real

def mute(name: str):
    if _mute_cache.get(name) == True:
        return
    _run_command(["/Mute", name])
    _mute_cache[name] = True
    logging.info(f"🔇 '{name}' muteado")

def unmute(name: str):
    if _mute_cache.get(name) == False:
        return
    _run_command(["/Unmute", name])
    _mute_cache[name] = False
    logging.info(f"🔈 '{name}' desmuteado")

def toggle_mute(name: str):
    _run_command(["/Switch", name])
    _mute_cache[name] = not _mute_cache.get(name, False)
    logging.info(f"🔃 '{name}' mute cambiado a {_mute_cache[name]}")
