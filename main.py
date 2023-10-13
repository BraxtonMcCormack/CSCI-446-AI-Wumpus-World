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
        self.agent_y = self.cave_size - 1

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
    def __init__(self, name, args):
        self.name = name
        self.args = args

    def __str__(self):
        return f"{self.name}({', '.join(map(str, self.args))}"

    def __iter__(self):
        return iter(self.args)

class KB:
    def __init__(self):
        self.clauses = []

    def tell(self, clause):
        self.clauses.append(clause)

    def ask(self, query):
        return query in self.clauses

def unify(subst, x, y):
    if subst is None:
        return None
    elif x == y:
        return subst
    elif isinstance(x, str) and x.islower():
        return unify_var(subst, x, y)
    elif isinstance(y, str) and y.islower():
        return unify_var(subst, y, x)
    elif isinstance(x, Predicate) and isinstance(y, Predicate):
        return unify(unify(subst, x.name, y.name), x.args, y.args)
    elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
        if not x or not y:
            return subst
        return unify(unify(subst, x[0], y[0]), x[1:], y[1:])
    else:
        return None

def unify_var(subst, var, x):
    if var in subst:
        return unify(subst, subst[var], x)
    elif x in subst:
        return unify(subst, var, subst[x])
    else:
        subst[var] = x
        return subst

def resolve(clause1, clause2):
    resolvents = set()
    for literal1 in clause1:
        for literal2 in clause2:
            subst = unify({}, literal1, negate(literal2))
            if subst is not None:
                resolvent = (clause1 | clause2) - {literal1, literal2}
                resolvents.add(resolvent)
    return resolvents

def negate(literal):
    if literal.name.startswith('~'):
        return Predicate(literal.name[1:], literal.args)
    else:
        return Predicate('~' + literal.name, literal.args)

def fol_resolution(kb, query):
    new_clause = query
    while True:
        clauses = list(kb.clauses)
        clauses.append(negate(new_clause))
        new = set()
        for i in range(len(clauses)):
            for j in range(i + 1, len(clauses)):
                resolvents = resolve(clauses[i], clauses[j])
                if not resolvents:
                    return True  # A contradiction has been found
                new.update(resolvents)
        if new.issubset(kb.clauses):
            return False  # No new knowledge can be gained
        kb.clauses.update(new)

