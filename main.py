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
        raise Exception

    return x5[row][column], x6[row][column], y5[row][column], y6[row][column]

def two_sets_intersection_python(x1, x2, y1, y2, x3, x4, y3, y4):
    def matrix_extremum(a, b, max=True):
        ops = operator.lt if max else operator.gt
        res = [[0]*len(a) for _ in range(len(b))]
        for i, e2 in enumerate(b):
            for j, e1 in enumerate(a):
                res[i][j] = e2 if ops(e1, e2) else e1
        return res

    def matrix_minus(m1, m2):
        res = [[0]* len(m1[0]) for _ in range(len(m1))]
        for idx_row, (row1, row2) in enumerate(zip(m1, m2)):
            for idx_col, (e1, e2) in enumerate(zip(row1, row2)):
                res[idx_row][idx_col] = e1 - e2
        return res
    
    x5 = matrix_extremum(x1, x3, max=True)
    x6 = matrix_extremum(x2, x4, max=False)

    y5 = matrix_extremum(y1, y3, max=True)
    y6 = matrix_extremum(y2, y4, max=False)

    width = matrix_minus(x6, x5)
    height = matrix_minus(y6, y5)

    best_val, best_row, best_col = -1, -1, -1

    for idx_row, (row_width, row_height) in enumerate(zip(width, height)):
        for idx_col, (r, h) in enumerate(zip(row_width, row_height)):
            if r > 0:
                area = r*h 
                if area > best_val:
                    best_val = area
                    best_row = idx_row 
                    best_col = idx_col 
    
    if best_val == -1:
        raise Exception

    return x5[best_row][best_col], x6[best_row][best_col], y5[best_row][best_col], y6[best_row][best_col]

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
        function = two_sets_intersection_python

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
    parser.add_argument("--engine", type=str, default="numpy", help="current options: rust numpy python")
    parser.add_argument("-n", type=int, default=20)
    parser.add_argument("-p", type=int, default=20)
    parser.add_argument("-s", "--seed", type=int, default=None)
    parser.add_argument('--display', action='store_true', dest='display')
    parser.add_argument('--no-display', action='store_false', dest='display')
    parser.add_argument("--window-width", type=int, default=1600)
    parser.add_argument("--window-height", type=int, default=900)
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    main(args)

