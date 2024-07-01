import cv2 as cv
import numpy as np

vid = cv.VideoCapture(0)

# resolution to represent each character by, in pixels
asciiWidth = 8

# ascii array to store the mapping

asciiArr = [" ", ".", ";", "c", "o", "P", "O", "?", "#", "█"]


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

    # ======================================================== quantize the image into bins =================================================================

    resizedFrame = cv.cvtColor(resizedFrame, cv.COLOR_BGR2GRAY)

    resizedFrame = resizedFrame % 10

    asciiFrame = np.zeros((originalX, originalX, 1), dtype=np.uint8)

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

    for i in range(0, originalX - 1, asciiWidth):
        for j in range(0, originalX - 1, asciiWidth):

            pixel = resizedFrame[i // asciiWidth, j // asciiWidth]

            asciiChar = asciiArr[pixel]

            cv.putText(asciiFrame, asciiChar, (i, j), fontFace=fontFace,
                       fontScale=fontScale, color=255, thickness=thickness, bottomLeftOrigin=False)

    cv.imshow("art", asciiFrame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv.destroyAllWindows()
