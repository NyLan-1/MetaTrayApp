# MetaTrayApp

Small utility that detects the Meta Horizon Link window at startup and sends it to the system tray.

## Purpose

Meta Horizon Link may open in the middle of the screen on Windows startup.  
This script waits for the window to appear, then sends a close event so the app minimizes to the tray instead of staying visible.

## Build

```bash
python -m PyInstaller --onefile --noconsole meta_tray.py
