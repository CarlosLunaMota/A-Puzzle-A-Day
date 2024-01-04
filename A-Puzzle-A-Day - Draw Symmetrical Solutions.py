from collections import defaultdict
from itertools import combinations
from pyx import *

# PYX TEXT SETTINGS:
text.set(text.LatexEngine)
text.preamble(r"\renewcommand{\familydefault}{\sfdefault}")

### PROBLEM DATA ###############################################################

TEXT = {(0,6):"Jan",(1,6):"Feb",(2,6):"Mar",(3,6):"Apr",(4,6):"May",(5,6):"Jun",
        (0,5):"Jul",(1,5):"Aug",(2,5):"Sep",(3,5):"Oct",(4,5):"Nov",(5,5):"Dec",
        (0,4):"01",(1,4):"02",(2,4):"03",(3,4):"04",(4,4):"05",(5,4):"06",(6,4):"07",
        (0,3):"08",(1,3):"09",(2,3):"10",(3,3):"11",(4,3):"12",(5,3):"13",(6,3):"14",
        (0,2):"15",(1,2):"16",(2,2):"17",(3,2):"18",(4,2):"19",(5,2):"20",(6,2):"21",
        (0,1):"22",(1,1):"23",(2,1):"24",(3,1):"25",(4,1):"26",(5,1):"27",(6,1):"28",
        (0,0):"29",(1,0):"30",(2,0):"31"}

BLACK = color.rgbfromhexstring("#000000")
WHITE = color.rgbfromhexstring("#FFFFFF")
GREY  = color.rgbfromhexstring("#AAAAAA")
LIGHT_GREY = color.rgbfromhexstring("#CCCCCC")

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

def draw(name, pieces):
    
    drawing = []

    # STYLES:
    BASE  = [style.linecap.round, style.linejoin.round, style.linestyle.solid]
    BASE += [style.linewidth.THick, BLACK]
    BOARD = BASE + [style.linewidth.THIck, deco.filled([GREY])]
    
    # BORDER:
    drawing.append((path.path(path.moveto(-0.5, -0.5),
                              path.lineto(-0.5,  7.5),
                              path.lineto( 6.5,  7.5),
                              path.lineto( 6.5,  5.5),
                              path.lineto( 7.5,  5.5),
                              path.lineto( 7.5, -0.5),
                              path.closepath()), BOARD))

    for (x,y) in TEXT:
        drawing.append((path.path(path.moveto(x  , y  ),
                                  path.lineto(x+1, y  ),
                                  path.lineto(x+1, y+1),
                                  path.lineto(x,   y+1),
                                  path.closepath()),
                                  BASE + [deco.filled([WHITE])]))
                                      
    # PIECES:
    for n,piece in enumerate(pieces[2:]):

        polygon = contour(piece)
        
        if len(polygon) == 4:
            drawing.append((path.path(path.moveto(*polygon[0]),
                                      path.lineto(*polygon[1]),
                                      path.lineto(*polygon[2]),
                                      path.lineto(*polygon[3]),
                                      path.closepath()),
                                      BASE + [deco.filled([LIGHT_GREY])]))

        
        elif len(polygon) == 6:
            drawing.append((path.path(path.moveto(*polygon[0]),
                                      path.lineto(*polygon[1]),
                                      path.lineto(*polygon[2]),
                                      path.lineto(*polygon[3]),
                                      path.lineto(*polygon[4]),
                                      path.lineto(*polygon[5]),
                                      path.closepath()),
                                      BASE + [deco.filled([LIGHT_GREY])]))
        
        elif len(polygon) == 8:
            drawing.append((path.path(path.moveto(*polygon[0]),
                                      path.lineto(*polygon[1]),
                                      path.lineto(*polygon[2]),
                                      path.lineto(*polygon[3]),
                                      path.lineto(*polygon[4]),
                                      path.lineto(*polygon[5]),
                                      path.lineto(*polygon[6]),
                                      path.lineto(*polygon[7]),
                                      path.closepath()),
                                      BASE + [deco.filled([LIGHT_GREY])]))
        
        else: print("WRONG POLYGON:", polygon)

    # DRAW:
    mycanvas = canvas.canvas()
    for (p, s) in drawing: mycanvas.stroke(p, s)

    # TEXT:
    mycanvas.text(5.1, 0.3, r"\Large A-Puzzle-A-Day", [text.halign.center, text.vshift.mathaxis])

    for piece in pieces[:2]:
        x,y = piece[0][0],piece[0][1]
        mycanvas.text(x+0.5, y+0.4, r"\Large "+TEXT[piece[0]], [text.halign.center, text.vshift.mathaxis])

    mycanvas.writePDFfile("./symmetrical/"+name)

