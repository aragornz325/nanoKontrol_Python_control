import rtmidi
import time
import threading
import logging
from led.led_map import LED_MAP

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [LED] %(message)s")

midi_out = rtmidi.MidiOut()
available_ports = midi_out.get_ports()

logging.info("Puertos MIDI disponibles:")
for i, name in enumerate(available_ports):
    logging.info(f"{i}: {name}")

for i, name in enumerate(available_ports):
    if "nanoKONTROL2" in name and "CTRL" in name:
        midi_out.open_port(i)
        logging.info(f"Puerto de salida MIDI para LEDs abierto: {name}")
        break
else:
    logging.warning("No se encontró el puerto de salida LED para nanoKONTROL2.")
    midi_out = None

_led_states = {}

def set_led(name: str, state: bool):
    if not midi_out:
        logging.warning("No MIDI OUT disponible para set_led.")
        return
    if name not in LED_MAP:
        logging.warning(f"LED '{name}' no está definido en el mapa.")
        return

    note_info = LED_MAP[name]
    status = (0x90 if state else 0x80) + note_info["channel"]
    value = 127 if state else 0
    midi_out.send_message([status, note_info["note"], value])
    logging.info(f"LED {name} {'encendido' if state else 'apagado'} (NOTE {note_info['note']}, canal {note_info['channel']})")

def toggle_led(name: str):
    _led_states[name] = not _led_states.get(name, False)
    set_led(name, _led_states[name])

def pulse_led(name: str, times: int = 3, interval: float = 0.1):
    if not midi_out:
        logging.warning("No MIDI OUT disponible para pulse_led.")
        return

    def _pulse():
        for _ in range(times):
            set_led(name, True)
            time.sleep(interval)
            set_led(name, False)
            time.sleep(interval)

    threading.Thread(target=_pulse, daemon=True).start()
