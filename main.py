import os
import random

class WumpusWorld:
    def __init__(self, filename):
        self.filename = filename
        self.cave = None
        self.num_safe = 0
        self.num_wumpus = 0
        self.num_arrows = 0
        self.cave_size = 0
        self.agent_x = 0
        self.agent_y = 0
        self.game_over = False  # Initialize game_over to False
        self.read_cave_file()
        self.place_agent_in_corner()

    def get_size(self):
        return self.cave_size-1
    
    def get_arrows(self):
        return self.num_arrows
    
    def get_wumpus_count(self):
        return self.num_wumpus
    
    def get_agent_coordinates(self):
        return self.agent_x, self.agent_y

    def read_cave_file(self):
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
                    self.cave_size = int(cave_size_part.split('x')[0])  # Set cave size
                    # self.num_safe = int(cave_size_part.split('x')[1])     #idk what I was thinking this line confused me for a good 15 minutes

            self.cave = [[[] for _ in range(self.cave_size)] for _ in range(self.cave_size)]

            for i in range(1, len(lines)):
                row = lines[i].strip('[]\n').split('],[')
                for j in range(len(row)):
                    self.cave[i-1][j] = row[j].split(',')

    def get_percept(self, x, y):
        if 0 <= x < len(self.cave) and 0 <= y < len(self.cave):
            values = self.cave[y][x]
            return values
            # print(f'Values at coordinates ({x}, {y}): {", ".join(values)}')
        else:
            print('Coordinates out of bounds.')

    def print_formatted_board(self):
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
            y = self.agent_y - 1
            while y >= 0:
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
            y = self.agent_y + 1
            while y < self.cave_size:
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



class Predicate:
    def __init__(self, name, args, is_negated=False):
        self.name = name
        self.args = args
        self.is_negated = is_negated

    def __str__(self):
        negation = "¬" if self.is_negated else ""
        return f"{negation}{self.name}({', '.join(map(str, self.args))})" # Convert args to string format

class KnowledgeBase:
    def __init__(self):
        self.clauses = []

    def add_clause(self, clause):
        self.clauses.append(clause)
    
    def is_contradictory(self, pred1, pred2):
        return pred1.name == pred2.name and pred1.args == pred2.args and pred1.is_negated != pred2.is_negated

    def resolve(self, clause1, clause2):
        # Perform resolution between two clauses
        for pred1 in clause1:
            for pred2 in clause2:
                # Matching predicate names but opposite in terms of negation
                if pred1.name == pred2.name and pred1.is_negated != pred2.is_negated:
                    unification = self.unify(pred1, pred2)
                    if unification:
                        # Create the resulting clause without pred1 and pred2
                        resulting_clause = [p for p in clause1 if p != pred1] + [p for p in clause2 if p != pred2]
                        # Apply substitution
                        resulting_clause = [self.substitute(p, unification) for p in resulting_clause]
                        return resulting_clause
        return None


    def unify(self, pred1, pred2):
        # Unify two predicates
        substitution = {}
        if pred1.name != pred2.name or pred1.is_negated == pred2.is_negated:
            return None
        for arg1, arg2 in zip(pred1.args, pred2.args):
            # Check if the arguments are strings and lowercased (i.e., variables)
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

    def substitute(self, predicate, substitution):
        # Substitute variables in a predicate
        new_args = [substitution[arg] if arg in substitution else arg for arg in predicate.args]
        return Predicate(predicate.name, new_args, predicate.is_negated)

    def is_consistent(self, new_clause):
        # Directly check for contradictory predicates with the new clause
        for pred_new in new_clause:
            for clause in self.clauses:
                for pred_clause in clause:
                    if self.is_contradictory(pred_new, pred_clause):
                        return False
        
        # Your original consistency check
        for clause in self.clauses:
            resolvent = self.resolve(clause, new_clause)
            if resolvent is not None:
                if not resolvent or all(p.is_negated for p in resolvent):
                    return False

        return True
    
    def reveal(self):
        for clause in self.clauses:
            clause_str = " ∧ ".join(map(str, clause))
            print(f"({clause_str})")
        
    

