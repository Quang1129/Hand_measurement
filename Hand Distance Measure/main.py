import numpy as np
import cv2
import cvzone
from cvzone.HandTrackingModule import HandDetector
import math
import random
import time

# Open webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)   # width and  1260 pixel
cap.set(4, 720)  # height and 720 pixel

# Hand Detection
detect = HandDetector(detectionCon=0.8, maxHands=1)

# Function
# x is the raw distance y is the value in cm
x = [300, 245, 200, 170, 145, 130, 112, 103, 93, 87, 80, 75, 70, 67, 62, 59, 57]
y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
coff = np.polyfit(x, y, 2) # Quadratic equation

# Game
cx, cy = 250, 250
color = (113,113,113)
counter = 0
point = 0
timeStart = time.time()
totaltime = 20

while True:
    success, img = cap.read()
    img = cv2.flip(img,1)

    if time.time() - timeStart < totaltime:
       hands = detect.findHands(img, draw = False)

       if hands:
        lmList = hands[0]['lmList']
        x, y, w, h = hands[0]['bbox']
        # the distance and coordinates of the 2 locations that I need to calculate
        x1, y1 = lmList[5][0], lmList[5][1]
        x2, y2 = lmList[17][0], lmList[17][1]

        distance = int(math.sqrt((x2-x1)**2+(y2-y1)**2))
        A, B, C = coff
        distance_cm = A*distance**2 + B*distance + C
        # print(distance_cm, distance)
        if distance_cm < 40 :
            if x < cx < x+w and y < cy < y + h:
                counter = 1
        cv2.rectangle(img, (x, y), (x + w, y + h), (215, 255, 255), 2)
        cvzone.putTextRect(img, f'{int(distance_cm)} cm', (x, y))
        if counter:
           counter +=1
           color = (0,255,0)
           if counter == 3 :
              cx = random.randint(150, 1000)
              cy = random.randint(150, 600 )
              color = (113, 113, 113)
              point +=1
              counter = 0



         # Button
        cv2.circle(img, (cx, cy), 40, color, cv2.FILLED )
        cv2.circle(img, (cx, cy), 30, (0,0,0), cv2.FILLED)
        cv2.circle(img, (cx, cy), 30, (255,255,255), 2)

        cvzone.putTextRect(img, f'Time: {int(totaltime-(time.time()-timeStart))}', (900,65), scale = 2)
        cvzone.putTextRect(img, f'Points: {point}', (50, 65), scale= 2)
    else:
        cvzone.putTextRect(img, 'Game Over', (420, 350), scale=4)
        cvzone.putTextRect(img, f'Your Points: {point}', (440, 400), scale= 3)
        cvzone.putTextRect(img, f'Press R to restart', (440, 500), scale=2, offset = 10)



    cv2.imshow("Image", img)
    key = cv2.waitKey(1)

    if key == ord('r'):
        timeStart = time.time()
        point = 0
