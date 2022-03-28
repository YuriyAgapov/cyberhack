import cv2
import mss as mss


# Provide screen area ops
class ScreenArea:
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def __str__(self):
        return f'l:{self.left},t:{self.top},r:{self.right},b:{self.bottom}'

    # returns area coords scaled by WxH
    def scaled(self, w, h):
        return ScreenArea(self.left * w, self.top * h, self.right * w, self.bottom * h)

    # returns image area
    def crop(self, img):
        return img[int(self.top):int(self.bottom), int(self.left):int(self.right)]


# base screen size (to calc scaling factors)
original_w = 1920
original_h = 1080

# screen zones (scaling factors)

# TECH title for hack mode detection area
id_rect_factor = ScreenArea(149 / original_w, 52 / original_h, 220 / original_w, 71 / original_h)

# symbols map area
matrix_rect_factor = ScreenArea(211 / original_w, 341 / original_h, 761 / original_w, 718 / original_h)

# sequences list area
sequences_rect_factor = ScreenArea(826 / original_w, 335 / original_h, 1231 / original_w, 565 / original_h)

# buffer line area
buffer_rect_factor = ScreenArea(824 / original_w, 181 / original_h, 1249 / original_w, 244 / original_h)

# buffer symbol box size factor
box_size_factor = 42 / original_w

# resoved sequences pos factor
text_pos_factor = 685 / original_h
