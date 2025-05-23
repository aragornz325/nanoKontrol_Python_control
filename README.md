# nanoKontrol2 MIDI Companion 🎛️

Controla tu entorno digital con precisión física usando tu Korg nanoKONTROL2.  
Esta app te permite mapear faders, knobs y botones a funciones del sistema operativo, multimedia, apps y más.

## 🚀 ¿Qué hace?

- 🎚 Control de volumen por aplicación (Spotify, navegador, Zoom, etc.)
- ⏯ Controles multimedia (Play/Pause, Next, Stop...)
- 🖥️ Lanzamiento de programas desde botones
- 💡 Feedback visual con LEDs del nanoKONTROL2
- 🔁 Sincronización entre estado físico y sistema operativo

## 🧠 Tecnologías utilizadas

- **Python**
- `rtmidi` para comunicación MIDI
- `dearpygui` para interfaz gráfica
- `pycaw` y `psutil` para manejo de audio y procesos
- `sounddevice` y `pyaudio` para detección avanzada
- Estructura modular para mapeo de acciones

## 📦 Instalación

```bash
git clone git@github.com:aragornz325/nanoKontrol_Python_control.git
cd pythonKontrol
pip install -r requirements.txt
python main.py
```

## 🧩 Mapeo de acciones

Cada botón o deslizador se puede configurar con acciones personalizadas:
- Lanzar apps
- Ajustar volumen
- Enviar comandos multimedia
- Encender/apagar LEDs
- Próximamente: configuración vía YAML

## 📈 Roadmap

- [x] Control por aplicación
- [x] Interfaz visual en tiempo real
- [ ] Soporte multiplataforma (Linux/Win/macOS)
- [ ] Sistema de plugins
- [ ] Perfiles personalizados

## 🤝 Contribuir

¡Toda ayuda es bienvenida! Ideas, testing, mejoras o documentación.
- Hacé un fork
- Creá tu feature branch
- Enviá un pull request

## ⚠️ Disclaimer

Este proyecto está en desarrollo y puede tener errores. No existe otra solución similar open source (al menos en este nivel) — ¡sumate a construirla!

## 📜 Licencia

MIT
