from actions.action_map import ACTIONS_MAP
from maps.cc_map import CC_MAP
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - [CONTROLLER] %(message)s")

_actions = {}
_cc_actions = {}

NOTE_TO_NAME = {v: k for k, v in ACTIONS_MAP.items()}


def register_action(name: str, callback):
    _actions[name] = callback
    logging.info(f"🎯 Acción registrada: {name}")


def register_cc_action(name: str, callback):
    _cc_actions[name] = callback
    logging.info(f"🎚 Acción CC registrada: {name}")


def handle_midi_event(message):
    status, control, value = message
    message_type = status & 0xF0
    channel = status & 0x0F

    if message_type == 0xB0:  # Control Change
        name = CC_MAP.get((channel, control))
        if name and name in _cc_actions:
            logging.info(f"📡 Ejecutando CC: {name} ({value})")
            _cc_actions[name](value)
        else:
            logging.info(f"📡 CC sin acción: {control} (Canal {channel})")
        return

    if message_type == 0x90 and value == 127:  # Note ON
        name = ACTIONS_MAP.get((channel, control))
        if name and name in _actions:
            logging.info(f"🟢 Ejecutando acción: {name}")
            _actions[name]()
        else:
            logging.warning(
                f"🟢 Botón presionado sin acción asignada: note {control} canal {channel}"
            )
        return
