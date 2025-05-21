import subprocess
import psutil
import time
import logging
import pygetwindow as gw
import win32process
import win32con
import win32gui
from led.led_control import set_led

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [YT] %(message)s")


def _get_youtube_window():
    for window in gw.getWindowsWithTitle("YouTube"):
        hwnd = window._hWnd
        if "Chrome" in window.title and win32gui.IsWindowVisible(hwnd):
            return window
    return None


def toggle_youtube_window_and_led(led_name="track1_rec"):
    yt_window = _get_youtube_window()

    if yt_window:
        try:
            hwnd = yt_window._hWnd
            logging.info(f"🛑 Cerrando ventana YouTube (HWND {hwnd})")
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            set_led(led_name, False)
            return
        except Exception as e:
            logging.error(f"💥 Error al cerrar ventana YouTube: {e}")
            return

    # Si no está, la lanza
    try:
        subprocess.Popen(
            [
                "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
                "--new-window",
                "https://www.youtube.com/",
            ]
        )
        logging.info("🚀 Lanzando YouTube en nueva ventana de Chrome")
        # Podés esperar 2 segundos y luego verificar de nuevo para encender el LED
        time.sleep(2)
        if _get_youtube_window():
            set_led(led_name, True)
    except Exception as e:
        logging.error(f"💥 No se pudo lanzar Chrome: {e}")
