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
    for parts in contours:
        xy = (glyph.decomposeOutline(parts))
        for p in xy:
            new_point = stitchcode.Point(x_offset + (p[0] / size), y_offset + (p[1] / size), False)
            if len(points) is 0 or straight_stitch.distance(points[-1], new_point) > 2:
                points.append(new_point)
        if len(points) is not 0:
            points[len(points)-1].jump = True
            coord.append(points)
            points = []
    if len(points) is not 0:
        points[len(points) - 1].jump = True
        coord.append(points)
    return coord

def scale_font(points) :
    last_point = points[-1]
    for i in range(len(points)-1, 1, -1):
        if abs(last_point - points[i]) < 3:
            points.pop(i)
        else:
            last_point = points[i]
    return points

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


def straight_stitch_string(message, size, x_offset, y_offset, font):
    char_list = list(message)
    points = []
    taken = 0
    for character in char_list:
        points.extend(straight_stitch_char(character, size, x_offset + taken, y_offset, font))
        try:
            taken = taken + (glyphquery.width(font, character)/size)
        except:
            taken = taken + 30

    return points


def satin_stitch_string(message, size, x_offset, y_offset, font):
    char_list = list(message)
    i = 0
    points = []
    taken = 0
    char_size = 50
    for character in char_list:
        if (character == ' '):
            taken = taken + char_size
        else:
            points.extend(satin_stitch_char(character, size, x_offset + taken, y_offset, font))
            try:
                char_size = (glyphquery.width(font, character) / size)
                taken = taken + char_size
            except:
                taken = taken + char_size

    return points, taken

def fill_stitch_string(message, size, x_offset, y_offset, font, slope, density, p_distance):
    char_list = list(message)
    points = []
    taken = 0
    char_size = 50
    for character in char_list:
        if (character == ' '):
            taken = taken + char_size
        else:
            points.extend(fill_stitch_char(character, size, x_offset + taken, y_offset, font, slope, density, p_distance))
            try:
                char_size = (glyphquery.width(font, character)/size)
                taken = taken + char_size

            except:
                taken = taken + char_size

    return points, taken

def fill_stitch_char(character, size, x_offset, y_offset, font, slope, density, p_distance):
    coord = get_char(character, size, x_offset, y_offset, font)
    flatten = []
    for co in coord:
        flatten.extend(co)
#    flatten.reverse()
#    flatten = coord[0]
    #flatten.pop(-1)
    #flatten.extend(coord[1])
    return fill_stitch.fill_stitch(flatten, slope, 10, density, p_distance)
#fill_stitch(points, slope, penitration_variance, density, penitration_distance):

def get_string_width(message, size):
    taken = 0
    char_size = 50
    char_list = list(message)
    for character in char_list:
        try:
            char_size = (glyphquery.width(font, character) / size)
            taken = taken + char_size

        except:
            taken = taken + char_size
    return taken




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


def write_to_file(emb, file_name):
    emb.translate_to_origin()
    #emb.scale(1)
    emb.flatten()
    emb.save("Output/" + file_name + ".exp")
    emb.save("Output/" + file_name + ".png")

if __name__ == "__main__":
    points = []
    font_file = "open-sans/OpenSans-Regular.ttf"
    font = ttx.TTFont(font_file)
    #points = satin_stitch_string("I love you", 30, 0, 0, font)
    points, w = fill_stitch_string("RB", 1, 0, 0, font, 1, 10, 10)

    emb = stitchcode.Embroidery()
    for p in points:
        emb.addStitch(straight_stitch.copy(p))
    write_to_file(emb, "r")


def debug():
    debug = []
    blah = []
    for section in points:
        for p in section:
            blah.append(p)
            debug.append(list(blah))

    count = 0
    for section in debug:
        emb = stitchcode.Embroidery()
        for p in section:
            emb.addStitch(straight_stitch.copy(p))
        write_to_file(emb, "A" + str(count))
        count = count + 1