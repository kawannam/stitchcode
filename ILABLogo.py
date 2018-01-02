import math
import stitchcode
from fill_stitch import fill_stitch
from straight_stitch import copy


class ILABLogo:

    def __init__(self):
        self.shapes = [[(0, 0), (0, 9), (3, 9), (3, 0), (0, 0)], # bottom of i
                       [(0, 10), (0, 13), (3, 13), (3, 10), (0, 10)], # top dot on i
                       [(2, 0), (2, 13), (5, 13), (5, 3), (8, 3), (8, 0), (2, 0)], # L
                       [(3, 0), (8, 9), (14, 0), (3, 0)], # A
                       [(10, 0), (10, 13), (13, 13), (13, 0), (10, 0)]] # stick of b

        self.shapes.append(self.get_circle((15, 4), 4))

    def get_circle(self, center, r):
        circle = []
        theta = 0
        res = math.pi / 50
        while theta < 2*math.pi:
            circle.append((center[0] + r*math.cos(theta), center[1] + r*math.sin(theta)))
            theta += res
        circle.append(circle[0])
        return circle


def write_to_file(emb, file_name):
    emb.translate_to_origin()
    # emb.scale(1)
    emb.flatten()
    emb.save("Output/" + file_name + ".exp")
    emb.save("Output/" + file_name + ".png")


if __name__ == "__main__":
    logo = ILABLogo()
    count = 0
    stitchpoints = []
    shape = []
    for i in logo.shapes:
        for j in i:
            shape.append(stitchcode.Point(j[0]*30, j[1]*30))
        stitchpoints.extend(fill_stitch(shape, 1, 1, 2, 100))
        shape = []
        stitchpoints[-1].color = count
        count = count + 1

    emb = stitchcode.Embroidery()

    for p in stitchpoints:
        emb.addStitch(copy(p))
    write_to_file(emb, "ilab")



