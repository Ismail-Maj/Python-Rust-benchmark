import numpy as np
import cv2

def generate_boxes(width_max, height_max, size=20):
    width = np.random.geometric(7 / width_max, size=size).clip(max=width_max)
    height = np.random.geometric(7 / height_max, size=size).clip(max=height_max)

    x = np.random.randint(0, width_max - width + 1, size=size)
    y = np.random.randint(0, height_max - height + 1, size=size)

    return x, x + width, y, y + height


def draw_boxes(image, boxes, color=(0, 0, 0), thickness=2):
    if boxes:
        for x1, x2, y1, y2 in zip(*boxes):
            cv2.rectangle(image, (x1, y1), (x2, y2), color=color, thickness=thickness)