def dist(P, Q):
    return sum(1 for (p,q) in zip(P,Q) if p!=q)

def symmetries(pieces):

    pixels = [pixel for piece in pieces for pixel in piece]

    x_min = min(x for x,y in pixels)
    y_min = min(y for x,y in pixels)

    P = tuple((x-x_min, y-y_min) for x,y in pixels)

    X = max(x for x,y in P)
    Y = max(y for x,y in P)

    
    return (all((X-x,  y) in P for x,y in P),   # Horizontal symmetry
            all((  x,Y-y) in P for x,y in P),   # Vertical   symmetry
            all((X-x,Y-y) in P for x,y in P),   # Central    symmetry
            all((  y,  x) in P for x,y in P),   # Diagonal   symmetry 
            all((Y-y,X-x) in P for x,y in P))   # Diagonal   symmetry

### MAIN FUNCTION ##############################################################

if __name__ == "__main__":

    # Pre-computed for efficiency:
    COMBINATIONS = ((5, 9), (7, 9), (2, 6), (3, 7), (4, 6), (6, 8), (3, 9),
                    (4, 8), (2, 7), (6, 7), (5, 8), (6, 9), (7, 8), (2, 3),
                    (5, 6, 8), (3, 5, 9), (4, 6, 7), (2, 4, 5), (6, 7, 8),
                    (3, 7, 8), (2, 6, 7), (4, 6, 9), (2, 4, 7), (4, 8, 9),
                    (2, 6, 9), (2, 7, 8), (2, 4, 9), (2, 8, 9), (3, 5, 6),
                    (4, 5, 6), (3, 4, 7), (5, 7, 9), (2, 3, 6), (5, 6, 7),
                    (3, 5, 8), (2, 5, 6), (3, 4, 9), (2, 3, 8), (4, 5, 8),
                    (3, 8, 9), (2, 5, 8), (4, 6, 8), (6, 7, 9), (4, 7, 9),
                    (3, 6, 7), (7, 8, 9), (2, 7, 9), (3, 4, 6), (5, 7, 8),
                    (3, 6, 9), (5, 6, 9), (3, 4, 8), (2, 3, 7), (2, 4, 6),
                    (2, 5, 7), (3, 7, 9), (4, 5, 9), (2, 6, 8), (2, 3, 9),
                    (2, 4, 8), (6, 8, 9), (2, 5, 9), (3, 5, 7), (2, 3, 4),
                    (3, 6, 8), (2, 5, 6, 8), (3, 5, 7, 9), (3, 4, 5, 6),
                    (4, 5, 6, 9), (4, 5, 7, 8), (2, 4, 6, 8), (2, 4, 5, 9),
                    (3, 4, 6, 7), (2, 3, 7, 9), (5, 6, 7, 9), (2, 6, 7, 8),
                    (2, 4, 7, 9), (2, 6, 8, 9), (3, 4, 6, 9), (2, 7, 8, 9),
                    (4, 6, 7, 9), (2, 3, 4, 6), (3, 5, 6, 7), (3, 6, 8, 9),
                    (2, 3, 6, 8), (3, 5, 7, 8), (2, 3, 4, 8), (4, 7, 8, 9),
                    (2, 4, 5, 6), (4, 6, 8, 9), (3, 5, 6, 9), (2, 3, 5, 9),
                    (3, 4, 5, 8), (2, 4, 6, 7), (3, 4, 7, 8), (3, 6, 7, 8),
                    (2, 4, 7, 8), (6, 7, 8, 9), (4, 6, 7, 8), (2, 5, 6, 7),
                    (4, 5, 6, 8), (2, 3, 6, 7), (2, 5, 6, 9), (2, 5, 7, 8),
                    (2, 3, 4, 7), (3, 5, 6, 8), (3, 4, 5, 7), (4, 5, 7, 9),
                    (2, 3, 6, 9), (2, 3, 7, 8), (5, 6, 7, 8), (2, 4, 6, 9),
                    (2, 3, 8, 9), (5, 6, 8, 9), (3, 4, 5, 9), (2, 4, 8, 9),
                    (3, 4, 6, 8), (4, 5, 8, 9), (2, 6, 7, 9), (3, 4, 7, 9),
                    (2, 3, 5, 6), (3, 6, 7, 9), (5, 7, 8, 9), (3, 7, 8, 9),
                    (4, 5, 6, 7), (3, 4, 8, 9), (3, 5, 6, 8, 9),
                    (2, 3, 5, 7, 9), (5, 6, 7, 8, 9), (2, 5, 7, 8, 9),
                    (2, 5, 6, 8, 9), (2, 3, 4, 5, 6), (3, 6, 7, 8, 9),
                    (3, 4, 5, 6, 8), (2, 4, 5, 7, 8), (2, 3, 4, 5, 8),
                    (3, 5, 6, 7, 8), (2, 3, 6, 8, 9), (4, 5, 6, 7, 8),
                    (2, 3, 4, 8, 9), (2, 5, 6, 7, 8), (4, 5, 6, 8, 9),
                    (2, 3, 5, 6, 7), (2, 4, 6, 7, 8), (2, 4, 5, 6, 7),
                    (2, 4, 6, 8, 9), (2, 3, 5, 6, 9), (2, 3, 5, 7, 8),
                    (2, 3, 4, 6, 7), (2, 4, 7, 8, 9), (2, 4, 5, 6, 9),
                    (3, 4, 5, 7, 9), (3, 4, 5, 6, 7), (2, 4, 5, 8, 9),
                    (2, 3, 6, 7, 9), (3, 4, 6, 8, 9), (3, 5, 6, 7, 9),
                    (2, 3, 4, 7, 9), (4, 6, 7, 8, 9), (4, 5, 6, 7, 9),
                    (2, 6, 7, 8, 9), (2, 3, 7, 8, 9), (2, 5, 6, 7, 9),
                    (2, 4, 6, 7, 9), (3, 4, 7, 8, 9), (2, 4, 5, 6, 8),
                    (2, 3, 4, 5, 7), (3, 4, 5, 7, 8), (3, 4, 5, 8, 9),
                    (2, 4, 5, 7, 9), (2, 3, 6, 7, 8), (2, 3, 4, 7, 8),
                    (2, 3, 5, 6, 8), (3, 4, 5, 6, 8, 9), (2, 4, 6, 7, 8, 9),
                    (2, 3, 5, 6, 7, 8), (2, 4, 5, 6, 7, 8), (2, 3, 4, 5, 6, 7),
                    (2, 3, 4, 5, 7, 8), (2, 3, 4, 5, 6, 9), (2, 3, 4, 6, 7, 8),
                    (2, 3, 4, 6, 8, 9), (3, 4, 6, 7, 8, 9), (2, 3, 4, 5, 6, 8),
                    (3, 4, 5, 6, 7, 8), (2, 3, 4, 7, 8, 9),
                    (2, 3, 5, 6, 7, 8, 9), (2, 3, 4, 5, 7, 8, 9),
                    (2, 3, 4, 5, 6, 7, 8), (2, 4, 5, 6, 7, 8, 9))

    ############################################################################

    day = defaultdict(list)
    
    with open("solutions.txt", 'r') as solutions:
        for solution in solutions:
            pieces = eval(solution[12:])
            day[solution[:5]].append(pieces)

    for name in day:
        best_score = tuple()
        for P in day[name]:
            score = []
            for C in COMBINATIONS:
                sym_C = symmetries([P[c] for c in C])
                if any(sym_C):
                    valid = True
                    for n in range(1,len(C)):
                        for A in combinations(C,n):
                            B = tuple(c for c in C if c not in A)
                            sym_A = symmetries([P[a] for a in A])
                            sym_B = symmetries([P[b] for b in B])
                            V = tuple((a,b) for (a,b,c) in zip(sym_A, sym_B, sym_C) if c)
                            if V and all(a and b for a,b in V): valid = False

                    if valid: score.append(len(C))

            if (len(score) > len(best_score) or
                len(score) == len(best_score) and tuple(sorted(score)) < best_score):
                    best, best_score = P, tuple(sorted(score))

        draw("{}".format(name), best)
        
        i = 0
        for C in COMBINATIONS:
            sym_C = symmetries([best[c] for c in C])
            if any(sym_C):
                valid = True
                for n in range(1,len(C)):
                    for A in combinations(C,n):
                        B = tuple(c for c in C if c not in A)
                        sym_A = symmetries([best[a] for a in A])
                        sym_B = symmetries([best[b] for b in B])
                        V = tuple((a,b) for (a,b,c) in zip(sym_A, sym_B, sym_C) if c)
                        if V and all(a and b for a,b in V): valid = False
                        
                if valid:
                    i += 1
                    draw("{}_{:02d}".format(name,i), best[:2]+[best[c] for c in C])
            
################################################################################
