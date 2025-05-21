# actions/audio/volumen_control.py

from config.assignments import KNOB_DEVICE_ASSIGNMENTS
from audio.device_control_nircmd import set_input_volume, set_output_volume

def set_volume_by_assignment(control_id: str, value: float):
    """
    Ajusta el volumen de un control específico basado en las asignaciones.
    """
    assignment = KNOB_DEVICE_ASSIGNMENTS.get(control_id)
    if not assignment:
        print(f"⚠️ No se encontró asignación para {control_id}")
        return

    percent = int(value * 100)

    if assignment["type"] == "device":
        if assignment["direction"] == "input":
            set_input_volume(assignment["target"], percent)
        elif assignment["direction"] == "output":
            set_output_volume(assignment["target"], percent)
    else:
        print(f"⚠️ Tipo de asignación no soportado aún: {assignment['type']}")

# actions/audio/volumen_control.py


def set_device_volume_scaled(control_id: str, raw: int, assignment):
    print(f"🎚️ {control_id}: MIDI {raw} → {assignment['target']}")

    if assignment["direction"] == "input":
        set_input_volume(assignment["target"], raw)
    elif assignment["direction"] == "output":
        set_output_volume(assignment["target"], raw)
