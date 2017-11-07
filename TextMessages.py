import stitchcode
import csv
import font_example
from fontTools import ttx
import straight_stitch
import satin_stitch
import fill_stitch

class Vis:
    middle = 2000
    spacing = 200
    unit_height = 50
    character_height = 90

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
        f = open("SampleData.csv", 'rb')
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
            self.unknown.append(max((1 - float(row[5]) - float(row[6]) - float(row[7]) - float(row[8]) - float(row[9])) * float(row[3]),0))
        f.close()

    def draw_section(self, base1, base2, new_points):
        line1 = []
        line2 = []
        line1.append(stitchcode.Point(self.middle, (0 * self.spacing), False))
        line2.append(stitchcode.Point(self.middle, (0 * self.spacing), False))
        for i in range(0, len(self.messages)):
            if self.type[i] == 'in':
                line1.append(stitchcode.Point(self.middle, ((i) * self.spacing), False))
                line1.append(stitchcode.Point(base1[i].x - (new_points[i] * self.unit_height), (i * self.spacing), False))
                line1.append(stitchcode.Point(base1[i].x - (new_points[i] * self.unit_height), ((i+1) * self.spacing), False))
                line1.append(stitchcode.Point(self.middle, ((i+1) * self.spacing), False))
                #line2.append(stitchcode.Point(base2[i].x, i * self.spacing, False))
            else:
                line2.append(stitchcode.Point(self.middle, ((i) * self.spacing), False))
                line2.append(stitchcode.Point(base2[i].x + (new_points[i] * self.unit_height), (i * self.spacing), False))
                line2.append(stitchcode.Point(base2[i].x + (new_points[i] * self.unit_height), ((i+1) * self.spacing), False))
                line2.append(stitchcode.Point(self.middle, ((i+1 ) * self.spacing), False))
                #line1.append(stitchcode.Point(base1[i].x, i * self.spacing, False))
        line1.append(stitchcode.Point(self.middle, (len(self.messages) * self.spacing), False))
        line2.append(stitchcode.Point(self.middle, (len(self.messages) * self.spacing), False))
        return line1, line2

    def draw_string(self, base1, base2, new_points):
        line1 = []
        line2 = []
        font_file = "open-sans/OpenSans-Light.ttf"
        font = ttx.TTFont(font_file)
        for i in range(0, len(self.messages)):
            if self.type[i] == 'in':
                letter = font_example.satin_stitch_string(self.messages[i], 15, (self.middle - 40 - (len(self.messages[i]) * (self.unit_height + self.character_height))), (i + 0.25) * self.spacing, font)
                line1.extend(letter)
            else:
                letter = font_example.satin_stitch_string(self.messages[i], 15, (base2[i].x + 40 + (len(self.messages[i]) * (self.unit_height ))), (i + 0.25) * self.spacing, font)
                line2.extend(letter)
        return line1, line2

    def generate(self):
        graph = []
        center = []
        for i in range(0, len(self.messages)):
            center.append(stitchcode.Point(2000, i*10, False))
        anger1, anger2 = self.draw_section(center, center, self.anger)
        disgust1, disgust2 = self.draw_section(anger1, anger2, self.disgust)
        fear1, fear2 = self.draw_section(disgust1, disgust2, self.fear)
        joy1, joy2 = self.draw_section(fear1, fear2, self.joy)
        sadness1, sadness2 = self.draw_section(joy1, joy2, self.sadness)
        unknown1, unknown2 = self.draw_section(sadness1, sadness2, self.unknown)

        words1, words2 = self.draw_string(sadness1, sadness2, self.messages)


        graph.extend(center)

        #graph.extend(anger1)
        #anger1.extend(list(center))
        anger1.append(stitchcode.Point(self.middle, len(self.messages), False))
        anger2.append(stitchcode.Point(self.middle, len(self.messages), False))
        graph.extend(fill_stitch.fill_stitch(anger1, 1, 1, 5, 20))
        graph.extend(fill_stitch.fill_stitch(anger2, 1, 1, 5, 20))

        #graph.extend(satin_stitch.satin_stitch(anger1, 5, 10))
        #graph.extend(satin_stitch.satin_stitch(anger2, 5, 10))

        #disgust1.reverse()
        #graph.extend(disgust1)
        #graph.extend(disgust2)
        #graph.extend(satin_stitch.satin_stitch(disgust1, 5, 10))
        #graph.extend(satin_stitch.satin_stitch(disgust2, 5, 10))

        #fear1.reverse()
        #graph.extend(fear1)
        #graph.extend(fear2)
        #graph.extend(satin_stitch.satin_stitch(fear1, 5, 10))
        #graph.extend(satin_stitch.satin_stitch(fear2, 5, 10))

        #joy1.reverse()
        #graph.extend(joy1)
        #graph.extend(joy2)
        #graph.extend(satin_stitch.satin_stitch(joy1, 5, 10))
        #graph.extend(satin_stitch.satin_stitch(joy2, 5, 10))

        #sadness1.reverse()
        #graph.extend(sadness1)
        #graph.extend(sadness2)
        #graph.extend(satin_stitch.satin_stitch(sadness1, 5, 10))
        #graph.extend(satin_stitch.satin_stitch(sadness2, 5, 10))

        #unknown1.reverse()
        # graph.extend(unknown1)
        # graph.extend(unknown2)
        #graph.extend(satin_stitch.satin_stitch(unknown1, 5, 10))
        #graph.extend(satin_stitch.satin_stitch(unknown2, 5, 10))

        #words1.reverse()
        graph.extend(words1)
        graph.extend(words2)

        return graph



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

    write_to_file(emb)
