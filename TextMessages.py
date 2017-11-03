import stitchcode
import csv
from straight_stitch import straight_stitch
from straight_stitch import line
from straight_stitch import copy

class Vis:
    def __init__(self):
        self.type = []
        self.length = []
        self.messages = []
        self.anger = []
        self.disgust = []
        self.fear = []
        self.joy = []
        self.sadness = []
        self.unknown = []

    def read_file(self):
        f = open('Messages.csv', 'rb')
        reader = csv.reader(f)
        for row in reader:
            self.type.append(row[2])
            self.length.append(row[3])
            self.messages.append(row[4])
            self.anger.append(float(row[5]) * float(row[3]))
            self.disgust.append(float(row[6]) * float(row[3]))
            self.fear.append( float(row[7]) * float(row[3]))
            self.joy.append(float(row[8]) * float(row[3]))
            self.sadness.append(float(row[9]) * float(row[3]))
            self.unknown.append((1 - float(row[5]) - float(row[6]) - float(row[7]) - float(row[8]) - float(row[9])) * float(row[3]))
        f.close()

    def draw_section(self, base1, base2, new_points):
        line1 = []
        line2 = []

        line1.append(stitchcode.Point(2000, 0, False))
        line2.append(stitchcode.Point(2000, 0, False))
        for i in range(0, len(self.messages)):
            if self.type[i] == 'in':
                line1.append(stitchcode.Point(2000 - (new_points[i] * 10) - base1[i].x, i * 10, False))
                line2.append(stitchcode.Point(line2[i - 1].x, i * 10, False))
            else:
                line2.append(stitchcode.Point(2000 + (new_points[i] * 10) + base2[i].x, i * 10, False))
                line1.append(stitchcode.Point(line1[i - 1].x, i * 10, False))
        return line1, line2

    def generate(self):
        center = []
        for i in range(0, len(self.messages)):
            center.append(stitchcode.Point(2000, i*10, False))
        anger1, anger2 = self.draw_section(center, center, self.anger)
        disgust1, disgust2 = self.draw_section(anger1, anger2, self.disgust)
        fear1, fear2 = self.draw_section(disgust1, disgust2, self.fear)
        joy1, joy2 = self.draw_section(fear1, fear2, self.joy)
        sadness1, sadness2 = self.draw_section(joy1, joy2, self.sadness)

        center.reverse()
        points.extend(center)

        anger2.reverse()
        points.extend(anger1)
        points.extend(anger2)

        disgust2.reverse()
        points.extend(disgust1)
        points.extend(disgust2)

        fear2.reverse()
        points.extend(fear1)
        points.extend(fear2)

        joy2.reverse()
        points.extend(joy1)
        points.extend(joy2)

        sadness2.reverse()
        points.extend(sadness1)
        points.extend(sadness2)
        return points


def write_to_file(emb):
    emb.translate_to_origin()
    #emb.scale(1)
    emb.flatten()
    emb.save("Output/messages.exp")
    emb.save("Output/messages.png")

if __name__ == "__main__":
    points = []
    vis = Vis()
    vis.read_file()
    points = vis.generate()
    emb = stitchcode.Embroidery()
    for p in points:
        emb.addStitch(p)
    emb.changeColorEXP1()
    points.reverse()
    for p in points:
        emb.addStitch(stitchcode.Point(20, p.y, False))

    write_to_file(emb)
