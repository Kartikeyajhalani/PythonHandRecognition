import cv2
import mediapipe as mp
import time

class hlmDetector():
    def __init__(self, static_image_mode = False, max_num_hands = 2, min_detection_confidence = 0.5, min_tracking_confidence = 0.5):
        self.static_image_mode = static_image_mode
        self.max_num_hands = max_num_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence
        #######INITIALIZATION OF HANDS############
        self.mpHands = mp.solutions.hands
        self.Hands = self.mpHands.Hands(self.static_image_mode, self.max_num_hands, self.min_detection_confidence, self.min_tracking_confidence)
        #######INITIALIZATION FOR DRAWING###########
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, img, Draw=True, colour=None,  thickness=2, circle_radius=2):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.Hands.process(imgRGB)
        if self.results.multi_hand_landmarks:
            for self.handlms in self.results.multi_hand_landmarks:
                if Draw:
                    self.mpDraw.draw_landmarks(img, self.handlms, self.mpHands.HAND_CONNECTIONS)
                    #############Here colour specifies color of both landmarks and and landmark connections##############
                    if colour:
                        self.mpDraw.draw_landmarks(img, self.handlms, self.mpHands.HAND_CONNECTIONS,
                                                   self.mpDraw.DrawingSpec(colour, thickness, circle_radius),
                                                   self.mpDraw.DrawingSpec(colour, thickness))
        return img

    def findHLms(self, img, handNo=0, Draw=False,  colour=None,  thickness=2, circle_radius=2):
        lmList = []
        if self.results.multi_hand_landmarks:
            self.myHand = self.results.multi_hand_landmarks[handNo]
            for id, lm in enumerate(self.myHand.landmark):
                y, x, c = img.shape
                wz = lm.z
                px, py = int(lm.x*x), int(lm.y*y)
                lmList.append([id, px, py, wz])
        ############Here colour specifies colour of only landmarks################
        if Draw:
            if colour:
                self.mpDraw.draw_landmarks(img, self.myHand, self.mpHands.HAND_CONNECTIONS,
                                           self.mpDraw.DrawingSpec(colour, thickness, circle_radius))
        return lmList

    #########NOTE:-It can only find if list is according to mediapipe###########
    def finOC(self, lmList):
        fingerBool = []
        if lmList:
            if lmList[4][1] < lmList[2][1]:
                fingerBool.append(1)
            else:
                fingerBool.append(0)
            for i in range(2, 6):
                if lmList[i * 4][2] > lmList[(i * 4) - 2][2]:
                    fingerBool.append(1)
                else:
                    fingerBool.append(0)
        return fingerBool

def main():
    frames = cv2.VideoCapture('http://192.168.225.55:4747/video?640x480')
    pTime = 0
    detector = hlmDetector()
    while True:
        ret, img = frames.read()
        img = detector.findHands(img)
        lmList = detector.findHLms(img)
        print(lmList)
        #####FPS#####
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv2.putText(img, f'FPS:{int(fps)}', (35, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 2)
        cv2.imshow("Webcam", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__ == "__main__":
    main()
