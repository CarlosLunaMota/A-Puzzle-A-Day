from collections import defaultdict
from pyx import *

# PYX TEXT SETTINGS:
text.set(text.LatexEngine)
text.preamble(r"\usepackage[utf8]{inputenc}")
text.preamble(r"\usepackage[T1]{fontenc}")
text.preamble(r"\usepackage{lmodern}")
text.preamble(r"\renewcommand{\familydefault}{\sfdefault}")

### PROBLEM DATA ###############################################################

TEXT = {(0,6):"Jan",(1,6):"Feb",(2,6):"Mar",(3,6):"Apr",(4,6):"May",(5,6):"Jun",
         (0,5):"Jul",(1,5):"Aug",(2,5):"Sep",(3,5):"Oct",(4,5):"Nov",(5,5):"Dec",
         (0,4):"01",(1,4):"02",(2,4):"03",(3,4):"04",(4,4):"05",(5,4):"06",(6,4):"07",
         (0,3):"08",(1,3):"09",(2,3):"10",(3,3):"11",(4,3):"12",(5,3):"13",(6,3):"14",
         (0,2):"15",(1,2):"16",(2,2):"17",(3,2):"18",(4,2):"19",(5,2):"20",(6,2):"21",
         (0,1):"22",(1,1):"23",(2,1):"24",(3,1):"25",(4,1):"26",(5,1):"27",(6,1):"28",
         (0,0):"29",(1,0):"30",(2,0):"31"}

CELLS = [(0,6),(1,6),(2,6),(3,6),(4,6),(5,6),
         (0,5),(1,5),(2,5),(3,5),(4,5),(5,5),
         (0,4),(1,4),(2,4),(3,4),(4,4),(5,4),(6,4),
         (0,3),(1,3),(2,3),(3,3),(4,3),(5,3),(6,3),
         (0,2),(1,2),(2,2),(3,2),(4,2),(5,2),(6,2),
         (0,1),(1,1),(2,1),(3,1),(4,1),(5,1),(6,1),
         (0,0),(1,0),(2,0)]

PIECES = (((0,0), ),                                  # Month
          ((0,0), ),                                  # Day
          ((0,0), (1,0), (0,1), (1,1), (0,2), (1,2)), # O
          ((0,0), (1,0), (2,0), (0,1), (2,1)),        # U
          ((0,0), (1,0), (2,0), (0,1), (0,2)),        # V
          ((0,0), (1,0), (1,1), (1,2), (2,2)),        # S
          ((0,0), (0,1), (1,1), (0,2), (1,2)),        # P
          ((0,0), (1,0), (2,0), (3,0), (2,1)),        # Y
          ((0,0), (1,0), (2,0), (2,1), (3,1)),        # Z
          ((0,0), (1,0), (0,1), (0,2), (0,3)))        # L

# https://lospec.com/palette-list/dreamscape8
COLOR = (color.rgbfromhexstring("#F4B46D"), # Month Background
         color.rgbfromhexstring("#F4B46D"), # Day Background
         color.rgbfromhexstring("#c9cca1"), # O Background
         color.rgbfromhexstring("#caa05a"), # U Background
         color.rgbfromhexstring("#8b4049"), # V Background
         color.rgbfromhexstring("#543344"), # S Background
         color.rgbfromhexstring("#ae6a47"), # P Background
         color.rgbfromhexstring("#63787d"), # Y Background
         color.rgbfromhexstring("#8ea091"), # Z Background
         color.rgbfromhexstring("#515262"), # L Background
         color.rgbfromhexstring("#BF712B"), # Board Border Background
         color.rgbfromhexstring("#000000"), # Grid Lines
         color.rgbfromhexstring("#000000")) # Text          

### AUXILIARY FUNCTIONS AND DATA STRUCTURES ####################################

def orientations(piece):

    max_x = max(x for (x,y) in piece)
    max_y = max(y for (x,y) in piece)
    return set([tuple(sorted((      x,       y) for (x,y) in piece)),
                tuple(sorted((      x, max_y-y) for (x,y) in piece)),
                tuple(sorted((max_x-x, max_y-y) for (x,y) in piece)),
                tuple(sorted((max_x-x,       y) for (x,y) in piece)),
                tuple(sorted((      y,       x) for (x,y) in piece)),
                tuple(sorted((      y, max_x-x) for (x,y) in piece)),
                tuple(sorted((max_y-y, max_x-x) for (x,y) in piece)),
                tuple(sorted((max_y-y,       x) for (x,y) in piece))])
               
