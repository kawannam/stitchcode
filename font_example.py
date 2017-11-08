from fontTools import ttx
from ttfquery import glyph, glyphquery
import stitchcode
import straight_stitch
import satin_stitch
import fill_stitch

def get_char(character, size, x_offset, y_offset, font):
    g = glyph.Glyph(glyphquery.glyphName(font, character))
    contours = g.calculateContours(font)
    seen = set()
    coord = []
    points = []
    for letter in contours:
        xy = (glyph.decomposeOutline(letter))
        for p in xy:
            new_point = stitchcode.Point(x_offset + (p[0] / size), y_offset + (p[1] / size), False)
            points.append(new_point)
        if len(points) is not 0:
            points[len(points)-1].jump = True
            coord.append(points)
            points = []
    if len(points) is not 0:
        points[len(points) - 1].jump = True
        coord.append(points)
    return coord

def straight_stitch_char(character, size, x_offset, y_offset, font):
    coord = get_char(character, size, x_offset, y_offset, font)
    letter = []
    for co in coord:
        letter.extend(straight_stitch.straight_stitch(co, 10))
    return letter

def satin_stitch_char(character, size, x_offset, y_offset, font):
    coord = get_char(character, size, x_offset, y_offset, font)
    letter = []
    for co in coord:
        co.reverse()
        letter.extend(satin_stitch.satin_stitch(co, 8, 8))
    return letter

def fill_stitch_char(character, size, x_offset, y_offset, font):
    coord = get_char(character, size, x_offset, y_offset, font)
    flatten = []
    for co in coord:
        flatten.extend(co)
    flatten.reverse()
    flatten = coord[0]
    flatten.pop(len(flatten)-1)
    return fill_stitch.fill_stitch(flatten, 1, 10, 5, 40)

def satin_stitch_string(message, size, x_offset, y_offset, font):
    char_list = list(message)
    i = 0
    points = []
    taken = 0
    for character in char_list:
        points.extend(satin_stitch_char(character, size, x_offset + taken, y_offset, font))
        try:
            taken = taken + (glyphquery.width(font, character)/size)
        except:
            taken = taken + 50

    return points


def getFont(charater, size, x_offset, y_offset):
    font_file = "open-sans/OpenSans-Light.ttf"
    font = ttx.TTFont(font_file)
    g = glyph.Glyph(glyphquery.glyphName(font, charater))
    contours = g.calculateContours(font)
    points = []
    for letter in contours:
        xy = (glyph.decomposeOutline(letter))
        for p in xy:
            points.append(stitchcode.Point(x_offset +(p[0]/size), y_offset + (p[1]/size), False))
    return points


def write_to_file(emb):
    emb.translate_to_origin()
    #emb.scale(1)
    emb.flatten()
    emb.save("Output/words.exp")
    emb.save("Output/words.png")

if __name__ == "__main__":
    points = []
    font_file = "open-sans/OpenSans-Light.ttf"
    font = ttx.TTFont(font_file)
    points = satin_stitch_string("I love you", 30, 0, 0, font)
    emb = stitchcode.Embroidery()
    for p in points:
        emb.addStitch(p)

    write_to_file(emb)

