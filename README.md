# A-Puzzle-A-Day

A computational study of the puzzle **A-Puzzle-A-Day** by [Dragonfjord](https://www.dragonfjord.com/).

In this repository you could find three python scripts:

* **A-Puzzle-A-Day - Find Solutions.py** finds all legal solutions for this puzzles and stores them in the **solutions.txt** file.
* **A-Puzzle-A-Day - Draw Solutions.py** reads **solutions.txt** and draws all legal solutions of any particular day into pdf's files stored in the **pic** folder. Then, the LaTeX file **All A-Puzzle-A-Day Solutions.tex** could be used to compile an hyperlinked pdf with all the solutions.
* **A-Puzzle-A-Day - Draw Puzzles.py** reads **solutions.txt** and then finds and draws all single solution puzzles defined by fixing the rectangular piece. Since this is the only piece that it's not a penomino, you can play with this puzzles by printing any of them and using a set of pentominoes (that we all have at home). The pictures are stored in the **puzzles** folder and they are sized so each square measures 1cm. You can scale the images up or down to fit your particular set of pentominoes.
