import subprocess
import psutil
import os
import logging
from led.led_control import set_led, pulse_led

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [APP] %(message)s")


def smart_launch_command(app):
    """
    Retorna una tupla (command, is_shell_required) basada en el nombre de la app.
    """
    # Si es ruta absoluta
    if os.path.isabs(app) and os.path.exists(app):
        return [app], False
    # Si parece un .exe
    if app.lower().endswith(".exe"):
        return [app], False
    # Caso genérico: nombre amigable, se lanza con start desde shell
    return f"start {app}", True


def toggle_app_and_led(process_name: str, led_name: str, launch_command=None):
    """
    Si el proceso está corriendo, lo mata (todos los que coincidan) y apaga el LED.
    Si no está, lo lanza y enciende el LED.
    """
    found = False

    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] and proc.info["name"].lower() == process_name.lower():
            try:
                logging.info(f"🛑 Cerrando {proc.pid} ({process_name})")
                proc.terminate()
                proc.wait(timeout=3)
                found = True
            except Exception as e:
                logging.error(f"💥 No se pudo terminar {proc.pid}: {e}")

    if found:
        set_led(led_name, False)
        return

    # Si no está, lo lanza
    if launch_command:
        try:
            command, use_shell = smart_launch_command(launch_command)
            logging.info(f"🚀 Lanzando: {launch_command}")
            subprocess.Popen(command, shell=use_shell)
            set_led(led_name, True)
        except Exception as e:
            logging.error(f"💥 Error al lanzar {launch_command}: {e}")
