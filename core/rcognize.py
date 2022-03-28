import logging

import cv2
from pytesseract import pytesseract

from screen_area import id_rect_factor

# scaling to prepare for recognition
scaling_factor = 1.7

# reverse scaling factor
back_scaling_factor = 1.0 / scaling_factor


def resize_img(img, scale_percent: float):
    width = int(img.shape[1] * scale_percent)
    height = int(img.shape[0] * scale_percent)
    dim = (width, height)

    # resize image
    return cv2.resize(img, dim, interpolation=cv2.INTER_AREA)


# try to correct common recognition errors
def fix_symbol_presentation(text: str):
    substitute_map = {'1C': ['1', 'i', 'I', 'w', 'U', 'W', 'C'],
                      '55': ['5', '6'],
                      'E9': ['E'],
                      '7A': ['7'],
                      'FF': ['F'],
                      'BD': ['B']}

    if text == '99':
        return '55'

    if text == 'ss':
        return '55'

    if text == 'SS':
        return '55'

    if text in substitute_map:
        return text

    for sym in substitute_map:
        if text[0] == sym[0] or text[-1] == sym[-1]:
            return sym

        exp = substitute_map[sym]
        if text[0] in exp:
            return sym

    logging.debug(f'Unknown symbol "{text}"')
    return text


def get_matrix_from_image(img):
    # prepare image for recognizing

    # make grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # invert b/w
    img = cv2.bitwise_not(img)

    # resize before bluring
    img = resize_img(img, scaling_factor)

    # minimal bluring
    img = cv2.GaussianBlur(img, (3, 3), 2)

    # slice by color
    img = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # recognize
    data = pytesseract.image_to_data(img, lang='eng', config='--psm 6')

    last_x = 0
    matrix = []
    current_row = []
    coord_row = []
    coord_map = []

    for i, elements in enumerate(data.splitlines()):
        if i == 0:
            continue

        elements = elements.split()
        try:
            x, y, w, h = int(elements[6]), int(elements[7]), int(elements[8]), int(elements[9])
            text = fix_symbol_presentation(elements[11])

            # make matrix
            if last_x > x:
                matrix.append(current_row)
                coord_map.append(coord_row)
                current_row = []
                coord_row = []
                last_x = 0
            last_x = x
            current_row.append(text)
            coord_row.append([x + w / 2, y + h / 2])

        except IndexError:
            # scip empty elements
            pass

    if len(current_row) > 0:
        matrix.append(current_row)
        coord_map.append(coord_row)

    return matrix, coord_map


def get_buffer_size(img, box_size):
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    thresh_img = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    cnts = cv2.findContours(thresh_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    min_x = 9999
    max_x = 0
    for cnt in cnts:
        if len(cnt) < 2:
            continue

        if cnt[0][0][0] < min_x:
            min_x = cnt[0][0][0]
        if cnt[1][0][0] < min_x:
            min_x = cnt[1][0][0]

        if cnt[0][0][0] > max_x:
            max_x = cnt[0][0][0]
        if cnt[1][0][0] > max_x:
            max_x = cnt[1][0][0]

    total_width = max_x - min_x
    return int(total_width/box_size)


# returns first recognized element on image
def get_id(image):
    # w = image.shape[1]
    # h = image.shape[0]
    # id_rect = id_rect_factor.scaled(w, h)
    # id_img = id_rect.crop(image)
    elements, _ = get_matrix_from_image(image)
    if len(elements) == 0:
        return ""
    if len(elements[0]) == 0:
        return ""
    return elements[0][0]
