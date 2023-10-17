import os
import random

class WumpusWorld:
    def __init__(self, filename):
        # Initialize the WumpusWorld instance with a filename.
        self.filename = filename
        self.cave = None
        self.num_safe = 0
        self.num_wumpus = 0
        self.num_arrows = 0
        self.cave_size = 0
        self.agent_x = 0
        self.agent_y = 0
        self.game_over = False
        # Read the cave layout from the specified file and place the agent in a corner.
        self.read_cave_file()
        self.place_agent_in_corner()

    def get_size(self):
        # Return the size of the cave.
        return self.cave_size - 1

    def get_safe(self):
        # Return the number of safe spaces.
        return self.num_safe

    def get_arrows(self):
        # Return the number of arrows the agent has.
        return self.num_arrows

    def get_wumpus_count(self):
        # Return the number of wumpuses in the cave.
        return self.num_wumpus

    def get_agent_coordinates(self):
        # Return the current coordinates of the agent.
        return self.agent_x, self.agent_y

    def read_cave_file(self):
        # Read the cave layout and game parameters from the specified file.
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            header_parts = lines[0].strip().split(',')
            self.num_wumpus = int(header_parts[1].strip(" Number of Wumpus: "))
            self.num_arrows = int(header_parts[1].strip(" Number of Wumpus: "))
            temp = header_parts[2].strip(" Number of safe: ")
            self.num_safe = str(temp)

            for part in header_parts:
                if 'Cave Size' in part:
                    cave_size_part = part.split(':')[1].strip()
                    self.cave_size = int(cave_size_part.split('x')[0])
            self.cave = [[[] for _ in range(self.cave_size)] for _ in range(self.cave_size)]

            # Parse the cave layout and store it in a 2D list.
            for i in range(1, len(lines)):
                row = lines[i].strip('[]\n').split('],[')
                for j in range(len(row)):
                    self.cave[i-1][j] = row[j].split(',')

    def get_percept(self, x, y):
        # Get the percept (list of objects) at the specified coordinates (x, y) in the cave.
        if 0 <= x < len(self.cave) and 0 <= y < len(self.cave):
            values = self.cave[y][x]
            return values
        else:
            print('Coordinates out of bounds.')

    def print_formatted_board(self):
        # Print a formatted representation of the cave with the agent's location and game status.
        for y in range(len(self.cave)):
            formatted_row = []
            for x in range(len(self.cave[y])):
                formatted_cell = ""
                for item in self.cave[y][x]:
                    if 'pit' in item:
                        formatted_cell = "[0]"
                    elif 'gold' in item:
                        formatted_cell = "[G]"
                    elif 'wumpus' in item:
                        formatted_cell = "[>]"
                    elif 'wall' in item:
                        formatted_cell = "[W]"
                    if not formatted_cell:
                        formatted_cell = "[ ]"
                if x == self.agent_x and y == self.agent_y:
                    formatted_cell = "[a]"
                formatted_row.append(formatted_cell)
            print("".join(formatted_row))

        print(f"Arrows remaining: {self.num_arrows}")
        print(f"Wumpuses remaining: {self.num_wumpus}")
        print(f"safe spaces remaining: {self.num_safe}")


    def hit_wall(self, x, y):
        # Check if the specified cell contains a wall
        for item in self.cave[y][x]:
            if 'wall' in item:
                return True
        return False

    def is_bad(self, x, y):
        for item in self.cave[y][x]:
            # Check if the specified cell contains a 'pit' or a 'wumpus'
            if 'pit' in item:
                print("You fell into a pit and died! Game over.")
                self.game_over = True
            elif 'wumpus' in item:
                print("You encountered a wumpus and got eaten! Game over.")
                self.game_over = True

    def is_glimmer(self, x, y):
        for item in self.cave[y][x]:
            # Check if the specified cell contains a 'pit' or a 'wumpus'
            if 'glimmer' in item:
                print("You found the gold and won!")
                self.game_over = True


    def move_up(self):
        if not self.game_over:
            if self.agent_y > 0 and not self.hit_wall(self.agent_x, self.agent_y - 1):
                self.cave[self.agent_y][self.agent_x] = [item for item in self.cave[self.agent_y][self.agent_x] if item != 'agent']
                self.agent_y -= 1
                self.cave[self.agent_y][self.agent_x].append('agent')
                self.is_bad(self.agent_x, self.agent_y)  # Check if the new cell is bad
                self.is_glimmer(self.agent_x, self.agent_y)

    def move_down(self):
        if not self.game_over:
            if self.agent_y < self.cave_size - 1 and not self.hit_wall(self.agent_x, self.agent_y + 1):
                self.cave[self.agent_y][self.agent_x] = [item for item in self.cave[self.agent_y][self.agent_x] if item != 'agent']
                self.agent_y += 1
                self.cave[self.agent_y][self.agent_x].append('agent')
                self.is_bad(self.agent_x, self.agent_y)
                self.is_glimmer(self.agent_x, self.agent_y)

    def move_left(self):
        if not self.game_over:
            if self.agent_x > 0 and not self.hit_wall(self.agent_x - 1, self.agent_y):
                self.cave[self.agent_y][self.agent_x] = [item for item in self.cave[self.agent_y][self.agent_x] if item != 'agent']
                self.agent_x -= 1
                self.cave[self.agent_y][self.agent_x].append('agent')
                self.is_bad(self.agent_x, self.agent_y)
                self.is_glimmer(self.agent_x, self.agent_y)

    def move_right(self):
        if not self.game_over:
            if self.agent_x < self.cave_size - 1 and not self.hit_wall(self.agent_x + 1, self.agent_y):
                self.cave[self.agent_y][self.agent_x] = [item for item in self.cave[self.agent_y][self.agent_x] if item != 'agent']
                self.agent_x += 1
                self.cave[self.agent_y][self.agent_x].append('agent')
                self.is_bad(self.agent_x, self.agent_y)
                self.is_glimmer(self.agent_x, self.agent_y)

    def __str__(self):
        result = f"Cave Size: {len(self.cave)}x{len(self.cave)}, Number of Wumpus: {self.num_wumpus}, Number of safe: {self.num_safe}\n"
        for row in self.cave:
            result += '['
            for cell in row:
                result += f"[{', '.join(cell)}], "
            result = result.rstrip(', ')
            result += ']\n'
        return result
    
    def place_agent_in_corner(self):
        # Place the agent in the bottom-right corner of the board
        self.agent_x = 0
        self.agent_y = 0 #self.cave_size - 1

    def is_game_over(self):
        return self.game_over  # A method that returns the game over variable
    
    def is_stench(self):
        # Check if there is a stench where the agent currently is
        for item in self.cave[self.agent_y][self.agent_x]:
            if 'stench' in item:
                return True
        return False

    def is_breeze(self):
        # Check if there is a breeze where the agent currently is
        for item in self.cave[self.agent_y][self.agent_x]:
            if 'breeze' in item:
                return True
        return False
    
    def teleport_agent(self, x, y):
        if not self.game_over:
            if 0 <= x < self.cave_size and 0 <= y < self.cave_size:
                self.cave[self.agent_y][self.agent_x] = [item for item in self.cave[self.agent_y][self.agent_x] if item != 'agent']
                self.agent_x = x
                self.agent_y = y
                self.cave[y][x].append('agent')
            else:
                print("Invalid teleport coordinates. Coordinates are out of bounds.")

    
    def update_cell(self, x, y, new_contents):
        if 0 <= x < self.cave_size and 0 <= y < self.cave_size:
            self.cave[y][x] = [new_contents]
        else:
            print("Invalid cell coordinates. Coordinates are out of bounds.")

    def shoot_left(self):
        if self.num_arrows > 0:
            self.num_arrows -= 1
            x = self.agent_x - 1
            while x >= 0:
                print(f"Arrow moving through coordinates: ({x}, {self.agent_y})")
                for item in self.cave[self.agent_y][x]:
                    if 'wall' in item:
                        return False  # Arrow hits a wall, return False
                    if 'wumpus' in item:
                        self.update_cell(x, self.agent_y, 'wall')  # Mark the wumpus as dead
                        self.num_wumpus -= 1
                        return True  # Return True when a wumpus is hit
                x -= 1
        return False  # Return False when the arrow misses the wumpus or goes out of bounds

    def shoot_up(self):
        if self.num_arrows > 0:
            self.num_arrows -= 1
            y = self.agent_y + 1
            while y <= 0:
                print(f"Arrow moving through coordinates: ({self.agent_x}, {y})")
                for item in self.cave[y][self.agent_x]:
                    if 'wall' in item:
                        return False  # Arrow hits a wall, return False
                    if 'wumpus' in item:
                        self.update_cell(self.agent_x, y, 'wall')  # Mark the wumpus as dead
                        self.num_wumpus -= 1
                        return True  # Return True when a wumpus is hit
                y += 1
        return False  # Return False when the arrow misses the wumpus or goes out of bounds

    def shoot_right(self):
        if self.num_arrows > 0:
            self.num_arrows -= 1
            x = self.agent_x + 1
            while x < self.cave_size:
                print(f"Arrow moving through coordinates: ({x}, {self.agent_y})")
                for item in self.cave[self.agent_y][x]:
                    if 'wall' in item:
                        return False  # Arrow hits a wall, return False
                    if 'wumpus' in item:
                        self.update_cell(x, self.agent_y, 'wall')  # Mark the wumpus as dead
                        self.num_wumpus -= 1
                        return True  # Return True when a wumpus is hit
                x += 1
        return False  # Return False when the arrow misses the wumpus or goes out of bounds

    def shoot_down(self):
        if self.num_arrows > 0:
            self.num_arrows -= 1
            y = self.agent_y - 1
            while y >= self.cave_size:
                print(f"Arrow moving through coordinates: ({self.agent_x}, {y})")
                for item in self.cave[y][self.agent_x]:
                    if 'wall' in item:
                        return False  # Arrow hits a wall, return False
                    if 'wumpus' in item:
                        self.update_cell(self.agent_x, y, 'wall')  # Mark the wumpus as dead
                        self.num_wumpus -= 1
                        return True  # Return True when a wumpus is hit
                y -= 1
        return False  # Return False when the arrow misses the wumpus or goes out of bounds

