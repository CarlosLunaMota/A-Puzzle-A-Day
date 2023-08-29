from itertools import combinations, chain
from collections import defaultdict
from pyx import *

### AUXILIARY FUNCTIONS AND DATA STRUCTURES ####################################

def is_connected(pixels):

    # DFS
    stack = [pixels.pop()]
    while stack:
        (x,y) = stack.pop()
        if (x+1,y) in pixels:
            stack.append( (x+1,y))
            pixels.remove((x+1,y))
        if (x,y+1) in pixels:
            stack.append( (x,y+1))
            pixels.remove((x,y+1))
        if (x-1,y) in pixels:
            stack.append( (x-1,y))
            pixels.remove((x-1,y))
        if (x,y-1) in pixels:
            stack.append( (x,y-1))
            pixels.remove((x,y-1))

    return len(pixels) == 0

def symmetries(pieces):

    # Normalize:
    pixels = tuple(chain.from_iterable(pieces))

    min_x = min(x for (x,y) in pixels)
    min_y = min(y for (x,y) in pixels)

    pixels = tuple((x-min_x,y-min_y) for (x,y) in pixels)

    max_x = max(x for (x,y) in pixels)
    max_y = max(y for (x,y) in pixels)

    # Check symmetries:
    v_sym = all((max_x-x,       y) in pixels for (x,y) in pixels)
    h_sym = all((      x, max_y-y) in pixels for (x,y) in pixels)
    d_sym = all((      y,       x) in pixels for (x,y) in pixels)
    D_sym = all((max_x-y, max_y-x) in pixels for (x,y) in pixels)
    r_sym = all((max_x-x, max_y-y) in pixels for (x,y) in pixels)
        
    return (v_sym or h_sym, d_sym or D_sym, r_sym)

def normalize(pieces):

    # Flatten pieces:
    pixels = tuple(chain.from_iterable(pieces))

    # Bounding box:
    min_x = min(x for (x,y) in pixels)
    min_y = min(y for (x,y) in pixels)
    max_x = max(x for (x,y) in pixels)
    max_y = max(y for (x,y) in pixels)

    # Return the best variant:
    return min((tuple(sorted((x-min_x, y-min_y) for (x,y) in pixels)),
                tuple( tuple(sorted((x-min_x, y-min_y) for (x,y) in p)) for p in pieces)),
               (tuple(sorted((x-min_x, max_y-y) for (x,y) in pixels)),
                tuple( tuple(sorted((x-min_x, max_y-y) for (x,y) in p)) for p in pieces)),
               (tuple(sorted((max_x-x, y-min_y) for (x,y) in pixels)),
                tuple( tuple(sorted((max_x-x, y-min_y) for (x,y) in p)) for p in pieces)),
               (tuple(sorted((max_x-x, max_y-y) for (x,y) in pixels)),
                tuple( tuple(sorted((max_x-x, max_y-y) for (x,y) in p)) for p in pieces)),
               (tuple(sorted((y-min_y, x-min_x) for (x,y) in pixels)),
                tuple( tuple(sorted((y-min_y, x-min_x) for (x,y) in p)) for p in pieces)),
               (tuple(sorted((y-min_y, max_x-x) for (x,y) in pixels)),
                tuple( tuple(sorted((y-min_y, max_x-x) for (x,y) in p)) for p in pieces)),
               (tuple(sorted((max_y-y, x-min_x) for (x,y) in pixels)),
                tuple( tuple(sorted((max_y-y, x-min_x) for (x,y) in p)) for p in pieces)),
               (tuple(sorted((max_y-y, max_x-x) for (x,y) in pixels)),
                tuple( tuple(sorted((max_y-y, max_x-x) for (x,y) in p)) for p in pieces)))[1]

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
    
