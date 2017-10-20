import stitchcode
from fill_stitch import fill_stitch

box_side = 100
box_offset = box_side + 40


def get_box(x, y):
    p1 = stitchcode.Point(x,y)
    p2 = stitchcode.Point(x, y + box_side)
    p3 = stitchcode.Point(x+box_side, y + box_side)
    p4 = stitchcode.Point(x + box_side, y)
    p5 = stitchcode.Point(x,y)
    return [p1, p2, p3, p4, p5]


def write_to_file(emb):
    emb.translate_to_origin()
    #emb.scale(1)
    emb.flatten()
    emb.save("Output/FillExample.exp")
    emb.save("Output/FillExample.png")
    emb.save("Output/FillExample.dst")


if __name__ == "__main__":
    points = []
    for i in range(0, 8, 2):
        for j in range(0, 8):
            box_points = []
            box = (get_box(j*box_offset, i*box_offset))
            box_points = fill_stitch(box, 1, j+3, (i*5) + 10)
            p1a = stitchcode.Point(box[0].x, box[0].y)
            points.append(p1a)
            p1b = stitchcode.Point(box[1].x, box[1].y)
            points.append(p1b)
            points.extend(box_points)
            points.append(stitchcode.Point(box[3].x, box[3].y))
        points.append(stitchcode.Point(8 * box_offset - 40, i*box_offset))
        points.append(stitchcode.Point(8 * box_offset - 40, (i+1) * box_offset))

        for j in range(0, 8):
            box = get_box(((7*box_offset) - (j * box_offset)), ((i+1) * box_offset))
            box_points = fill_stitch(box, 1, 10 - j, (i*5) + 10)
            p1a = stitchcode.Point(box[0].x, box[0].y)
            points.append(p1a)
            p1b = stitchcode.Point(box[1].x, box[1].y)
            points.append(p1b)
            points.extend(box_points)
            points.append(stitchcode.Point(box[3].x, box[3].y))
            points.append(stitchcode.Point(box[0].x, box[0].y))

    emb = stitchcode.Embroidery()
    for p in points:
        emb.addStitch(p)
    write_to_file(emb)
