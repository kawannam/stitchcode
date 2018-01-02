from __future__ import division
import stitchcode
from LineSegment import LineSegment
import straight_stitch


def find_intersections(points, x, y, slope):
    intersection_set = []
    line_segments = []
    for i in range(0, len(points) - 1):
        if points[i].jump:
            continue
        suggested_point = intersection(LineSegment(points[i], points[i + 1]), stitchcode.Point(x, y), slope)
        if suggested_point is not None:
            if suggested_point == points[i]:
                index = get_surrounding_point_indexes(points, i)
                is_significant_corner = intersection(LineSegment(points[index[0]], points[index[1]]), stitchcode.Point(x, y), slope)
                if is_significant_corner is not None:
                    intersection_set.append(suggested_point)
                else:
                    intersection_set.append(suggested_point)
                    intersection_set.append(stitchcode.Point(suggested_point.x, suggested_point.y))
            elif suggested_point != points[i + 1]:
                intersection_set.append(suggested_point)
    #for n in range(0, len(intersection_set)-1, 2):
    #    line_segments.append(LineSegment(intersection_set[n], intersection_set[n + 1]))
    while len(intersection_set) > 0:
        p1 = find_closest_points(intersection_set)
        line_segments.append(LineSegment(intersection_set[0], straight_stitch.copy(intersection_set[p1])))
        if (p1 != 0):
            intersection_set.pop(p1)
        intersection_set.pop(0)
    return line_segments

def find_closest_points(points):
    p2 = 1
    if len(points) == 1:
        return 0
    close_dist = straight_stitch.distance(points[0], points[1])
    for j in range(1, len(points)):
        if 0 is not p2:
            dist = straight_stitch.distance(points[0], points[j])
            if close_dist > dist:
                close_dist = dist
                p2 = j
    return p2


def fill_stitch(points, slope, penitration_variance, density, penitration_distance):
    # TODO: Error checking - is a 2D shape(x and y have multiple values)
    # TODO: Error checking - hull algorithm to remove overlap?
    line_segs_sets = [[]]
    start_point, finish_point = find_starting_point(points, slope)
    if slope == 0:
        current = start_point.y
        finish = finish_point.y
    else:
        current = start_point.x
        finish = finish_point.x

    current_y = start_point.y
    current_x = start_point.x - 1000

    while current < finish:
        line_segs = find_intersections(points, current_x, current_y, slope)

        for line in line_segs:
            found = False
            for seg_set in line_segs_sets:
                if len(seg_set) is not 0:
                    if is_along(seg_set[-1], line.p1, density+15) or is_along(seg_set[-1], line.p2, density+15):
                    #if is_along(seg_set[-1], line.p1, density + 15):
                        seg_set.append(line)
                        found = True
                        break
            if not found:
                line_segs_sets.append([])
                line_segs_sets[-1].append(line)


        if slope == 0:
            current_y += density
            current = current_y
        else:
            current_x += density
            current = current_x

    answer = []
    temp = []
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
            answer.extend(straight_stitch.line(p1, p2, penitration_distance))
        if len(answer) is not 0:
            answer[-1].jump = True
            if len(temp) is not 0:
                connection_line = connect(points, temp[-1][-1], answer[0])
                if len(connection_line) is not 0:
                    temp.append(connection_line)
            temp.append(answer)
            answer = []
    fill_points = []
    for item in temp:
        fill_points.extend(item)
    return fill_points

def connect(points, start, stop):
    path = []
    found_start = False
    found_stop = False
    found_start_first =False
    count = 0
    while count < (len(points)*2):
        i = count % (len(points)-1)
        if is_along(LineSegment(points[i], points[i+1]), start, 1):
            found_start = True
            if not found_stop:
                found_start_first = True
        if is_along(LineSegment(points[i], points[i+1]), stop, 1):
            found_stop = True
        if found_start or found_stop:
            path.append(straight_stitch.copy(points[i]))
        if found_start and found_stop:
            break
        count = count + 1
    if not found_start_first:
        path.reverse()
    if found_start and found_stop:
        return path
    return []


def is_along(line_seg, point, tolerance):
    ab = straight_stitch.distance(line_seg.p1, line_seg.p2)
    ap = straight_stitch.distance(line_seg.p1, point)
    pb = straight_stitch.distance(line_seg.p2, point)
    if abs(ap + pb - ab) < tolerance:
        return True
    return False


def get_surrounding_point_indexes(points, i):
    before = i - 1
    after = i + 1
    if before < 0:
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