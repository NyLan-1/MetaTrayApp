# MetaTrayApp

MetaTrayApp is a small Windows utility that automatically sends the Meta Horizon Link window to the system tray after sign-in.

## Why this exists

Meta Horizon Link may open visibly in the middle of the screen when Windows starts.  
This utility watches for that window and closes it the same way as clicking the X button, so the app goes to the system tray instead of staying open on screen.

## What it does

- starts silently
- watches for the Meta Horizon Link window
- sends it to the tray when detected

## Installation

There are two ways to install MetaTrayApp.

### Option 1: Use the installer

If you downloaded the installer, run `MetaTrayApp-Setup.exe`.

The installer will:

- install the application in your user profile
- register it to start automatically with Windows
- add an uninstall entry to Windows

After installation, the app will start automatically at your next Windows sign-in and will reduce the Meta Horizon Link window to the system tray.

### Option 2: Manual installation

If you prefer not to use the installer, you can use the compiled executable directly.

#### Typical executable location

If you built the project locally, the executable is usually here:

```text
dist\meta_tray.exe
```

#### Test it first

Before using it at startup:

1. Open Meta Horizon Link
2. Run `dist\meta_tray.exe`
3. Confirm that Meta Horizon Link is sent to the system tray

#### Start automatically with Windows

The easiest manual method is to use the Windows startup folder.

Press `Win + R`, type the following command, then press Enter:

```text
shell:startup
```

Then place one of the following in that folder:

- `meta_tray.exe`
- a shortcut to `meta_tray.exe`

Using a shortcut is recommended.

#### How to create a shortcut

1. Right-click `meta_tray.exe`
2. Click `Create shortcut`
3. Move that shortcut into the folder opened by `shell:startup`

## Build from source

Create and activate a virtual environment:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install PyInstaller:

```powershell
python -m pip install pyinstaller
```

Build the executable:

```powershell
python -m PyInstaller --onefile --noconsole meta_tray.py
```

The executable will be created here:

```text
dist\meta_tray.exe
```

## Files

- `meta_tray.py`: source code
- `README.md`: project instructions

## Notes

- Meta Horizon Link may still remain visible for a few seconds during startup depending on how fast Windows launches startup apps
- this project keeps the repository clean by excluding build files through `.gitignore`
- the recommended way to share the compiled app is through GitHub Releases, not by committing the `.exe` into the repository
