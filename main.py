import cv2 as cv
import numpy as np
from math import floor

vid = cv.VideoCapture(0)

# resolution to represent each character by, in pixels
asciiWidth = 4

# ascii array to store the mapping

asciiArr = [' ', '.', '-', "'", ':', '=', '+', '!', 'r', 'c', '*', 'v', ')', 'J', '7',
            '(', '|', 'F', 'i', '}', 'f', 'a', ']', '2', 'E', 'S', 'w', 'B', 'g', '0', '%', '&', '@']


while (True):

    ret, frame = vid.read()
    originalX, originalY, _ = frame.shape

    orininalDims = (originalX, originalY)

    # ===========================================  crop the original rectangular image to a square ============================================================
    # original image:
    #     =======================
    #     =======================
    #     =======================
    #     =======================
    #     =======================

    # cropped image:
    #       newYstart    newYend
    #     =====.==========.======
    #     =====.==========.======
    #     =====.==========.======
    #     =====.==========.======
    #     =====.==========.======

    newYstart = (originalY // 2) - (originalX // 2)
    newYend = (originalY // 2) + (originalX // 2)

    frame = frame[:, newYstart: newYend, :]

    resizedFrame = cv.resize(
        frame, (originalX // asciiWidth, originalX // asciiWidth))

    resizedFrame = cv.GaussianBlur(resizedFrame, ksize=(3, 3), sigmaX=3)

    # ======================================================== quantize the image into bins =================================================================

    resizedFrame = cv.cvtColor(resizedFrame, cv.COLOR_BGR2GRAY)

    resizedFrame = resizedFrame // len(asciiArr)

    asciiFrame = np.zeros((originalX, originalX), dtype=np.uint8)

    # ======================================================== assign respective ascii values to the frame ==================================================
    # using nested loops, which is a horrible way to do it

    # some weird roundabout way to get the font to reder based on pixel size:
    # calculating a factor here
    fontScale = 10
    fontFace = cv.FONT_HERSHEY_PLAIN

    ((fw, fh), baseline) = cv.getTextSize(
        "", fontFace=fontFace, fontScale=fontScale, thickness=1)  # empty string is good enough
    factor = (fh-1) / fontScale

    # using the factor now
    thickness = 1
    height_in_pixels = 4  # or 20, code works either way
    fontScale = (height_in_pixels - thickness) / factor

    for i in range(0, originalX, asciiWidth):
        for j in range(0, originalX , asciiWidth):

            pixel = resizedFrame[i // asciiWidth, j // asciiWidth]

            asciiChar = asciiArr[pixel % len(asciiArr)]

            asciiFrame = cv.putText(asciiFrame, asciiChar, (i, j), fontFace=fontFace,
                                    fontScale=fontScale, color=255, thickness=thickness, bottomLeftOrigin=False)

    asciiFrame = cv.rotate(asciiFrame, cv.ROTATE_90_CLOCKWISE)

    cv.imshow("art", asciiFrame)
    cv.imshow("original", resizedFrame * 20)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv.destroyAllWindows()
