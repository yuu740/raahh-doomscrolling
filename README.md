# 💀 Doomscroll Blocker AI
**Doomscroll Blocker** is a high-impact productivity tool designed to keep you focused. Using computer vision, it monitors your presence. If you look away from your screen or down at your phone for too long, a synchronized "raahh" skeleton alarm hijacks your monitor to "scream" you back into focus.

## ✨ Key Features
- Real-Time Focus Tracking: Uses lightweight Haar Cascade algorithms to detect your face presence without draining system resources.

- Synchronized AV Alarm: Features a perfectly synced video and audio alarm loop using millisecond-precision logic.

- Modal Overlay UI: The alarm video appears as a high-visibility modal overlay directly on your monitoring screen.

- Portable Executable: Packaged into a single .exe file for Windows—no Python installation required for end-users.

## 🛠️ Technical Stack
- Language: Python 3.13

- Computer Vision: OpenCV (cv2)

- Audio Engine: Pygame

- Packaging: PyInstaller

## 🚀 How to Use
### For Users (Windows)
- Go to the Releases section.

- Download the latest `raahh_winver.exe`.

- Run the application and ensure your webcam is enabled.

- If you look away for more than 1.5 seconds, the alarm will trigger!

### For Developers (Source Code)
- Clone this repository.

- Install the required dependencies:

```powershell
pip install opencv-python pygame numpy
```
- Run the script:

```powershell
python app.py
```
## 💬 Feedback & Contributions
Feedback is highly appreciated! As this is the initial release, your input is invaluable in making this tool better.

- Found a bug? Please open an issue.

- Have an idea? I am actively looking for suggestions on performance, UI improvements, or even a future mobile version.

- Want to contribute? Feel free to fork the repo and submit a pull request!

## 📜 License
This project is open-source and available for educational and productivity purposes. Use it to stop scrolling and start doing!
