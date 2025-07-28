import cv2
import time
import math
import numpy as np
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from HandTrackingModule import HandDetector

wCam, hCam = 640, 480
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)

detector = HandDetector(maxHands=1, detectionCon=0.85, trackCon=0.8)

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol, maxVol = volRange[0], volRange[1]
hmin, hmax = 50, 200
volBar, volPer, vol = 400, 0, 0
color = (0, 215, 255)

tipIds = [4, 8, 12, 16, 20]
mode = ''
active = 0

pyautogui.FAILSAFE = False

SMOOTHING_FACTOR = 0.5
prev_cursor_x, prev_cursor_y = 0, 0

def putText(mode, loc=(250, 450), color=(0, 255, 255)):
    cv2.putText(img, str(mode), loc, cv2.FONT_HERSHEY_COMPLEX_SMALL, 3, color, 3)

pTime = 0
while True:
    success, img = cap.read()
    if not success:
        print("Failed to capture frame from camera.")
        break

    img = detector.find_hands(img)
    lmList = detector.find_position(img, draw=False)

    fingers = []
    if len(lmList) != 0:
        thumbOpen = lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]
        if thumbOpen:
            fingers.append(1 if lmList[tipIds[0]][1] >= lmList[tipIds[0] - 1][1] else 0)
        else:
            fingers.append(1 if lmList[tipIds[0]][1] <= lmList[tipIds[0] - 1][1] else 0)

        for id in range(1, 5):
            fingers.append(1 if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2] else 0)

        if fingers == [0, 0, 0, 0, 0] and active == 0:
            mode = 'N'
        elif (fingers == [0, 1, 0, 0, 0] or fingers == [0, 1, 1, 0, 0]) and active == 0:
            mode = 'Scroll'
            active = 1
        elif fingers == [1, 1, 0, 0, 0] and active == 0:
            mode = 'Volume'
            active = 1
        elif fingers == [1, 1, 1, 1, 1] and active == 0:
            mode = 'Cursor'
            active = 1

    if mode == 'Scroll':
        putText('Scroll', loc=(250, 450), color=(0, 255, 255))

        if fingers == [0, 1, 1, 0, 0]:
            x1, y1 = lmList[8][1], lmList[8][2]
            x2, y2 = lmList[12][1], lmList[12][2]

            cv2.circle(img, (x1, y1), 10, (0, 255, 0), cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, (0, 255, 0), cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 3)

            length = math.hypot(x2 - x1, y2 - y1)
            midpoint_x, midpoint_y = (x1 + x2) // 2, (y1 + y2) // 2

            if abs(y2 - y1) > 50:
                if y2 > y1:
                    putText('Scroll Up', loc=(250, 450), color=(0, 255, 0))
                    pyautogui.scroll(300)
                else:
                    putText('Scroll Down', loc=(250, 450), color=(0, 0, 255))
                    pyautogui.scroll(-300)
            else:
                putText('Scroll Ready', loc=(250, 450), color=(255, 255, 0))

        elif fingers == [0, 0, 0, 0, 0]:
            active = 0
            mode = 'N'

    if mode == 'Volume':
        putText('Volume')
        if fingers[-1] == 1:
            active = 0
            mode = 'N'
        else:
            x1, y1 = lmList[4][1], lmList[4][2]
            x2, y2 = lmList[8][1], lmList[8][2]
            cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

            cv2.circle(img, (x1, y1), 10, color, cv2.FILLED)
            cv2.circle(img, (x2, y2), 10, color, cv2.FILLED)
            cv2.line(img, (x1, y1), (x2, y2), color, 3)
            cv2.circle(img, (cx, cy), 8, color, cv2.FILLED)

            length = math.hypot(x2 - x1, y2 - y1)
            vol = np.interp(length, [hmin, hmax], [minVol, maxVol])
            volBar = np.interp(vol, [minVol, maxVol], [400, 150])
            volPer = np.interp(vol, [minVol, maxVol], [0, 100])

            volN = int(vol)
            if volN % 4 != 0:
                volN -= volN % 4
                volN = max(min(volN, 0), -64)

            volume.SetMasterVolumeLevel(vol, None)
            if length < 50:
                cv2.circle(img, (cx, cy), 11, (0, 0, 255), cv2.FILLED)

            cv2.rectangle(img, (30, 150), (55, 400), (209, 206, 0), 3)
            cv2.rectangle(img, (30, int(volBar)), (55, 400), (215, 255, 127), cv2.FILLED)
            cv2.putText(img, f'{int(volPer)}%', (25, 430), cv2.FONT_HERSHEY_COMPLEX, 0.9, (209, 206, 0), 3)

    if mode == 'Cursor':
        putText('Cursor')
        cv2.rectangle(img, (110, 20), (620, 350), (255, 255, 255), 3)

        if fingers[1:] == [0, 0, 0, 0]:
            active = 0
            mode = 'N'
        else:
            x1, y1 = lmList[8][1], lmList[8][2]
            screenWidth, screenHeight = pyautogui.size()

            X = int(np.interp(x1, [110, 620], [0, screenWidth - 1]))
            Y = int(np.interp(y1, [20, 350], [0, screenHeight - 1]))

            X = int(SMOOTHING_FACTOR * X + (1 - SMOOTHING_FACTOR) * prev_cursor_x)
            Y = int(SMOOTHING_FACTOR * Y + (1 - SMOOTHING_FACTOR) * prev_cursor_y)

            prev_cursor_x, prev_cursor_y = X, Y

            pyautogui.moveTo(X, Y)

            thumb_x, thumb_y = lmList[4][1], lmList[4][2]
            palm_x, palm_y = lmList[9][1], lmList[9][2]
            thumb_palm_distance = math.hypot(thumb_x - palm_x, thumb_y - palm_y)

            CLICK_THRESHOLD = 40
            if thumb_palm_distance < CLICK_THRESHOLD:
                cv2.circle(img, (lmList[4][1], lmList[4][2]), 10, (0, 0, 255), cv2.FILLED)
                pyautogui.click()

            pinky_x, pinky_y = lmList[20][1], lmList[20][2]
            pinky_palm_distance = math.hypot(pinky_x - palm_x, pinky_y - palm_y)

            RIGHT_CLICK_THRESHOLD = 50
            if pinky_palm_distance < RIGHT_CLICK_THRESHOLD:
                cv2.circle(img, (lmList[20][1], lmList[20][2]), 10, (255, 0, 0), cv2.FILLED)
                pyautogui.rightClick()

    cTime = time.time()
    fps = 1 / ((cTime + 0.01) - pTime)

    pTime = cTime
    cv2.putText(img, f'FPS:{int(fps)}', (480, 50), cv2.FONT_ITALIC, 1, (255, 0, 0), 2)

    cv2.imshow('Hand LiveFeed', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()