import stitchcode
import csv
import font_example
from fontTools import ttx
import straight_stitch
import satin_stitch
import fill_stitch

class Vis:
    middle = 100
    spacing = 100
    unit_height = 15
    character_height = 40

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

    def draw_section(self, base, new_points):
        line1 = []
        line2 = []
        bar1 = []
        bar2 = []
        for i in range(0, len(self.messages)):
            if self.type[i] == 'in':
                top = self.middle - ((base[i] + new_points[i]) * self.unit_height )
                bottom = self.middle - (base[i] * self.unit_height )
                line1.append(stitchcode.Point(bottom, ((i) * self.spacing), False))
                line1.append(stitchcode.Point(top, (i * self.spacing), False))
                line1.append(stitchcode.Point(top, ((i+1) * self.spacing), False))
                line1.append(stitchcode.Point(bottom, ((i+1) * self.spacing), False))
                line1.append(stitchcode.Point(bottom, ((i) * self.spacing), False))
                bar1.extend(fill_stitch.fill_stitch(line1, 1, 1, 5, 20))
                line1 = []
            else:
                top = self.middle + ((base[i] + new_points[i]) * self.unit_height)
                bottom = self.middle + (base[i] * self.unit_height)
                line2.append(stitchcode.Point(bottom, ((i) * self.spacing), False))
                line2.append(stitchcode.Point(top, (i * self.spacing), False))
                line2.append(stitchcode.Point(top, ((i+1) * self.spacing), False))
                line2.append(stitchcode.Point(bottom, ((i+1 ) * self.spacing), False))
                line2.append(stitchcode.Point(bottom, ((i) * self.spacing), False))
                bar2.extend(fill_stitch.fill_stitch(line2, 1, 1, 5, 20))
                line2 = []
        return bar1, bar2

    def draw_string(self, base1, base2, new_points):
        line1 = []
        line2 = []
        font_file = "open-sans/OpenSans-Light.ttf"
        font = ttx.TTFont(font_file)
        for i in range(0, len(self.messages)):
            if self.type[i] == 'in':
                letter = font_example.satin_stitch_string(self.messages[i], 30, (self.middle - 20 - (len(self.messages[i]) * (self.unit_height + self.character_height))), (i + 0.25) * self.spacing, font)
                line1.extend(letter)
            else:
                letter = font_example.satin_stitch_string(self.messages[i], 30, (base2[i].x + 20 + (len(self.messages[i]) * (self.unit_height ))), (i + 0.25) * self.spacing, font)
                line2.extend(letter)
        return line1, line2

    def generate(self):
        graph = []
        center = []
        base = []
        for i in range(0, len(self.messages)):
            center.append(stitchcode.Point(2000, i*10, False))
            base.append(0)

        anger1, anger2 = self.draw_section(base, self.anger)
        disgust1, disgust2 = self.draw_section(self.anger, self.disgust)
        fear1, fear2 = self.draw_section(self.disgust, self.fear)
        joy1, joy2 = self.draw_section(self.fear, self.joy)
        sadness1, sadness2 = self.draw_section(self.joy, self.sadness)
        unknown1, unknown2 = self.draw_section(self.sadness, self.unknown)

        words1, words2 = self.draw_string(unknown1, unknown2, self.messages)


        #graph.extend(center)

        #graph.extend(anger1)
        #anger1.extend(list(center))
        #anger1.append(straight_stitch.copy(anger1[len(anger1)-1]))

        #anger2.append(straight_stitch.copy(anger2[0]))
        #graph.extend(fill_stitch.fill_stitch(anger1, 1, 1, 5, 20))
        graph.extend(anger1)
        graph.extend(anger2)
        graph[len(graph)-1].color = 1

        graph.extend(disgust1)
        graph.extend(disgust2)
        graph[len(graph) - 1].color = 0

        graph.extend(fear1)
        graph.extend(fear2)
        graph[len(graph) - 1].color = 1

        graph.extend(joy1)
        graph.extend(joy2)
        graph[len(graph) - 1].color = 0

        graph.extend(sadness1)
        graph.extend(sadness2)
        graph[len(graph) - 1].color = 1

        graph.extend(unknown1)
        graph.extend(unknown2)
        graph[len(graph) - 1].color = 0

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
