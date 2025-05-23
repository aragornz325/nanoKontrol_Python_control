import time
import threading
import random
import os
import platform
import subprocess
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import simpleaudio as sa

from core.utils.font_3x5_map import FONT_3x5
from core.utils.path import get_soundEqualizer_path

LED_LAYOUT = [
    ["track1_solo", "track1_mute", "track1_rec"],
    ["track2_solo", "track2_mute", "track2_rec"],
    ["track3_solo", "track3_mute", "track3_rec"],
    ["track4_solo", "track4_mute", "track4_rec"],
    ["track5_solo", "track5_mute", "track5_rec"],
    ["track6_solo", "track6_mute", "track6_rec"],
    ["track7_solo", "track7_mute", "track7_rec"],
    ["track8_solo", "track8_mute", "track8_rec"],
]


def scroll_marquee(text: str, delay: float = 0.1, set_led_fn=None):
    """
    Desplaza un texto en un LED de matriz de 8x3.
    El texto se desplaza de derecha a izquierda, y cada letra se muestra
    durante un tiempo determinado por el parámetro delay.

    Args:
        text (str): El texto a desplazar.
        delay (float): Tiempo de espera entre cada desplazamiento (en segundos).
        set_led_fn (function): Función para controlar los LEDs. Debe aceptar dos argumentos:
            - led_name: Nombre del LED a encender/apagar.
            - state: Estado del LED (True para encender, False para apagar).

    Returns:
        naranpol

    """
    if set_led_fn is None:
        raise ValueError("Debes pasar una función set_led_fn para controlar los LEDs.")

    buffer = []
    for char in text.upper():
        cols = FONT_3x5.get(char, FONT_3x5[" "])
        buffer.extend(cols)
        buffer.append([0, 0, 0])

    buffer = [[0, 0, 0]] * 8 + buffer + [[0, 0, 0]] * 8

    for i in range(len(buffer) - 7):
        window = buffer[i : i + 8]
        for x, col in enumerate(window):
            for y, val in enumerate(col):
                set_led_fn(LED_LAYOUT[x][y], bool(val))
        time.sleep(delay)

    for channel in LED_LAYOUT:
        for led in channel:
            set_led_fn(led, False)


def launch_marquee_thread(text: str, delay: float = 0.25, set_led_fn=None):
    """
    lanza el thread de la marquecina

    Args:
        text (str): El texto a desplazar.
        delay (float): Tiempo de espera entre cada desplazamiento (en segundos).
        set_led_fn (function): Función para controlar los LEDs. Debe aceptar dos argumentos:
            - led_name: Nombre del LED a encender/apagar.
            - state: Estado del LED (True para encender, False para apagar).

    Returns:
        naranpol

    """

    threading.Thread(
        target=scroll_marquee, args=(text, delay, set_led_fn), daemon=True
    ).start()


def preview_letter(char: str):
    """
    genera una coso pa ver como queda la letra

    Args:
        char (str): la letra para previzualizar

    Returns:
        str: un string con tres filas
    """
    rows = ["" for _ in range(3)]
    for col in FONT_3x5.get(char.upper(), [[0, 0, 0]]):
        for i in range(3):
            rows[i] += "#" if col[i] else " "
    return "\n".join(rows)


def play_audio_equalizer(wav_filename: str, set_led_fn=None, interval: float = 0.1):
    """
    Reproduce un archivo de audio WAV y visualiza su espectro de frecuencias en tiempo real usando
    los LED S,M,R de cada canal
    Esta función analiza el archivo de audio en ventanas solapadas, calcula el espectro de frecuencias,
    lo divide en bandas espaciadas logarítmicamente y asigna la energía de cada banda a los niveles de los LEDs.
    La función `set_led_fn` proporcionada se utiliza para actualizar el estado de los LEDs.
    Args:
        wav_filename (str): Nombre del archivo de audio WAV a reproducir (relativo a este archivo).
                            debe estar en la carpeta /core/utils
        set_led_fn (callable): Función para controlar los LEDs. Debe aceptar dos argumentos:
            - led: El identificador del LED (de LED_LAYOUT).
            - state: Booleano que indica si el LED debe estar encendido (True) o apagado (False).
        interval (float, opcional): Intervalo de tiempo (en segundos) entre cada actualización del ecualizador. Por defecto es 0.1.
    Raises:
        ValueError: Si no se proporciona `set_led_fn`.
    Notas:
        - La función inicia dos hilos en segundo plano: uno para la reproducción de audio y otro para la visualización del ecualizador.
        - Las bandas de frecuencia están espaciadas logarítmicamente entre 60 Hz y 1600 Hz.
        - Se asume que el layout y la lógica de mapeo de los LEDs están definidos en otro lugar (por ejemplo, en `LED_LAYOUT`).
    """
    if set_led_fn is None:
        raise ValueError("Debes pasar una función set_led_fn para controlar los LEDs.")

    wav_path = get_soundEqualizer_path()

    def run_equalizer():
        audio = AudioSegment.from_wav(wav_path).set_channels(1)
        samples = np.array(audio.get_array_of_samples())
        frame_rate = audio.frame_rate

        window_size = 4096
        hop = int(frame_rate * interval)
        total = len(samples)

        for start in range(0, total - window_size, hop):
            window = samples[start : start + window_size]
            spectrum = np.abs(np.fft.fft(window))[: window_size // 2]
            freqs = np.fft.fftfreq(window_size, d=1 / frame_rate)[: window_size // 2]

            # Nuevo rango más intermedio: 60Hz a 1600Hz
            bands = np.logspace(np.log10(60), np.log10(1600), num=9).astype(int)
            max_spectrum = np.max(spectrum)
            levels = []
            for i in range(8):
                low, high = bands[i], bands[i + 1]
                mask = (freqs >= low) & (freqs < high)
                energy = np.mean(spectrum[mask]) if np.any(mask) else 0
                amplified = energy * 4.2
                level = int(np.clip(amplified / max_spectrum * 3, 0, 3))
                levels.append(level)

            for x, lvl in enumerate(levels):
                for y in range(3):
                    set_led_fn(LED_LAYOUT[x][y], y >= (3 - lvl))
            time.sleep(interval)

        for channel in LED_LAYOUT:
            for led in channel:
                set_led_fn(led, False)

    def play_wav():
        wave_obj = sa.WaveObject.from_wave_file(str(wav_path))
        wave_obj.play()

    threading.Thread(target=run_equalizer, daemon=True).start()
    threading.Thread(target=play_wav, daemon=True).start()
