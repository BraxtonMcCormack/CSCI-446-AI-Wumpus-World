#! /bin/python3
import sys, getopt, random


class Cave:
    """
    Cave.py used to house the cave that Agents will traverse for Project 2 of CSCI 446

    The cave is a 2 dimensional array of room conditions. They contain either Gold, Walls, Pits, Wumpus, or any of the
    peripheral effects of those, like stench, breezes, or glimmer. The objects, Walls, Pits, and Wumpus, have a probability
    associated with each one so that it all adds up to 1 with safe taking up the probability that the objects dont take up.
    Gold is placed after the safe rooms are identified. The only change to a cave can be the killing of a Wumpus.

    Written by Bowen Kruse, Rory McLean, and Will Jardee (10/14/2021)

    8/10/2023: Added save_cave method, added passed options to constructor, removed traversal methods
    """

    def __init__(self, pit_probs, obs_probs, wump_probs, dimensions, agent=False):
        """
        Initialization method for the cave object
        """
        self.dimension = dimensions
        self.rooms = None
        self.wumpus_prob = wump_probs
        self.pit_prob = pit_probs
        self.wall_prob = obs_probs
        self.safe = 1 - (pit_probs + obs_probs + wump_probs)
        self.wumpus_count = 0
        self.agent=agent

    def generate(self):
        """
        Create 2d list of room objects and sets conditions based on given probabilities

        :return: nothing
        """
        self.rooms = [[self.get_condition_assignment()
                       for _ in range(self.dimension)]
                      for _ in range(self.dimension)]
        for i in range(self.dimension):
            for j in range(self.dimension):
                if 'wumpus' in self.rooms[i][j]:
                    self.set_neighbor_percepts((i, j), 'stench')
                if 'pit' in self.rooms[i][j]:
                    self.set_neighbor_percepts((i, j), 'breeze')

        self.place_gold()
        if self.agent: 
            self.place_agent()

    def set_neighbor_percepts(self, current_coord, percept):
        """
        Set respective percepts i.e. stench breeze glimmer to neighboring rooms of objects

        :param current_coord: location of objects emitting percepts
        :param percept: percept to populate the adjacent rooms with
        :return: nothing
        """
        x, y = current_coord
        # left neighbor bottom neighbor right neighbor top neighbor
        neighbors = [(x - 1, y), (x, y - 1), (x + 1, y), (x, y + 1)]
        for i in neighbors:
            n_x, n_y = i
            # if room is on edge of cave don't try to set outside neighbors
            if 0 <= n_x < self.dimension and 0 <= n_y < self.dimension:
                room = self.rooms[n_x][n_y]
                if percept not in room and 'wumpus' not in room and 'pit' not in room and 'wall' not in room:
                    self.rooms[n_x][n_y].append(percept)

    def place_gold(self):
        """
        Place the gold in a random safe room in the cave

        :return: nothing
        """
        free_spots = []
        # find all free spots where gold could be placed
        for i in range(self.dimension):
            for j in range(self.dimension):
                if 'safe' in self.rooms[i][j]:
                    free_spots.append((i, j))
        # chooses randomly with uniform distribution a free spot in the cave for the gold
        uniform_choice = int(random.uniform(0, self.dimension-1))

        gold_coord = free_spots[uniform_choice]
        # replaces free condition with gold condition
        self.rooms[gold_coord[0]][gold_coord[1]].append('gold')
        self.rooms[gold_coord[0]][gold_coord[1]].append('glimmer')

    def place_agent(self):
        """
        Place the Agent in a random safe room in the cave

        :return: nothing
        """
        free_spots = []
        # find all free spots where agent could be placed
        for i in range(self.dimension):
            for j in range(self.dimension):
                if 'safe' in self.rooms[i][j] and 'gold' not in self.rooms[i][j]:
                    free_spots.append((i, j))
        # chooses randomly with uniform distribution a free spot in the cave for the gold
        uniform_choice = int(random.uniform(0, self.dimension-1))
        agent_coord = free_spots[uniform_choice]
        # return tuple where agent is to be placed
        return agent_coord
    
    def get_condition_assignment(self):
        """
        Generates an object or safe condition to fill a room

        :return: random choice based on probabilities
        """
        this_choice = random.choices(['pit', 'wumpus', 'wall', 'safe'],
                                     weights=(self.pit_prob, self.wumpus_prob, self.wall_prob, self.safe))
        # Keep track of the amount of Wumpus in board so that the agent can be given that amount of arrows
        if this_choice[0] == 'wumpus':
            self.wumpus_count += 1
        return this_choice


    def display_cave(self):
        """
        Displays the cave in a readable format

        :return: nothing
        """
        print('---------------------------')
        for row in self.rooms:
            row_conditions = []
            for col in row:
                row_conditions.append(col)
            print(row_conditions)
        print('---------------------------')


    def save_cave(self, file):
        """
        Saves the cave in a readable format

        :return: nothing
        """
        output_file = open(file, 'w')
        # preamble with cave size and number of wumpus
        output_file.write("Cave Size: {0}x{0}, Number of Wumpus: {1}\n".format(self.dimension, self.wumpus_count))
        # print row by row
        for row in self.rooms:
            row_conditions = []
            for col in row:
                row_conditions.append(col)
            output_file.write(str(row_conditions) + "\n")


