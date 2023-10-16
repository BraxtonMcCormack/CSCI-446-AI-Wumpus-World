import numpy as np
import sys

WUMPUS = "'wumpus'"
PIT = "'pit'"
GOLD = "'gold'"
WALL = "'wall'"
SAFE = "'safe'"
WUMPUS_PERCEPT = "'stench'"
PIT_PERCEPT = "'breeze'"
GOLD_PERCEPT = "'glimmer'"
OBSTACLES = [WUMPUS, PIT, WALL, GOLD]
ITEMS = [WUMPUS, PIT, GOLD, WALL, SAFE, WUMPUS_PERCEPT, PIT_PERCEPT, GOLD_PERCEPT]

def reader(file: str) -> np.array:
    """
    Takes a file name and returns an np.array of the file contents.
    :param file: File name.
    :return: numpy array of the cave information.
    """
    cave_file = open(file, "r")
    header = cave_file.readline()    # Disregard the preamble line
    cave = []
    for line in cave_file:
        # split each line into cells
        cave.append([i.strip("[ ]") for i in line.strip("\n [ ]").split("],")])
    return header, np.array(cave)


def TEST_safe_start(cave):
    """Tests that the (0,0) location does not have an obstacle"""
    if WUMPUS in cave[0, 0] or PIT in cave[0, 0] or WALL in cave[0, 0]:
        raise Exception("!! Starting cell not safe !!")

def TEST_wumpus_percepts(cave):
    """Tests that all Wumpus are surrounded by stench and that all stench are next to wumpus."""
    for i in np.arange(0, cave.shape[0]):
        for j in np.arange(0, cave.shape[1]):
            # Gets adjacent cells and tests that it does not go off the board.
            adjacent = [(i, j+1), (i+1, j), (i-1, j), (i, j-1)]
            adjacent = [adj_elem for adj_elem in adjacent if adj_elem[0] >= 0 and adj_elem[0] < cave.shape[0]]
            adjacent = [adj_elem for adj_elem in adjacent if adj_elem[1] >= 0 and adj_elem[1] < cave.shape[1]]

            # Test if WUMPUS is surrounded by WUMPUS_PERCEPT
            if WUMPUS in cave[i, j]:
                for elem in adjacent:
                    if WUMPUS_PERCEPT not in cave[elem]:
                        raise Exception(f"!! {WUMPUS_PERCEPT} missing from cell {elem} !!")
            
            #Test if WUMPUS_PERCEPT is next to WUMPUS
            if WUMPUS_PERCEPT in cave[i, j]:
                wumpus_ad = False
                for elem in adjacent:
                    if WUMPUS in cave[elem]:
                        wumpus_ad = True
                if not wumpus_ad:
                    raise Exception(f"!! {WUMPUS} not adjacent to {WUMPUS_PERCEPT} at ({i}, {j})")
    print(f"Passed TEST_wumpus_percepts")

def TEST_pit_percepts(cave):
    """Tests that all pit are surrounded by breeze and that all breeze are next to pit."""
    for i in np.arange(0, cave.shape[0]):
        for j in np.arange(0, cave.shape[1]):
            # Gets adjacent cells and tests that it does not go off the board.
            adjacent = [(i, j+1), (i+1, j), (i-1, j), (i, j-1)]
            adjacent = [adj_elem for adj_elem in adjacent if adj_elem[0] >= 0 and adj_elem[0] < cave.shape[0]]
            adjacent = [adj_elem for adj_elem in adjacent if adj_elem[1] >= 0 and adj_elem[1] < cave.shape[1]]

            # Test if PIT is surrounded by PIT_PERCEPT
            if PIT in cave[i, j]:
                for elem in adjacent:
                    if PIT_PERCEPT not in cave[elem]:
                        raise Exception(f"!! {PIT_PERCEPT} missing from cell {elem} !!")
                    
            #Test if PIT_PERCEPT is next to PIT
            if PIT_PERCEPT in cave[i, j]:
                pit_ad = False
                for elem in adjacent:
                    if PIT in cave[elem]:
                        pit_ad = True
                if not pit_ad:
                    raise Exception(f"!! {PIT} not adjacent to {PIT_PERCEPT} at ({i}, {j})") 
    print("Passed TEST_pit_percepts")