class Agent:
    def __init__(self, board, num_arrows, wumpus_locations, ax, ay):
        self.board = board
        self.num_arrows = num_arrows
        self.kb = KB()
        self.kb.tell(Predicate('HaveArrow', []))  # Provide an empty list of args
        self.kb.tell(Predicate('WumpusAlive', []))  # Provide an empty list of args
        self.wumpus_locations = []
        self.location = (ax, ay)

    def update_kb(self):
        precepts = self.board.get_percept(self.location[0], self.location[1])
        for precept in precepts:
            if precept == 'stench':
                self.kb.tell(Predicate('stench', [self.location[0], self.location[1]]))
            elif precept == 'breeze':
                self.kb.tell(Predicate('breeze', [self.location[0], self.location[1]]))
            elif precept == 'glimmer':
                self.kb.tell(Predicate('glimmer', [self.location[0], self.location[1]]))

    def move(self, direction):
        if direction == 'up':
            self.location = (self.location[0], self.location[1] - 1)
        elif direction == 'down':
            self.location = (self.location[0], self.location[1] + 1)
        elif direction == 'left':
            self.location = (self.location[0] - 1, self.location[1])
        elif direction == 'right':
            self.location = (self.location[0] + 1, self.location[1])

        self.update_kb()
        self.make_safe_move()

    def shoot(self, direction):
        if self.num_arrows <= 0:
            return

        if direction == 'up':
            board.shoot_up()
            # target_location = (self.location[0], self.location[1] + 1)
        elif direction == 'down':
            board.shoot_down()
            # target_location = (self.location[0], self.location[1] - 1)
        elif direction == 'left':
            board.shoot_left()
            # target_location = (self.location[0] - 1, self.location[1])
        elif direction == 'right':
            board.shoot_right()
            # target_location = (self.location[0] + 1, self.location[1])

        # if target_location in self.wumpus_locations:
        #     self.kb.tell(Predicate('WumpusDead'))
        #     self.wumpus_locations.remove(target_location)
        
        self.num_arrows -= 1

    def make_safe_move(self):
        # Check adjacent cells for 'breeze' or 'stench'
        adjacent_cells = [
            (self.location[0], self.location[1] - 1),  # Up
            (self.location[0], self.location[1] + 1),  # Down
            (self.location[0] - 1, self.location[1]),  # Left
            (self.location[0] + 1, self.location[1])   # Right
        ]

        for adj_cell in adjacent_cells:
            if not fol_resolution(self.kb, Predicate('safe', [adj_cell[0], adj_cell[1]])):
                # if 'breeze' in self.board.get_percept(adj_cell[0], adj_cell[1]) or 'stench' in self.board.get_percept(adj_cell[0], adj_cell[1]):
                for item in self.board.get_percept(adj_cell[0], adj_cell[1]):
                    if 'stench' or 'breeze' in item:
                        # It's not safe to move to the adjacent cell
                        self.kb.tell(Predicate('Notsafe', [adj_cell[0], adj_cell[1]]))

        # Now, check if the current cell is marked as 'Notsafe'
        if fol_resolution(self.kb, Predicate('Notsafe', [self.location[0], self.location[1]])):
            print("Unsafe move detected! Avoiding...")
            # Implement logic to choose a safe move

    def teleport(self, x, y):
        self.location = (x, y)
        self.update_kb()
        self.make_safe_move()

    def explore(self):
        while True:
            print("Exploring")
            # 1. Check for glimmer (gold)
            # if 'glimmer' in self.board.get_percept(self.location[0], self.location[1]):
            for item in self.board.get_percept(self.location[0], self.location[1]):
                if 'glimmer' in item:
                    print("Agent found gold!")
                    # Implement code to grab the gold, then return to the entrance if necessary
                    return

            # 2. Use logical inference to decide the next move
            next_move = self.decide_next_move()

            if next_move is None:
                print("Agent cannot make a safe move. Exiting exploration.")
                return

            # 3. Execute the chosen move
            if next_move.startswith('move'):
                self.move(next_move.replace('move ', ''))
            elif next_move.startswith('shoot'):
                self.shoot(next_move.replace('shoot ', ''))

    def decide_next_move(self):
        # Use logical inference to decide the next move

        # Check for 'stench' and 'breeze' in the current location
        # if 'stench' in self.board.get_percept(self.location[0], self.location[1]):
        for item in self.board.get_percept(self.location[0], self.location[1]):
            if 'stench' in item:
                self.kb.tell(Predicate('stench', [self.location[0], self.location[1]]))
        # if 'breeze' in self.board.get_percept(self.location[0], self.location[1]):
        for item in self.board.get_percept(self.location[0], self.location[1]):
            if 'breeze' in item:
                self.kb.tell(Predicate('breeze', [self.location[0], self.location[1]]))

        # Implement logical inference to determine the next move based on the agent's current knowledge.
        # This can involve resolution, goal-based reasoning, and other logical reasoning methods.

        # For example, check if there is a safe move based on the current knowledge.
        safe_moves = []
        for move in ['up', 'down', 'left', 'right']:
            new_location = self.get_new_location(move)
            board.print_formatted_board()
            query = Predicate('safe', [new_location[0], new_location[1]])
            if fol_resolution(self.kb, query):
                safe_moves.append(move)

        if safe_moves:
            return safe_moves[0]  # Choose the first safe move
        else:
            return None  # No safe move is found, consider backtracking or other strategies

    def get_new_location(self, direction):
        if direction == 'up':
            board.move_up()
            return (self.location[0], self.location[1] - 1)
        elif direction == 'down':
            board.move_down()
            return (self.location[0], self.location[1] + 1)
        elif direction == 'left':
            board.move_left()
            return (self.location[0] - 1, self.location[1])
        elif direction == 'right':
            board.move_right()
            return (self.location[0] + 1, self.location[1])
        
if __name__ == "__main__":
    # Define the Wumpus World environment
    # You need to create a 'Board' class or similar to represent the environment
    # and define methods like 'move', 'shoot', 'get_percept', and 'teleport'.

    # Initialize the Wumpus World board (replace with your own 'Board' class)
    filename = os.path.join('caves', '10x10-1.cave')
    board = WumpusWorld(filename)

    ax, ay = board.get_agent_coordinates()
    num_arrows = board.get_arrows()
    wumpus_locations = []  # for when I was trying to teach the agent to hunt the wumpus

    # Create the agent
    agent = Agent(board, num_arrows, wumpus_locations, ax, ay)

    # Start the exploration
    agent.explore()