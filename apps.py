import psutil
import os
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [SCAN] %(message)s")


def list_launchable_apps():
    procesos = []

    for proc in psutil.process_iter(["pid", "name", "exe"]):
        try:
            name = proc.info["name"]
            exe = proc.info["exe"]
            if not name:
                continue

            path = exe if exe and os.path.exists(exe) else None
            launch_cmd = (
                path if path else (name if name.lower().endswith(".exe") else f"start {name}")
            )
            procesos.append((name, path or "❌ No path", launch_cmd))

        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    # Mostrar resultados útiles
    for name, path, cmd in sorted(procesos):
        logging.info(f"🧩 {name:25} | 📂 {path} | 🧠 launch: {cmd}")


if __name__ == "__main__":
    list_launchable_apps()