def TEST_gold_percepts(cave):
    """Test that glimmer only shows up with gold and that all gold have a glimmer."""
    for i in np.arange(0, cave.shape[0]):
        for j in np.arange(0, cave.shape[1]):

            #Test if GOLD and GOLD_PERCEPT show up together
            if GOLD in cave[i, j]:
                if GOLD_PERCEPT not in cave[i, j]:
                    raise Exception(f"!! {GOLD} in ({i}, {j}) missing {GOLD_PERCEPT} !!")
            if GOLD_PERCEPT in cave[i, j]:
                if GOLD not in cave[i, j]:
                    raise Exception(f"!! {GOLD_PERCEPT} in ({i}, {j}) without {GOLD} !!")
    print("Passed TEST_gold_percepts")

def TEST_wumpus_count(cave, header):
    """Tests that the number of Wumpus reported in header is correct."""
    #Count number of WUMPUS
    wump_count = 0
    for i in np.arange(0, cave.shape[0]):
        for j in np.arange(0, cave.shape[1]):
            if WUMPUS in cave[i, j]:
                wump_count += 1

    #Get number of WUMPUS from header
    wump_count_header = int(header.split(", ")[1].split(": ")[1])

    #Test if numbers match up
    if wump_count != wump_count_header:
        raise Exception(f"!! {wump_count} {WUMPUS} present, but {wump_count_header} {WUMPUS} count in header !!")
    print("Passed TEST_wumpus_count")

def TEST_safe_count(cave, header):
    """Tests that the number of Wumpus reported in header is correct."""
    #Count number of SAFE
    safe_count = 0
    for i in np.arange(0, cave.shape[0]):
        for j in np.arange(0, cave.shape[1]):
            if SAFE in cave[i, j]:
                safe_count += 1

    #Get number of SAFE from header
    safe_count_header = int(header.split(", ")[2].split(": ")[1])

    #Test if numbers match up
    if safe_count != safe_count_header:
        raise Exception(f"!! {safe_count} {SAFE} present, but {safe_count_header} {SAFE} count in header !!")
    print("Passed TEST_safe_count")

def TEST_header_size(cave, header):
    """Tests that the cave size reported in the header is correct."""
    #Get size information from header
    size_header = header.split(", ")[0].split(": ")[1].split("x")
    size_header = [int(i) for i in size_header]

    #Test if size information matches with numpy array size
    for dim in zip(size_header, cave.shape):
        if dim[0] != dim[1]:
            raise Exception(f"!! Header size incorrect !!")
    print("Passed TEST_header_size")

def TEST_one_obstable_in_cell(cave):
    """Tests that obstacles do not exist in the same location."""
    for i in np.arange(0, cave.shape[0]):
        for j in np.arange(0, cave.shape[1]):
            #Count number of obstacles
            obstacle_count = len([obj for obj in cave[i, j] if obj in OBSTACLES])

            if obstacle_count > 1:
                raise Exception(f"!! Cell ({i}, {j}) contains {obstacle_count} obstacles !!")
    print("Passed TEST_one_obstable_in_cell")

def TEST_typo(cave):
    """Tests that only the predetermined objects exists in the caves."""
    for i in np.arange(0, cave.shape[0]):
        for j in np.arange(0, cave.shape[1]):
            #Gets all items and ensures they have a match in the ITEMS list defined above; all valid items must be in there
            for elem in cave[i, j].split(", "):
                if elem not in ITEMS:
                    raise Exception(f"!! {elem} in cell ({i}, {j}) not defined !!")
    print("Passed TEST_typo")
                

def run_tests(file_name):
    """Runs the tests defined earlier in this file."""
    header, cave = reader(file_name)

    print(f"Testing {file_name}:")

    # Run tests
    TEST_typo(cave)
    TEST_safe_start(cave)
    TEST_wumpus_percepts(cave)
    TEST_pit_percepts(cave)
    TEST_gold_percepts(cave)
    TEST_wumpus_count(cave, header)
    TEST_safe_count(cave, header)
    TEST_one_obstable_in_cell(cave)
    TEST_header_size(cave, header)

    print("All tests passed")
    print("-"*35)

if __name__ == "__main__":
    # runs the test suite on the first argument passed
    run_tests(sys.argv[1])
    