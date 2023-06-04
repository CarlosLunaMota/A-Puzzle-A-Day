from collections import defaultdict
from pyx import *

### AUXILIARY FUNCTIONS AND DATA STRUCTURES ####################################

def contour(pixels):
    
    # Get all segments:
    
    segments = []
    
    for x,y in pixels:
        if (x-1,y) not in pixels: segments.append(((x,   y),   (x,  y+1)))
        if (x+1,y) not in pixels: segments.append(((x+1, y),   (x+1,y+1)))
        if (x,y-1) not in pixels: segments.append(((x,   y),   (x+1,y  )))
        if (x,y+1) not in pixels: segments.append(((x,   y+1), (x+1,y+1)))
    
    # Remove redundant points:

    points = set([s[0] for s in segments] + [s[1] for s in segments])

    for p in points:
        q,r = [_ for _ in points if (p,_) in segments or (_,p) in segments] 
        if p[0] == q[0] == r[0] or p[1] == q[1] == r[1]:
            if (p,q) in segments: segments.remove((p,q))
            if (q,p) in segments: segments.remove((q,p))
            if (p,r) in segments: segments.remove((p,r))
            if (r,p) in segments: segments.remove((r,p)) 
            segments.append((q,r))
    
    # Get polygon:
    
    q = segments[0][0]
    p, r = [_ for _ in points if (q,_) in segments or (_,q) in segments]
    polygon = [p, q, r]
    while polygon[-1] != polygon[0]:
        q = polygon[-1]
        p, r = [_ for _ in points if (q,_) in segments or (_,q) in segments]
        if p == polygon[-2]: polygon.append(r)
        else:                polygon.append(p)

    return polygon[1:]
    
def draw_low(name, solutions):

    X = 0.1     # Scale
    Y = 1.0     # Width
    R = 15      # Row Length
    
    drawing = []

    drawing = [(path.path(path.moveto(            0,   0),
                          path.lineto(            0, 7*X),
                          path.lineto((R-1)*Y + 7*X, 7*X),
                          path.lineto((R-1)*Y + 7*X,   0),
                          path.closepath()), [color.grey.white])]
    
    for day,pieces in enumerate(solutions):

        r,c = (day//R)*Y, (day%R)*Y, # Row, Column
    
        # PIECES:
        for piece in pieces[:2]:

            STYLE = [deco.filled([color.grey.black])]
            
            poly = contour(piece)

            drawing.append((path.path(path.moveto(poly[0][0]*X+c, poly[0][1]*X-r),
                                      path.lineto(poly[1][0]*X+c, poly[1][1]*X-r),
                                      path.lineto(poly[2][0]*X+c, poly[2][1]*X-r),
                                      path.lineto(poly[3][0]*X+c, poly[3][1]*X-r),
                                      path.closepath()), STYLE))

        for piece in pieces[2:]:

            STYLE = []
            
            poly = contour(piece)

            if len(poly) == 4:
                drawing.append((path.path(path.moveto(poly[0][0]*X+c, poly[0][1]*X-r),
                                          path.lineto(poly[1][0]*X+c, poly[1][1]*X-r),
                                          path.lineto(poly[2][0]*X+c, poly[2][1]*X-r),
                                          path.lineto(poly[3][0]*X+c, poly[3][1]*X-r),
                                          path.closepath()), STYLE))
            
            elif len(poly) == 6:
                drawing.append((path.path(path.moveto(poly[0][0]*X+c, poly[0][1]*X-r),
                                          path.lineto(poly[1][0]*X+c, poly[1][1]*X-r),
                                          path.lineto(poly[2][0]*X+c, poly[2][1]*X-r),
                                          path.lineto(poly[3][0]*X+c, poly[3][1]*X-r),
                                          path.lineto(poly[4][0]*X+c, poly[4][1]*X-r),
                                          path.lineto(poly[5][0]*X+c, poly[5][1]*X-r),
                                          path.closepath()), STYLE))
            
            elif len(poly) == 8:
                drawing.append((path.path(path.moveto(poly[0][0]*X+c, poly[0][1]*X-r),
                                          path.lineto(poly[1][0]*X+c, poly[1][1]*X-r),
                                          path.lineto(poly[2][0]*X+c, poly[2][1]*X-r),
                                          path.lineto(poly[3][0]*X+c, poly[3][1]*X-r),
                                          path.lineto(poly[4][0]*X+c, poly[4][1]*X-r),
                                          path.lineto(poly[5][0]*X+c, poly[5][1]*X-r),
                                          path.lineto(poly[6][0]*X+c, poly[6][1]*X-r),
                                          path.lineto(poly[7][0]*X+c, poly[7][1]*X-r),
                                          path.closepath()), STYLE))
            
            else: print("WRONG POLYGON:", poly)

    # DRAW:
    mycanvas = canvas.canvas()
    for (p, s) in drawing: mycanvas.stroke(p, s)

    mycanvas.writePDFfile("./pic/"+name)


### MAIN FUNCTION ##############################################################

if __name__ == "__main__":

    puzzles = defaultdict(list)
    
    with open("solutions.txt", 'r') as solutions:
        for solution in solutions:
            puzzles[solution[:5]].append(eval(solution[12:]))

    for name in puzzles:
        draw_low(name, puzzles[name])
 
################################################################################
