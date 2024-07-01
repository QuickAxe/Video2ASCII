import cv2 as cv
import numpy as np
from math import floor

vid = cv.VideoCapture(0)

# resolution to represent each character by, in pixels
asciiWidth = 4

# ascii array to store the mapping
asciiArr = [' ', '.', '-', "'", ':', '_', ',', '^', '=', ';', '>', '<', '+', '!', 'r', 'c', '*', '/', 'z', '?', 's', 'L', 'T', 'v', ')', 'J', '7',
            '(', '|', 'F', 'i', '{', 'C', '}', 'f', 'I', '3', '1', 't', 'l', 'u', '[', 'n', 'e', 'o', 'Z', '5', 'Y', 'x', 'j', 'y', 'a', ']', '2',
            'E', 'S', 'w', 'q', 'k', 'P', '6', 'h', '9', 'd', '4', 'V', 'p', 'O', 'G', 'b', 'U', 'A', 'K', 'X', 'H', 'm', '8', 'R', 'D', '#', '$',
            'B', 'g', '0', 'M', 'N', 'W', 'Q', '%', '&', '@']

while (True):

    ret, frame = vid.read()
    originalX, originalY, _ = frame.shape

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

    # resizedFrame = (resizedFrame / 255) * (len(asciiArr) + 1)
    # resizedFrame = resizedFrame // len(asciiArr) * len(asciiArr)
    # resizedFrame = [  [ int(i) for i in j ] for j in resizedFrame]

    # ======================================================== assign respective ascii values to the frame ==================================================
    # using nested loops, which is a horrible way to do it

    # ------  some weird roundabout way to get the font to reder based on pixel size -----------------
    # calculating a factor here
    fontScale = 10
    fontFace = cv.FONT_HERSHEY_PLAIN

    ((fw, fh), baseline) = cv.getTextSize(
        "", fontFace=fontFace, fontScale=fontScale, thickness=1)  # empty string is good enough
    factor = (fh-1) / fontScale

    thickness = 1
    height_in_pixels = asciiWidth  # or 20, code works either way
    fontScale = (height_in_pixels - thickness) / factor

    # =================================================================== main conversion ====================================================================

    asciiFrame = np.zeros((originalX, originalX), dtype=np.uint8)

    for i in range(0, originalX, asciiWidth):
        for j in range(0, originalX, asciiWidth):

            pixel = resizedFrame[i // asciiWidth, j // asciiWidth]

            asciiChar = asciiArr[int(pixel / 256 * len(asciiArr))]

            asciiFrame = cv.putText(asciiFrame, asciiChar, (j, i), fontFace=fontFace,
                                    fontScale=fontScale, color=255, thickness=thickness, bottomLeftOrigin=False)

    cv.imshow("art", asciiFrame)
    cv.imshow("original", (resizedFrame // len(asciiArr)))

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv.destroyAllWindows()
