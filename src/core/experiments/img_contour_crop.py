import cv2
import imutils
import numpy as np
from PIL import Image


def contour_crop(img, thresh=120, color=255):
    # convert the image to grayscale and threshold it
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh = cv2.threshold(gray, thresh, color,
                           cv2.THRESH_BINARY_INV)[1]

    #  find the largest contour in the threshold image
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)

    color_mask = (color, color, color)

    # Extract image inside c
    output = img.copy()
    mask = np.zeros_like(output)  # Create mask where white is what we want, black otherwise
    cv2.drawContours(mask, [c], -1, color_mask, -1)  # Draw filled contour in mask
    out = np.zeros_like(output)  # Extract out the object and place into output image
    out[mask == color_mask] = output[mask == color_mask]

    # Crop image to contour area
    (y, x, z) = np.where(mask == color_mask)
    (topy, topx) = (np.min(y), np.min(x))
    (bottomy, bottomx) = (np.max(y), np.max(x))
    out = out[topy:bottomy + 1, topx:bottomx + 1]

    # TODO: Figure out a way to stop converting between PIL.Image and cv2.img
    # return out
    return Image.fromarray(out)
