LED_MAP = {}

# Cada track (1 a 8) usa su propio canal MIDI (0 a 7)
for i in range(8):
    channel = i + 1  # canal MIDI real (0-indexed)
    LED_MAP[f"track{i+1}_rec"] = {"note": 64 + i, "channel": channel}
    LED_MAP[f"track{i+1}_mute"] = {"note": 48 + i, "channel": channel}
    LED_MAP[f"track{i+1}_solo"] = {"note": 32 + i, "channel": channel}

# Bloque de transporte (en canal 0 = MIDI Channel 1)
LED_MAP.update(
    {
        "rewind": {"note": 43, "channel": 0},
        "forward": {"note": 44, "channel": 0},
        "stop": {"note": 42, "channel": 0},
        "play": {"note": 41, "channel": 0},
        "record": {"note": 45, "channel": 0},
        "track forward": {"note": 2, "channel": 0},
        "track backward": {"note": 1, "channel": 0},
    }
)
