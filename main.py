import os
import random

class WumpusWorld:
    def __init__(self, filename):
        self.board = []
        self.arrows = 0
        self.gold_found = False
        self.wumpus_killed = 0
        self.pit_falls = 0
        self.wumpus_kills = 0
        self.total_cells_explored = 0
        self.load_board(filename)

        # Set the initial agent position to the bottom-left corner
        self.agent_position = (len(self.board) - 1, 0)
        self.scent = False
        self.breeze = False

    def load_board(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()
            for i, line in enumerate(reversed(lines)):  # Reverse lines to make the bottom-left corner (0, 0)
                row = line.strip()[2:-2]  # Remove outer brackets and leading/trailing spaces
                cell_data = row.split("],[")
                row_data = []
                for cell in cell_data:
                    flags = cell.split(",")
                    cell_flags = [flag.strip(" '") for flag in flags]
                    if 'wumpus' in cell_flags:
                        self.arrows += 1
                    row_data.append(cell_flags)
                self.board.insert(0, row_data)  # Insert at the beginning of the board

    def print_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if (i, j) == self.agent_position:
                    print('[a]', end=' ')
                elif 'gold' in self.board[i][j] and not self.gold_found:
                    print('[G]', end=' ')
                elif 'pit' in self.board[i][j]:
                    print('[o]', end=' ')
                elif 'wumpus' in self.board[i][j]:
                    print('[W]', end=' ')
                elif 'stench' in self.board[i][j] and self.scent:
                    print('[S]', end=' ')
                elif 'breeze' in self.board[i][j] and self.breeze:
                    print('[B]', end=' ')
                elif 'safe' in self.board[i][j] and len(self.board[i][j]) == 1:
                    print('[ ]', end=' ')
                else:
                    print('[W]', end=' ')
            print()  # Move to the next row

    def move(self, direction):
        x, y = self.agent_position
        if direction == "w" and x > 0:
            x -= 1
        elif direction == "s" and x < len(self.board) - 1:
            x += 1
        elif direction == "a" and y > 0:
            y -= 1
        elif direction == "d" and y < len(self.board[self.agent_position[0]]) - 1:
            y += 1
        
        self.agent_position = (x, y)
        self.total_cells_explored += 1

        # Check for breeze and stench in the new cell
        self.scent = 'stench' in self.board[x][y]
        self.breeze = 'breeze' in self.board[x][y]

        if 'gold' in self.board[x][y]:
            self.gold_found = True

        if 'pit' in self.board[x][y]:
            self.pit_falls += 1
            # End the game if the agent falls into a pit
            print("You fell into a pit! Game over.")
            self.print_board()
            return True

        if 'wumpus' in self.board[x][y]:
            # End the game if the agent encounters a wumpus
            if self.arrows > 0:
                print("You were killed by a wumpus! Game over.")
                self.arrows -= 1
                self.wumpus_kills += 1
                self.board[x][y].remove('wumpus')
                self.agent_position = (len(self.board) - 1, 0)  # Reset agent position
                self.scent = False  # Reset scent
                self.breeze = False  # Reset breeze
            else:
                print("You were killed by a wumpus, and you're out of arrows! Game over.")
                self.print_board()
                return True

        return False

    def shoot(self, direction):
        x, y = self.agent_position

        if direction == "w":
            for i in range(x, -1, -1):
                if 'wumpus' in self.board[i][y]:
                    self.board[i][y].remove('wumpus')
                    print("You hear a scream! You killed a wumpus!")
                    self.wumpus_killed += 1
                    break
        elif direction == "s":
            for i in range(x, len(self.board)):
                if 'wumpus' in self.board[i][y]:
                    self.board[i][y].remove('wumpus')
                    print("You hear a scream! You killed a wumpus!")
                    self.wumpus_killed += 1
                    break
        elif direction == "a":
            for j in range(y, -1, -1):
                if 'wumpus' in self.board[x][j]:
                    self.board[x][j].remove('wumpus')
                    print("You hear a scream! You killed a wumpus!")
                    self.wumpus_killed += 1
                    break
        elif direction == "d":
            for j in range(y, len(self.board[i])):
                if 'wumpus' in self.board[x][j]:
                    self.board[x][j].remove('wumpus')
                    print("You hear a scream! You killed a wumpus!")
                    self.wumpus_killed += 1
                    break

    def random_move(self):
        directions = ['w', 'a', 's', 'd']
        safe_moves = []
        for direction in directions:
            x, y = self.agent_position
            if direction == "w" and x > 0:
                x -= 1
            elif direction == "s" and x < len(self.board) - 1:
                x += 1
            elif direction == "a" and y > 0:
                y -= 1
            elif direction == "d" and y < len(self.board[self.agent_position[0]]) - 1:
                y += 1

            if 'pit' not in self.board[x][y] and 'wumpus' not in self.board[x][y]:
                safe_moves.append(direction)

        if safe_moves:
            return random.choice(safe_moves)
        else:
            return None

    def play_game(self):
        while not self.gold_found:
            self.print_board()
            action = input("Enter 'WASD' to move or 'S' to shoot an arrow (Q to quit): ").lower()

            if action == 'q':
                print("Quitting the game.")
                break

            if action in ['w', 'a', 's', 'd']:
                if self.move(action):
                    break
            elif action == 's' and self.arrows > 0:
                direction = input("Enter direction to shoot (W, A, S, D): ").lower()
                self.arrows -= 1
                self.shoot(direction)

        if self.gold_found:
            self.print_board()
            print("You found the gold! You win!")

if __name__ == "__main__":
    filename = os.path.join('caves', '05x05-1.cave')
    game = WumpusWorld(filename)
    game.play_game()
