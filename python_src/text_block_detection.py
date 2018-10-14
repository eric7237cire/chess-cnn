# https://github.com/LinxiFan/LiteOCR/blob/master/liteocr/ocr.py
# https://stackoverflow.com/questions/23506105/extracting-text-opencv
from collections import namedtuple
import numpy as np
import cv2

def show_image(image):
    cv2.imshow('image',image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


image_bgr = cv2.imread(r'..\data\screenshots\ss.png', cv2.IMREAD_COLOR)

img_gray = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2GRAY)

#show_image(img_gray)

#https://docs.opencv.org/3.0-beta/modules/imgproc/doc/miscellaneous_transformations.html#cv2.adaptiveThreshold
img_bw = cv2.adaptiveThreshold(img_gray, 255,
                               cv2.ADAPTIVE_THRESH_MEAN_C,
                               cv2.THRESH_BINARY, 11, 5)

#show_image(img_bw)

# https://docs.opencv.org/3.0-beta/modules/imgproc/doc/filtering.html?highlight=morphologyex#cv2.morphologyEx
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
print(kernel)
img = cv2.morphologyEx(img_gray, cv2.MORPH_GRADIENT, kernel)

#show_image(img)
# cut off all gray pixels < 30.
# `cv2.THRESH_BINARY | cv2.THRESH_OTSU` is also good, but might overlook certain light gray areas
_, img = cv2.threshold(img, 30, 255, cv2.THRESH_BINARY)
# connect horizontally oriented regions
horizontal_pooling  = 25
kernel = cv2.getStructuringElement(cv2.MORPH_RECT,
                                   (horizontal_pooling, 1))

print(kernel)
img = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)

#show_image(img)
thin_line_thresh = 7

# https://docs.opencv.org/3.4/d9/d61/tutorial_py_morphological_ops.html
# remove all thin textbox borders (e.g. web page textbox)
if thin_line_thresh > 0:
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT,
                                       (thin_line_thresh, thin_line_thresh))
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

#show_image(img)

# http://docs.opencv.org/trunk/d9/d8b/tutorial_py_contours_hierarchy.html
_, contours, hierarchy = cv2.findContours(img, cv2.RETR_CCOMP,
                                          cv2.CHAIN_APPROX_SIMPLE)

MIN_TEXT_SIZE = 15
MAX_TEXT_SIZE = 200
UNIFORMITY_THRESH = 0.1
THIN_LINE_THRESH = 7
CONF_THRESH = 20
BOX_EXPAND_FACTOR = 0.15
HORIZONTAL_POOLING = 25
CROP_RESIZE_HEIGHT = 100   # height of crops to feed into tesseract.
Box = namedtuple('Box', ['x', 'y', 'w', 'h'])
min_text_size=MIN_TEXT_SIZE
max_text_size=MAX_TEXT_SIZE
uniformity_thresh=UNIFORMITY_THRESH
thin_line_thresh=THIN_LINE_THRESH
conf_thresh=CONF_THRESH
box_expand_factor=BOX_EXPAND_FACTOR
horizontal_pooling=HORIZONTAL_POOLING
def crop(img, box):
    """
    Crop a numpy image with bounding box (x, y, w, h)
    """
    x, y, w, h = box
    return img[y:y+h, x:x+w]

for contour in contours:
    x, y, w, h = box = Box(*cv2.boundingRect(contour))
    # remove regions that are beyond size limits
    if (w < min_text_size or h < min_text_size
        or h > max_text_size):
        continue
    # remove regions that are almost uniformly white or black
    binary_region = crop(img_bw, box)
    uniformity = np.count_nonzero(binary_region) / float(w * h)
    if (uniformity > 1 - uniformity_thresh
        or uniformity < uniformity_thresh):
        continue
    # expand the borders a little bit to include cutoff chars
    expansion = int(min(h, w) * box_expand_factor)
    x = max(0, x - expansion)
    y = max(0, y - expansion)
    h, w = h + 2 * expansion, w + 2 * expansion
    if h > w: # further extend the long axis
        h += 2 * expansion
    elif w > h:
        w += 2 * expansion
    # image passed to Tess should be grayscale.
    # http://stackoverflow.com/questions/15606379/python-tesseract-segmentation-fault-11
    box = Box(x, y, w, h)
    img_crop = crop(img_gray, box)
    # make sure that crops passed in tesseract have minimum x-height
    # http://github.com/tesseract-ocr/tesseract/wiki/FAQ#is-there-a-minimum-text-size-it-wont-read-screen-text
    img_crop = cv2.resize(img_crop, (int(img_crop.shape[1]
        * CROP_RESIZE_HEIGHT / img_crop.shape[0]), CROP_RESIZE_HEIGHT))

    show_image(img_crop)
    #ocr_text, conf = self.run_tess(img_crop)
    #if conf > conf_thresh:
        #yield Blob(ocr_text, box, conf)