import os

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
            self.num_safe = 0
            self.num_wumpus = 0

            for part in header_parts:
                if 'Cave Size' in part:
                    cave_size_part = part.split(':')[1].strip()
                    self.cave_size = int(cave_size_part.split('x')[0])  # Set cave size
                    self.num_safe = int(cave_size_part.split('x')[1])

            self.cave = [[[] for _ in range(self.cave_size)] for _ in range(self.cave_size)]

            for i in range(1, len(lines)):
                row = lines[i].strip('[]\n').split('],[')
                for j in range(len(row)):
                    self.cave[i-1][j] = row[j].split(',')

    def debug(self, x, y):
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
                    # elif 'stench' in item:                #If you want to see stench and breeze these are here but I don't
                    #     formatted_cell = "[?]"
                    # elif 'breeze' in item:
                    #     formatted_cell = "[~]"
                    elif 'wall' in item:
                        formatted_cell = "[W]"
                if not formatted_cell:
                    formatted_cell = "[ ]"  # Default for empty cell
                if x == self.agent_x and y == self.agent_y:
                    formatted_cell = "[a]"  # Agent position
                formatted_row.append(formatted_cell)
            print("".join(formatted_row))

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
        if not self.game_over:
            for x in range(self.agent_x - 1, -1, -1):
                if 'wumpus' in self.cave[self.agent_y][x]:
                    self.update_cell(x, self.agent_y, 'wall')
                    return True
            return False

    def shoot_up(self):
        if not self.game_over:
            for y in range(self.agent_y - 1, -1, -1):
                if 'wumpus' in self.cave[y][self.agent_x]:
                    self.update_cell(self.agent_x, y, 'wall')
                    return True
            return False

    def shoot_right(self):
        if not self.game_over:
            for x in range(self.agent_x + 1, self.cave_size):
                if 'wumpus' in self.cave[self.agent_y][x]:
                    self.update_cell(x, self.agent_y, 'wall')
                    return True
            return False

    def shoot_down(self):
        if not self.game_over:
            for y in range(self.agent_y + 1, self.cave_size):
                if 'wumpus' in self.cave[y][self.agent_x]:
                    self.update_cell(self.agent_x, y, 'wall')
                    return True
            return False

if __name__ == "__main__":
    filename = os.path.join('caves', '10x10-1.cave')
    game = WumpusWorld(filename)
    game.print_formatted_board()

    while not game.is_game_over():
        user_input = input("Enter 'w' to move up, 'a' to move left, 's' to move down, 'd' to move right, or 'q' to quit: ")

        if user_input == 'w':
            game.move_up()
        elif user_input == 'a':
            game.move_left()
        elif user_input == 's':
            game.move_down()
        elif user_input == 'd':
            game.move_right()
        elif user_input == 'sw':
            if (game.shoot_up):
                print("You hear a squeel")
            else: print("You miss and are down an arrow.")
        elif user_input == 'sa':
            if (game.shoot_left):
                print("You hear a squeel")
            else: print("You miss and are down an arrow.")
        elif user_input == 'ss':
            if (game.shoot_down):
                print("You hear a squeel")
            else: print("You miss and are down an arrow.")
        elif user_input == 'sd':
            if (game.shoot_right):
                print("You hear a squeel")
            else: print("You miss and are down an arrow.")
        elif user_input == 'q':
            break  # Quit the game
        else:
            print("Invalid input. Please enter 'w', 'a', 's', 'd', or 'q'.")

        game.print_formatted_board()

        # Check for stench and breeze and inform the player
        if game.is_stench():
            print("You smell a stench!")
        if game.is_breeze():
            print("You feel a breeze!")

    # game.teleport_agent(x, y)
    # game.get_agent_coordinates()
