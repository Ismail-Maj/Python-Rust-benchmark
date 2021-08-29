import numpy as np

def two_sets_intersection(x1, x2, y1, y2, x3, x4, y3, y4):

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