import rtmidi
import subprocess
import logging
import time
from actions.volumen_device_control import set_device_volume_scaled
from audio.fader_assignments import FADER_ASSIGNMENTS
from audio.volumen_control import set_volume_for_app
from audio.youtube_control_audio import set_volume_for_youtube_window
from config.assignments import KNOB_DEVICE_ASSIGNMENTS
from controller_registry import register_action, register_cc_action, handle_midi_event
from core.utils.app_control import toggle_app_and_led
from core.utils.youtube_control import toggle_youtube_window_and_led
from led.led_control import pulse_led


logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")


def set_volume_scaled(app, raw):
    try:
        value = float(raw) / 127.0
        logging.info(f"📏 Valor normalizado para {app}: {value:.2f}")
        set_volume_for_app(app, max(0.0, min(value, 1.0)))
    except Exception as e:
        logging.error(f"💥 Error en conversión de volumen: {e}")


def setup_actions():
    # Botones (NOTE)
    # register_action(
    #     "track1_rec", lambda: (subprocess.Popen("wt.exe"), pulse_led("track1_rec"))
    # )
    register_action(
        "track1_rec",
        lambda: toggle_app_and_led(
            process_name="Spotify.exe",
            led_name="track1_rec",
            launch_command=r"C:\Users\rodri\AppData\Roaming\Spotify\Spotify.exe",
        ),
    )

    register_action("track4_rec", lambda: toggle_youtube_window_and_led("track4_rec"))

    register_action(
        "track2_rec",
        lambda: (subprocess.Popen(["notepad.exe"]), pulse_led("track2_rec")),
    )
    register_action(
        "track3_rec",
        lambda: toggle_app_and_led(
            process_name="Discord.exe",
            led_name="track3_rec",
            launch_command="start Discord.exe",
        ),
    )

    # Transporte
    register_action("stop", lambda: pulse_led("stop"))
    register_action("play", lambda: pulse_led("play"))

    # Faders (CC)
    register_cc_action("track4_fader", lambda v: set_volume_for_youtube_window(v / 127.0))
    for control, app in FADER_ASSIGNMENTS.items():
        register_cc_action(control, lambda v, app=app: set_volume_scaled(app, v))

    # Knobs (CC)
    for control, assignment in KNOB_DEVICE_ASSIGNMENTS.items():
        logging.info(f"🔧 Registrando control: {control}")
        register_cc_action(
            control,
            lambda v, control=control, a=assignment: set_device_volume_scaled(
                control, v, a
            ),
        )


def main():
    midi_in = rtmidi.MidiIn()
    available_ports = midi_in.get_ports()

    if not available_ports:
        print("No MIDI device found.")
        return

    for i, name in enumerate(available_ports):
        if "nanoKONTROL2" in name:
            midi_in.open_port(i)
            break
    else:
        print("nanoKONTROL2 not found.")
        return

    setup_actions()

    midi_in.set_callback(lambda msg, data=None: handle_midi_event(msg[0]))

    print("MCC Command Deck v2 armado y operativo. Presiona Ctrl+C para salir.")
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Finalizando daemon.")
    finally:
        midi_in.close_port()


if __name__ == "__main__":
    main()
