import stitchcode
import csv
import font
import Words
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
        self.convoNum = []
        self.convoTags = []

    def read_file(self):
        f = open("word6.csv", 'rb')
        reader = csv.reader(f)
        for row in reader:
            self.convoNum.append(row[self.CONVO_NUM])
            self.convoTags.append(row[self.CONVO_TAG])
        f.close()


    def draw_string(self):
        line1 = []
        line2 = []
        i = 0
        while(i < len(self.convoNum)):
            tag_num1 = self.convoNum[i]
            count1 = 0
            y = i * self.spacing * -1
            x = 0
            words = Words.Words()
            while ( i < len(self.convoNum)) and (tag_num1 == self.convoNum[i]):
                count1 = count1 + 1
                i = i + 1
            tag1 = self.convoTags[i-1]

            stitch_width = 10
            count2 = 0
            if i < len(self.convoTags):
                tag_num2 = self.convoNum[i]
                while ( i < len(self.convoNum)) and (tag_num2 == self.convoNum[i]):
                    count2 = count2 + 1
                    i = i + 1
                tag2 = self.convoTags[i - 1]
                count = count1 + count2
                #print "y: {} count: {} tags: {}".format(y, count, tag2)
                # satin_stitch(input_points, penetration_distance, width):
                row_height, pts = words.write_words(tag2, count, "out", x+20, y)
                line2.extend(pts)

            else:
                count = count1 + count2
            # write_words(self, words, unit_height, type, x, y):

            row_height, pts = words.write_words(tag1, count, "in", x-20, y)
            line1.extend(pts)

        return line1, line2

    def generate(self):
        graph1, graph2 = self.draw_string()
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

    write_to_file(emb1, "word_in6")
    write_to_file(emb2, "word_out6")


