# archivo deprecado
# no se usa en la version 3


from pathlib import Path
import json

# Estructura ASSIGNMENTS generada a partir del listado recibido
assignments = {}

dispositivos = [
    (0, "Asignador de sonido Microsoft - Input", "input"),
    (1, "Microphone (Microsoft LifeCam V", "input"),
    (2, "Micrófono (e2eSoft iVCam)", "input"),
    (3, "Micrófono (Realtek(R) Audio)", "input"),
    (4, "Micrófono (Iriun Webcam)", "input"),
    (5, "Auriculares con micrófono (Zone", "input"),
    (6, "Micrófono (Iriun Webcam #2)", "input"),
    (7, "Micrófono (Iriun Webcam #3)", "input"),
    (8, "Asignador de sonido Microsoft - Output", "output"),
    (9, "Altavoces (Realtek(R) Audio)", "output"),
    (10, "Auriculares (Zone 300)", "output"),
    (11, "Controlador primario de captura de sonido", "input"),
    (12, "Microphone (Microsoft LifeCam VX-800)", "input"),
    (13, "Micrófono (e2eSoft iVCam)", "input"),
    (14, "Micrófono (Realtek(R) Audio)", "input"),
    (15, "Micrófono (Iriun Webcam)", "input"),
    (16, "Auriculares con micrófono (Zone 300)", "input"),
    (17, "Micrófono (Iriun Webcam #2)", "input"),
    (18, "Micrófono (Iriun Webcam #3)", "input"),
    (19, "Controlador primario de sonido", "output"),
    (20, "Altavoces (Realtek(R) Audio)", "output"),
    (21, "Auriculares (Zone 300)", "output"),
    (22, "Altavoces (Realtek(R) Audio)", "output"),
    (23, "Auriculares (Zone 300)", "output"),
    (24, "Micrófono (e2eSoft iVCam)", "input"),
    (25, "Micrófono (Realtek(R) Audio)", "input"),
    (26, "Micrófono (Iriun Webcam)", "input"),
    (27, "Auriculares con micrófono (Zone 300)", "input"),
    (28, "Micrófono (Iriun Webcam #2)", "input"),
    (29, "Micrófono (Iriun Webcam #3)", "input"),
    (30, "Microphone (Microsoft LifeCam VX-800)", "input"),
    (31, "Auriculares con micrófono (@System32\\drivers\\bthhfenum.sys,#2;%1 Hands-Free%0;(Zone 300))", "output"),
    (32, "Auriculares con micrófono (@System32\\drivers\\bthhfenum.sys,#2;%1 Hands-Free%0;(Zone 300))", "input"),
    (33, "MIDI (Iriun Webcam Audio #2)", "input"),
    (34, "Varios micrófonos (Realtek HD Audio Mic input)", "input"),
    (35, "Headphones 1 (Realtek HD Audio 2nd output with SST)", "output"),
    (36, "Headphones 2 (Realtek HD Audio 2nd output with SST)", "output"),
    (37, "Altavoz de PC (Realtek HD Audio 2nd output with SST)", "input"),
    (38, "Mezcla estéreo (Realtek HD Audio Stereo input)", "input"),
    (39, "Mic in at front panel (black) (Mic in at front panel (black))", "input"),
    (40, "Speakers 1 (Realtek HD Audio output with SST)", "output"),
    (41, "Speakers 2 (Realtek HD Audio output with SST)", "output"),
    (42, "Altavoz de PC (Realtek HD Audio output with SST)", "input"),
    (43, "MIDI (Iriun Webcam Audio #3)", "input"),
    (44, "Input ()", "input"),
    (45, "Output (@System32\\drivers\\bthhfenum.sys,#4;%1 Hands-Free HF Audio%0;(S22 de Rodrigo))", "output"),
    (46, "Input (@System32\\drivers\\bthhfenum.sys,#4;%1 Hands-Free HF Audio%0;(S22 de Rodrigo))", "input"),
    (47, "Auriculares ()", "output"),
    (48, "Micrófono (Microsoft LifeCam VX-800)", "input"),
    (49, "MIDI (Iriun Webcam Audio)", "input"),
    (50, "Micrófono ()", "input")
]

# Generar el diccionario de asignaciones
for index, name, type_ in dispositivos:
    key = f"device_{index:02d}"
    assignments[key] = {
        "index": index,
        "device_name": name,
        "type": type_
    }

# Guardar en assignments.py como un diccionario Python válido
assignments_file = Path("config/assignments.py")
assignments_file.write_text(f"ASSIGNMENTS = {json.dumps(assignments, indent=4, ensure_ascii=False)}\n")

assignments_file.resolve()
