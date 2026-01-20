[Setup]
AppName=InstaSend
AppVersion=1.0.0
PrivilegesRequired=lowest
DefaultDirName={localappdata}\InstaSend
DefaultGroupName=InstaSend
UninstallDisplayIcon={app}\InstaSend.exe
Compression=lzma2
SolidCompression=yes
OutputDir=.
OutputBaseFilename=InstaSend-Setup
SetupIconFile=assets\icon.ico

[Files]
Source: "dist\InstaSend.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\InstaSend"; Filename: "{app}\InstaSend.exe"
Name: "{userdesktop}\InstaSend"; Filename: "{app}\InstaSend.exe"

[Run]
Filename: "{app}\InstaSend.exe"; Description: "Launch InstaSend"; Flags: postinstall nowait