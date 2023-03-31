import easyocr

def imageToText(image):
    reader = easyocr.Reader(['en'])
    result = reader.readtext(image,paragraph="False",detail = 0)
    print(result[0])
    return result[0]