class Predicate:
    def __init__(self, name, args, is_negated=False):
        # Initialize a Predicate instance with a name, arguments, and negation status.
        self.name = name  # Name of the predicate.
        self.args = args  # List of arguments.
        self.is_negated = is_negated  # Boolean indicating negation (default is False).

    def __str__(self):
        # Convert the Predicate object to a string representation.
        negation = "¬" if self.is_negated else ""  # Include a ¬ symbol for negated predicates.
        args_str = ', '.join(map(str, self.args))  # Convert arguments to a comma-separated string.
        return f"{negation}{self.name}({args_str})"

# Define a class named KnowledgeBase for managing fol
class KnowledgeBase:
    def __init__(self):
        # Initialize an empty list to store logical clauses.
        self.clauses = []

    # Method to add a new logical clause to the knowledge base.
    def add_clause(self, clause):
        self.clauses.append(clause)

    # Method to check if two predicates are contradictory.
    def is_contradictory(self, pred1, pred2):
        return pred1.name == pred2.name and pred1.args == pred2.args and pred1.is_negated != pred2.is_negated

    # Method to resolve two logical clauses by finding a unifying substitution.
    def resolve(self, clause1, clause2):
        for pred1 in clause1:
            for pred2 in clause2:
                if pred1.name == pred2.name and pred1.is_negated != pred2.is_negated:
                    # Attempt to unify the predicates and return the resulting clause.
                    unification = self.unify(pred1, pred2)
                    if unification:
                        resulting_clause = [p for p in clause1 if p != pred1] + [p for p in clause2 if p != pred2]
                        resulting_clause = [self.substitute(p, unification) for p in resulting_clause]
                        return resulting_clause
        return None

    # Method to unify two predicates by finding a substitution that makes them identical.
    def unify(self, pred1, pred2):
        substitution = {}
        if pred1.name != pred2.name or pred1.is_negated == pred2.is_negated:
            return None
        for arg1, arg2 in zip(pred1.args, pred2.args):
            is_arg1_var = isinstance(arg1, str) and arg1.islower()
            is_arg2_var = isinstance(arg2, str) and arg2.islower()

            if arg1 != arg2:
                if is_arg1_var and is_arg2_var:
                    substitution[arg1] = arg2
                elif is_arg1_var:
                    substitution[arg1] = arg2
                elif is_arg2_var:
                    substitution[arg2] = arg1
                else:
                    return None
        return substitution

    # Method to substitute variables in a predicate based on a given substitution.
    def substitute(self, predicate, substitution):
        new_args = [substitution[arg] if arg in substitution else arg for arg in predicate.args]
        return Predicate(predicate.name, new_args, predicate.is_negated)

    # Method to check if adding a new clause to the knowledge base is consistent with existing clauses.
    def is_consistent(self, new_clause):
        for pred_new in new_clause:
            for clause in self.clauses:
                for pred_clause in clause:
                    if self.is_contradictory(pred_new, pred_clause):
                        return False

        for clause in self.clauses:
            resolvent = self.resolve(clause, new_clause)
            if resolvent is not None:
                if not resolvent or all(p.is_negated for p in resolvent):
                    return False

        return True

    # Method to reveal the contents of the knowledge base by printing its clauses.
    def reveal(self):
        for clause in self.clauses:
            clause_str = " ∧ ".join(map(str, clause))
            print(f"({clause_str})")
        
