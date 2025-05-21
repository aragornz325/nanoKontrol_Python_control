from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from comtypes import CLSCTX_ALL, CoInitialize
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [AUDIO] %(message)s")

_session_cache = {}
_session_names = {}

def set_volume_for_app(target_name: str, volume: float):
    """
    Establece el volumen para una app activa.
    :param target_name: Parte del nombre del proceso, e.g. "Spotify"
    :param volume: Nivel de volumen entre 0.0 y 1.0
    """
    try:
        CoInitialize()
    except:
        pass

    target_name = target_name.lower()

    # Verificar si ya está en caché y sesión activa
    if target_name in _session_cache:
        try:
            current_sessions = [s.Process.name().lower() for s in AudioUtilities.GetAllSessions() if s.Process]
            if all(target_name not in s for s in current_sessions):
                raise RuntimeError("Sesión ya no está activa")

            _session_cache[target_name].SetMasterVolume(volume, None)
            logging.info(f"🔊 (cache) Volumen de {target_name} → {volume:.2f}")
            return
        except Exception as e:
            logging.warning(f"⚠️ Caché inválida para {target_name}, se reinicia: {e}")
            del _session_cache[target_name]  # Resetear si falla

    # Buscar la sesión manualmente
    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process and target_name in session.Process.name().lower():
            interface = session._ctl.QueryInterface(ISimpleAudioVolume)
            _session_cache[target_name] = interface
            _session_names[target_name] = session.Process.name()
            interface.SetMasterVolume(volume, None)
            logging.info(f"🔊 Volumen de {session.Process.name()} → {volume:.2f}")
            return

    logging.warning(f"❌ No se encontró ninguna sesión de audio con '{target_name}' activa.")

def list_active_audio_sessions():
    """Muestra las sesiones activas que tienen audio asociado."""
    try:
        CoInitialize()
    except:
        pass

    sessions = AudioUtilities.GetAllSessions()
    for session in sessions:
        if session.Process:
            logging.info(f"🎧 Sesión activa: {session.Process.name()}")
