import stitchcode
from straight_stitch import straight_stitch

def write_to_file(emb):
    emb.translate_to_origin()
    #emb.scale(1)
    emb.flatten()
    emb.save("Output/colorChange.exp")
    emb.save("Output/colorChange.png")


if __name__ == "__main__":
    points = []
    line_points = []
    for i in range (0, 100):
        line_points.append(stitchcode.Point(i*10, 10, True))
        line_points.append(stitchcode.Point(i*10, 25, True))
    emb = stitchcode.Embroidery()
    points = straight_stitch(line_points, 5)
    print("HERE")
    for p in points:
	    #stitchcode.changeColorEXP1()
        emb.addStitch(p)
    write_to_file(emb)
