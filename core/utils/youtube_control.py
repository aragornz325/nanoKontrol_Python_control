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
    """
    Busca una ventana visible de Chrome con "YouTube" en el título.

    Devuelve:
        Un objeto ventana que representa la primera ventana visible de Chrome con "YouTube" en el título,
        o None si no se encuentra ninguna.
    """
    for window in gw.getWindowsWithTitle("YouTube"):
        hwnd = window._hWnd
        if "Chrome" in window.title and win32gui.IsWindowVisible(hwnd):
            return window
    return None


def toggle_youtube_window_and_led(led_name="track1_rec"):
    """
    Alterna la visibilidad de una ventana de YouTube en Chrome y actualiza el estado de un LED especificado.
    Si una ventana de YouTube está abierta, intenta cerrarla y apaga el LED indicado.
    Si no se encuentra una ventana de YouTube, lanza una nueva ventana de Chrome con YouTube y enciende el LED después de verificar que la ventana está abierta.
    Args:
        led_name (str): Nombre del LED a actualizar. Por defecto es "track1_rec".
    Excepciones:
        Registra errores si no puede cerrar la ventana de YouTube o lanzar Chrome.
    """
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
