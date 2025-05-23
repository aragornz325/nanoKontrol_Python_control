[Setup]
AppName=pythonKontrol
AppVersion=1.0
DefaultDirName={userappdata}\pythonKontrol
DefaultGroupName=pythonKontrol
OutputDir=dist_installer
OutputBaseFilename=pythonKontrol_installer
Compression=lzma
SolidCompression=yes

[Files]
Source: "dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\pythonKontrol"; Filename: "{app}\main.exe"; WorkingDir: "{app}"
Name: "{userdesktop}\pythonKontrol"; Filename: "{app}\main.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Opciones adicionales:"
Name: "auto_start"; Description: "Ejecutar automáticamente al iniciar Windows"; GroupDescription: "Opciones adicionales:"



[Registry]
Root: HKCU; Subkey: "Software\Microsoft\Windows\CurrentVersion\Run"; ValueType: string; ValueName: "pythonKontrol"; ValueData: """{app}\main.exe"""; Flags: uninsdeletevalue; Tasks: auto_start

[Run]
Filename: "{app}\main.exe"; Description: "Iniciar pythonKontrol"; Flags: nowait postinstall skipifsilent
