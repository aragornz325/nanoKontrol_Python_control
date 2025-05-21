from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume
from comtypes import CoInitialize
import win32process
import win32gui
import logging
import psutil


from core.utils.youtube_control import _get_youtube_window


def set_volume_for_youtube_window(volume: float):
    try:
        CoInitialize()
        yt_window = _get_youtube_window()
        if not yt_window:
            logging.warning("❌ No se encontró ventana de YouTube.")
            return

        hwnd = yt_window._hWnd
        _, parent_pid = win32process.GetWindowThreadProcessId(hwnd)

        parent_proc = psutil.Process(parent_pid)
        children = parent_proc.children(recursive=True)
        all_pids = [parent_pid] + [p.pid for p in children]

        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.pid in all_pids:
                interface = session._ctl.QueryInterface(ISimpleAudioVolume)
                interface.SetMasterVolume(volume, None)
                logging.info(
                    f"🔊 Volumen de YouTube (PID {session.Process.pid}) → {volume:.2f}"
                )
                return

        logging.warning(
            f"❌ No se encontró sesión de audio entre los subprocesos de YouTube (PID {parent_pid})"
        )

    except Exception as e:
        logging.error(f"💥 Error al ajustar volumen YouTube: {e}")
