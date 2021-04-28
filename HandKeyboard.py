import cv2
import HandTrackingModule as htm
import time
import TextRecognition as tr

frames = cv2.VideoCapture('http://192.168.225.55:4747/mjpegfeed?1280x720')
# framesAsus = cv2.VideoCapture('Finger Touching.mp4')
detector = htm.hlmDetector()
texter = tr.text_recog()
pTime = 0
characters = texter.text_char('Keyboard.png')
characters.remove(['V', '820', '500', '880', '570', '0'])
characters.remove(['p', '550', '83', '593', '156', '0'])
characters.remove(['a', '603', '105', '643', '156', '0'])
characters.remove(['c', '656', '105', '691', '156', '0'])
characters.remove(['e', '700', '105', '742', '156', '0'])
tip_ids = [8]

for char in characters:
    char[2] = (int(char[2]) + 70)
    char[4] = (int(char[4]) + 70)
while True:
    ##############For first camera###########
    ret, img = frames.read()
    img = cv2.flip(img, 1)
    h, w, c = img.shape
    img = detector.findHands(img)
    lmList = detector.findHLms(img)
    finger_bools = detector.finOC(lmList)
    # lmList_2 = detector.findHLms(img, 1)
    #########################################

    ###############For second camera#############
    # ret2, imgAsus = framesAsus.read()
    # imgAsus = cv2.resize(imgAsus, (1280, 720))
    # i = 640
    # while i < 720:
    # cv2.line(imgAsus, (0, 680), (1280, 680), (255, 0, 255), 2)
    #     # i = i + 10
    # print(imgAsus.shape)
    # imgAsus = cv2.flip(imgAsus, 0)
    # # imgAsus = detector.findHands(imgAsus)
    # # lmList2 = detector.findHLms(imgAsus)
    # ############################################
    if lmList:
        for ids in tip_ids:
            for char in characters:
                ###########Printing Keyboard########
                cv2.putText(img, char[0], (int(char[1]), h - int(char[2]) + 40), cv2.FONT_HERSHEY_PLAIN,
                            2, (0, 0, 0), 2)
                img = cv2.rectangle(img, (int(char[1]), h - int(char[2])), (int(char[3]), h - int(char[4])),
                                    (0, 255, 0), 2)
                x1, y1 = int(char[1]), h - int(char[2])
                x2, y2 = int(char[3]), h - int(char[4])
                cv2.circle(img, (x1, y1), 5, (255, 0, 255), 2)
                cv2.circle(img, (x2, y2), 5, (255, 0, 255), 2)
                # print(char)
                ####################################
                if lmList[ids][1] > x1 and lmList[ids][1] < x2:
                    if lmList[ids][2] < y1 and lmList[ids][2] > y2:
                        if finger_bools:
                            if finger_bools[0] and finger_bools[2] and finger_bools[3] and finger_bools[4]:
                                cv2.putText(img, char[0], (630, 100), cv2.FONT_HERSHEY_COMPLEX, 4, (255, 0, 255), 2)
                                print(char[0], (
                                    int(char[1]), h - int(char[2])), (int(char[3]), h - int(char[4])), lmList[ids])
                            else:
                                pass

            # print(char[0], lmList[ids][2], (h - int(char[2])), lmList[ids][2], (h - int(char[4])))

    # img = cv2.flip(img, 0)
    ##########FPS##########
    cTime = time.time()
    fps = int(1/(cTime - pTime))
    pTime = cTime
    cv2.putText(img, f"FPS:{int(fps)}", (5, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 4)

    cv2.imshow("Webcam", img)
    # cv2.imshow("Webcam2", imgAsus)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
