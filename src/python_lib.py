def two_sets_intersection(x1, x2, y1, y2, x3, x4, y3, y4):
    # can't multicore because of the GIL
    best = 0
    best_cords = None
    for ex4, ex3, ey4, ey3 in zip(x4, x3, y4, y3):
        for ex1, ex2, ey1, ey2 in zip(x1, x2, y1, y2):
            ex5, ex6 = min(ex2, ex4), max(ex1, ex3)
            ey5, ey6 = min(ey2, ey4), max(ey1, ey3)
            width, height = ex5 - ex6, ey5 - ey6
            if width > 0:
                surface = width * height
                if surface > best:
                    best = surface
                    best_cords = (ex5, ex6, ey5, ey6)
    if best <= 0:
        raise ValueError("empty intersection")

    return best_cords

