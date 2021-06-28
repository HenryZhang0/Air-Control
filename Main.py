import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import math as m
import pyautogui
import mouse
import numpy as np


# Setting Variables
showFps = True
hand = [None, None, None, None, None, None]


class Main(object):
    def run(self):
        # CV variables
        ##########################
        wCam, hCam = 1280, 720
        frameR = 100  # Frame Reduction
        smoothening = 4
        pTime = 0
        cTime = 0
        cap = cv2.VideoCapture(1)
        cap.set(3, wCam)
        cap.set(4, hCam)
        detector = htm.handDetector()
        wScr, hScr = pyautogui.size()
        plocX, plocY = 0, 0
        clocX, clocY = 0, 0
        #########################

        while True: #main loop

            s, img = cap.read()
            img = detector.findHands(img, draw=True)
            lmList, bbox = detector.findPosition(img, draw=False)
            
            
            if len(lmList) != 0:
                hand[0] = lmList[0][1:]
                hand[1] = lmList[4][1:]
                hand[2] = lmList[8][1:]
                hand[3] = lmList[12][1:]
                hand[4] = lmList[16][1:]
                hand[5] = lmList[20][1:]

                #mouse stuff        
                x1, y1 = lmList[8][1:]
                x2, y2 = lmList[12][1:]
                #

                cv2.putText(img, str(int(distance(hand[0], hand[2]))), average(hand[0], hand[2], round=True), cv2.FONT_HERSHEY_PLAIN, 2,
                            (255, 0, 0), 2)
            
            fingersUp = detector.fingersUp()
            cv2.rectangle(img, (frameR, frameR), (wCam - frameR, hCam - frameR),
                  (255, 255, 255), 2)

            if fingersUp == [0,1,0,0,0]:
                # 5. Convert Coordinates
                x3 = np.interp(x1, (frameR, wCam - frameR), (0, wScr))
                y3 = np.interp(y1, (frameR, hCam - frameR), (0, hScr))
                # 6. Smoothen Values
                clocX = plocX + (x3 - plocX) / smoothening
                clocY = plocY + (y3 - plocY) / smoothening

                mouse.move(wScr - clocX, clocY, absolute=True)
                cv2.circle(img, (x1, y1), 6, (255, 0, 255), cv2.FILLED)

                plocX, plocY = clocX, clocY  # smoothening vars

        # left  click
            if fingersUp[1] == 1:
                # 9. Find distance between fingers
                length = distance(hand[0],hand[2])
                print(length)
                # 10. Click mouse if distance short
                if length < 200:
                    cv2.circle(img, hand[2],
                            10, (0, 255, 0), cv2.FILLED)
                    mouse.press('left')
                else:
                    mouse.release('left')



            # displaying fps count
            if showFps:
                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime
                cv2.putText(img, str(int(fps)), (10, 70), cv2.FONT_HERSHEY_PLAIN, 3,
                            (255, 0, 255), 3)

        # viewing window
            cv2.imshow("Image", img)
            cv2.waitKey(1)

# end of main

# calculations


def average(*points, round=False):
    totalx = 0
    totaly = 0

    for p in points:
        totalx += p[0]
        totaly += p[1]

    return (int(totalx/len(points)), int(totaly/len(points))) if round else (totalx/len(points), totaly/len(points))


def distance(a, b):
    return (abs(a[0]-b[0])**2+abs(a[1]-b[1])**2)**0.5


def angle(a, b):
    return m.degrees(m.atan2(b[1]-a[1], b[0]-a[0]))


if __name__ == "__main__":
    Main().run()
