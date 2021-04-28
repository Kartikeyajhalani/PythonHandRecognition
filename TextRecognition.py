import cv2
import pytesseract

class text_recog():
    def __init__(self):
        pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

    def text_char(self, img):
        self.image = img
        img = cv2.imread(img)
        imgrgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        cong = r'-l eng --psm 3 --oem 3'
        boxes = pytesseract.image_to_boxes(imgrgb, config=cong)
        self.h, self.w, c = img.shape
        self.characters = []
        for char in boxes.splitlines():
            char = char.split()
            self.characters.append(char)
            # self.characters.remove(['V', '820', '500', '880', '570', '0'])
            # characters = self.characters
        return self.characters


    def draw_on_img(self, image_into_print, char_set):
        image_into_print = cv2.imread(image_into_print)
        for char in char_set:
            for char in char_set:
                cv2.putText(image_into_print, char[0], (int(char[1]), self.h - int(char[2]) + 40), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
                image_into_print = cv2.rectangle(image_into_print, (int(char[1]), self.h - int(char[2])), (int(char[3]), self.h - int(char[4])),(0, 255, 0), 2)
        # return image_into_print

# print(text_marks('Keyboard.png'))
