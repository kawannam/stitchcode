import stitchcode
def write_to_file(emb):
    emb.translate_to_origin()
    emb.save("Output/SizeExample.exp")
    emb.save("Output/SizeExample.ksm")
    emb.save("Output/SizeExample.png")
    emb.save("Output/SizeExample.dst")



if __name__ == "__main__":
    points = []
    points.append(stitchcode.Point(0, 0, False))
    points.append(stitchcode.Point(10, 0, False))
    emb = stitchcode.Embroidery()
    for p in points:
        emb.addStitch(p)
    write_to_file(emb)