class StatisticTracker:
    def __init__(self):
        self.points = 10000     #Initial points
        self.actionCost = 1     #The cost of one action
        self.goldCost = 1000    #The reward of finding gold
        self.deathCost = 10000  #The cost of one death
    '''Returns points'''
    def getPoints(self):
        return self.points
    '''Helper Functions to change cost'''
    def costAction(self):
        self.points -= self.actionCost
    def costGold(self):
        self.points += self.goldCost
    def costDeath(self):
        self.points -= self.deathCost
   

# Define a class named Agent for an AI agent in a Wumpus World game.
class Agent:
    def __init__(self, world, kb, st):
        # Initialize the agent with a world, knowledge base, and statistics tracker.
        self.world = world
        self.kb = kb
        self.st = st
        coord = world.get_agent_coordinates()
        self.ax = int(coord[0])  # X-coordinate of the agent's position.
        self.ay = int(coord[1])  # Y-coordinate of the agent's position.
        self.maxX = world.get_size()  # Maximum X-coordinate in the world.
        self.maxY = world.get_size()  # Maximum Y-coordinate in the world.
        self.minXandY = 0  # Minimum X and Y coordinates.
        self.game_over = False  # Flag to indicate if the game is over.
        self.stenches = []  # List to store stenches in the current position.
        self.breezes = []  # List to store breezes in the current position.
        self.visited = set()  # Set to keep track of visited positions.
        self.strict_safety_mode = True  # Flag for strict safety mode.
        self.arrow_count = int(world.get_arrows())  # Number of arrows the agent has.

    # Method to observe the environment and update the knowledge base.
    def observe(self):
        # Get percepts at the current position.
        percepts = self.world.get_percept(self.ax, self.ay)
        print("==================================")
        print(f"Agent's current position: ({self.ax}, {self.ay})")
        print(f"Percepts at position ({self.ax}, {self.ay}): {percepts}")
        no_stench = True
        no_breeze = True

        for item in percepts:
            # Update the knowledge base based on percepts.
            if 'wall' in item:
                self.kb.add_clause([Predicate("Wall", [self.ax, self.ay])])

            if 'glimmer' in item:
                # Found gold, win the game.
                print("Found gold! Win!")
                self.st.costGold()
                self.kb.add_clause([Predicate("Gold", [self.ax, self.ay])])
                self.kb.reveal()
                self.game_over = True
                return

            if 'pit' in item:
                # Fell into a pit, lose the game.
                print("Fell into a pit! Loss!")
                self.st.costDeath()
                self.game_over = True
                return

            if 'wumpus' in item:
                # Eaten by the Wumpus, lose the game.
                print("Eaten by the Wumpus! Loss!")
                self.st.costDeath()
                self.game_over = True
                return

            if 'stench' in item:
                # Update knowledge with possible Wumpus locations.
                no_stench = False
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    adjacent_x, adjacent_y = self.ax + dx, self.ay + dy
                    if self._is_valid_coordinate(adjacent_x, adjacent_y):
                        self.kb.add_clause([Predicate("PossibleWumpus", [adjacent_x, adjacent_y])])

            if 'breeze' in item:
                # Update knowledge with possible pit locations.
                no_breeze = False
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    adjacent_x, adjacent_y = self.ax + dx, self.ay + dy
                    if self._is_valid_coordinate(adjacent_x, adjacent_y):
                        self.kb.add_clause([Predicate("PossiblePit", [adjacent_x, adjacent_y])])

        if no_stench:
            # If no stench detected, mark adjacent cells as safe.
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                adjacent_x, adjacent_y = self.ax + dx, self.ay + dy
                if self._is_valid_coordinate(adjacent_x, adjacent_y):
                    self.kb.add_clause([Predicate("Safe", [adjacent_x, adjacent_y]),
                                        Predicate("Safe", [adjacent_x-1, adjacent_y]),
                                        Predicate("Safe", [adjacent_x+1, adjacent_y]),
                                        Predicate("Safe", [adjacent_x, adjacent_y-1]),
                                        Predicate("Safe", [adjacent_x, adjacent_y+1])])
                    self.kb.add_clause([Predicate("Pit", [adjacent_x, adjacent_y], is_negated=True),
                                        Predicate("Wumpus", [adjacent_x, adjacent_y], is_negated=True)])

        if no_breeze:
            # If no breeze detected, mark adjacent cells as safe.
            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                adjacent_x, adjacent_y = self.ax + dx, self.ay + dy
                if self._is_valid_coordinate(adjacent_x, adjacent_y):
                    self.kb.add_clause([Predicate("Safe", [adjacent_x, adjacent_y]),
                                        Predicate("Safe", [adjacent_x-1, adjacent_y]),
                                        Predicate("Safe", [adjacent_x+1, adjacent_y]),
                                        Predicate("Safe", [adjacent_x, adjacent_y-1]),
                                        Predicate("Safe", [adjacent_x, adjacent_y+1])])
                    self.kb.add_clause([Predicate("Pit", [adjacent_x, adjacent_y], is_negated=True),
                                        Predicate("Wumpus", [adjacent_x, adjacent_y], is_negated=True)])

        print(f"Knowledge base after processing percepts:")
        self.kb.reveal()

    # Method to check if a given coordinate is valid.
    def _is_valid_coordinate(self, x, y):
        return 0 <= x < self.maxX and 0 <= y < self.maxY

    # Method to rank the risks associated with a given coordinate.
    def rank_risks(self, x, y):
        risk_score = 0

        if not self.kb.is_consistent([Predicate("Safe", [x, y])]):
            risk_score += 1000

        if self.kb.is_consistent([Predicate("Wumpus", [x, y])]):
            risk_score += 100
        if self.kb.is_consistent([Predicate("Pit", [x, y])]):
            risk_score += 5
        if self.kb.is_consistent([Predicate("Wall", [x, y])]):
            risk_score += 100

        return risk_score

    # Method to make decisions based on the knowledge and environment observations.
    def think(self):
        self.st.costAction()
        if self.shoot_arrow():
            return
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random.shuffle(directions)

        safe_moves = []
        risky_moves = []

        for dx, dy in directions:
            new_x, new_y = self.ax + dx, self.ay + dy
            if self._is_valid_coordinate(new_x, new_y) and (new_x, new_y) not in self.visited:
                risk = self.rank_risks(new_x, new_y)
                if risk == 0:
                    safe_moves.append((new_x, new_y))
                elif not self.strict_safety_mode and risk < 10:
                    risky_moves.append((new_x, new_y))

        if safe_moves:
            move = random.choice(safe_moves)
            self.move_to(move[0], move[1])
        elif risky_moves:
            sorted_risky_moves = sorted(risky_moves, key=lambda coord: self.rank_risks(coord[0], coord[1]))
            move = sorted_risky_moves[0]
            self.move_to(move[0], move[1])
            print(f"Took a calculated risk by moving to ({move[0]}, {move[1]})")
        else:
            self.risky_move()

    # Method to make a risky move when no safe moves are available.
    def risky_move(self):
        valid_positions = [(x, y) for x in range(self.maxX) for y in range(self.maxY)]
        random.shuffle(valid_positions)
        for x, y in valid_positions:
            if (x, y) not in self.visited:
                self.move_to(x, y)
                return
        print("No valid positions to teleport!")

    # Method to move to a new position and update visited set.
    def move_to(self, new_x, new_y):
        self.ax, self.ay = new_x, new_y
        self.visited.add((new_x, new_y))
        print(f"Moved to ({self.ax}, {self.ay})")

    # Method to teleport the agent to a specified position.
    def teleport(self, x, y):
        if self.minXandY <= x < self.maxX and self.minXandY <= y < self.maxY:
            self.ax = x
            self.ay = y
            print(f"Teleported to ({self.ax}, {self.ay})")
        else:
            print("Invalid teleport coordinates!")

    # Method to shoot an arrow at the Wumpus if possible.
    def shoot_arrow(self):
        potential_wumpus_locations = {
            (x, y) for x in range(self.maxX) for y in range(self.maxY)
            if self.kb.is_consistent([Predicate("Wumpus", [x, y])])
        }

        if not potential_wumpus_locations or self.arrow_count <= 0:
            print("No potential Wumpus locations found or out of arrows!")
            return False

        best_shot = self.identify_best_shot(potential_wumpus_locations)

        if not best_shot:
            print("No good shot identified.")
            return False

        x, y, direction = best_shot

        if (x, y) != (self.ax, self.ay):
            print(f"Moving to ({x}, {y}) to shoot Wumpus.")
            self.ax, self.ay = x, y

        hit = self.execute_shot(direction)

        self.update_knowledge_after_shot(x, y, hit)

        return hit

    # Method to identify the best shot at a potential Wumpus location.
    def identify_best_shot(self, potential_wumpus_locations):
        for wx, wy in potential_wumpus_locations:
            if wx == self.ax:
                return (self.ax, self.ay, "up") if wy > self.ay else (self.ax, self.ay, "down")
            elif wy == self.ay:
                return (self.ax, self.ay, "right") if wx > self.ax else (self.ax, self.ay, "left")

        wx, wy = next(iter(potential_wumpus_locations))
        return (
            (wx - 1, wy, "right") if abs(wx - self.ax) > abs(wy - self.ay) else
            (wx + 1, wy, "left") if wx < self.ax else
            (wx, wy - 1, "up") if wy > self.ay else
            (wx, wy + 1, "down")
        )

    # Method to execute a shot in a specified direction and reduce arrow count.
    def execute_shot(self, direction):
        self.arrow_count -= 1
        self.world.teleport_agent(self.ax, self.ay)

        if direction == "left":
            return self.world.shoot_left()
        if direction == "right":
            return self.world.shoot_right()
        if direction == "up":
            return self.world.shoot_up()
        if direction == "down":
            return self.world.shoot_down()

        return False

    # Method to update knowledge after a shot is executed.
    def update_knowledge_after_shot(self, x, y, hit):
        if hit:
            print(f"Killed Wumpus at ({x}, {y})!")
            self.kb.add_clause([Predicate("DeadWumpus", [x, y])])
        else:
            print("Missed!")
            self.kb.add_clause([Predicate("NoWumpus", [x, y])])

    # Method to run the agent's decision-making loop until the game is over.
    def run(self):
        while not self.game_over:
            self.observe()
            if not self.game_over:
                self.think()
        print("points:")
        print(self.st.getPoints())




def main():
    # Define the filename for the Wumpus World configuration.
    filename = os.path.join('caves', '05x05-1.cave')
    
    # Create an instance of the KnowledgeBase to store logical information.
    kb = KnowledgeBase()
    
    # Create an instance of the WumpusWorld using the specified configuration file.
    world = WumpusWorld(filename)
    
    # Create an instance of the StatisticTracker to keep track of game statistics.
    stat_track = StatisticTracker()
    
    # Create an instance of the Agent and initialize it with the world, knowledge base, and statistics tracker.
    agent = Agent(world, kb, stat_track)
    
    # Run the agent's decision-making loop to play the Wumpus World game.
    agent.run()

    

if __name__ == "__main__":
    main()