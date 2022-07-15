# Import required packages
import cv2
import pytesseract
import os
from pytesseract import Output
import pandas


# https://www.geeksforgeeks.org/text-detection-and-extraction-using-opencv-and-ocr/
# https://stackoverflow.com/a/67272995/19324525
# Keep the countour commands, it performes better with them even though they don't do anything

def ocr(image, filedate):
    img = "./process/"
    img += image
    img = cv2.imread(image)

    # Preprocessing the image starts
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Performing OTSU threshold
    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))

    # Applying dilation on the threshold image
    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)

    # Finding contours
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
    # Creating a copy of image
    im2 = img.copy()

    cropped = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
    cropped = cv2.threshold(cropped, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    cropped = 255 - cropped
    cropped = cv2.GaussianBlur(cropped, (5, 5), 0)

    # Apply OCR on the cropped image
    results = pytesseract.image_to_data(cropped, output_type='data.frame',
                                        config="--psm 11 -l eng -c tessedit_char_whitelist==abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\\ \\'\\?")
    # text = pytesseract.image_to_string(cropped,
    #                                    config="--psm 12 -l eng -c tessedit_char_whitelist==abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ\\ \\'\\?")

    text = results[results.conf >= 60]  # Ignore each word below threshold
    lines = text.groupby(['page_num', 'block_num', 'par_num', 'line_num'])['text'].apply(
        lambda x: ' '.join(list(x))).tolist()
    # print(lines)
    # A text file is created and flushed
    txt = "./process/"
    txt += filedate
    ext = '.txt'
    txt += ext
    file = open(txt, "a+")
    for i in range(len(lines)):
        if (lines[i].strip()) and (len(lines[i].split()) > 1):  # Don't accept empty line or single word lines
            print(lines[i])
            # Open the file in append mode

            # Appending the text into file
            file.write(lines[i])
            file.write("\n")
        # Close the file
    file.close

# for i in range(len(line_conf)):
# 	if len(line_conf[i].split()) > 1: #Don't accept single word lines
# 		print(line_conf[i])
# 		# Open the file in append mode
# 		file = open(txt, "a")
# 		# Appending the text into file
# 		file.write(line_conf[i])
# 		file.write("\n")

# 		# Close the file
# 		file.close


# Looping through the identified contours
# Then rectangular part is cropped and passed on
# to pytesseract for extracting text from it
# Extracted text is then written into the text file
# for cnt in contours:
# 	x, y, w, h = cv2.boundingRect(cnt)

# 	# Drawing a rectangle on copied image
# 	rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)

# 	# Cropping the text block for giving input to OCR
# 	cropped = im2[y:y + h, x:x + w]
# cropped = thresh1[y:y + h, x:x + w]


# for i in range(0, len(results["text"])):
# 	# extract the bounding box coordinates of the text region from
# 	# the current result
# 	x = results["left"][i]
# 	y = results["top"][i]
# 	w = results["width"][i]
# 	h = results["height"][i]

# 	# extract the OCR text itself along with the confidence of the
# 	# text localization
# 	text = results["text"][i]
# 	conf = int(float(results["conf"][i]))

# 	# filter out weak confidence text localizations

# 	# display the confidence and text to our terminal
# 	print("Confidence: {}".format(conf))
# 	print("Text: {}".format(text))
# 	print("")
