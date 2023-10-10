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
            print(f'Values at coordinates ({x}, {y}): {", ".join(values)}')
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
        print(f"Safe spaces remaining: {self.num_safe}")


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

    def is_glitter(self, x, y):
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
                self.is_glitter(self.agent_x, self.agent_y)

    def move_down(self):
        if not self.game_over:
            if self.agent_y < self.cave_size - 1 and not self.hit_wall(self.agent_x, self.agent_y + 1):
                self.cave[self.agent_y][self.agent_x] = [item for item in self.cave[self.agent_y][self.agent_x] if item != 'agent']
                self.agent_y += 1
                self.cave[self.agent_y][self.agent_x].append('agent')
                self.is_bad(self.agent_x, self.agent_y)
                self.is_glitter(self.agent_x, self.agent_y)

    def move_left(self):
        if not self.game_over:
            if self.agent_x > 0 and not self.hit_wall(self.agent_x - 1, self.agent_y):
                self.cave[self.agent_y][self.agent_x] = [item for item in self.cave[self.agent_y][self.agent_x] if item != 'agent']
                self.agent_x -= 1
                self.cave[self.agent_y][self.agent_x].append('agent')
                self.is_bad(self.agent_x, self.agent_y)
                self.is_glitter(self.agent_x, self.agent_y)

    def move_right(self):
        if not self.game_over:
            if self.agent_x < self.cave_size - 1 and not self.hit_wall(self.agent_x + 1, self.agent_y):
                self.cave[self.agent_y][self.agent_x] = [item for item in self.cave[self.agent_y][self.agent_x] if item != 'agent']
                self.agent_x += 1
                self.cave[self.agent_y][self.agent_x].append('agent')
                self.is_bad(self.agent_x, self.agent_y)
                self.is_glitter(self.agent_x, self.agent_y)

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

    def get_agent_coordinates(self):
        return self.agent_x, self.agent_y
    
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

class FOLEngine:
    def __init__(self):
        self.knowledge_base = []

    def tell(self, sentence):
        self.knowledge_base.append(sentence)

    def ask(self, query):
        for sentence in self.knowledge_base:
            if self.satisfies(sentence, query):
                return True
        return False

    def satisfies(self, sentence, query):
        # Implement the logic for checking if a sentence satisfies a query
        if sentence == query:
            return True
        return False

    def unify(self, var, x, substitution):
        if var in substitution:
            return self.unify(substitution[var], x, substitution)
        elif x in substitution:
            return self.unify(var, substitution[x], substitution)
        elif var != x:
            substitution[var] = x
            return substitution
        return substitution

class Agent:
    def __init__(self, engine):
        self.engine = engine
        self.percepts = []

    def perceive(self, percept):
        for item in percept:
            # Check if the specified cell contains a 'pit' or a 'wumpus'
            self.percepts.append(item)

    def decide(self):
        # Make decisions based on percepts and agent's knowledge
        for percept in self.percepts:
            if "stench" in percept:
                rule = "Wumpus nearby"  # Example rule: If there's a stench, there might be a Wumpus nearby
                self.engine.tell(rule)
            elif "breeze" in percept:
                rule = "Pit nearby"  # Example rule: If there's a breeze, there might be a pit nearby
                self.engine.tell(rule)
            elif "glitter" in percept:
                rule = "Gold nearby"  # Example rule: If there's a glitter, there might be gold nearby
                self.engine.tell(rule)

    def get_action(self):
        # Implement agent's action selection logic here
        # For simplicity, let's assume the agent moves randomly (without reasoning)

        possible_actions = ["move_up", "move_down", "move_left", "move_right"]

        # Randomly select an action
        selected_action = random.choice(possible_actions)

        return selected_action

class KnowledgeBase:
    def __init__(self):
        self.knowledge = []

    def add_knowledge(self, sentence):
        self.knowledge.append(sentence)

    def query(self, query):
        for sentence in self.knowledge:
            if self.unify(query, sentence):
                return True
        return False

    def unify(self, var, x, substitution):
        if var in substitution:
            return self.unify(substitution[var], x, substitution)
        elif x in substitution:
            return self.unify(var, substitution[x], substitution)
        elif var != x:
            substitution[var] = x
            return substitution
        return substitution

if __name__ == "__main__":
    filename = os.path.join('caves', '10x10-1.cave')
    game = WumpusWorld(filename)
    engine = FOLEngine()
    agent = Agent(engine)
    knowledge_base = KnowledgeBase()

    while not game.is_game_over():
        percept = game.get_percept(game.agent_x, game.agent_y)  # Get percept from the game
        agent.perceive(percept)  # Update agent's knowledge based on percept
        agent.decide()  # Make a decision based on agent's knowledge
        action = agent.get_action()  # Get the agent's action

        # Take the selected action in the game
        if action == "move_up":
            game.move_up()
        elif action == "move_down":
            game.move_down()
        elif action == "move_left":
            game.move_left()
        elif action == "move_right":
            game.move_right()
        elif action == "shoot_up":
            game.shoot_up()
        elif action == "shoot_down":
            game.shoot_down()
        elif action == "shoot_left":
            game.shoot_left()
        elif action == "shoot_right":
            game.shoot_right()

    game.print_formatted_board()
    print(f"Agent coordinates: ({game.get_agent_coordinates()[0]}, {game.get_agent_coordinates()[1]})")