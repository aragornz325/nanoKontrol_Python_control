@echo off

REM 🧠 Limpieza
rmdir /s /q build
rmdir /s /q dist
del *.spec

REM 🧩 Compilar daemon
pyinstaller ^
  --clean ^
  --noconfirm ^
  --windowed ^
  --onefile ^
  --icon=icon.ico ^
  --add-data="bin/SoundVolumeView.exe;bin" ^
  --add-data="bin/nircmd.exe;bin" ^
  mcc_command_deck_v3.py

REM 🧩 Compilar configurador UI
pyinstaller ^
  --clean ^
  --noconfirm ^
  --windowed ^
  --onefile ^
  --icon=icon.ico ^
  --add-data="bin/SoundVolumeView.exe;bin" ^
  --add-data="bin/nircmd.exe;bin" ^
  ui/configurator.py

REM ⏳ Esperar a que se generen los EXE
:wait1
if exist dist\mcc_command_deck_v3.exe goto wait2
timeout /t 1 > nul
goto wait1

:wait2
if exist dist\configurator.exe goto continue
timeout /t 1 > nul
goto wait2

:continue

REM 🚀 Compilar main con splash
pyinstaller ^
  --clean ^
  --noconfirm ^
  --onefile ^
  --windowed ^
  --icon=icon.ico ^
  --splash=splash.png ^
  --add-data="splash.png;." ^
  --add-data="bin/SoundVolumeView.exe;bin" ^
  --add-data="core/utils/percu.wav;core/utils" ^
  --add-data="bin/nircmd.exe;bin" ^
  --add-data="icon.ico;." ^
  --add-data="dist\\mcc_command_deck_v3.exe;." ^
  --add-data="dist\\configurator.exe;." ^
  main.py