def draw(name, pieces):
    
    drawing = []

    # STYLES:
    BASE  = [style.linecap.round, style.linejoin.round, style.linestyle.solid]
    BASE += [style.linewidth.normal, COLOR[11]]
    BOARD = BASE + [style.linewidth.THIck, deco.filled([COLOR[10]])]
    CELLS = BASE + [style.linewidth.thick, deco.filled([COLOR[0]])]

    # BORDER:
    drawing.append((path.path(path.moveto(-0.5, -0.5),
                              path.lineto(-0.5,  7.5),
                              path.lineto( 6.5,  7.5),
                              path.lineto( 6.5,  5.5),
                              path.lineto( 7.5,  5.5),
                              path.lineto( 7.5, -0.5),
                              path.closepath()), BOARD))
    
    # PIECES:
    for n,piece in enumerate(pieces):
        for x,y in piece:
            drawing.append((path.path(path.moveto(  x,   y),
                                      path.lineto(x+1,   y),
                                      path.lineto(x+1, y+1),
                                      path.lineto(  x, y+1),
                                      path.closepath()),
                                      BASE + [COLOR[n], deco.filled([COLOR[n]])]))

            if (x-1,y) not in piece:
                 drawing.append((path.path(path.moveto(x,  y),
                                           path.lineto(x,y+1)),
                                           BASE + [style.linewidth.Thick]))
            if (x+1,y) not in piece:
                 drawing.append((path.path(path.moveto(x+1,  y),
                                           path.lineto(x+1,y+1)),
                                           BASE + [style.linewidth.Thick]))
            if (x,y-1) not in piece:
                 drawing.append((path.path(path.moveto(  x,y),
                                           path.lineto(x+1,y)),
                                           BASE + [style.linewidth.Thick]))
            if (x,y+1) not in piece:
                 drawing.append((path.path(path.moveto(  x,y+1),
                                           path.lineto(x+1,y+1)),
                                           BASE + [style.linewidth.Thick]))

    # DRAW:
    mycanvas = canvas.canvas()
    for (p, s) in drawing: mycanvas.stroke(p, s)

    # TEXT:
    mycanvas.text(5.1, 0.3, r"\Large A-Puzzle-A-Day", [text.halign.center, text.vshift.mathaxis])

    for piece in pieces[:2]:
        x,y = piece[0][0],piece[0][1]
        mycanvas.text(x+0.5, y+0.4, r"\large "+TEXT[piece[0]], [text.halign.center, text.vshift.mathaxis])

    
    mycanvas.writePDFfile(name)

def search(pieces=list(), cells=CELLS, solutions=defaultdict(int)):

    # We have found a solution
    if len(pieces) >= 10:
        name = TEXT[pieces[0][0]] + TEXT[pieces[1][0]]
        solutions[name] += 1
        print("\t{:03d}".format(solutions[name]))
        with open("solutions.txt", "a+") as output:
            output.write("{}-{:03d} : {}\n".format(name, solutions[name], pieces))
        draw(name+"-{:03d}".format(solutions[name]), pieces)

    # General case:
    elif len(pieces) >= 2:
        for piece in orientations(PIECES[len(pieces)]):
            for (x,y) in CELLS:
                candidate = tuple((x+dx,y+dy) for (dx,dy) in piece)
                if all(cell in cells for cell in candidate):
                    new_cells  = set(c for c in cells if c not in candidate)
                    new_pieces = pieces[:] + [candidate]
                    search(new_pieces, new_cells, solutions)
            
    # First iteration
    else:
        for m in cells:
            if m[1] > 4:
                for d in cells:
                    if d[1] < 5:
                        new_cells  = set(c for c in cells if c!=m and c!=d)
                        new_pieces = [(m,), (d,)]
                        print(TEXT[m] + TEXT[d] + ":")
                        search(new_pieces, new_cells, solutions)

### MAIN FUNCTION ##############################################################

if __name__ == "__main__":

    search()

################################################################################
