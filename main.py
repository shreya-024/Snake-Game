import cvzone
import cv2
import numpy as np
import math
import random
from cvzone.HandTrackingModule import HandDetector

cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

detector = HandDetector(detectionCon=0.8, maxHands=1)

class SnakeGameClass:
    def __init__(self, pathFood):
        self.points = []#all points of snake
        self.lengths = [] # distance between each point
        self.currentLength = 0 # total length of snake
        self.allowedLength = 150 # total allowed length
        self.previousHead = 0, 0 #previous head point

        self.imgFood = cv2.imread(pathFood, cv2.IMREAD_UNCHANGED)
        self.hfood, self.wfood, _ = self.imgFood.shape
        self.foodPoint = 0, 0
        self.randomFoodLocation()

        self.score = 0
        self.gameOver = False
        self.maxScore = 0


    def randomFoodLocation(self):
        self.foodPoint = random.randint(100,1000), random.randint(100,600)

    def update(self, imgMain, currentHead):

        if self.gameOver:
            cvzone.putTextRect(imgMain, "Game Over", [300, 400])
            cvzone.putTextRect(imgMain, f"Score: {self.score}", [300, 550])

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
                self.randomFoodLocation()
                self.allowedLength += 50
                self.score += 1
                print(self.score)

            #Draw Snake
            if self.points:
                for i,point in enumerate(self.points):
                    if i!=0: 
                        cv2.line(imgMain, self.points[i-1], self.points[i],(0,0,255), 20)
                cv2.circle(imgMain, self.points[-1], 20, (200,0,200), cv2.FILLED)
        
            #Draw Food
            rx, ry = self.foodPoint
            imgMain = cvzone.overlayPNG(imgMain,self.imgFood, (rx , ry ))

            #check for collision
            pts = np.array(self.points[:-2], np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(imgMain, [pts], False, (0,200, 0), 3)
            mindist = cv2.pointPolygonTest(pts, (cx,cy), True)
        
            if -1 <= mindist <= 1:
                self.gameOver = True
                self.points = []#all points of snake
                self.lengths = [] # distance between each point
                self.currentLength = 0 # total length of snake
                self.allowedLength = 150 # total allowed length
                self.previousHead = 0, 0 #previous head point
                self.randomFoodLocation()
                self.maxScore = max(0,self.score)

        cvzone.putTextRect(imgMain, f"Highest Score: {self.maxScore}", [20, 20], scale = 1, thickness = 2, colorT = (225, 0, 225), colorR = (225, 225, 225))
        return imgMain

game = SnakeGameClass("Donut.png")


while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    hands, img = detector.findHands(img, flipType=False)

    if hands:
        lmList = hands[0]['lmList']
        pointIndex = lmList[8][0:2]
        img = game.update(img, pointIndex)
    cv2.imshow("Image",img)
    key = cv2.waitKey(5)
    if key == ord('r'):
        game.gameOver = False

