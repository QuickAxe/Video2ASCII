import cv2 as cv
import numpy as np
from math import floor


path = "./sampleVid.mp4"

# comment the below line to use a video file, with the path specified above
# path = 0

vid = cv.VideoCapture(path)

# resolution to represent each character by, in pixels
asciiWidth = 15

# ascii array to store the mapping
asciiArr = [' ', '.', '-', "'", ':', '_', ',', '^', '=', ';', '>', '<', '+', '!', 'r', 'c', '*', '/', 'z', '?', 's', 'L', 'T', 'v', ')', 'J', '7',
            '(', '|', 'F', 'i', '{', 'C', '}', 'f', 'I', '3', '1', 't', 'l', 'u', '[', 'n', 'e', 'o', 'Z', '5', 'Y', 'x', 'j', 'y', 'a', ']', '2',
            'E', 'S', 'w', 'q', 'k', 'P', '6', 'h', '9', 'd', '4', 'V', 'p', 'O', 'G', 'b', 'U', 'A', 'K', 'X', 'H', 'm', '8', 'R', 'D', '#', '$',
            'B', 'g', '0', 'M', 'N', 'W', 'Q', '%', '&', '@']
asciiLevels = len(asciiArr)

while (True):

    ret, frame = vid.read()
    
    if not ret:
        print("video either not available, or has ended :(")
        break
    
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
    grayFrame = cv.cvtColor(resizedFrame, cv.COLOR_BGR2GRAY)

    # ======================================================== assign respective ascii values to the frame ==================================================
    # using nested loops, which is a horrible way to do it

    # ----------------  some weird roundabout way to get the font to render based on pixel size -----------------
    # calculating a factor here
    fontScale = asciiWidth*32
    fontFace = cv.FONT_HERSHEY_PLAIN

    ((fw, fh), baseline) = cv.getTextSize(
        "", fontFace=fontFace, fontScale=fontScale, thickness=1)  # empty string is good enough
    factor = (fh-1) / fontScale

    thickness = 1
    height_in_pixels = asciiWidth  # or 20, code works either way
    fontScale = (height_in_pixels - thickness) / factor

    # =================================================================== main conversion ====================================================================

    asciiFrame = np.zeros((originalX, originalX, 3), dtype=np.uint8)
    grayFrame = np.rint(np.multiply(grayFrame, asciiLevels/256)).astype(int)
     
    
    
    for i in range(0, originalX, asciiWidth):
        for j in range(0, originalX, asciiWidth):

            pixel = grayFrame[i // asciiWidth, j // asciiWidth]

            # map the intensity value to an ascii character
            asciiChar = asciiArr[pixel]

            # find the colour of the original image, to set the ascii character to that colour
            b, g, r = resizedFrame[i // asciiWidth, j // asciiWidth]
            color = (int(b), int(g), int(r))

            # add the ascii character to the output frame
            asciiFrame = cv.putText(asciiFrame, asciiChar, (j, i), fontFace=fontFace,
                                    fontScale=fontScale, color=color, thickness=thickness, bottomLeftOrigin=False)

    cv.imshow("art", asciiFrame)

    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv.destroyAllWindows()
