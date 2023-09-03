from cvzone.HandTrackingModule import HandDetector
from turtle import delay
import random
import cvzone
import time
import cv2
import os


cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)
detector = HandDetector(detectionCon=0.8, maxHands=1)
current_path = os.path.dirname(os.path.realpath(__file__))
timer = 0
stateResult = False
startGame = False
scores = [0, 0]  # [AI, User]

while True:
    imgBG = cv2.imread(os.path.join(current_path,"recources", "bg.jpg"))
    success, frame = cap.read()
    imgScaled = cv2.resize(frame, (0, 0), None, 0.875, 0.875)
    imgScaled = imgScaled[:, 80:480]
    hand, img = detector.findHands(imgScaled)

    cv2.putText(imgBG, str("Me"), (280, 190), cv2.FONT_HERSHEY_TRIPLEX, 1.8, (204, 204, 255), 4)
    cv2.putText(imgBG, str("You"), (940, 50), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (204, 204, 255), 4)
    cv2.putText(imgBG, str("Ai Score: "), (110, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(imgBG, str("Your Score: "), (80, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    cv2.putText(imgBG, str("For Start Game Press 'S'  - For Exit Press 'Q' "), (350, 650), cv2.FONT_HERSHEY_COMPLEX, 0.7, (255, 255, 255), 2)
    imgBG[70:490, 800:1200] = imgScaled

    if startGame:
        if stateResult is False:
            timer = time.time() - initialTime
            cv2.putText(imgBG, str(int(timer)), (605, 435), cv2.FONT_HERSHEY_TRIPLEX, 1.5, (0, 0, 255), 4)
            if timer > 3:
                randomNumber = random.randint(1, 3)
                playerMode = None
                stateResult = True
                timer = 0
                if hand:
                    hand = hand[0]
                    fingers = detector.fingersUp(hand)
                    if fingers == [0, 0, 0, 0, 0]:
                        playerMode = 1
                        imgUser = cv2.imread(os.path.join(current_path, "recources", "1.png"), cv2.IMREAD_UNCHANGED)
                        imgBG = cvzone.overlayPNG(imgBG, imgUser, (950, 500))
                    if fingers == [1, 1, 1, 1, 1]:
                        playerMode = 2
                        imgUser = cv2.imread(os.path.join(current_path, "recources", "2.png"), cv2.IMREAD_UNCHANGED)
                        imgBG = cvzone.overlayPNG(imgBG, imgUser, (950, 500))
                    if fingers == [0, 1, 1, 0, 0]:
                        playerMode = 3
                        imgUser = cv2.imread(os.path.join(current_path, "recources", "3.png"), cv2.IMREAD_UNCHANGED)
                        imgBG = cvzone.overlayPNG(imgBG, imgUser, (950, 500))

                    imgAI = cv2.imread(os.path.join(current_path, "recources", f"{randomNumber}.png"), cv2.IMREAD_UNCHANGED)
                    imgBG = cvzone.overlayPNG(imgBG, imgAI, (250, 500))

                    # Player Wins
                    if (playerMode == 1 and randomNumber == 3) or \
                            (playerMode == 2 and randomNumber == 1) or \
                            (playerMode == 3 and randomNumber == 2):
                        scores[1] += 1
                        
                    # AI Wins
                    if (playerMode == 3 and randomNumber == 1) or \
                            (playerMode == 1 and randomNumber == 2) or \
                            (playerMode == 2 and randomNumber == 3):
                        scores[0] += 1

                    # Equal
                    if (playerMode == 1 and randomNumber == 1) or \
                            (playerMode == 2 and randomNumber == 2) or \
                            (playerMode == 3 and randomNumber == 3):
                        scores[1] += 0     
                        scores[0] += 0    
        
        if stateResult:
            imgBG = cvzone.overlayPNG(imgBG, imgAI, (250, 500))
            if playerMode == 1:
                imgUser = cv2.imread(os.path.join(current_path, "recources", "1.png"), cv2.IMREAD_UNCHANGED)
                imgBG = cvzone.overlayPNG(imgBG, imgUser, (950, 500))
            if playerMode == 2:
                imgUser = cv2.imread(os.path.join(current_path, "recources", "2.png"), cv2.IMREAD_UNCHANGED)
                imgBG = cvzone.overlayPNG(imgBG, imgUser, (950, 500))
            if playerMode == 3:
                imgUser = cv2.imread(os.path.join(current_path, "recources", "3.png"), cv2.IMREAD_UNCHANGED)
                imgBG = cvzone.overlayPNG(imgBG, imgUser, (950, 500))
            
            if (playerMode == 1 and randomNumber == 3) or \
                                (playerMode == 2 and randomNumber == 1) or \
                                (playerMode == 3 and randomNumber == 2):
                cv2.putText(imgBG, "Player Wins", (520, 400), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
            if (playerMode == 3 and randomNumber == 1) or \
                                (playerMode == 1 and randomNumber == 2) or \
                                (playerMode == 2 and randomNumber == 3):
                cv2.putText(imgBG, "AI Wins", (520, 410), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
            if (playerMode == 1 and randomNumber == 1) or \
                                (playerMode == 2 and randomNumber == 2) or \
                                (playerMode == 3 and randomNumber == 3):
                cv2.putText(imgBG, "EQUAL", (520, 420), cv2.FONT_HERSHEY_COMPLEX, 1, (0,255,0), 2)
     
    cv2.putText(imgBG, str(scores[0]), (220, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (204, 255, 204), 2)
    cv2.putText(imgBG, str(scores[1]), (220, 90), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (204, 255, 204), 2)

    cv2.namedWindow("Rock Paper Scissors Game  -  Application Coded by  Nima Zare (@OfficialNimaZare)  -  2023", cv2.WINDOW_GUI_EXPANDED)
    cv2.imshow("Rock Paper Scissors Game  -  Application Coded by  Nima Zare (@OfficialNimaZare)  -  2023", imgBG)

    key = cv2.waitKey(1)

    if key == ord('s'):
        startGame = True
        initialTime = time.time()
        stateResult = False

    if key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

'''
Application Coded By  Nima Zare

Telegram, Instagram :  @OfficialNimaZare

Email :   OfficialNimaZare@gmail.com

All Rights Reserved. 2023.08.30
'''