class Agent:
    def __init__(self, world, kb):
        self.world = world
        self.kb = kb
        coord = world.get_agent_coordinates()
        self.ax = int(coord[0])
        self.ay = int(coord[1])
        self.maxX = world.get_size()
        self.maxY = world.get_size()
        self.minXandY = 0
        self.game_over = False
        self.stenches = []  
        self.breezes = []
        self.visited = set()
        self.strict_safety_mode = True

    def observe(self):
        percepts = self.world.get_percept(self.ax, self.ay)
        print(f"Agent's current position: ({self.ax}, {self.ay})")
        print(f"Percepts at position ({self.ax}, {self.ay}): {percepts}")
        for item in percepts:
            print(item)
            
            if 'wall' in item:
                self.kb.add_clause([Predicate("Wall", [self.ax, self.ay])])

            if 'glimmer' in item:
                print("Found gold! Win!")
                self.kb.add_clause([Predicate("Gold", [self.ax, self.ay])])
                self.game_over = True
                return

            if 'safe' in item:
                self.kb.add_clause([Predicate("Safe", [self.ax, self.ay]), Predicate("Pit", [self.ax, self.ay], is_negated=True), Predicate("Wumpus", [self.ax, self.ay], is_negated=True)])
                if (self.kb.is_consistent([Predicate("Wumpus", [self.ax, self.ay])]) == False):
                    if (self.kb.is_consistent([Predicate("Pit", [self.ax, self.ay])]) == False):
                        if (self.kb.is_consistent([Predicate("Breeze", [self.ax, self.ay])]) == False):
                            if (self.kb.is_consistent([Predicate("Stench", [self.ax, self.ay])]) == False):
                                if (self.kb.is_consistent([Predicate("Wall", [self.ax, self.ay])]) == False):
                                    self.kb.add_clause([Predicate("Safe", [self.ax + 1, self.ay])])
                                    self.kb.add_clause([Predicate("Safe", [self.ax - 1, self.ay])])
                                    self.kb.add_clause([Predicate("Safe", [self.ax, self.ay + 1])])
                                    self.kb.add_clause([Predicate("Safe", [self.ax, self.ay - 1])])

            if 'pit' in item:
                print("Fell into a pit! Loss!")
                self.game_over = True
                return

            if 'wumpus' in item:
                print("Eaten by the Wumpus! Loss!")
                self.game_over = True
                return

            # Common logic for handling stenches and breezes
            def handle_smell_or_breeze(smell_type, entity_type):
                print(f"{smell_type} detected! Considering possible {entity_type} positions...")
                possible_entity_locations = []
                for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                    adjacent_x, adjacent_y = self.ax + dx, self.ay + dy
                    if self._is_valid_coordinate(adjacent_x, adjacent_y) and \
                    not self.kb.is_consistent([Predicate("Safe", [adjacent_x, adjacent_y])]) and \
                    (adjacent_x, adjacent_y) not in self.visited:
                        self.kb.add_clause([Predicate(entity_type, [adjacent_x, adjacent_y], is_negated=True)])
                        self.visited.add((adjacent_x, adjacent_y)) # mark as visited to avoid loops
                for loc in possible_entity_locations:
                    self.kb.add_clause([Predicate(entity_type, [loc[0], loc[1]])])
            
            if 'stench' in item:
                handle_smell_or_breeze('Stench', 'Wumpus')
            
            if 'breeze' in item:
                handle_smell_or_breeze('Breeze', 'Pit')

            print(f"Knowledge base after processing percepts:")
            self.kb.reveal()
        

    def _is_valid_coordinate(self, x, y):
        return 0 <= x < self.maxX and 0 <= y < self.maxY    
         
    def rank_risks(self, x, y):
        risk_score = 0

        # Check if the position is explicitly marked as safe
        if not self.kb.is_consistent([Predicate("Safe", [x, y])]):
            risk_score += 1000  # high value for cells that are not known to be safe

        if self.kb.is_consistent([Predicate("Wumpus", [x, y])]):
            risk_score += 100
        if self.kb.is_consistent([Predicate("Pit", [x, y])]):
            risk_score += 5
        if self.kb.is_consistent([Predicate("Wall", [x, y])]):
            risk_score += 100

        return risk_score

    def think(self):
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
                elif not self.strict_safety_mode and risk < 10:  # Check for strict_safety_mode here
                    risky_moves.append((new_x, new_y))

        if safe_moves:
            move = random.choice(safe_moves)
            self.move_to(move[0], move[1])
        elif risky_moves:
            # Sorting risky moves by risk score and choosing the least risky
            sorted_risky_moves = sorted(risky_moves, key=lambda coord: self.rank_risks(coord[0], coord[1]))
            move = sorted_risky_moves[0]
            self.move_to(move[0], move[1])
            print(f"Took a calculated risk by moving to ({move[0]}, {move[1]})")
        else:
            self.teleport_randomly()

    def teleport_randomly(self):
        valid_positions = [(x, y) for x in range(self.maxX) for y in range(self.maxY)]
        random.shuffle(valid_positions)
        for x, y in valid_positions:
            if (x, y) not in self.visited:
                self.move_to(x, y)
                return
        print("No valid positions to teleport!")

    def move_to(self, new_x, new_y):
        self.ax, self.ay = new_x, new_y
        self.visited.add((new_x, new_y))
        print(f"Moved to ({self.ax}, {self.ay})")
    
    def teleport(self, x, y):
        if self.minXandY <= x < self.maxX and self.minXandY <= y < self.maxY:
            self.ax = x
            self.ay = y
            print(f"Teleported to ({self.ax}, {self.ay})")
        else:
            print("Invalid teleport coordinates!")

    def explore(self):
        while not self.game_over:
            self.observe()
            if not self.game_over:  # Check if game over after observing
                self.think()
            
            # self.game_over = True

        # print(self.kb.reveal())
        # percepts = self.world.get_percept(0, 1)
        # print(percepts)



def main():
    filename = os.path.join('caves', '10x10-1.cave')
    kb = KnowledgeBase()
    world = WumpusWorld(filename)
    agent = Agent(world, kb)
    # for item in world.get_percept(0,9):
    #     print(item)

    agent.explore()

    

if __name__ == "__main__":
    main()