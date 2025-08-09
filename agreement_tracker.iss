[Setup]
AppName=Agreement Tracker
AppVersion=1.0
WizardStyle=modern
DefaultDirName={autopf}\Agreement Tracker
DefaultGroupName=Agreement Tracker
UninstallDisplayIcon={app}\agreement_tracker.exe
Compression=lzma2
SolidCompression=yes
OutputDir=output

[Files]
Source="dist\agreement_tracker.exe"; DestDir="{app}"; Flags: ignoreversion

[Icons]
Name="{autoprograms}\Agreement Tracker"; Filename="{app}\agreement_tracker.exe"

[Run]
Filename="{app}\agreement_tracker.exe"; Description="Launch Agreement Tracker"; Flags: nowait postinstall skipifsilent