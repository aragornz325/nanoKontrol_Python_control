CC_MAP = {}

# Cada track (1 a 8) usa su propio canal MIDI (1 a 8)
for i in range(8):
    channel = i + 1  # 1-indexed para coincidir con el setup real del nanoKONTROL2
    CC_MAP[(channel, 0 + i)] = f"track{i+1}_fader"
    CC_MAP[(channel, 16 + i)] = f"track{i+1}_knob"
    CC_MAP[(8, 23)] = "track8_knob"