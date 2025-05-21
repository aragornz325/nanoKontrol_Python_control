# cc_map.py

CC_MAP = {}

for track in range(8):
    channel = track  # canal MIDI 0 a 7
    CC_MAP[(channel, 0 + track)] = f"track{track+1}_fader"
    CC_MAP[(channel, 16 + track)] = f"track{track+1}_knob"
