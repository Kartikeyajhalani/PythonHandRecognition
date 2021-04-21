import cv2
import HandTrackingModule as htm
import pytesseract
import time

frames = cv2.VideoCapture('http://192.168.225.55:4747/video?640x480')
framesAsus = cv2.VideoCapture('http://192.168.225.132:4747/video?640x480')
detector = htm.hlmDetector()
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
pTime = 0

while True:
    ##############For first camera###########
    ret, img = frames.read()
    img = detector.findHands(img)
    lmList = detector.findHLms(img)
    finger_Bool = detector.finOC(lmList)
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    boxes = pytesseract.pytesseract.image_to_boxes(imgRGB)
    print(boxes)
    ##########################################

    ###############For second camera#############
    ret2, imgAsus = framesAsus.read()
    imgAsus = cv2.flip(imgAsus, 0)
    imgAsus = detector.findHands(imgAsus)
    lmList2 = detector.findHLms(imgAsus)
    ############################################
    i = 0
    while i < 480:
        cv2.line(imgAsus, (0, i), (639, i), (0, 255, 0), 3)
    if lmList:
        if finger_Bool[1] == 0:
            if finger_Bool[0] and finger_Bool[2] and finger_Bool[3] and finger_Bool[4]:
                if lmList2[8] > 400:
                    print(True)


    cTime = time.time()
    fps = int(1/(cTime - pTime))
    pTimec= cTime
    cv2.putText(img, f"FPS:{int(fps)}", (50, 50), cv2.FONT_HERSHEY_COMPLEX, 3, (255, 0, 255), 4)
    cv2.imshow("Webcam", img)
    cv2.imshow("Webcam2", imgAsus)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
