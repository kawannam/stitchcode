import math
from copy import copy
import stitchcode
from fill_stitch import fill_stitch

class Potato:
    SQUARE = 0
    STAR = 1

    def __init__(self, shape):
        resolution = 2 * math.pi / 100
        self.circle = self.gen_circle(resolution)
        self.body = self.gen_body()
        self.spots = self.gen_spots()
        self.shape = self.gen_shape(shape)

        inlaid = copy(self.shape)
        self.circle.extend(inlaid)
        self.circle.append(self.circle[0])

    def gen_circle(self, res):
        circ = []
        theta = 0
        while theta < 2 * math.pi:
            circ.append((math.cos(theta), math.sin(theta)))
            theta += res

        #circ.append(circ[0])
        return circ

    def gen_body(self):
        body = []
        start_rot = -math.pi / 8
        end_rot = 7*math.pi / 8
        res = math.pi / 50
        theta = start_rot
        while theta <= end_rot:
            body.append((math.cos(theta), math.sin(theta)))
            theta += res

        body.extend([(-0.94, 0.35), (-0.75, 0.89), (-0.69, 1.19),
            (-0.5, 1.5), (-0.32, 1.67), (-0.08, 1.79),
            (0.38, 2.16), (0.63, 2.3), (0.83, 2.32), (1.07, 2.37),
            (1.21, 2.32), (1.38, 2.29), (1.59, 2.15), (1.72, 1.98),
            (1.82, 1.82), (1.93, 1.71), (2, 1.5), (1.97, 1.34),
            (1.87, 1.15), (1.75, 0.97), (1.68, 0.81), (1.49, 0.7),
            (1.39, 0.54), (1.32, 0.39), (1.26, 0.24), (1.18, 0.07),
            (1.13, -0.09)])
        body.append(body[0])
        return body

    def gen_spots(self):
        spots = [[(0.71, 2.03), (0.84, 2.03), (0.92, 1.91), (1.71, 2.03)],
                [(1, 1.24), (1.24, 1.29), (1.42, 1.28), (1.48, 1.14), (1.23, 1.14), (1, 1.24)],
                [(0.05, 1.38), (0.25, 1.51), (0.44, 1.42), (0.26, 1.37), (0.05, 1.38)],
                [(0.94, 0.84), (1.08, 0.8), (1.05, 0.65), (0.94, 0.84)]]
        return spots

    def gen_shape(self, shape):
        if shape == Potato.SQUARE:
            return [(0.4, 0.4), (-0.4, 0.4), (-0.4, -0.4), (0.4, -0.4), (0.4, 0.4)]
        elif shape == Potato.STAR:
            pent1 = [(0.5, 0.5), (0, 0.8), (-0.5, 0.5), (-0.3, -0.5), (0.3, -0.5)]
            pent2 = [(a, -b) for (a, b) in pent1]
            star = []
            for i in range(len(pent1)):
                star.extend([pent1[i], pent2[len(pent2) - i - 1]])
            star.append(star[0])
            return star


def write_to_file(emb, file_name):
    emb.translate_to_origin()
    # emb.scale(1)
    emb.flatten()
    emb.save("Output/" + file_name + ".exp")
    emb.save("Output/" + file_name + ".png")


if __name__ == "__main__":
    potato = Potato(Potato.SQUARE)
    stitchpoints = []
    scale = 60

    stitchpoints.extend(fill_stitch([stitchcode.Point(x*scale,y*scale) for (x, y) in potato.circle], 1, 1, 2, 100))
    stitchpoints[-1].color = 1
    stitchpoints.extend(fill_stitch([stitchcode.Point(x*scale,y*scale) for (x, y) in potato.body], 1, 1, 2, 100))
    stitchpoints[-1].color = 2
    stitchpoints.extend(fill_stitch([stitchcode.Point(x*scale,y*scale) for (x, y) in potato.shape], 1, 1, 2, 100))
    stitchpoints[-1].color = 3
    it = 4
    for spot in potato.spots:
        stitchpoints.extend(fill_stitch([stitchcode.Point(x*scale,y*scale) for (x, y) in spot], 1, 1, 2, 100))
        stitchpoints[-1].color = it
        it += 1

    emb = stitchcode.Embroidery()

    for p in stitchpoints:
        emb.addStitch(copy(p))
    write_to_file(emb, "potato")