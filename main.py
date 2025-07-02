import cv2
import numpy as np
import math
import random
import pygame
import mediapipe as mp

pygame.init()

# Load sounds
point_s = pygame.mixer.Sound("point.wav")
gameover_s = pygame.mixer.Sound("gameOver.wav")

cap = cv2.VideoCapture(0)
cap.set(3, 1260)
cap.set(4, 1080)

# MediaPipe hands setup
mp_hands = mp.solutions.hands
hands_detector = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.8)
mp_draw = mp.solutions.drawing_utils

class SnakeGameClass:
    def __init__(self, pathSnake, point_s, gameover_s):
        self.points = []
        self.lengths = []
        self.currentLength = 0
        self.allowedLength = 50
        self.previousHead = 0, 0

        self.foodImgs = [cv2.resize(cv2.imread(path, cv2.IMREAD_UNCHANGED), (40, 40)) for path in foodPaths]
        self.currentFoodImg = random.choice(self.foodImgs)
        self.hfood, self.wfood, _ = self.currentFoodImg.shape
        self.foodPoint = 0, 0
        self.randomFoodLocation()

        self.imgSnake = cv2.imread(pathSnake, cv2.IMREAD_UNCHANGED)
        self.imgSnake = cv2.resize(self.imgSnake, (60, 60))
        self.hSnake, self.wSnake, _ = self.imgSnake.shape

        self.score = 0
        self.gameOver = False
        with open("score.txt", "r") as f:
            self.maxScore = int(f.read())

        self.point_s = point_s
        self.gameover_s = gameover_s

    def overlayPNG(self, imgBack, imgFront, pos):
        hf, wf, _ = imgFront.shape
        x, y = pos
        if y + hf > imgBack.shape[0] or x + wf > imgBack.shape[1] or x < 0 or y < 0:
            return imgBack
        alpha = imgFront[:, :, 3] / 255.0
        for c in range(3):
            imgBack[y:y+hf, x:x+wf, c] = imgBack[y:y+hf, x:x+wf, c] * (1 - alpha) + imgFront[:, :, c] * alpha
        return imgBack

    def drawText(self, img, text, pos, scale=1, color=(255,255,255), bgcolor=(0,0,0)):
        font = cv2.FONT_HERSHEY_SIMPLEX
        thickness = 2
        size = cv2.getTextSize(text, font, scale, thickness)[0]
        x, y = pos
        cv2.rectangle(img, (x-10, y - size[1] - 10), (x + size[0] + 10, y + 10), bgcolor, -1)
        cv2.putText(img, text, (x, y), font, scale, color, thickness)

    def randomFoodLocation(self):
        self.foodPoint = random.randint(200, 1000), random.randint(100, 500)
        self.currentFoodImg = random.choice(self.foodImgs)

    def update(self, imgMain, currentHead):
        if self.gameOver:
            self.drawText(imgMain, "Game Over", [580, 200], scale=2, color=(255,255,255), bgcolor=(204,0,0))
            self.drawText(imgMain, f"Score: {self.score}", [600, 240], scale=2, color=(255,255,255), bgcolor=(204,0,0))
            self.maxScore = max(self.maxScore, self.score)
            with open("score.txt", "w") as f:
                f.write(str(self.maxScore))
            self.drawText(imgMain, "Press Space to Start Again!", [450, 300], scale=1.5, color=(0,0,0), bgcolor=(255,255,255))
        else:
            px, py = self.previousHead
            cx, cy = currentHead
            self.points.append([cx, cy])
            distance = math.hypot(cx - px, cy - py)
            self.lengths.append(distance)
            self.currentLength += distance
            self.previousHead = cx, cy

            if self.currentLength > self.allowedLength:
                for i, l in enumerate(self.lengths):
                    self.currentLength -= l
                    self.lengths.pop(i)
                    self.points.pop(i)
                    if self.currentLength < self.allowedLength:
                        break

            # Eat food
            rx, ry = self.foodPoint
            if rx < cx < rx + self.wfood and ry < cy < ry + self.hfood:
                self.point_s.play()
                self.randomFoodLocation()
                self.allowedLength += 20
                self.score += 1

            self.drawText(imgMain, f"Score: {self.score}", [1150, 40], scale=1,
                          color=(255,255,255), bgcolor=(0,102,204))

            for i in range(1, len(self.points)):
                color_intensity = int(255 * (i / len(self.points)))
                cv2.line(imgMain, tuple(self.points[i-1]), tuple(self.points[i]), (0, color_intensity, 0), 20)

            if self.points:
                hx, hy = self.points[-1]
                imgMain = self.overlayPNG(imgMain, self.imgSnake, (hx - self.wSnake//2, hy - self.hSnake//2))

            imgMain = self.overlayPNG(imgMain, self.currentFoodImg, self.foodPoint)

            pts = np.array(self.points[:-2], np.int32).reshape((-1,1,2))
            mindist = cv2.pointPolygonTest(pts, (cx, cy), True)
            if -0.25 <= mindist <= 0.25:
                self.gameover_s.play()
                self.gameOver = True
                self.points, self.lengths = [], []
                self.currentLength = 0
                self.allowedLength = 50
                self.previousHead = 0, 0
                self.randomFoodLocation()

        self.drawText(imgMain, f"Highest Score: {self.maxScore}", [10, 40], scale=1,
                      color=(255,255,255), bgcolor=(51,153,102))
        return imgMain

# Assets
foodPaths = ["banana.png", "apple.png", "food.png"]
game = SnakeGameClass("snake.png", point_s, gameover_s)

while True:
    success, img = cap.read()
    if not success:
        break

    img = cv2.flip(img, 1)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands_detector.process(imgRGB)

    game.drawText(img, "Use your INDEX finger to move the Snake", [450, 20], scale=1,
                  color=(255,255,255), bgcolor=(0,0,0))

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            h, w, _ = img.shape
            cx = int(handLms.landmark[8].x * w)
            cy = int(handLms.landmark[8].y * h)
            pointIndex = (cx, cy)
            img = game.update(img, pointIndex)
            break

    cv2.imshow("Snake Game", img)
    key = cv2.waitKey(1)
    if key == ord(' '):
        game.gameOver = False
        game.score = 0
