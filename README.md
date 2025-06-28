# 🐍 Hand-Controlled Snake Game 🎮

An interactive Snake Game controlled by your **index finger**, using webcam input! Built with **OpenCV**, **CvZone**, **Pygame**, and **Hand Tracking Module**. Eat the food, grow longer, and avoid crashing into yourself!

---

## ✨ Features

- 🖐️ Control the snake using your **index finger**
- 🍎 Random food items: apple, banana, and donut
- 🔊 Sound effects for eating food and game over
- 🧠 Smart collision detection
- 💾 Persistent **high score** tracking
- 🎨 Smooth UI using `cvzone.putTextRect` and image overlays

---

## 📦 Requirements

Make sure to install the following dependencies:

```bash
pip install opencv-python cvzone pygame numpy
Also, ensure your webcam is working properly.

🚀 How to Run
Clone this repository:

bash
Copy
Edit
git clone https://github.com/your-username/hand-controlled-snake-game.git
cd hand-controlled-snake-game
Add the required files to the project directory:

bash
Copy
Edit
📁 hand-controlled-snake-game/
│
├── main.py
├── score.txt               # Create this file manually and add 0 as initial content
├── snake.png               # Snake head image (PNG)
├── apple.png               # Food image
├── banana.png              # Food image
├── food.png                # Food image
├── point.wav               # Sound effect on eating food
└── gameOver.wav            # Sound effect on game over
Run the game:

bash
Copy
Edit
python main.py
🎮 Controls
Use your index finger to control the snake (tracked using webcam).

Eat food to increase your score and length.

Avoid hitting your own body.

Press the spacebar to restart after Game Over.

🧠 How it Works
Uses cvzone.HandTrackingModule to detect the index finger position in real-time.

Snake follows the finger, growing as it eats food.

Food is randomly selected from 3 options.

Score and highest score are displayed.

Collision with your own body ends the game.