def main(argv):
    """
    Main method for generating a Wumpus World cave. For details, run
        python <path-to-this-file>/generate-cave.py -h
    or read the documentation below. This function is intended to be run through the command line. 

    Written by: Will Jardee 8/10/2023
    """

    # Set defauls
    pit_prob, obstacle_prob, wumpus_prob = 0.05, 0.05, 0.05
    dimension = 5
    output = None
    agent = False

    # Parse passed options
    opts, args = getopt.getopt(argv,"hf:d:p:o:w:a:",["file=", "dim=", "pit-prob=", "obstacle-prob=", "wumpus-prob=", "agent="])
    for opt, arg in opts:
        # help option
        if opt == '-h':
            print ("Script for generating caves in accordance with the 'Wumpus World' problem. Cells are filled\n" +
                   "with objects (pits, gold, obstacles, wumpus) and populated with descriptors of 'breeze', 'glimmer',\n"
                   "and 'stench' next to pits, gold, and wumpus, respectively.\n\n"
                   "Passable arguments:\n" +
                   "    -f, --file: File to output the document in (default = None/print to terminal)\n" +
                   "    -d, --dim: Length of a side of the cave. Caves are square. (default = 5)\n" +
                   "    -p, --pit-prob: Probability of a pit being placed on any cell. (default = 0.05)\n" + 
                   "    -o, --obstacle-prob: Probability of a obstacle (wall) being placed on any cell. (default = 0.05)\n" +
                   "    -w, --wumpus-prob: Probability of a wumpus being placed on any cell. (default = 0.05)\n" + 
                   "    -a, --agent: Place the agent in a random safe position where the gold is not. (default = False)\n\n" + 
                   "Example usage:\n" +
                   "    python generate-cave.py -p 0.10 --obstacle-prob 0.01 -d 3\n" + 
                   "    python generate-cave.py -d 25 -f 25dim-cave.txt"
                   )
            sys.exit()

        # parse options
        elif opt in ("-p", "--pit-prob"):
            pit_prob = float(arg)
        elif opt in ("-o", "--obstacle-prob"):
            obstacle_prob = float(arg)
        elif opt in ("-w", "--wumpus-prob"):
            wumpus_prob = float(arg)
        elif opt in ("-d", "--dim"):
            dimension = int(arg)
        elif opt in ("-f", "--file"):
            output = arg
        elif opt in ("-a", "--agent"):
            agent = bool(arg)

    # Create cave object and fill it.
    cave = Cave(pit_prob, obstacle_prob, wumpus_prob, dimension, agent)
    cave.generate()

    # Either print out a rough visual of the cave, or save to file
    if output is None:
        cave.display_cave()
    else: 
        cave.save_cave(output)
        print(output)


if __name__ == "__main__":
    main(sys.argv[1:])
