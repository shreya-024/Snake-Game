import cv2
import numpy as np
import math
import random
from cvzone.HandTrackingModule import HandDetector
import pygame

pygame.init()

cap = cv2.VideoCapture(0)
cap.set(3, 1260)
cap.set(4, 1080)

detector = HandDetector(detectionCon=0.8, maxHands=1)

def putTextWithBackground(img, text, pos, scale=1, thickness=2, colorT=(255,255,255), colorR=(0,0,0)):
    font = cv2.FONT_HERSHEY_SIMPLEX
    text_size, _ = cv2.getTextSize(text, font, scale, thickness)
    text_w, text_h = text_size
    x, y = pos
    cv2.rectangle(img, (x, y - text_h - 10), (x + text_w + 10, y + 10), colorR, -1)
    cv2.putText(img, text, (x + 5, y), font, scale, colorT, thickness, cv2.LINE_AA)

def overlayPNG(background, overlay, pos):
    x, y = pos
    h, w, _ = overlay.shape
    if y + h > background.shape[0] or x + w > background.shape[1]:
        return background
    alpha = overlay[:, :, 3] / 255.0
    for c in range(3):
        background[y:y+h, x:x+w, c] = (1 - alpha) * background[y:y+h, x:x+w, c] + alpha * overlay[:, :, c]
    return background

class SnakeGameClass:
    def __init__(self, pathSnake, point_s, gameover_s):
        self.points = []
        self.lengths = []
        self.currentLength = 0
        self.allowedLength = 50
        self.previousHead = 0, 0

        self.foodImgs = [cv2.resize(cv2.imread(path, cv2.IMREAD_UNCHANGED), (40, 40), interpolation=cv2.INTER_AREA) for path in foodPaths]
        self.currentFoodImg = random.choice(self.foodImgs)
        self.hfood, self.wfood, _ = self.currentFoodImg.shape
        self.foodPoint = 0, 0
        self.randomFoodLocation()

        self.imgSnake = cv2.imread(pathSnake, cv2.IMREAD_UNCHANGED)
        self.imgSnake = cv2.resize(self.imgSnake, (60, 60), interpolation=cv2.INTER_AREA)
        self.hSnake, self.wSnake, _ = self.imgSnake.shape

        self.score = 0
        self.gameOver = False
        with open("score.txt", "r") as f:
            self.maxScore = int(f.read())

        self.point_s = point_s
        self.gameover_s = gameover_s

    def randomFoodLocation(self):
        self.foodPoint = random.randint(200, 1000), random.randint(100, 500)
        self.currentFoodImg = random.choice(self.foodImgs)
        self.hfood, self.wfood, _ = self.currentFoodImg.shape

    def update(self, imgMain, currentHead):
        if self.gameOver:
            putTextWithBackground(imgMain, "Game Over", [580, 200], scale=2, colorT=(255,255,255), colorR=(204,0,0))
            putTextWithBackground(imgMain, f"Score: {self.score}", [600, 240], scale=2, colorT=(255,255,255), colorR=(204,0,0))
            self.maxScore = max(self.maxScore, self.score)
            with open("score.txt", "w") as f:
                f.write(str(self.maxScore))
            putTextWithBackground(imgMain, "Press Space to Start Again!", [450, 300], scale=2, colorT=(0,0,0), colorR=(255,255,255))
        else:
            px, py = self.previousHead
            cx, cy = currentHead

            self.points.append([cx, cy])
            distance = math.hypot(cx - px, cy - py)
            self.lengths.append(distance)
            self.currentLength += distance
            self.previousHead = cx, cy

            if self.currentLength > self.allowedLength:
                for i, length in enumerate(self.lengths):
                    self.currentLength -= length
                    self.lengths.pop(i)
                    self.points.pop(i)
                    if self.currentLength < self.allowedLength:
                        break

            rx, ry = self.foodPoint
            if rx < cx < rx + self.wfood and ry < cy < ry + self.hfood:
                self.point_s.play()
                self.randomFoodLocation()
                self.allowedLength += 20
                self.score += 1
                print(self.score)

            putTextWithBackground(imgMain, f"Score: {self.score}", [1200, 20], scale=1, thickness=2, colorT=(255,255,255), colorR=(0,102,204))

            if self.points:
                for i, point in enumerate(self.points):
                    if i != 0:
                        color_intensity = int(255 * (i / len(self.points)))
                        cv2.line(imgMain, self.points[i - 1], self.points[i], (0, color_intensity, 0), 20)
                hx, hy = self.points[-1]
                imgMain = overlayPNG(imgMain, self.imgSnake, (hx - self.wSnake // 2, hy - self.hSnake // 2))

            rx, ry = self.foodPoint
            imgMain = overlayPNG(imgMain, self.currentFoodImg, (rx, ry))

            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            mindist = cv2.pointPolygonTest(pts, (cx, cy), True)

            if -0.25 <= mindist <= 0.25:
                self.gameover_s.play()
                self.gameOver = True
                self.points = []
                self.lengths = []
                self.currentLength = 0
                self.allowedLength = 50
                self.previousHead = 0, 0
                self.randomFoodLocation()

        putTextWithBackground(imgMain, f"Highest Score: {self.maxScore}", [0, 20], scale=1, thickness=2, colorT=(255,255,255), colorR=(51,153,102))

        return imgMain

foodPaths = ["banana.png", "apple.png", "food.png"]
point_s = pygame.mixer.Sound("point.wav")
gameover_s = pygame.mixer.Sound("gameOver.wav")
game = SnakeGameClass("snake.png", point_s, gameover_s)

while True:
    success, img = cap.read()
    if not success:
        print("Failed to grab frame from camera")
        break
    img = cv2.flip(img, 1)
    putTextWithBackground(img, "Use your INDEX finger to move the Snake", [500, 20], scale=1, thickness=2, colorT=(255,255,255), colorR=(0,0,0))

    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2]
        img = game.update(img, pointIndex)

    cv2.imshow("Image", img)
    key = cv2.waitKey(1)
    if key == ord(' '):
        game.gameOver = False
        game.score = 0
