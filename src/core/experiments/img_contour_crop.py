import imutils
import cv2

# load the image and display it
image = cv2.imread("jigsaw_examples/1000_tropics_jigsaw/piece_4.jpg")


# convert the image to grayscale and threshold it
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 110, 255,
                       cv2.THRESH_BINARY_INV)[1]

#  find the largest contour in the threshold image
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
c = max(cnts, key=cv2.contourArea)
# draw the shape of the contour on the output image, compute the
# bounding box, and display the number of points in the contour
output = image.copy()
cv2.drawContours(output, [c], -1, (0, 255, 0), 3)
(x, y, w, h) = cv2.boundingRect(c)
text = "original, num_pts={}".format(len(c))
cv2.putText(output, text, (x, y - 15), cv2.FONT_HERSHEY_SIMPLEX,
            0.9, (0, 255, 0), 2)
# show the original contour image
print("[INFO] {}".format(text))


scale_percent = 33  # percent of original size
width = int(output.shape[1] * scale_percent / 100)
height = int(output.shape[0] * scale_percent / 100)
dim = (width, height)

# resize image
image2 = cv2.resize(output, dim, interpolation=cv2.INTER_AREA)

cv2.imshow("Original Contour", image2)

cv2.waitKey(0)
