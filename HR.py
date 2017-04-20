import stitchcode
from straight_stitch import straight_stitch
from fill_stitch import fill_stitch
import math

from satin_stitch import satin_stitch

def write_to_file(emb):
    emb.translate_to_origin()
    emb.save("Output/HRExample.exp")
    emb.save("Output/HRExample.png")
    emb.save("Output/HRExample.dst")

heart_rate = [77, 120, 126, 125, 125, 132, 135, 131, 136, 137, 151, 164, 171, 166, 160, 155, 152, 160, 159, 159, 159, 159, 165, 149, 144, 154, 161, 165, 168, 167, 168, 165, 165, 166, 151, 149, 153, 150, 150, 152, 153, 151, 153, 156, 137, 151, 150]

heartPoints = [(0, 2), (1, 3), (2, 3), (3, 2), (3, 1), (2, -1), (1, -2), (0, -3), (-1, -2), (-2, -1), (-3, 1), (-3, 2), (-2, 3), (-1, 3),
               (0, 2)]
def heart(center, size):
    points= []
    for p in heartPoints:
        points.append(stitchcode.Point(center.x + (p[0] * size), center.y + (p[1] * size)))
    return points;


def copy(p):
    return stitchcode.Point(p.x, p.y)


if __name__ == "__main__":
    points = []
    radius = 200
    center = stitchcode.Point(radius, radius)
    top = stitchcode.Point(radius, radius*2)
    bottom = stitchcode.Point(radius, 0)
    left = stitchcode.Point(0, radius)
    for j in range(radius, 40, -10):
        for i in range(0, 61):
            angle = (2 * math.pi * i)/60
            points.append(stitchcode.Point(center.x + (math.cos(angle)*j), center.y + (math.sin(angle)*j)))
    points.extend(straight_stitch([copy(center), top, copy(center), left, copy(center), bottom, copy(center)], 10, 0))

    data = []
    for i in range(0, len(heart_rate)):
        angle = ((2 * math.pi * i) / 60 - (math.pi/2)) * -1
        data.append(stitchcode.Point(center.x + (math.cos(angle) * heart_rate[i]), center.y + (math.sin(angle) * heart_rate[i])))
    points.extend(satin_stitch(data, 2, 15))

    points.extend(fill_stitch(heart(center, 10), 2, 1, 10))

    emb = stitchcode.Embroidery()
    for p in points:
        emb.addStitch(p)
    write_to_file(emb)