def draw_symmetries(name, pieces, improve=True):

    # Normalize:
    if improve:
        pixels = tuple(chain.from_iterable(pieces))

        min_x = min(x for (x,y) in pixels)
        min_y = min(y for (x,y) in pixels)

        pixels = tuple((x-min_x,y-min_y) for (x,y) in pixels)

        max_x = max(x for (x,y) in pixels)
        max_y = max(y for (x,y) in pixels)

        # Check symmetries:
        v_sym = all((max_x-x,       y) in pixels for (x,y) in pixels)
        h_sym = all((      x, max_y-y) in pixels for (x,y) in pixels)
        d_sym = all((      y,       x) in pixels for (x,y) in pixels)
        D_sym = all((max_x-y, max_y-x) in pixels for (x,y) in pixels)

        if D_sym and not d_sym:
            pieces = tuple(tuple((x,max_y-y) for (x,y) in p) for p in pieces)
        if h_sym and not v_sym:
            pieces = tuple(tuple((y,x) for (x,y) in p) for p in pieces)

    
    # DRAW:
    drawing = []

    BASE  = [style.linecap.round, style.linejoin.round, style.linestyle.solid]
    BASE += [style.linewidth.THick, color.rgbfromhexstring("#000000")]
    BASE += [deco.filled([color.rgbfromhexstring("#CCCCCC")])]
                                      
    for piece in pieces:

        polygon = contour(piece)
        
        if len(polygon) == 4:
            drawing.append((path.path(path.moveto(*polygon[0]),
                                      path.lineto(*polygon[1]),
                                      path.lineto(*polygon[2]),
                                      path.lineto(*polygon[3]),
                                      path.closepath()), BASE))
        
        elif len(polygon) == 6:
            drawing.append((path.path(path.moveto(*polygon[0]),
                                      path.lineto(*polygon[1]),
                                      path.lineto(*polygon[2]),
                                      path.lineto(*polygon[3]),
                                      path.lineto(*polygon[4]),
                                      path.lineto(*polygon[5]),
                                      path.closepath()), BASE))
        
        elif len(polygon) == 8:
            drawing.append((path.path(path.moveto(*polygon[0]),
                                      path.lineto(*polygon[1]),
                                      path.lineto(*polygon[2]),
                                      path.lineto(*polygon[3]),
                                      path.lineto(*polygon[4]),
                                      path.lineto(*polygon[5]),
                                      path.lineto(*polygon[6]),
                                      path.lineto(*polygon[7]),
                                      path.closepath()), BASE))
        
        else: print("WRONG POLYGON:", polygon)

    mycanvas = canvas.canvas()
    for (p, s) in drawing: mycanvas.stroke(p, s)

    mycanvas.writePDFfile("./symmetries/"+name)
    
### MAIN FUNCTION ##############################################################

if __name__ == "__main__":

    # Read Puzzles
    puzzles = []    
    with open("solutions.txt", 'r') as solutions:
        for solution in solutions:
            puzzles.append(tuple(eval(solution[12:])[2:]))

    # Classify symmetric shapes
    min_pieces = 2
    max_pieces = 7
    shapes = defaultdict(set)
    for puzzle in puzzles:
        for num_pieces in range(min_pieces, max_pieces+1):
            for pieces in combinations(puzzle, num_pieces):
                if is_connected(list(chain.from_iterable(pieces))):
                    pieces = normalize(pieces)
                    sym    = symmetries(pieces)
                    if any(sym): shapes[num_pieces, sym].add(pieces)

                
    # Draw symmetric shapes
    for num_pieces, sym in sorted(shapes.keys()):
        print("Sym-{}-{}{}{}-{:04d}".format(num_pieces,
                                            "m" if sym[0] else "",
                                            "d" if sym[1] else "",
                                            "r" if sym[2] else "",
                                            len(shapes[num_pieces, sym])))
        for i, pieces in enumerate(shapes[num_pieces, sym]):
            name = "Sym-{}-{}{}{}-{:04d}".format(num_pieces,
                                                 "m" if sym[0] else "",
                                                 "d" if sym[1] else "",
                                                 "r" if sym[2] else "",
                                                 i)
            draw_symmetries(name, pieces)

################################################################################
