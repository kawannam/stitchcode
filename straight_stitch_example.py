import stitchcode
from straight_stitch import straight_stitch

box_side = 100
box_offset = box_side + 30

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
            for l in range(0, (i+1)):
                box = (get_box(j*box_offset, i*box_offset))
                box_points = straight_stitch(box, (j+7)*2)
                points.extend(box_points)
            p1 = stitchcode.Point(box_points[0].x, box_points[0].y, True)
            p2 = stitchcode.Point(box_points[len(box_points)-1].x, box_points[len(box_points)-1].y, True)
            points.append(p2)
        points.append(stitchcode.Point(8*box_offset - 20, i*box_offset, True))
        points.append(stitchcode.Point(8 * box_offset - 20, (i+1) * box_offset, True))

        for j in range(0, 8):
            for l in range(0, (i+2)):
                box = get_box(((7*box_offset) - (j * box_offset)), ((i+1) * box_offset))
                box_points = straight_stitch(box, 25 - (j * 2))
                points.extend(box_points)
            p1 = stitchcode.Point(box_points[0].x, box_points[0].y, True)
            p2 = stitchcode.Point(box_points[len(box_points) - 1].x, box_points[len(box_points) - 1].y, True)
            points.append(p2)
    emb = stitchcode.Embroidery()
    for p in points:
        emb.addStitch(p)
    write_to_file(emb)