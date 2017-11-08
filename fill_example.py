import fill_stitch
import stitchcode

def write_to_file(emb):
    emb.translate_to_origin()
    #emb.scale(1)
    emb.flatten()
    emb.save("Output/reTest1.exp")
    emb.save("Output/reTest1.png")
    emb.save("Output/reTest1.dst")

if __name__ == "__main__":
    ps = []
    ps.append(stitchcode.Point(0,0))
    ps.append(stitchcode.Point(0,50))
    ps.append(stitchcode.Point(50,50))
    ps.append(stitchcode.Point(50,0))
    ps.append(stitchcode.Point(0, 0))
    points = fill_stitch.fill_stitch(ps, 1, 3, 5)
    emb = stitchcode.Embroidery()
    for p in points:
        emb.addStitch(p)
    write_to_file(emb)