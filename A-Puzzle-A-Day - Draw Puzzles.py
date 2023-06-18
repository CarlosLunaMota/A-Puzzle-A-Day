from collections import defaultdict
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
GREY  = color.rgbfromhexstring("#CCCCCC")

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
    
def draw_puzzle(name, pieces):
    
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
    for n,piece in enumerate(pieces):

        polygon = contour(piece)
        
        if len(polygon) == 4:
            drawing.append((path.path(path.moveto(*polygon[0]),
                                      path.lineto(*polygon[1]),
                                      path.lineto(*polygon[2]),
                                      path.lineto(*polygon[3]),
                                      path.closepath()),
                                      BASE + [deco.filled([GREY])]))

        
        elif len(polygon) == 6:
            drawing.append((path.path(path.moveto(*polygon[0]),
                                      path.lineto(*polygon[1]),
                                      path.lineto(*polygon[2]),
                                      path.lineto(*polygon[3]),
                                      path.lineto(*polygon[4]),
                                      path.lineto(*polygon[5]),
                                      path.closepath()),
                                      BASE + [deco.filled([GREY])]))
        
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
                                      BASE + [deco.filled([GREY])]))
        
        else: print("WRONG POLYGON:", polygon)

    # DRAW:
    mycanvas = canvas.canvas()
    for (p, s) in drawing: mycanvas.stroke(p, s)

    # TEXT:
    mycanvas.text(5.1, 0.3, r"\Large A-Puzzle-A-Day", [text.halign.center, text.vshift.mathaxis])

    for piece in pieces[:2]:
        x,y = piece[0][0],piece[0][1]
        mycanvas.text(x+0.5, y+0.4, r"\Large "+TEXT[piece[0]], [text.halign.center, text.vshift.mathaxis])

    mycanvas.writePDFfile("./puzzles/"+name)

def draw_pieces():
    
    drawing = []

    # STYLES:
    BASE  = [style.linecap.round, style.linejoin.round, style.linestyle.solid]
    BASE += [style.linewidth.THick, BLACK]

    # L:
    drawing.append((path.path(path.moveto(0,0), path.lineto(2,0),
                              path.lineto(2,1), path.lineto(1,1),
                              path.lineto(1,4), path.lineto(0,4),
                              path.closepath()), BASE))        

    # N:
    drawing.append((path.path(path.moveto(2.5,0.5), path.lineto(3.5,0.5),
                              path.lineto(3.5,2.5), path.lineto(2.5,2.5),
                              path.lineto(2.5,4.5), path.lineto(1.5,4.5),
                              path.lineto(1.5,1.5), path.lineto(2.5,1.5),
                              path.closepath()), BASE))        

    # P:
    drawing.append((path.path(path.moveto(0,4.5), path.lineto(1,4.5),
                              path.lineto(1,5.5), path.lineto(2,5.5),
                              path.lineto(2,7.5), path.lineto(0,7.5),
                              path.closepath()), BASE))

    # U:
    drawing.append((path.path(path.moveto(2.5,5.5), path.lineto(3.5,5.5),
                              path.lineto(3.5,6.5), path.lineto(4.5,6.5),
                              path.lineto(4.5,5.5), path.lineto(5.5,5.5),
                              path.lineto(5.5,7.5), path.lineto(2.5,7.5),
                              path.closepath()), BASE))   

    # V:
    drawing.append((path.path(path.moveto(5,0), path.lineto(8,0),
                              path.lineto(8,3), path.lineto(7,3),
                              path.lineto(7,1), path.lineto(5,1),
                              path.closepath()), BASE))

    # Y:
    drawing.append((path.path(path.moveto(7,3.5), path.lineto(7,5.5),
                              path.lineto(6,5.5), path.lineto(6,6.5),
                              path.lineto(7,6.5), path.lineto(7,7.5),
                              path.lineto(8,7.5), path.lineto(8,3.5),
                              path.closepath()), BASE))  

    # Z:
    drawing.append((path.path(path.moveto(3,4), path.lineto(3,5),
                              path.lineto(5,5), path.lineto(5,3),
                              path.lineto(6,3), path.lineto(6,2),
                              path.lineto(4,2), path.lineto(4,4),
                              path.closepath()), BASE))

    # DRAW:
    mycanvas = canvas.canvas()
    for (p, s) in drawing: mycanvas.stroke(p, s)

    mycanvas.writePDFfile("./pic/pieces")

### MAIN FUNCTION ##############################################################

if __name__ == "__main__":

    draw_pieces()
    
    puzzles = defaultdict(lambda: defaultdict(list))
    
    with open("solutions.txt", 'r') as solutions:
        for solution in solutions:
            pieces = eval(solution[12:])
            assert(tuple(sorted(pieces[2])) == pieces[2])
            puzzles[solution[:5]][pieces[2]].append(pieces[:3])

    for name in puzzles:

        SINGLE = [P for P in puzzles[name].values() if len(P)==1]
        DOUBLE = [P for P in puzzles[name].values() if len(P)==2]

        if SINGLE:
            for i,P in enumerate(SINGLE):
                draw_puzzle(name+"-{:02d}".format(i+1), P[0])
                print(r"        \SPUZZLE{"+name[:3]+"}{"+name[3:]+"}{"+
                      "{:02d}".format(i+1)+"}")
        else:
            for i,P in enumerate(DOUBLE):
                draw_puzzle(name+"-{:02d}".format(i+1), P[0])
                print(r"        \DPUZZLE{"+name[:3]+"}{"+name[3:]+"}{"+
                      "{:02d}".format(i+1)+"}")

################################################################################
