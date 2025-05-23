import subprocess
import psutil
import time
import logging
import threading
from led.led_control import set_led, pulse_led

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [EMULATOR] %(message)s")

EMULATOR_PATH = r"C:\Users\rodri\AppData\Local\Android\Sdk\emulator\emulator.exe"
ADB_PATH = r"C:\Users\rodri\AppData\Local\Android\Sdk\platform-tools\adb.exe"

emulator_toggle_lock = threading.Lock()


def _run_led_pulse_async(led_name: str, times=25, interval=0.15):
    threading.Thread(
        target=pulse_led, args=(led_name, times, interval), daemon=True
    ).start()


def _is_emulator_running(avd_name: str) -> bool:
    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            if (
                proc.info["name"] == "emulator.exe"
                and "-avd" in proc.info["cmdline"]
                and avd_name in proc.info["cmdline"]
            ):
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return False


def _kill_emulator_with_adb(avd_name: str) -> bool:
    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            if (
                proc.info["name"] == "emulator.exe"
                and "-avd" in proc.info["cmdline"]
                and avd_name in proc.info["cmdline"]
            ):
                for arg in proc.info["cmdline"]:
                    if arg.startswith("-port"):
                        port = arg.replace("-port", "")
                        adb_port = f"127.0.0.1:{port}"
                        subprocess.run(
                            [ADB_PATH, "-s", adb_port, "emu", "kill"], timeout=5
                        )
                        return True
                subprocess.run([ADB_PATH, "emu", "kill"], timeout=5)
                return True
        except Exception as e:
            logging.error(f"💥 Error usando ADB para cerrar {avd_name}: {e}")
    return False


def _force_kill_emulator(avd_name: str) -> bool:
    killed = False
    for proc in psutil.process_iter(["pid", "name", "cmdline"]):
        try:
            if proc.info["name"] in [
                "emulator.exe",
                "qemu-system-x86_64.exe",
            ] and avd_name in " ".join(proc.info["cmdline"]):
                proc.kill()
                killed = True
        except Exception as e:
            logging.error(f"💥 Error forzando cierre: {e}")
    return killed


def toggle_android_emulator(avd_name: str, led_name="track2_rec"):
    if not emulator_toggle_lock.acquire(blocking=False):
        logging.warning("⚠️ Emulador en transición. Ignorando solicitud duplicada.")
        _run_led_pulse_async(led_name, times=1, interval=0.1)
        return

    def _run():
        _run_led_pulse_async(led_name, times=25, interval=0.1)
        try:
            if _is_emulator_running(avd_name):
                logging.info(f"🔍 Emulador {avd_name} activo. Cerrando...")
                success = _kill_emulator_with_adb(avd_name)
                time.sleep(3)
                if not success or _is_emulator_running(avd_name):
                    logging.warning("⚠️ ADB falló. Intentando cierre forzado...")
                    _force_kill_emulator(avd_name)
                    time.sleep(2)

                if not _is_emulator_running(avd_name):
                    set_led(led_name, False)
                    logging.info(f"✅ Emulador {avd_name} cerrado")
                else:
                    logging.error(f"💥 No se pudo cerrar {avd_name}")
                return

            logging.info(f"🚀 Lanzando emulador {avd_name}")
            subprocess.Popen(
                [EMULATOR_PATH, "-avd", avd_name],
                creationflags=subprocess.CREATE_NO_WINDOW,
            )
            time.sleep(4)

            if _is_emulator_running(avd_name):
                set_led(led_name, True)
                logging.info(f"✅ Emulador {avd_name} iniciado")
            else:
                set_led(led_name, False)
                logging.warning(f"⚠️ El emulador {avd_name} no se lanzó correctamente")
        except Exception as e:
            logging.error(f"💥 Error general al alternar emulador: {e}")
            set_led(led_name, False)
        finally:
            emulator_toggle_lock.release()

    threading.Thread(target=_run, daemon=True).start()
