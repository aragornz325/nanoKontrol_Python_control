# =================== ENUMS ===================

from enum import Enum


class Action(Enum):
    NONE = ""
    LAUNCH_APP = "launch_app"
    YOUTUBE = "youtube"
    SET_VOLUME = "set_volume"
    YOUTUBE_VOLUME = "youtube_volume"
    OPEN_BROWSER = "open_browser"
    APP_VOLUME = "app_volume"
    KNOB_VOLUME = "knob_volume"
    PLAY_PAUSE = "play_pause"
    NEXT_TRACK = "next_track"
    PREV_TRACK = "prev_track"
    STOP = "stop"
    TOGGLE_DEVICE_MUTE = "toggle_device_mute"
    LAUNCH_EMULATOR = "launch_emulator"
    MAQUEE = "marquee"
    DRUM = "drum"


class Fader(Enum):
    TRACK_1 = "track1_fader"
    TRACK_2 = "track2_fader"
    TRACK_3 = "track3_fader"
    TRACK_4 = "track4_fader"
    TRACK_5 = "track5_fader"
    TRACK_6 = "track6_fader"
    TRACK_7 = "track7_fader"
    TRACK_8 = "track8_fader"


class Knob(Enum):
    TRACK_1 = "track1_knob"
    TRACK_2 = "track2_knob"
    TRACK_3 = "track3_knob"
    TRACK_4 = "track4_knob"
    TRACK_5 = "track5_knob"
    TRACK_6 = "track6_knob"
    TRACK_7 = "track7_knob"
    TRACK_8 = "track8_knob"


class Button(Enum):
    TRACK_1_REC = "track1_rec"
    TRACK_1_SOLO = "track1_solo"
    TRACK_1_MUTE = "track1_mute"
    TRACK_2_REC = "track2_rec"
    TRACK_2_SOLO = "track2_solo"
    TRACK_2_MUTE = "track2_mute"
    TRACK_3_REC = "track3_rec"
    TRACK_3_SOLO = "track3_solo"
    TRACK_3_MUTE = "track3_mute"
    TRACK_4_REC = "track4_rec"
    TRACK_4_SOLO = "track4_solo"
    TRACK_4_MUTE = "track4_mute"
    TRACK_5_REC = "track5_rec"
    TRACK_5_SOLO = "track5_solo"
    TRACK_5_MUTE = "track5_mute"
    TRACK_6_REC = "track6_rec"
    TRACK_6_SOLO = "track6_solo"
    TRACK_6_MUTE = "track6_mute"
    TRACK_7_REC = "track7_rec"
    TRACK_7_SOLO = "track7_solo"
    TRACK_7_MUTE = "track7_mute"
    TRACK_8_REC = "track8_rec"
    TRACK_8_SOLO = "track8_solo"
    TRACK_8_MUTE = "track8_mute"


class Transport(Enum):
    REWIND = "rewind"
    PLAY = "play"
    FORWARD = "forward"
    STOP = "stop"
    RECORD = "record"
    CYCLE = "cycle"


class MultimediaActions(Enum):
    PLAY_PAUSE = "play/pause media"
    NEXT_TRACK = "next track"
    PREV_TRACK = "previous track"
    STOP = "stop media"


class Label(Enum):
    FADERS = "Faders"
    KNOBS = "Knobs"
    BOTONES = "Botones"
