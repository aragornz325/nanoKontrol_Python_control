import rtmidi
import subprocess
import logging
import time
from core.utils.marquee import play_audio_equalizer, launch_marquee_thread
from actions.volumen_device_control import set_device_volume_scaled
from audio.volumen_control import set_volume_for_app
from audio.youtube_control_audio import set_volume_for_youtube_window
from config.assignments import KNOB_DEVICE_ASSIGNMENTS
from controller_registry import register_action, register_cc_action, handle_midi_event
from core.enums.data import Action, Transport, MultimediaActions
from core.utils.app_control import toggle_app_and_led
from core.utils.launch_emulator import toggle_android_emulator
from core.utils.scann_devices import set_volume_for_device, toggle_mute_for_device
from core.utils.youtube_control import toggle_youtube_window_and_led
from db.assignments_db import get_all_assignments, init_db
import os
import keyboard

from led.led_control import pulse_led, set_led


logging.basicConfig(level=logging.INFO, format="%(asctime)s - [Main] %(message)s")


def execute_action(action: str, params: str, value=None, control_id=None):
    try:
        action_enum = Action(action)
    except ValueError:
        logging.warning(f"⚠️ Acción no reconocida: {action}")
        return
    # ========= ACCIONES DE CONTROL DE APLICACIONES =================
    if action_enum == Action.LAUNCH_APP:
        process_name = os.path.basename(params)
        toggle_app_and_led(
            process_name=process_name,
            led_name=control_id,
            launch_command=params,
        )

    elif action_enum == Action.LAUNCH_EMULATOR:
        if not params:
            logging.warning(f"⚠️ No se especificó emulador para {control_id}")
            return
        try:
            toggle_android_emulator(params, led_name=control_id)
        except Exception as e:
            logging.error(f"💥 Error al alternar emulador {params}: {e}")

    # =========== ACCIONES DE MARQUEE & DRUM =================
    elif action_enum == Action.MAQUEE:
        if not params:
            logging.warning(f"⚠️ No se especificó texto para marquee en {control_id}")
            return
        try:
            launch_marquee_thread(params, set_led_fn=set_led)
        except Exception as e:
            logging.error(f"💥 Error al iniciar marquee: {e}")

    elif action_enum == Action.DRUM:
        try:
            play_audio_equalizer("percu.wav", set_led_fn=set_led)
        except Exception as e:
            logging.error(f"💥 Error al iniciar marquee: {e}")

    # ========== ACCIONES DE CONTROL =================
    elif action_enum == Action.YOUTUBE:
        toggle_youtube_window_and_led(led_name=control_id)

    elif action_enum == Action.PLAY_PAUSE:
        press_media_key(
            MultimediaActions.PLAY_PAUSE.value,
            Transport.PLAY.value,
        )
    elif action_enum == Action.NEXT_TRACK:
        press_media_key(
            MultimediaActions.NEXT_TRACK.value,
            Transport.FORWARD.value,
        )
    elif action_enum == Action.PREV_TRACK:
        press_media_key(
            MultimediaActions.PREV_TRACK.value,
            Transport.REWIND.value,
        )
    elif action_enum == Action.STOP.value:
        press_media_key(
            MultimediaActions.STOP.value,
            Transport.STOP.value,
        )

    # ============ ACCIONES DE VOLUMEN =================

    elif action_enum == Action.TOGGLE_DEVICE_MUTE:
        if not params:
            logging.warning(f"⚠️ No se especificó dispositivo para mute en {control_id}")
            return
        try:
            toggle_mute_for_device(params, led_name=control_id)
        except Exception as e:
            logging.error(f"💥 Error al alternar mute del dispositivo {params}: {e}")

    elif action_enum == Action.SET_VOLUME:
        try:
            v = float(value) / 127.0
            set_volume_for_app(params, v)
        except Exception as e:
            logging.error(f"💥 No se pudo setear volumen: {e}")

    elif action_enum == Action.KNOB_VOLUME:
        if not params:
            logging.warning(f"⚠️ No se especificó dispositivo en {control_id}")
            return
        try:
            volume_percent = int((int(value) / 127.0) * 100)

            set_volume_for_device(params, volume_percent)
            logging.info(f"🎛️ {control_id} → {params} = {volume_percent}%")
        except Exception as e:
            logging.error(f"💥 Error al ajustar volumen de dispositivo {params}: {e}")

    elif action_enum == Action.YOUTUBE_VOLUME:
        try:
            v = float(value) / 127.0
            set_volume_for_youtube_window(v)
        except Exception as e:
            logging.error(f"💥 No se pudo setear volumen de YouTube: {e}")

    elif action_enum == Action.OPEN_BROWSER:
        subprocess.Popen(["start", params], shell=True)

    elif action_enum == Action.APP_VOLUME:
        try:
            v = float(value) / 127.0
            set_volume_for_app(params, max(0.0, min(v, 1.0)))
            logging.info(f"🔊 Volumen {params} → {v:.2f}")
        except Exception as e:
            logging.error(f"💥 No se pudo setear volumen de app '{params}': {e}")

    else:
        logging.warning(f"⚠️ Acción no implementada: {action}")


def set_volume_scaled(app, raw):
    try:
        value = float(raw) / 127.0
        logging.info(f"📏 Valor normalizado para {app}: {value:.2f}")
        set_volume_for_app(app, max(0.0, min(value, 1.0)))
    except Exception as e:
        logging.error(f"💥 Error en conversión de volumen: {e}")


def press_media_key(key_name, led_name=None):
    try:
        keyboard.send(key_name)
        print(f"🎮 Tecla multimedia enviada: {key_name}")
        if led_name:
            pulse_led(led_name, times=2, interval=0.1)  # 2 parpadeos rápidos
    except Exception as e:
        print(f"💥 Error enviando tecla: {e}")


def setup_actions():
    assignments = get_all_assignments()

    for control_id, action_name, params in assignments:
        if control_id.endswith("_fader") or control_id.endswith("_knob"):
            # CC (Continuous Control)
            register_cc_action(
                control_id,
                lambda value, a=action_name, p=params, c=control_id: execute_action(
                    a, p, value=value, control_id=c
                ),
            )
        else:
            # NOTE (Botón)
            register_action(
                control_id,
                lambda a=action_name, p=params, c=control_id: execute_action(
                    a, p, control_id=c
                ),
            )


def main():
    init_db()
    midi_in = rtmidi.MidiIn()
    available_ports = midi_in.get_ports()

    if not available_ports:
        logging.error("No MIDI device found.")
        return

    for i, name in enumerate(available_ports):
        if "nanoKONTROL2" in name:
            midi_in.open_port(i)
            break
    else:
        logging.fatal("nanoKONTROL2 not found.")
        return

    setup_actions()

    midi_in.set_callback(lambda msg, data=None: handle_midi_event(msg[0]))

    logging.info("MCC Command Deck v2 armado y operativo. Presiona Ctrl+C para salir.")
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        logging.info("Finalizando daemon.")
    finally:
        midi_in.close_port()


if __name__ == "__main__":
    main()
