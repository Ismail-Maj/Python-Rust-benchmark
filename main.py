import cv2
import numpy as np
import sys


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


def max_intersection(A, B):
    x1, x2, y1, y2 = A
    x3, x4, y3, y4 = B
    x1, x3 = np.expand_dims(x1, axis=0), np.expand_dims(x3, axis=1)
    y1, y3 = np.expand_dims(y1, axis=0), np.expand_dims(y3, axis=1)
    x2, x4 = np.expand_dims(x2, axis=0), np.expand_dims(x4, axis=1)
    y2, y4 = np.expand_dims(y2, axis=0), np.expand_dims(y4, axis=1)
    x5, y5 = np.maximum(x1, x3), np.maximum(y1, y3)
    x6, y6 = np.minimum(x2, x4), np.minimum(y2, y4)
    width, height = x6 - x5, y6 - y5
    area = width.clip(min=0) * height  # must clip one to avoid negative * negative -> positive

    best_index = area.argmax()
    line, column = best_index // area.shape[1], best_index % area.shape[1]

    if area[line][column] <= 0:
        return None

    return [x5[line][column]], [x6[line][column]], [y5[line][column]], [y6[line][column]]


if __name__ == "__main__":
    width_max = 1600
    height_max = 900
    image = np.full((height_max, width_max, 3), 255, dtype=np.uint8)
    A = generate_boxes(width_max, height_max)
    B = generate_boxes(width_max, height_max)
    draw_boxes(image, A, color=(0, 0, 255))
    draw_boxes(image, B, color=(255, 0, 0))
    cv2.imshow("window", image)
    cv2.waitKey()
    draw_boxes(image, max_intersection(A, B), thickness=-1)
    cv2.imshow("window", image)
    cv2.waitKey()
