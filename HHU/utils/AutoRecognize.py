import pytesseract
from PIL import Image
import os
import sys
import re
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract'

class AutoRecognize(object):
    def autoRecognize(self):
        image=Image.open(sys.path[1]+"/HHU/image/verify.jpg")
        text=pytesseract.image_to_string(image)
        return text

    def dispose_text(self,text):
        result=""
        for one in re.findall('(\w*)',text.replace(' ','')):
            result+=one
        return result
    def get_verify(self):
        return self.dispose_text(self.autoRecognize())

# image = image.point(lambda x: 0 if x < 143 else 255)
# image.save("1.jpg")
#print(AutoRecognize().get_verify())