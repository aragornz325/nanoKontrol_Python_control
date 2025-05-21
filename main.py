import sys, subprocess, os
from pystray import Icon, MenuItem, Menu
from PIL import Image

DAEMON_PROC = None


def resource_path(relative_path):
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, relative_path)


def start_daemon():
    global DAEMON_PROC
    daemon_path = resource_path("mcc_command_deck_v3.exe")
    if not os.path.exists(daemon_path):
        print(f"❌ No se encontró: {daemon_path}")
        return
    DAEMON_PROC = subprocess.Popen([daemon_path])


def stop_daemon():
    global DAEMON_PROC
    if DAEMON_PROC:
        DAEMON_PROC.terminate()
        DAEMON_PROC = None


def open_config_ui(icon, item):
    # En modo empaquetado, lanzamos el EXE de la UI
    if getattr(sys, "frozen", False):
        subprocess.Popen([resource_path("configurator.exe")])
    else:
        subprocess.Popen([sys.executable, resource_path("ui/configurator.py")])


def exit_app(icon, item):
    stop_daemon()
    icon.stop()


if __name__ == "__main__":
    start_daemon()
    image = Image.open(resource_path("icon.ico"))
    menu = Menu(
        MenuItem("🛠 Configurar...", open_config_ui), MenuItem("❌ Salir", exit_app)
    )
    Icon("nanoKONTROL", image, "nanoKontrol", menu).run()
