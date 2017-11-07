from __future__ import division
import stitchcode
from LineSegment import LineSegment
import straight_stitch
import satin_stitch


def find_intersections(points, x, y, slope):
    intersection_set = []
    line_segments = []
    for i in range(0, len(points) - 1):
        #Find where the given line segment and fill line intersect
        suggested_point = intersection(LineSegment(points[i], points[i + 1]), stitchcode.Point(x, y), slope)
        #If they intersect
        if suggested_point is not None:
            #If they intersect at an edge of a line segment
           ''' if suggested_point == points[i]:
                index = get_surrounding_point_indexes(points, i)
                blah = intersection(LineSegment(points[index[0]], points[index[1]]), stitchcode.Point(x, y), slope)
                if blah is not None:
                    intersection_set.append(suggested_point)
                else:
                    intersection_set.append(suggested_point)
                    intersection_set.append(straight_stitch.copy(suggested_point))'''
           if suggested_point != points[i + 1]:
                intersection_set.append(suggested_point)
    while len(intersection_set) > 1:
        p1, p2 = find_closest_points(intersection_set)
        point1 = intersection_set[p1]
        point2 = intersection_set[p2]
        if (point2.y - point1.y != 0):
            if(abs(abs(((point2.x - point1.x) / (point2.y - point1.y)) - abs(slope))) > 0.01):
                print "???????"
            line_segments.append(LineSegment(intersection_set[p1], intersection_set[p2]))
        if point1.y is point2.y and point1.x is not point2.x:
            print"?"
            #    line_segments.append(LineSegment(intersection_set[p2], intersection_set[p1]))
        intersection_set.pop(p2)
        intersection_set.pop(p1)

    #if len(intersection_set) is 1:
    #    line_segments.append(LineSegment(intersection_set[0], straight_stitch.copy(intersection_set[0])))

    return line_segments


def find_closest_points(points):
    p1 = 0
    p2 = 1
    close_dist = straight_stitch.distance(points[0], points[1])
    for i in range(0, len(points)-1):
        for j in range(i+1, len(points)):
            if p1 is p2:
                return p1, p2
            dist = straight_stitch.distance(points[i], points[j])
            if close_dist > dist:
                close_dist = dist
                p1 = i
                p2 = j
    return p1, p2

def fill_stitch(points, slope, penitration_variance, density, penitration_distance):
    # TODO: Error checking - is a 2D shape(x and y have multiple values)
    # TODO: Error checking - hull algorithm to remove overlap?
    temp = []
    for i in range(0, len(points)-1):
        temp.append(points[i])
        while (i < len(points)-1 and satin_stitch.are_points_too_close(points[i], points[i+1])):
            i = i + 1

    points = temp
    line_segs_sets = [[]]
    start_point, finish_point = find_starting_point(points, slope)
    if slope == 0:
        current = start_point.y
        finish = finish_point.y
    else:
        current = start_point.x
        finish = finish_point.x

    current_y = start_point.y
    current_x = start_point.x

    while current < finish:
        line_segs = find_intersections(points, current_x, current_y, slope)

        for i in range(0, len(line_segs)):
            if len(line_segs_sets) <= i:
                line_segs_sets.append([])
            line_segs_sets[i].append(line_segs[i])

        if slope == 0:
            current_y += density
            current = current_y
        else:
            current_x += density
            current = current_x

    points = []
    top = True
    for set in line_segs_sets:
        for line in set:
            if top:
                p1 = line.p1
                p2 = line.p2
                top = False
            else:
                p1 = line.p2
                p2 = line.p1
                top = True
            points.extend(straight_stitch.line(p1, p2, penitration_distance))
        #points[len(points)-1].jump = True
    return points


def get_surrounding_point_indexes(points, i):
    before = i - 1
    after = i + 1
    if before < 0:
        #The last element is the same as the first, move two back
        before = len(points) - 2
    if after > len(points) - 1:
        after = 0
    return [before, after]


def find_starting_point(points, slope):
    min_x = points[0].x
    min_y = points[0].y
    max_x = points[0].x
    max_y = points[0].y
    for i in range(1, len(points)):
        if points[i].x < min_x:
            min_x = points[i].x
        elif points[i].x > max_x:
            max_x = points[i].x
        if points[i].y < min_y:
            min_y = points[i].y
        elif points[i].y > max_y:
            max_y = points[i].y
    if slope == 0:
        return stitchcode.Point(min_x, min_y), stitchcode.Point(min_x, max_y)
    if slope < 0:
        finish_x = max_x - ((1/slope) * abs(max_y-min_y))
        return stitchcode.Point(min_x, min_y),stitchcode.Point(finish_x, min_y)
    if slope > 0:
        start_x = min_x -((1/slope) * abs(max_y-min_y))
        return stitchcode.Point(start_x, min_y), stitchcode.Point(max_x, min_y)

def get_line_direction(a, b):
    return stitchcode.Point((a.x - b.x),(a.y - b.y))

def intersection(line_segment, point, slope):
    line_seg_direction = get_line_direction(line_segment.p2, line_segment.p1)
    step1 = ((point.x - line_segment.p1.x)*slope)
    step2 = (line_segment.p1.y - point.y) + step1
    step3 = (line_seg_direction.x * slope)
    step4 = (step3 - line_seg_direction.y)
    if step4 != 0:
        t2 = step2/step4
        if (t2 >= 0) and (t2 <= 1):
            # Line intersect at single point
            x = (line_segment.p1.x + (t2 * line_seg_direction.x))
            y = (line_segment.p1.y + (t2 * line_seg_direction.y))
            return stitchcode.Point(x,y)
    else:
        p_direction = get_line_direction(line_segment.p1, point)
        if (p_direction.x == 0) and (p_direction.y == 0):
            # Lines entirely overlap
            return line_segment.p1
        else:
            if straight_stitch.distance(line_segment.p1, point) < straight_stitch.distance(line_segment.p2, point):
                far = line_segment.p2
                near = line_segment.p1
            else:
                far = line_segment.p1
                near = line_segment.p2
            side1 = straight_stitch.distance(far, near) + straight_stitch.distance(near, point)
            side2 = straight_stitch.distance(far, point)
            if abs(side1 - side2) < .0001:
                #Line completely overlaps
                return line_segment.p1
    #Lines do not intersect
    return None