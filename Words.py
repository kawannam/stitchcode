import stitchcode
import csv
import font
from fontTools import ttx
import straight_stitch
import satin_stitch
import fill_stitch


class Words:

    def __init__(self):
        self.SECTION_HEIGHT = 15
        self.MAX_WIDTH = 3600

    def greedy_lines(self, words, height):
        tags = words.split("#")
        for i in range(0, len(tags)):
            tags[i] = tags[i].strip()
        tags.sort(key=len)
        rows = []
        i = 0
        added = True
        max_char = self.MAX_WIDTH/(height * 0.87)
        while (len(tags) > 0):
            rows.append([])
            added = False
            for j in range(len(tags)-1, -1, -1):
                temp = tags[j]
                if (len(rows[i]) + len(tags[j]) <= max_char ):
                    rows[i].extend(tags[j])
                    rows[i].append(" ")
                    tags.pop(j)
                    added = True
            if not added:
                return None
            rows[i] = "".join(rows[i]).strip()
            i = i+1
        return rows


    def how_many_lines(self, words, height):
        count = 1
        rows = self.greedy_lines(words, height)
        while (rows is None) or len(rows) > count:
            count = count + 1
            rows = self.greedy_lines(words, ((height*1.1)/count))
        return count, (height / count), rows

    def write_words(self, words, unit_height, type, x, y):
        points = []
        height = 0
        if unit_height <= 2:
            if type == "in":
                points.extend(straight_stitch.straight_stitch(
                    [stitchcode.Point(x, y, False), stitchcode.Point(x - len(words), y, False), stitchcode.Point(x, y, False)], 30))
            else:
                points.extend(straight_stitch.straight_stitch(
                    [stitchcode.Point(x, y, False), stitchcode.Point(x + len(words), y, False),stitchcode.Point(x, y, False)], 30))
            i = 1
        else:
            font_file = "Consolas.ttf"
            my_font = ttx.TTFont(font_file)
            count, height, rows = self.how_many_lines(words, unit_height*self.SECTION_HEIGHT)
            if (unit_height*self.SECTION_HEIGHT/count < self.SECTION_HEIGHT):
                print("ERROR")
            for i in range(0, len(rows)):
                m_y = y - ((height ) * (i))
                points.append(stitchcode.Point(x, m_y, False))
                #print "height: {} row: {}".format(height,rows[i])
                letters, width = font.fill_stitch_string(rows[i], 1462 / (height*0.8), x, m_y, my_font, 1, 10, 100)
                #letters, width =font.satin_stitch_string(rows[i], 1462 / (height), x, m_y, my_font)
                if type == "in":
                    letters = [stitchcode.Point(p.x - width, p.y) for p in letters]
                #(message, size, x_offset, y_offset, font, slope, density, p_distance):
                points.extend(letters)
        return height, points




def write_to_file(emb):
    emb.translate_to_origin()
    #emb.scale(1)
    emb.flatten()
    emb.save("Output/tags.exp")
    emb.save("Output/tags.png")

if __name__ == "__main__":
    font_file = "Consolas.ttf"
    my_font = ttx.TTFont(font_file)

    words = Words()
    points = words.write_words("#Badminton #Cofee #Water #Tea Badeeee #Coffe #Wassr #Teeee", 2, "in", 0, 0)
    #def write_words(self, words, unit_height, type, x, y):
    emb = stitchcode.Embroidery()
    for p in points:
        emb.addStitch(p)

    write_to_file(emb)

