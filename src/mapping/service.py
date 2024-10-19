import math


def distance(p1x, p1y, p2x, p2y):
    return math.sqrt(math.pow(p1x - p2x, 2) + math.pow(p1y - p2y, 2))


def meshl(xcount, ycount, overlap):
    meshGrid = []
    for i in range(xcount * ycount):
        meshGrid.append(((i % xcount) + overlap) / (xcount - (1 - 2 * overlap)))
    return meshGrid


def meshr(xcount, ycount, overlap):
    meshGrid = []
    for i in range(xcount * ycount):
        meshGrid.append(
            (math.floor(i / xcount) + overlap) / (ycount - (1 - 2 * overlap))
        )
    return meshGrid
