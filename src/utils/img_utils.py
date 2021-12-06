from PIL import Image
import numpy

import cv2


def resize(image, size):
    print(f'Resizing image to:{size}')
    resized_image = image.resize(size)
    return resized_image


def cut_image_to_grid(pil_image):
    img = cv2.cvtColor(numpy.array(pil_image), cv2.COLOR_RGB2BGR)
    img_height = img.shape[0]
    img_width = img.shape[1]

    # TODO: Use dynamic cell size
    M = 30
    N = 30

    for y in range(0, img_height, M):
        for x in range(0, img_width, N):
            if (img_height - y) < M or (img_width - x) < N:
                break

            y1 = y + M
            x1 = x + N

            # check whether the patch width or height exceeds the image width or height
            if x1 >= img_width and y1 >= img_height:
                x1 = img_width - 1
                y1 = img_height - 1
                cv2.rectangle(img, (x, y), (x1, y1), (0, 255, 0), 1)
            elif y1 >= img_height:  # when patch height exceeds the image height
                y1 = img_height - 1
                cv2.rectangle(img, (x, y), (x1, y1), (0, 255, 0), 1)
            elif x1 >= img_width:  # when patch width exceeds the image width
                x1 = img_width - 1
                cv2.rectangle(img, (x, y), (x1, y1), (0, 255, 0), 1)
            else:
                cv2.rectangle(img, (x, y), (x1, y1), (0, 255, 0), 1)

    return Image.fromarray(img)
