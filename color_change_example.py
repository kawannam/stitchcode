import stitchcode
from straight_stitch import straight_stitch
from straight_stitch import line
from straight_stitch import copy

def write_to_file(emb):
    emb.translate_to_origin()
    #emb.scale(1)
    emb.flatten()
    emb.save("Output/colorChange.exp")
    emb.save("Output/colorChange.png")


if __name__ == "__main__":
    points = line(stitchcode.Point(0, 0, True), stitchcode.Point(0, 500, True), 20)
    emb = stitchcode.Embroidery()
    print("HERE")
    for p in points:
        emb.addStitch(p)
    emb.changeColorEXP2()
    points.reverse()
    i = 0;
    for p in points:
        emb.addStitch(stitchcode.Point(20, p.y, False, i))
        i = i+1

    write_to_file(emb)
