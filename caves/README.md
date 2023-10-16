# Wumpus World Caves

In case of errors in files, please direct issues to the grader.

To aid in testing the FOL system, the environments have been pre-generated and
selected in such a way to test general functionality and specific interactions.
You will find ten ".cave" files, which are us-ascii encoded text files that can be
opened with any editor that can handle ".txt" files, and are described below.

Files are written as $n \times n$ matrices. The files are written such that the
agent starts in the bottom, left corner. For each ".cave" there is a
corresponding ".png" of the same name visualizing the cave, with the following
legend:
  - White: safe
  - Yellow: gold
  - Black: wall
  - Red: Wumpus
  - Blue: pit

Sensory effects from elements that provide them have already been filled in;
Wumpus is surrounded by "stench", Pit is surrounded by "breeze", and "glimmer"
is on the same cell as "gold". To provide more random caves (with no guarantee
of solvability), there is a generate-cave.py file that can run to randomly
generate more caves. Run 
```
python generate-cave.py --help
```
to get more information about the script (the file should have an appropriate
shebang and executable rights, so if you are running on a bash emulator you can
run `./generate-cave.py --help` instead). To aid with visualizing the data, there 
is a `print-cave.py` file that can be used to create a .png file. Run 
```
python print-cave.py --help
```
to get more details. This file should be usable with outputs from 
`generate-caves.py`.

The File should be read from top to bottom, and from left to right. Notice that
this puts the starting position (index [0,0] in the images) in the top left
corner of the .cave file and the bottom left of the .png file. Each line in the file 
is a different row of the cave. Each entry in the list is a cell in the cave. So, for 
example, if our first row looks like
```
[[safe], [safe, stench], [wumpus]]
```
then it can be read that that the first cell is Safe, the second is Safe with a
Stench tag, and the last cell contains a Wumpus. The first line of the file
should be pulled out and parsed separately as it contains information about the
cave; cave size and number of Wumpus.


Below is a list of the 10 different caves provided. Their name contains the
size and their purpose is described below. 

- 5x5-1.cave (1): Trivial Possible<br>
    This cave is as simple as it gets. The gold is adjacent to the entrance,
    and there are no obstacles. This cave tests if your system can solve the
    simplest problems.
- 5x5-2.cave (2): Trivial Not Possible<br>
    This cave is as simple as it gets for unsolvable problems. The gold is
    hidden in the corner by pits. This cave should be impossible to solve and
    tests if your system has a failure/impossible state.
- 10x10-1.cave (4): Regular solvable<br>
    This cave is not trivial, but a moderately developed agent should be able
    to solve it with 100% accuracy, given it only acts with moves it is
    positive are safe. This cave tests general functionality.
- 10x10-2.cave (4): Bad Start<br>
    This cave is similar to "Regular solvable", with an added Wumpus and two
    Pits near the entrance. The Wumpus should be able to be solved exactly, but
    the Pits will both be a 50/50 guess. Ultimately, the solution should be
    found roughly 25% of the time. This cave tests the systems ability to make
    arbitrary choices with no good information.
- 15x15-2.cave (7): Random - Hard<br>
    This cave was randomly generated with a probability of Walls, Wumpus, and
    Pits generation set to 5%. This cave tests general functionality.
- 15x15-1.cave (10): A Bad Time in Wumpus World<br>
    This cave is very unfair. A solution does exist, but even a completely
    formed rule set cannot solve it with certainty. The cave tests the limit of
    your system.
- 20x20-2.cave (3): Random - Easy<br>
    This cave was randomly generated with a probability of Wumpus and Pits
    generation set to 1% and wall generation set to 10%. This cave tests
    general functionality.
- 20x20-1.cave (9): A Wumpus' World<br>
    This cave only holds Wumpus. Arrow logic is necessary to succeed and there
    is no path to the gold that is void of 'stench' positions. This cave tests
    arrow and Wumpus logic.
- 25x25-2.cave (6): Random - Med<br>
    This cave was randomly generated with a probability of Walls, Wumpus, and
    Pits generation set to 3%. This cave tests general functionality.
- 25x25-1.cave (9): Maze<br>
    This cave only contains Walls. There are multiple paths to the solution and
    various dead-end paths. This cave tests the ability of the system to
    traverse and how/when the system backtracks.

