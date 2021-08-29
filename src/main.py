import cv2
import time
import numpy as np
import argparse

import generation

import rust_lib
import numpy_lib
import python_lib


def main(args): 
    np.random.seed(args.seed)

    image = np.full((args.window_height, args.window_width, 3), 255, dtype=np.uint8)

    A = generation.generate_boxes(args.window_width, args.window_height, size=args.n)
    B = generation.generate_boxes(args.window_width, args.window_height, size=args.p)

    if args.display:
        generation.draw_boxes(image, A, color=(0, 0, 255))
        generation.draw_boxes(image, B, color=(255, 0, 0))
        cv2.imshow("window", image)
        cv2.waitKey()

    x1, x2, y1, y2 = A
    x3, x4, y3, y4 = B

    if args.engine == "rust-multicore":
        function = rust_lib.two_sets_intersection_multicore
    elif args.engine == "rust":
        function = rust_lib.two_sets_intersection
    elif args.engine == "numpy":
        function = numpy_lib.two_sets_intersection
    elif args.engine == "python":
        function = python_lib.two_sets_intersection
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
    parser.add_argument("--engine", type=str, default="numpy", help="current options: rust-multicore rust numpy python")
    parser.add_argument("-n", type=int, default=20) # red boxes
    parser.add_argument("-p", type=int, default=20) # blue boxes
    parser.add_argument("-s", "--seed", type=int, default=None)
    parser.add_argument('--display', dest='display', default=False, action='store_true')
    parser.add_argument('--no-display', dest='display', action='store_false')
    parser.set_defaults(display=True)
    parser.add_argument("--window-width", type=int, default=1600)
    parser.add_argument("--window-height", type=int, default=900)
    return parser


if __name__ == "__main__":
    args = get_parser().parse_args()
    print("duration: %0.5f" % main(args))

