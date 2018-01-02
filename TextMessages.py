import stitchcode
import csv
import font
from fontTools import ttx
import straight_stitch
import satin_stitch
import fill_stitch

class Vis:
    middle = 100
    spacing = 15
    unit_height = 15
    character_height = 15
    DATE = 1
    TYPE = 2
    LENGTH = 3
    MESSAGE = 4
    CONVO_NUM = 5
    CONVO_TAG = 6
    ANGER = 7
    DISGUST = 8
    FEAR = 9
    JOY = 10
    SADNESS = 11

    def __init__(self):
        self.type = []
        self.length = []
        self.messages = []
        self.convoNum = []
        self.convoTags = []
        self.anger = []
        self.disgust = []
        self.fear = []
        self.joy = []
        self.sadness = []
        self.unknown = []

    def read_file(self):
        f = open("mess6.csv", 'rb')
        reader = csv.reader(f)
        for row in reader:
            self.type.append(row[self.TYPE])
            self.length.append(row[self.LENGTH])
            self.messages.append(row[self.MESSAGE])
            self.convoNum.append(row[self.CONVO_NUM])
            self.convoTags.append(row[self.CONVO_TAG])
            self.anger.append(float(row[self.ANGER]) * float(row[self.LENGTH]))
            self.disgust.append(float(row[self.DISGUST]) * float(row[self.LENGTH]))
            self.fear.append( float(row[self.FEAR]) * float(row[self.LENGTH]))
            self.joy.append(float(row[self.JOY]) * float(row[self.LENGTH]))
            self.sadness.append(float(row[self.SADNESS]) * float(row[self.LENGTH]))
            self.unknown.append(max((1 - float(row[self.ANGER]) - float(row[self.DISGUST]) - float(row[self.FEAR]) - float(row[self.JOY]) - float(row[self.SADNESS])) * float(row[self.LENGTH]),0))
        f.close()

    def draw_section(self, base, new_points):
        line1 = []
        line2 = []
        for i in range(0, len(self.messages)):
            if self.type[i] == 'in':
                x_top = self.middle - (((base[i] + new_points[i]) * self.spacing))
                x_bottom = self.middle - (base[i] * self.spacing)
                y_top = i * self.unit_height
                y_center = (i * self.unit_height) + (self.unit_height / 2)
                line1.extend(straight_stitch.straight_stitch(
                    [stitchcode.Point(self.middle, y_center, False), stitchcode.Point(x_top, y_center, False)], 30))
                line1.extend(
                    satin_stitch.satin_stitch(
                        [stitchcode.Point(x_top, y_top, False), stitchcode.Point(x_bottom, y_top, False)], 6,
                        self.unit_height))
                # satin_stitch(input_points, penetration_distance, width):
                line1.extend(straight_stitch.straight_stitch(
                    [stitchcode.Point(x_bottom, y_center, False), stitchcode.Point(self.middle, y_center, False)], 30))
            else:
                x_top = self.middle + ((base[i] + new_points[i]) * self.spacing)
                x_bottom = self.middle + (base[i] * self.spacing)
                y_top = (i + 1) * self.unit_height
                y_center = (i * self.unit_height) + (self.unit_height / 2)
                line2.extend(straight_stitch.straight_stitch(
                    [stitchcode.Point(self.middle, y_center, False), stitchcode.Point(x_top, y_center, False)], 30))
                line2.extend(
                    satin_stitch.satin_stitch(
                        [stitchcode.Point(x_top, y_top, False), stitchcode.Point(x_bottom, y_top, False)], 6,
                        self.unit_height))
                # satin_stitch(input_points, penetration_distance, width):
                line2.extend(straight_stitch.straight_stitch(
                    [stitchcode.Point(x_bottom, y_center, False), stitchcode.Point(self.middle, y_center, False)], 30))
            base[i] = base[i] + new_points[i]
        return line1, line2, base

    def generate(self):
        graph1 = []
        graph2 = []
        center = []
        base = []
        for i in range(0, len(self.messages)):
            center.append(stitchcode.Point(2000, i*10, False))
            base.append(0)

        unknown1, unknown2, base = self.draw_section(base, self.unknown)
        anger1, anger2, base = self.draw_section(base, self.anger)
        disgust1, disgust2, base = self.draw_section(base, self.disgust)
        fear1, fear2, base = self.draw_section(base, self.fear)
        joy1, joy2, base = self.draw_section(base, self.joy)
        sadness1, sadness2, base = self.draw_section(base, self.sadness)

        graph1.extend(sadness1)
        graph1[-1] .color = 1
        graph2.extend(sadness2)
        graph2[-1].color = 1

        #joy1.reverse()
        graph1.extend(joy1)
        graph1[-1].color = 2
        #joy2.reverse()
        graph2.extend(joy2)
        graph2[-1].color = 2

        graph1.extend(fear1)
        graph1[-1].color = 3
        graph2.extend(fear2)
        graph2[-1].color = 3

        #disgust1.reverse()
        graph1.extend(disgust1)
        graph1[-1].color = 4
        #disgust2.reverse()
        graph2.extend(disgust2)
        graph2[-1].color = 4

        graph1.extend(anger1)
        graph1[-1].color = 5
        graph2.extend(anger2)
        graph2[-1].color = 5

       # unknown1.reverse()
        graph1.extend(unknown1)
        graph1[-1].color = 1
        #unknown2.reverse()
        graph2.extend(unknown2)
        graph2[-1].color = 1

        return graph1, graph2



def write_to_file(emb, name):
    emb.translate_to_origin()
    #emb.scale(1)
    emb.flatten()
    emb.save("Output/" + name + ".exp")
    emb.save("Output/" + name + ".png")

if __name__ == "__main__":
    points = []
    vis = Vis()
    vis.read_file()
    points1, points2 = vis.generate()
    emb1 = stitchcode.Embroidery()
    emb2 = stitchcode.Embroidery()
    for p in points1:
        emb1.addStitch(p)
    for p in points2:
        emb2.addStitch(p)

    write_to_file(emb1, "mes6_in")
    write_to_file(emb2, "mes6_out")

