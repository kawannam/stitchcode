from __future__ import division
import stitchcode
import LineSegment
import csv
import math


class Fill:

    def __init__(self):
        self.last_point = 0
        self.jump= False
        self.emb = stitchcode.Embroidery()

    def read_files (self, points, slope):
        #assume a shape 0 point and last point are the same
        #assume x and y values both have multiple values
        #run orthoganal algorithm to ensure no overlapping sections
        startPoint, finishPoint = self.findStart(points, slope)
        lineSegs = []
        if slope == 0:
            currentY = startPoint.y
            while currentY <= finishPoint.y:
                intersSet = []
                for i in range(0, len(points)-1):
                    suggestedPoint = self.intersection(points[i], points[i + 1],
                                                        stitchcode.Point(startPoint.x, currentY), slope)
                    if suggestedPoint is not None:
                        if suggestedPoint == points[i]:
                            index = self.getSurroundingPointIndex(points, i)
                            blah = self.intersection(points[index[0]], points[index[1]],
                                                     stitchcode.Point(startPoint.x, currentY), slope)
                            if blah is not None:
                                intersSet.append(suggestedPoint)
                            else:
                                intersSet.append(suggestedPoint)
                                intersSet.append(suggestedPoint)
                        elif suggestedPoint != points[i + 1]:
                            intersSet.append(suggestedPoint)
                for i in range (0, len(intersSet), 2):
                    lineSegs.append(LineSegment.LineSegment(intersSet[i], intersSet[i + 1]))
                currentY += 1
        else:
            currentX = startPoint.x
            while currentX < finishPoint.x:
                intersSet = []
                for i in range(0, len(points)-1):
                    suggestedPoint = self.intersection(points[i], points[i+1], stitchcode.Point(currentX, startPoint.y), slope)
                    if suggestedPoint is not None:
                        if suggestedPoint == points[i]:
                            index = self.getSurroundingPointIndex(points, i)
                            blah = self.intersection(points[index[0]], points[index[1]], stitchcode.Point(currentX, startPoint.y), slope)
                            if blah is not None:
                                intersSet.append(suggestedPoint)
                            else:
                                intersSet.append(suggestedPoint)
                                intersSet.append(suggestedPoint)
                        elif suggestedPoint != points[i+1]:
                            intersSet.append(suggestedPoint)
                for i in range (0, len(intersSet), 2):
                    lineSegs.append(LineSegment.LineSegment(intersSet[i], intersSet[i + 1]))
                currentX += 1
        for line in lineSegs:
            self.emb.addStitch(line.p1)
            self.emb.addStitch(line.p2)

        """for i in range (0, maxX(points)):
            y = x*slope + i;
            for j in range(1, points.lenght):
                does (j-1 to j intersct with (x*slope + i - y) )
                    yes - add to thing
            pair points in thing to make lines
            add line to lines to stitchf

    def sort(lines):
        alter tsp to sort lines"""

    def getSurroundingPointIndex(self, points, i):
        before = i - 1
        after = i + 1
        if before < 0:
            before = len(points) - 2
        if after > len(points) - 1:
            after = 0
        return [before, after]


    def findStart(self, points, slope):
        minX = points[0].x
        minY = points[0].y
        maxX = points[0].x
        maxY = points[0].y
        for i in range(1, len(points)):
            if points[i].x < minX:
                minX = points[i].x
            elif points[i].x > maxX:
                maxX = points[i].x
            if points[i].y < minY:
                minY = points[i].y
            elif points[i].y > maxY:
                maxY = points[i].y
        if slope == 0:
            return stitchcode.Point(minX, minY), stitchcode.Point(minX, maxY)
        if slope < 0:
            finishX = maxX - (slope * (maxY-minY))
            return stitchcode.Point(minX, minY),stitchcode.Point(finishX, minY)
        if slope > 0:
            startX = minX -(slope * (maxY-minY))
            return stitchcode.Point(startX, maxY), stitchcode.Point(maxX, maxY)

    def intersection(self, point1, point2, point3, slope):
        x1 = 1
        y1 = slope
        x2 = point2.x - point1.x
        y2 = point2.y - point1.y
        a = point3.x
        b = point3.y
        c = point1.x
        d = point1.y
        if x1 == 0:
            return None
        else:
            step1 = ((a - c)*y1)/x1
            step2 = (d - b) + step1
            step3 = ((x2 * y1)/x1)
            step4 = (step3 - y2)
            if step4 != 0:
                t2 = step2/step4
                if (t2 >= 0) and (t2 <= 1):
                    x = (point1.x + (t2*x2))
                    y = (point1.y + (t2*y2))
                    return stitchcode.Point(x,y)
            else:
                x3 = point1.x - point3.x
                y3 = point1.y - point3.y
                if (x3 == 0) and (y3 == 0):
                    #return [point1, point2]
                    return point1
                else:
                    if self.distance(point1, point3) < self.distance(point2, point3):
                        far = point2
                        near = point1
                    else:
                        far = point1
                        near = point2
                    side1 = self.distance(far, near) + self.distance(near, point3)
                    side2 = self.distance(far, point3)
                    if abs(side1 - side2) < .0001:
                        #return [point1, point2]
                        return point1
        return None

    def write_to_file(self):
        self.emb.translate_to_origin()
        self.emb.scale(2)
        self.emb.flatten()
        self.emb.save("Output/fillTest1.exp")
        self.emb.save("Output/fillTest.png")
        self.emb.save("Output/fillTest.dst")

    def distance( self, a, b):
        return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

if __name__ == "__main__":
    shape = Fill()
    ps = []
    ps.append(stitchcode.Point(0,0))
    ps.append(stitchcode.Point(10,20))
    ps.append(stitchcode.Point(10,40))
    ps.append(stitchcode.Point(20,40))
    ps.append(stitchcode.Point(20,20))
    ps.append(stitchcode.Point(40,0))
    ps.append(stitchcode.Point(0,0))
    shape.read_files(ps, 0)
    shape.write_to_file()