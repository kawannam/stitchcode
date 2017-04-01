import math
import stitchcode

def distance(a, b):
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)


def midway_point(point1, point2, ratio):
    point3 = stitchcode.Point(point1.x, point1.y)
    if (point2.x - point1.x) != 0:
        point3.x = (ratio * (point2.x - point1.x)) + point1.x
    if (point2.y - point1.y) != 0:
        point3.y = (ratio * (point2.y - point1.y)) + point1.y
    return point3


def line(point1, point2, penetration_distance, weight=0):
    dis = distance(point1, point2)
    loop = int(math.floor(dis / penetration_distance))
    points = []
    for i in range(0, loop):
        points.append(midway_point(point1, point2, (i * penetration_distance) / dis))
    for i in range(0, weight):
        points.extend(list(reversed(points)))
       # points.extend(list(points))
    return points


def straight_stitch(input_points, penetration_distance, weight=0):
    output_points = []
    for i in range(0, len(input_points)-1):
        output_points.extend(line(input_points[i], input_points[i + 1], penetration_distance, weight))

     output_points.append(input_points[len(input_points)-1])
    return output_points
