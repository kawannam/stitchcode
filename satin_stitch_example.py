import stitchcode
from satin_stitch import satin_stitch

box_side = 80
box_offset = box_side + 60

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
    emb.save("Output/LineExample.exp")
    emb.save("Output/LineExample.png")
    emb.save("Output/LineExample.dst")



if __name__ == "__main__":
    points = []
    for i in range(0, 8, 2):
        for j in range(0, 8):
            box_points = []
            box = (get_box(j*box_offset, i*box_offset))
            box_points = satin_stitch(box, 3 + j, (i*3) + 10)
            points.extend(box_points)
            p2 = stitchcode.Point(box_points[len(box_points)-1].x, box_points[len(box_points)-1].y, True)
            points.append(p2)
        points.append(stitchcode.Point(8*box_offset - 20, i*box_offset, True))
        points.append(stitchcode.Point(8 * box_offset - 20, (i+1) * box_offset, True))

        for j in range(0, 8):
            box = get_box(((7*box_offset) - (j * box_offset)), ((i+1) * box_offset))
            box_points = satin_stitch(box, 10 - j, (i*3) + 10)
            points.extend(box_points)
            p2 = stitchcode.Point(box_points[len(box_points) - 1].x, box_points[len(box_points) - 1].y, True)
            points.append(p2)
    emb = stitchcode.Embroidery()
    for p in points:
        emb.addStitch(p)
    write_to_file(emb)
