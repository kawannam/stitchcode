import stitchcode
import math
import straight_stitch


def single_satin_stitch(point1, point2, width):
    if point1.x < point2.x:
        outside_y = 1
    else:
        outside_y = -1
    if point1.y < point2.y:
        outside_x = -1
    else:
        outside_x = 1
    distance = straight_stitch.distance(point1, point2)
    x = ((((abs(point2.y - point1.y) * width) / distance)*outside_x) + point1.x)
    y = ((((abs(point2.x - point1.x) * width) / distance)*outside_y) + point1.y)
    return stitchcode.Point(x, y, False)


def satin_line(point1, point2, density, width):
    points = []
    line_points = straight_stitch.line(point1, point2, density)
    for i in range(0, len(line_points)-1):
        points.append(line_points[i])
        if (straight_stitch.distance(line_points[i], line_points[i + 1]) != 0):
            points.append(single_satin_stitch(line_points[i], line_points[i + 1], width))
    points.append(line_points[len(line_points)-1])
    return points

def blah (p1, p2, width):
    z = p2.x - p1.x
    w = p2.y - p1.y
    dist = straight_stitch.distance(p1, p2)
    m = (dist + width)/dist
    return stitchcode.Point(p1.x + z*m, p1.y + w*m)

MIN_DISTANCE = 1

def are_points_too_close(point1, point2):
    if abs(point1.x - point2.x) < MIN_DISTANCE and abs(point1.y - point2.y) < MIN_DISTANCE:
        return True
    return False

def satin_corner(point1, point2, point3, penitration_length, width):
    if (are_points_too_close(point1, point2) or
        are_points_too_close(point2, point3) or
            are_points_too_close(point1, point3)):
                return
    p1 = point2
    p2 = single_satin_stitch(point2, blah(point1, point2, width), width)
    p3 = single_satin_stitch(point2, point3, width)
    p12 = straight_stitch.distance(p1, p2)
    p13 = straight_stitch.distance(p1, p3)
    p23 = straight_stitch.distance(p2, p3)
    z1 = p2.x - p1.x
    w1 = p2.y - p1.y
    z2 = p3.x - p1.x
    w2 = p3.y - p1.y
    theta = math.acos(((z1*z2) + (w1*w2))/(math.sqrt(z1**2 + w1**2) * math.sqrt(z2**2 + w2**2)))

    theta2 = math.acos((p12**2 + p13**2 - p23**2)/(2*p12*p13))
    cross = (point2.x - point1.x)*(point3.y - point1.y) - (point2.y - point1.y)*(point3.x - point1.x)
    if (cross > 0 or (abs(theta - math.pi) < 0.001)):
        return []
    sub_division = (width*theta)/penitration_length
    if sub_division == 0:
        return
    partial_angle = (theta/sub_division)
    points = []
    sub_division = int(math.ceil(sub_division))
    for i in range(0, sub_division):
        x = p2.x - p1.x
        y = p2.y - p1.y
        magx = x*math.cos(partial_angle*i + math.pi) + y*math.sin(partial_angle*i + math.pi)
        magy = -1*x*math.sin(partial_angle*i + math.pi) + y*math.cos(partial_angle*i + math.pi)
        points.append(stitchcode.Point(p1.x - magx, p1.y - magy))
        points.append(stitchcode.Point(p1.x - (magx*0.2), p1.y - (magy*0.2)))
    return points


def satin_stitch(input_points, penetration_distance, width):
    output_points = []
    for i in range(0, len(input_points) - 1):
        if not(are_points_too_close(input_points[i], input_points[i+1])):
            output_points.extend(satin_line(input_points[i], input_points[i + 1], penetration_distance, width))
            if i < len(input_points)-2:
                corner = satin_corner(input_points[i], input_points[i+1],  input_points[i + 2], penetration_distance, width)
                if corner == None > 0:
                    output_points.extend(corner)
    if input_points[0] == input_points[len(input_points) - 1] and len(input_points) >= 3:
        corner = satin_corner(input_points[len(input_points) - 2], input_points[0], input_points[1], penetration_distance, width)
        if corner == None > 0:
            output_points.extend(corner)
    return output_points
