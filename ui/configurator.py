import os
import subprocess
import sys
from pathlib import Path

import psutil

from core.enums.data import Fader, Knob, Button, Label, Transport, Action
from core.utils.scann_devices import list_audio_devices

sys.path.append(str(Path(__file__).resolve().parents[1]))

import threading
import time
import rtmidi
from dearpygui import dearpygui as dpg
from db.assignments_db import init_db, get_all_assignments, save_assignment


# =================== FUNCIONES ===================


def is_nanokontrol_connected():
    try:
        midi_in = rtmidi.MidiIn()
        ports = midi_in.get_ports()
        return any("nanoKONTROL2" in p for p in ports)
    except Exception:
        return False


def update_led_status():
    if is_nanokontrol_connected():
        dpg.set_value("led_status", "🟢 Conectado")
        dpg.configure_item("led_status", color=(0, 255, 0))
    else:
        dpg.set_value("led_status", "🔴 No conectado")
        dpg.configure_item("led_status", color=(255, 0, 0))


def setup_led_checker():
    def loop():
        while True:
            update_led_status()
            time.sleep(2)

    threading.Thread(target=loop, daemon=True).start()


# =================== SETUP ===================

init_db()
stored_assignments = {
    control_id: {"action": action_name, "params": params}
    for control_id, action_name, params in get_all_assignments()
}

FADERS = [f.value for f in Fader]
KNOBS = [k.value for k in Knob]
BUTTONS = [b.value for b in Button]
TRANSPORT = [t.value for t in Transport]
ALL_BUTTONS = BUTTONS + TRANSPORT
ACTIONS = [a.value for a in Action]

combo_ids = {}
param_ids = {}
container_ids = {}


DEVICE_ALIASES = {
    "Auriculares (salida por defecto)": "DefaultRenderDevice",
    "Micrófono (entrada por defecto)": "DefaultCaptureDevice",
}

real_devices = list_audio_devices()


PHYSICAL_DEVICE_MAP = {
    **DEVICE_ALIASES,
    **{f'{d["name"]} ({d["device_type"]})': d["id"] for d in real_devices},
}
PHYSICAL_DEVICES = list(PHYSICAL_DEVICE_MAP.keys())


def debug_csv_headers():
    from pathlib import Path
    import tempfile
    import csv

    temp_file = Path(tempfile.gettempdir()) / "audio_devices.csv"
    print(f"📂 Leyendo archivo: {temp_file}")

    with open(temp_file, encoding="utf-8", newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        headers = reader.fieldnames
        print("🧠 Encabezados detectados en el CSV:")
        for h in headers:
            print(f"  - {h}")


def save_callback(sender, app_data, user_data):
    control_id = user_data
    action = dpg.get_value(combo_ids[control_id])
    params = dpg.get_value(param_ids[control_id])

    if action in ["knob_volume", "toggle_device_mute"]:
        id_val = PHYSICAL_DEVICE_MAP.get(params)
        if id_val:
            params = id_val

    save_assignment(control_id, action, params)
    print(f"[{control_id}] asignado a '{action}' con parámetros: {params}")


def update_param_field(control_id):
    action = dpg.get_value(combo_ids[control_id])
    param_tag = param_ids[control_id]
    container = container_ids[control_id]

    # Eliminar el parámetro actual
    dpg.delete_item(param_tag, children_only=False)

    if action in ["knob_volume", "toggle_device_mute"]:
        dpg.add_combo(
            PHYSICAL_DEVICES,
            default_value="",
            width=250,
            tag=param_tag,
            parent=container,
        )
    else:
        dpg.add_input_text(
            default_value="",
            hint="Parámetros",
            width=250,
            tag=param_tag,
            parent=container,
        )


def render_controls(name, controls):
    with dpg.child_window(label=name, width=-1, height=0):
        for control in controls:
            container_tag = f"{control}_container"
            with dpg.group(horizontal=True, tag=container_tag):
                dpg.add_text(control, bullet=True)

                combo_tag = f"{control}_combo"
                param_tag = f"{control}_param"

                default_action = stored_assignments.get(control, {}).get("action", "")
                default_params = stored_assignments.get(control, {}).get("params", "")

                combo_ids[control] = combo_tag
                param_ids[control] = param_tag
                container_ids[control] = container_tag

                # Acción con callback
                dpg.add_combo(
                    ACTIONS,
                    default_value=default_action,
                    width=180,
                    tag=combo_tag,
                    callback=lambda s, a, u: update_param_field(u),
                    user_data=control,
                )

                # Campo de parámetros inicial
                dpg.add_input_text(
                    default_value=default_params,
                    hint="Parámetros",
                    width=250,
                    tag=param_tag,
                )


def restart_daemon():
    exe_name = "mcc_command_deck_v3.exe"

    # 🧨 Matar procesos existentes del daemon
    for proc in psutil.process_iter(["pid", "name"]):
        if proc.info["name"] == exe_name:
            try:
                proc.kill()
                print(f"🔪 Proceso '{exe_name}' terminado (PID {proc.pid})")
            except Exception as e:
                print(f"⚠️ No se pudo terminar el proceso {proc.pid}: {e}")

    # 🚀 Relanzar el daemon desde el mismo folder del EXE
    exe_path = os.path.join(os.path.dirname(sys.executable), exe_name)
    if os.path.exists(exe_path):
        subprocess.Popen([exe_path])
        print(f"🚀 Daemon relanzado desde: {exe_path}")
    else:
        print(f"❌ No se encontró el ejecutable: {exe_path}")


def save_all_assignments():
    for control_id in combo_ids:
        action = dpg.get_value(combo_ids[control_id])
        params = dpg.get_value(param_ids[control_id])

        # Reemplazar nombre legible por ID si corresponde
        if action in ["knob_volume", "toggle_device_mute"]:
            id_val = PHYSICAL_DEVICE_MAP.get(params)
            if id_val:
                params = id_val

        save_assignment(control_id, action, params)
        print(f"[{control_id}] => {action} [{params}]")


# debug_csv_headers()


def build_ui():
    with dpg.window(label="nanoKontrol Configurator", width=800, height=600):
        dpg.add_text("Asignador de Controles nanoKONTROL2")
        dpg.add_separator()

        dpg.add_text("🔴 No conectado", tag="led_status", color=(255, 0, 0))
        setup_led_checker()

        with dpg.child_window(autosize_x=True, autosize_y=False, height=450):
            with dpg.tab_bar():
                with dpg.tab(label=Label.FADERS.value):
                    render_controls(Label.FADERS.value, FADERS)
                with dpg.tab(label=Label.KNOBS.value):
                    render_controls(Label.KNOBS.value, KNOBS)
                with dpg.tab(label=Label.BOTONES.value):
                    render_controls(Label.BOTONES.value, ALL_BUTTONS)

        dpg.add_separator()
        dpg.add_button(
            label="Guardar y relanzar daemon",
            callback=lambda: (save_all_assignments(), restart_daemon()),
            width=100,
            height=50,
        )


# =================== START UI ===================

dpg.create_context()
dpg.create_viewport(title="nanoKONTROL2 Config", width=800, height=700)
dpg.setup_dearpygui()
build_ui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
