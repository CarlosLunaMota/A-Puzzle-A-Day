# A-Puzzle-A-Day

A computational study of the puzzle **A-Puzzle-A-Day** by [Dragonfjord](https://www.dragonfjord.com/).

In this repository you could find five python scripts:

* **A-Puzzle-A-Day - Find Solutions.py** finds all legal solutions for this puzzles and stores them in the **solutions.txt** file.

* **A-Puzzle-A-Day - Draw Solutions.py** reads **solutions.txt** and draws all legal solutions of any particular day into pdf's files stored in the **solutions** folder. Then, the LaTeX file **All A-Puzzle-A-Day Solutions.tex** could be used to compile an hyperlinked pdf with all the solutions. For example, for Feb 31st you fill find:

 <p align=center> <img src="/pic/Solution%20Example%20-%20Feb31.png" height="200"></p>

* **A-Puzzle-A-Day - Draw Puzzles.py** reads **solutions.txt** and then finds and draws all single solution puzzles defined by fixing the rectangular piece. Since this is the only piece that it's not a penomino, you can play with this puzzles by printing any of them and using the set of pentominoes that we all have at home. The pictures are stored in the **puzzles** folder and they are sized so each square measures 1 cm. Finally, the LaTeX file **A-Puzzle-A-Day Single-Solution Puzzless.tex** could be used to compile an hyperlinked pdf with all of the puzzles. For example, for Feb 31st you fill find:

<p align=center> <img src="/pic/Puzzle%20Example%20-%20Feb31.png" height="200"></p>

* **A-Puzzle-A-Day - Draw Symmetrical Solutions.py** reads **solutions.txt** and then finds the ones with the most subsets of pieces that have some kind of symmetry. The pictures are stored in the **symmetrical** folder and the LaTeX file **A-Puzzle-A-Day Symmetrical Solutions.tex** could be used to compile an hyperlinked pdf with these curated solutions. For example, for Feb 31st you fill find:

<p align=center> <img src="/pic/Symmetrical%20Example%20-%20Feb31.png" height="200"></p>

* **A-Puzzle-A-Day - Symmetries.py** reads **solutions.txt**, finds all subsets of pieces that exhibit some kind of symmetry and stores them in the **symmetries** folder.
