import cv2
import mediapipe as mp
import time
import HandTrackingModule as htm
import math as m


# Setting Variables
showFps = False
hand = [None, None, None, None, None, None]


class Main(object):
    def run(self):
        # CV variables
        pTime = 0
        cTime = 0
        cap = cv2.VideoCapture(1)
        detector = htm.handDetector()

        # main loop
        while True:
            s, img = cap.read()
            img = detector.findHands(img, draw=True)
            lmList = detector.findPosition(img, draw=True)
            if len(lmList) != 0:
                hand[0] = lmList[0][1:]
                hand[1] = lmList[4][1:]
                hand[2] = lmList[8][1:]
                hand[3] = lmList[12][1:]
                hand[4] = lmList[16][1:]
                hand[5] = lmList[20][1:]

                #print(distance(hand[1], hand[2]))
                #print(average(hand[1],hand[2],round = True), tuple(hand[1]))
                cv2.putText(img, str(int(distance(hand[1], hand[2]))), average(hand[1], hand[2], round=True), cv2.FONT_HERSHEY_PLAIN, 2,
                            (255, 0, 0), 2)

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
