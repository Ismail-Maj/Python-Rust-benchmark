import cv2
import time
import numpy as np
import argparse
import rust_lib
import operator


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


def two_sets_intersection_numpy(x1, x2, y1, y2, x3, x4, y3, y4):

    x5 = np.maximum(np.expand_dims(x1, axis=0), np.expand_dims(x3, axis=1))
    x6 = np.minimum(np.expand_dims(x2, axis=0), np.expand_dims(x4, axis=1))

    y5 = np.maximum(np.expand_dims(y1, axis=0), np.expand_dims(y3, axis=1))
    y6 = np.minimum(np.expand_dims(y2, axis=0), np.expand_dims(y4, axis=1))

    width, height = x6 - x5, y6 - y5

    area = width.clip(min=0) * height  # must clip one to avoid negative * negative -> positive

    best_index = area.argmax()
    row, column = best_index // area.shape[1], best_index % area.shape[1]

    if area[row][column] <= 0:
        raise ValueError("empty intersection")

    return x5[row][column], x6[row][column], y5[row][column], y6[row][column]

def main(args): 
    np.random.seed(args.seed)

    image = np.full((args.window_height, args.window_width, 3), 255, dtype=np.uint8)

    A = generate_boxes(args.window_width, args.window_height, size=args.n)
    B = generate_boxes(args.window_width, args.window_height, size=args.p)

    if args.display:
        draw_boxes(image, A, color=(0, 0, 255))
        draw_boxes(image, B, color=(255, 0, 0))
        cv2.imshow("window", image)
        cv2.waitKey()

    x1, x2, y1, y2 = A
    x3, x4, y3, y4 = B

    if args.engine == "rust":
        function = rust_lib.two_sets_intersection 
    elif args.engine == "numpy":
        function = two_sets_intersection_numpy
    else:
        raise ValueError("engine doesn't exist!")

    t = time.time()
    min_x, max_x, min_y, max_y = function(x1, x2, y1, y2, x3, x4, y3, y4)
    t = time.time()-t

    if args.display:
        cv2.rectangle(image, (min_x, min_y), (max_x, max_y), color=(0,0,0), thickness=-1)
        cv2.imshow("window", image)
        cv2.waitKey() 
    
    return t

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("--engine", type=str, default="numpy", help="current options: rust numpy")
    parser.add_argument("-n", type=int, default=20)
    parser.add_argument("-p", type=int, default=20)
    parser.add_argument("-s", "--seed", type=int, default=None)
    parser.add_argument("-d", "--display", type=bool, default=True)
    parser.add_argument("--window-width", type=int, default=1600)
    parser.add_argument("--window-height", type=int, default=900)
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    print("%0.5f" % main(args))

