# 🐍 Hand-Tracked Snake Game

A modern twist on the classic Snake game — play using just your index finger, tracked in real-time via your webcam! Built using Python, OpenCV, pygame, and cvzone.

---

## 🎮 Features

- 🖐️ **Hand Gesture Control**: Move the snake using your index finger — no keyboard needed.
- 🍎 **Multiple Food Types**: Randomly spawning banana, apple, and donut images.
- 🐍 **Snake Growth Mechanism**: Each food increases your snake’s length.
- 💥 **Game Over Logic**: Collision with the snake’s own body ends the game.
- 🔊 **Sound Effects**: Fun sounds play when you eat or collide.
- 🧠 **High Score Memory**: Highest score persists across sessions (stored in `score.txt`).
- 📸 **Live Webcam Feed**: Integrated directly into gameplay using OpenCV.

---

## 🧰 Tech Stack

- **Python 3.11 (MediaPipe supported versions: Python 3.9, 3.10, 3.11, 3.12)**
- **OpenCV** – for webcam access, frame processing, and drawing.
- **cvzone** – for easy hand tracking and image overlays.
- **pygame** – for handling sound effects.
- **MediaPipe** (via cvzone) – for detecting and tracking the index finger.

---

## 🚀 Getting Started

### ✅ Prerequisites

Install dependencies:

```bash
pip install opencv-python cvzone pygame numpy
pip install mediapipe==0.10.9
```
Make sure the following files are in your working directory:

```
main.py
snake.png
banana.png
apple.png
food.png
point.wav
gameOver.wav
score.txt   # Create with a starting value of 0
```
▶️ How to Play

Run the game:

```bash
python main.py
```
Use your index finger to move the snake.

Eat food to grow and increase your score.

Avoid hitting your own body.

Press Space to restart after Game Over.

💡 Highlights

Uses OpenCV to process real-time video from your webcam.

Snake and food are overlaid as PNG images for a rich game feel.

Dynamic color snake trail based on length and movement.

High score is saved between runs using a simple text file.

Clean and minimal interface with helpful instructions on-screen.
