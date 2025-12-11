# Neon Russian Typing Defender — Mobile Build Guide

This project is a Pygame-based typing defender. You can run it on desktop and package it for Android using Buildozer (python-for-android). iOS requires a Mac and Xcode with python-for-android; see notes below.

## Desktop (Windows)

```powershell
python -m pip install pygame
python main.py
```

## Android (via WSL2 Ubuntu + Buildozer)

Buildozer works on Linux. On Windows, use WSL2 (Ubuntu) and build the APK there.

### 1) Set up WSL2 + Ubuntu
- Enable WSL and install Ubuntu from Microsoft Store.
- Open Ubuntu and update:
```bash
sudo apt update && sudo apt upgrade -y
```

### 2) Install Buildozer and dependencies
```bash
sudo apt install -y python3-pip python3-venv git openjdk-17-jdk unzip libffi-dev libssl-dev
pip3 install --user buildozer
pip3 install --user cython
```

### 3) Bring the project into WSL
In Windows, the repo is at `C:\Users\yahya\spacegame`. In WSL it’s typically accessible under `/mnt/c/Users/yahya/spacegame`.
```bash
cd /mnt/c/Users/yahya/spacegame
python3 -m venv .venv
source .venv/bin/activate
pip install buildozer
```

### 4) Build the APK
```bash
buildozer android debug
```
- First run downloads Android SDK/NDK and recipes; it takes time.
- The output APK will be in `bin/` (e.g., `bin/neonrussian-0.1.0-debug.apk`).
- Copy it to your phone and install (enable unknown sources) or use `adb install`.

### 5) Notes
- Soft keyboard: `main.py` enables text input on Android using `pygame.key.start_text_input()`.
- If fonts for Cyrillic render poorly, package a TTF and load it via `pygame.font.Font('yourfont.ttf', size)` and add it to `source.include_exts`.
- If you see window size issues, consider using device resolution from `pygame.display.get_desktop_sizes()` and pass to `set_mode`.

## iOS (advanced)
- Requires macOS, Xcode, and python-for-android iOS toolchain (experimental). Alternatively, port the game to Kivy and use Xcode via Kivy iOS.

## Alternative: Web App
Since you also have `index.html`/`game.js`, if the game logic exists in JS, wrapping as an Android/iOS app via Capacitor or Cordova is often simpler. If desired, I can set that up.
