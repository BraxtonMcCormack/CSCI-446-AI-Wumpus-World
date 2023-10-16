#! /bin/python3
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
import sys, getopt

# Set all values you do not with to color to '0'
SAFE = 1
WUMPUS = 2
BREEZE = 0
PIT = 3
STENCH = 0
GOLD = 4
GLIMMER = 0
WALL = 5
CAVE_OBJECTS = [SAFE, WUMPUS, BREEZE, PIT, STENCH, GOLD, GLIMMER, WALL]
CAVE_OBJECTS.sort()

# Define the colors to use. All '0' above should have 'None' here
COLORS = {
    SAFE: 'white',
    WUMPUS: 'red',
    BREEZE: None,
    PIT: 'blue',
    STENCH: None,
    GOLD: 'yellow',
    GLIMMER: None,
    WALL: 'black',
}
# Create the color map for image definition later.
cmap = colors.ListedColormap([COLORS[i] for i in CAVE_OBJECTS if COLORS[i] is not None])

# Define how the cells are defined in the .cave files
transform = {
    "'safe'": SAFE,
    "'wumpus'": WUMPUS,
    "'stench'": STENCH,
    "'pit'": PIT,
    "'breeze'": BREEZE,
    "'gold'": GOLD,
    "'glimmer'": GLIMMER,
    "'wall'": WALL,
}

def reader(file: str) -> np.array:
    """
    Takes a file name and returns an np.array were cells are tagged with integers
    corresponding to the constants defined above.
    :param file: File name.
    :return: numpy array of the cave encoded as defined in the code preamble.
    """
    cave_file = open(file, "r")
    header = cave_file.readline()    # Disregard the preamble line
    # size = [int(i) for i in header.split(",")[0].split(": ")[-1].split("x")]
    cave = []
    for line in cave_file:
        # split each line into cells
        line = [i.strip("[ ]") for i in line.strip("\n [ ]").split("],")]
        line_split = []
        # split the cells and disregard SAFE and another defined '0' above
        for cell in line:
            cell_split = [transform[i] for i in cell.split(", ") if transform[i] not in [SAFE, 0]]
            # set default to SAFE
            line_split.append(SAFE if len(cell_split) == 0 else cell_split[0])
        # add the line to the cave
        cave.append(line_split)
    return np.array(cave)

def print_image(cave: np.array, name:str = None, target: str = None, 
                grid: bool = False, start:bool = False) -> None:
    """
    Plots the cave object using the cmap defined above. See that documentation to change colors.
    :param cave: The array object to plot.
    :param name: The name of the file printed, this is identical to the input name.
    :param target: File name to save to. If none is defined will present the plot.
    :param grid: Whether to show a grid over the graph. Default: False
    """
  
    #Plot the graph
    plt.matshow(cave, cmap=cmap, vmax=CAVE_OBJECTS[-1])

    # Crop the image to just the cave
    plt.xlim((0-0.5, cave.shape[1]-0.5))
    plt.ylim((0-0.5, cave.shape[0]-0.5))

    # Add the grid lines
    if grid:
        plt.vlines(np.arange(cave.shape[1])+ 0.5, ymin=-0.5, ymax=cave.shape[0]+0.5,
                    colors='grey', linestyles='dashed')
        plt.hlines(np.arange(cave.shape[0])+ 0.5, xmin=-0.5, xmax=cave.shape[1]+0.5,
                    colors='grey', linestyles='dashdot')
    
    if start:
        plt.text(0, 0, "start", horizontalalignment='center', verticalalignment='center')    
    plt.title(name)

    plt.tick_params(axis='both', which='major',
               labelsize=10, labelbottom=True,
               bottom=True, top=False, labeltop=False)

    # Save or print
    if target is None:
        plt.show()
    else: 
        plt.savefig(target)


def main(argv):
    """
    Main method for print a Wumpus World cave. For details, run
        python <path-to-this-file>/print-cave.py -h
    or read the documentation below. This function is intended to be run through the command line. 

    Written by: Will Jardee 10/05/2023
    """
    output=None
    grid=False
    # Parse passed options
    opts, args = getopt.getopt(argv,"hc:f:g:s:",["cave=", "file=", "grid=", "start="])
    for opt, arg in opts:
        # help option
        if opt == '-h':
            print("Script for printing .cave files.\n\n" +
                   "Passable arguments:\n" +
                   "    -c, --cave: File to import\n" +
                   "    -f, --file: Output file to save to. Must include the file extension. If none is given, opens new. (default = 5)\n" +
                   "    -g, --grid: Whether to print grid lines. (default = False)\n" +
                   "    -s, --start: Whether to print 'start' at (0,0). (default = False)\n" +
                   "Example usage:\n" +
                   "    python print-cave.py -c '20x20-1.cave' --file test.png -g 'True'\n"
                   )
            sys.exit()

        # parse options
        elif opt in ("-c", "--cave"):
            input_cave = arg
        elif opt in ("-f", "--file"):
            output = arg
        elif opt in ("-g", "--grid"):
            grid = bool(arg)
        elif opt in ("-s", "--start"):
            start = bool(arg)

    print(f"reading {input_cave} and saving to {output}.")

    cave = reader(input_cave)
    print_image(cave, name=input_cave, target=output, grid=grid, start=start)

if __name__ == "__main__":
    main(sys.argv[1:])