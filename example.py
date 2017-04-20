import stitchcode

box_side = 100
box_offset = box_side + 30

def get_box(x, y):
    p1 = stitchcode.Point(x,y)
    p2 = stitchcode.Point(x, y + box_side)
    p3 = stitchcode.Point(x+box_side, y + box_side)
    p4 = stitchcode.Point(x + box_side, y)
    p5 = stitchcode.Point(x,y)
    return [p1, p2, p3, p4, p5]


