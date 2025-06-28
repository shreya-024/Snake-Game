import cvzone
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

class SnakeGameClass:
    def __init__(self, pathSnake, point_s, gameover_s):
        self.points = []#all points of snake
        self.lengths = [] # distance between each point
        self.currentLength = 0 # total length of snake
        self.allowedLength = 50 # total allowed length
        self.previousHead = 0, 0 #previous head point

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
        self.foodPoint = random.randint(200,1000), random.randint(100,500)
        self.currentFoodImg = random.choice(self.foodImgs)  
        self.hfood, self.wfood, _ = self.currentFoodImg.shape

    def update(self, imgMain, currentHead):

        if self.gameOver:
            
            cvzone.putTextRect(imgMain, "Game Over", [320, 200])
            cvzone.putTextRect(imgMain, f"Score: {self.score}", [320, 240])
            self.maxScore = max(self.maxScore,self.score)
            with open("score.txt", "w") as f:
                f.write(str(self.maxScore))
            cvzone.putTextRect(imgMain, "Press Space to Start Again!", [320, 300], scale = 2)
            
        else:
            px, py = self.previousHead
            cx, cy = currentHead

            self.points.append([cx, cy])
            distance = math.hypot(cx-px, cy-py)
            self.lengths.append(distance)
            self.currentLength += distance
            self.previousHead = cx, cy

           # Length Reduction
            if self.currentLength > self.allowedLength:
                for i,length in enumerate(self.lengths):
                    self.currentLength -= length
                    self.lengths.pop(i)
                    self.points.pop(i)
                    if self.currentLength < self.allowedLength:
                        break

            # check if snake ate the food
            rx, ry = self.foodPoint
            if rx < cx < rx +self.wfood and ry < cy < ry + self.hfood:
                self.point_s.play()
                self.randomFoodLocation()
                self.allowedLength += 20
                self.score += 1
                print(self.score)
            cvzone.putTextRect(imgMain, f"Score: {self.score}", [1200, 20], scale = 1, thickness = 2, colorT = (225, 0, 225), colorR = (225, 225, 225))

            #Draw Snake
            if self.points:
                for i,point in enumerate(self.points):
                    if i!=0: 
                        color_intensity = int(255 * (i / len(self.points)))
                        cv2.line(imgMain, self.points[i-1], self.points[i],(0, color_intensity, 0), 20)
                hx, hy = self.points[-1]
                imgMain = cvzone.overlayPNG(imgMain, self.imgSnake, (hx - self.wSnake // 2, hy - self.hSnake // 2))

                        
            #Draw Food
            rx, ry = self.foodPoint
            imgMain = cvzone.overlayPNG(imgMain,self.currentFoodImg, (rx , ry ))

            #check for collision
            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            mindist = cv2.pointPolygonTest(pts, (cx,cy), True)
        
            if -0.25 <= mindist <= 0.25:
                self.gameover_s.play()
                self.gameOver = True
                self.points = []#all points of snake
                self.lengths = [] # distance between each point
                self.currentLength = 0 # total length of snake
                self.allowedLength = 50 # total allowed length
                self.previousHead = 0, 0 #previous head point
                self.randomFoodLocation()  

        cvzone.putTextRect(imgMain, f"Highest Score: {self.maxScore}", [0, 20], scale = 1, thickness = 2, colorT = (225, 0, 225), colorR = (225, 225, 225))

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
    img = cv2.flip(img,1)
    hands, img = detector.findHands(img, flipType=False)
    
    if hands:
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2]
        img = game.update(img, pointIndex)
    cv2.imshow("Image",img)
    key = cv2.waitKey(1)
    if key == ord(' '):
        game.gameOver = False
        game.score = 0
        


