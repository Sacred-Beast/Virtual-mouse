# Virtual-mouse

# Virtual Mouse using Hand Gestures

This project turns your webcam into a virtual mouse controller using hand gestures, powered by OpenCV, MediaPipe, and PyAutoGUI. Move your hand in front of the camera to control the mouse pointer, click, right-click, double-click, and scroll—all without touching your mouse!

## Features

- **Move Mouse:** Make a fist and move your hand to control the mouse pointer.
- **Left Click:** Raise only your index finger.
- **Double Click:** Raise your index and middle fingers.
- **Right Click:** Raise four fingers (all except the thumb).
- **Scroll:** Raise all five fingers and move your hand up or down.



## Requirements

- Python 3.7+
- Webcam

### Python Packages

- `opencv-python`
- `mediapipe`
- `pyautogui`
- `numpy`

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/Sacred-Beast/Virtual_mouse.git
   cd virtual_mouse
   ```

2. **Install dependencies:**
   ```sh
   pip install opencv-python mediapipe pyautogui numpy
   ```

3. **(Optional) For best results, run in a well-lit environment.**

## Usage

Run the script:
```sh
python vir_mouse.py
```

- A window will open showing your webcam feed.
- Use the gestures described above to control your mouse.
- Press `q` to exit.

## How It Works

- Uses **MediaPipe** to detect hand landmarks in real-time.
- Maps the position of your hand to your screen coordinates.
- Recognizes finger patterns to trigger mouse actions using **PyAutoGUI**.

## Troubleshooting

- If the mouse is not moving smoothly, try adjusting the `smoothening` parameter in the script.
- Make sure your webcam is not being used by another application.
- If you get permission errors, try running your terminal as administrator.

## License

This project is open-source and free to use.

---

**Enjoy touchless control of your computer!** 
