import cv2
from time import time
from time import sleep
import numpy as np
from windowcapture import WindowCapture
import pytesseract
import pydirectinput as di

# Initialize the WindowCapture class
wincap = WindowCapture('Nostalgia2')
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'
loop_time = time()


def captcha_detection(screenshot):
    unmodified_image = screenshot

    # Sets columns and rows
    height, width = unmodified_image.shape[0:2]
    startRow = int(height * .455)
    startCol = int(width * .474)
    endRow = int(height * .50)
    endCol = int(width * .50)

    # Applies column and rows values
    cropped_image = unmodified_image[startRow:endRow, startCol:endCol]
    # HSV Array
    lower = np.array([0, 100, 255])
    upper = np.array([100, 200, 255])
    # Converts the image to HSV
    hsv = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2HSV)
    # Applies HSV Filter
    mask = cv2.inRange(hsv, lower, upper)
    # Inverts the colors
    inverted_image = np.invert(mask)
    # Upscale the image
    upscale_width = 200
    upscale_height = 200
    upscale_points = (upscale_width, upscale_height)
    resized_image = cv2.resize(inverted_image, upscale_points, interpolation=cv2.INTER_LINEAR)
    # Detect the captcha
    captcha = pytesseract.image_to_string(resized_image, lang='eng',
                                          config='-c tessedit_char_whitelist=0123456789 --psm 6')
    return captcha


def captcha_resolver(captcha):

    print('Captcha is :', captcha)
    di.typewrite(captcha)
    print('Typing done, script will resume in 5 seconds...')
    # TODO : MOVE MOUSE TO DETECTED BUTTON
    # TODO : CLICK BUTTON
    sleep(5)


def main_engine():
    while (True):
        global screenshot
        global loop_time
        # Input the hourglass to detect
        hourglass_image = cv2.imread('images\hourglass_image.png')

        # Takes screenshot each frame and saves it to variable screenshot
        screenshot = wincap.get_screenshot()
        #creenshot = cv2.imread('images\captcha.png')

        # Do CV2 template matching for hourglass
        hourglass_matching = cv2.matchTemplate(screenshot, hourglass_image, cv2.TM_CCOEFF_NORMED)

        # TODO : ADD DETECTION FOR ACCEPT BUTTON
        # TODO : FIND X, Y COORDONATES OF ACCEPT BUTTON

        # Get the position of the hourglass
        min_val_hg, max_val_hg, min_loc_hg, max_loc_hg = cv2.minMaxLoc(hourglass_matching)

        # Set the treshold to 0.9
        threshold = 0.9

        if max_val_hg >= threshold:
            print("Found captcha at : %s" % str(max_loc_hg))
            captcha = captcha_detection(screenshot)

            captcha_resolver(captcha)

        #cv2.imshow('Debug window - Press Q to exit program', screenshot)

        #if cv2.waitKey(1) == ord('q'):
            #cv2.destroyAllWindows()
            #break

    print('Done.')


def main():
    main_engine()


if __name__ == "__main__":
    main()
