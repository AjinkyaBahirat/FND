import os
import easyocr
IMAGE_PATH = 'static/uploads/sampletext.png'
reader = easyocr.Reader(['en'])
result = reader.readtext(IMAGE_PATH,paragraph="False",detail = 0)
print(result)