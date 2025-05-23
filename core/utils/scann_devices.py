import subprocess
import csv
from pathlib import Path
import tempfile
import logging
import time

from core.utils.path import get_SoundVolumeView_path
from led.led_control import set_led, toggle_led

SOUNDVOL_PATH = get_SoundVolumeView_path()
_last_device_update = {}
_last_volume_sent = {}


def set_volume_for_device(
    device_name: str,
    volume_percent: int,
):
    """
    Establece el volumen para un dispositivo de audio especificado a un porcentaje dado.
    Esta función actualiza el volumen del dispositivo usando una herramienta externa,
    aplicando un intervalo mínimo de 100ms entre actualizaciones e ignorando cambios menores al 2%.
    Registra la operación y maneja los errores de forma controlada.
    Args:
        device_name (str): Nombre del dispositivo de audio a ajustar.
        volume_percent (int): Nivel de volumen deseado como porcentaje (0-100).
    Raises:
        subprocess.CalledProcessError: Si falla el comando externo de ajuste de volumen.
        Exception: Para cualquier otro error inesperado durante la operación.
    """
    global _last_device_update, _last_volume_sent

    now = time.time()
    volume = max(0, min(volume_percent, 100))

    last_time = _last_device_update.get(
        device_name,
        0,
    )
    last_volume = _last_volume_sent.get(
        device_name,
        None,
    )

    # No actualizar si no pasaron 100ms
    if now - last_time < 0.1:
        return

    # No actualizar si el cambio es menor a 2%
    if last_volume is not None and abs(last_volume - volume) < 2:
        return

    try:
        subprocess.run(
            [str(SOUNDVOL_PATH), "/SetVolume", device_name, str(volume)], check=True
        )
        _last_device_update[device_name] = now
        _last_volume_sent[device_name] = volume
        logging.info(f"🎚️ {device_name} → {volume}%")
    except subprocess.CalledProcessError as e:
        logging.error(f"💥 SoundVolumeView error: {e}")
    except Exception as e:
        logging.error(f"💥 Error general al ajustar '{device_name}': {e}")


def is_device_muted(device_name: str) -> bool | None:
    """
    Retorna True si el dispositivo está muteado, False si no. None si falla.
    """
    try:
        result = subprocess.run(
            [str(SOUNDVOL_PATH), "/GetMute", device_name],
            capture_output=True,
            text=True,
            timeout=2,
        )
        if result.returncode == 0:
            val = result.stdout.strip()
            if val == "1":
                return True
            elif val == "0":
                return False
        logging.warning(
            f"❓ Estado de mute indefinido para '{device_name}': {result.stdout.strip()}"
        )
    except Exception as e:
        logging.error(f"💥 Error al obtener estado mute: {e}")
    return None


def toggle_mute_for_device(device_param: str, led_name: str = None):
    try:
        subprocess.run([str(SOUNDVOL_PATH), "/Switch", device_param], check=True)
        logging.info(f"🔇 Toggle mute para '{device_param}'")

        if led_name:
            time.sleep(0.1)
            if device_param.startswith("Default"):
                muted = is_device_muted(device_param)
                if muted is not None:
                    set_led(led_name, muted)
                    logging.info(f"💡 LED '{led_name}' → {'ON' if muted else 'OFF'}")
                else:
                    logging.warning(
                        f"⚠️ No se pudo determinar si '{device_param}' está muteado"
                    )
            else:
                toggle_led(led_name)  # fallback visual sin estado real
                logging.info(f"💡 LED '{led_name}' → toggled (sin verificación real)")
    except Exception as e:
        logging.error(f"💥 Error al alternar mute de '{device_param}': {e}")


def list_audio_devices():
    """
    Retorna una lista de dispositivos físicos detectados por SoundVolumeView.
    Cada ítem contiene: name, direction, device_type, id
    """
    temp_file = Path(tempfile.gettempdir()) / "audio_devices.csv"

    # 🔎 DEBUG: Verificar si el path es correcto
    print("🧪 SoundVolumeView path →", SOUNDVOL_PATH)

    subprocess.run([str(SOUNDVOL_PATH), "/scomma", str(temp_file)], check=True)

    devices = []
    with open(temp_file, encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        first_row = next(reader, None)
        if not first_row:
            raise RuntimeError("⚠️ No se detectaron dispositivos en el archivo CSV.")

        # Detectar columnas automáticamente (por compatibilidad futura)
        item_type_key = next(
            (k for k in first_row.keys() if k.lower() in ["type", "item type"]), None
        )
        name_key = next(
            (
                k
                for k in first_row.keys()
                if "name" in k.lower() and "command" not in k.lower()
            ),
            None,
        )
        direction_key = next(
            (k for k in first_row.keys() if "direction" in k.lower()), None
        )
        dev_type_key = next(
            (
                k
                for k in first_row.keys()
                if "device name" in k.lower() or "device type" in k.lower()
            ),
            None,
        )
        id_key = next(
            (k for k in first_row.keys() if "command-line" in k.lower()), None
        )

        if not all([item_type_key, name_key, direction_key, dev_type_key, id_key]):
            raise RuntimeError(
                "❌ No se pudieron detectar las columnas necesarias del CSV."
            )

        # Incluir el primer row (ya leído)
        if first_row[item_type_key] in ["Device", "Subunit"]:
            devices.append(
                {
                    "name": first_row[name_key],
                    "direction": first_row[direction_key],
                    "device_type": first_row[dev_type_key],
                    "id": first_row[id_key],
                }
            )

        # Continuar con el resto
        for row in reader:
            if row[item_type_key] in ["Device", "Subunit"]:
                devices.append(
                    {
                        "name": row[name_key],
                        "direction": row[direction_key],
                        "device_type": row[dev_type_key],
                        "id": row[id_key],
                    }
                )

    return devices
