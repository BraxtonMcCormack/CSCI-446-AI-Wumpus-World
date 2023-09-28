import os
import random

class WumpusWorld:
    def __init__(self, filename):
        self.load_world(filename)
        self.agent_pos = (1, 1)  # Start from (1, 1) at the bottom left
        self.num_arrows = self.num_wumpus
        self.wumpus_positions = self.find_wumpus_positions()
        self.gold_found = 0
        self.wumpus_killed = 0
        self.pits_fallen = 0
        self.wumpus_kills = 0
        self.cells_explored = 0

    def load_world(self, filename):
        with open(filename, 'r') as file:
            lines = file.readlines()

        header = lines[0].strip()
        # Extract values using regular expressions
        import re
        match = re.match(r'Cave Size: (\d+)x(\d+), Number of Wumpus: (\d+), Number of safe: (\d+)', header)
        if match:
            self.cave_size = int(match.group(1))
            self.num_wumpus = int(match.group(3))
            self.num_safe = int(match.group(4))
        else:
            raise ValueError("Invalid header format in the cave file.")

        # Split each line using '],[' as the delimiter
        self.world = [line.strip().strip('[[').strip(']]').split('],[') for line in lines[1:]]


    def find_wumpus_positions(self):
        wumpus_positions = []
        for i in range(self.cave_size):
            for j in range(self.cave_size):
                if i < len(self.world) and j < len(self.world[i]):
                    cell_contents = self.world[i][j]
                    if cell_contents and any('wumpus' in cell for cell in cell_contents):
                        wumpus_positions.append((i, j))
        return wumpus_positions

    def is_safe(self, x, y):
        if x < 1 or x > self.cave_size or y < 1 or y > self.cave_size:
            return False

        # Adjust the indexing to match the 0-based index in Python lists
        if 'pit' in self.world[self.cave_size - x][y - 1]:  # Flip the coordinate system
            self.pits_fallen += 1
            return False
        if 'wumpus' in self.world[self.cave_size - x][y - 1]:  # Flip the coordinate system
            self.wumpus_kills += 1
            return False
        return True

    def print_cave(self):
        for row in self.world:
            print(' '.join([cell if cell else ' ' for cell in row]))
        print()

    def play_game(self):
        while True:
            self.cells_explored += 1
            self.print_cave()
            print(f"Agent's position: ({self.agent_pos[1]}, {self.agent_pos[0]})")
            print(f"Arrows left: {self.num_arrows}")
            print(f"Gold found: {self.gold_found}")
            print(f"Wumpus killed: {self.wumpus_killed}")
            print(f"Pits fallen into: {self.pits_fallen}")
            print(f"Wumpus kills: {self.wumpus_kills}")
            print(f"Total cells explored: {self.cells_explored}")

            if 'gold' in self.world[self.cave_size - self.agent_pos[0]][self.agent_pos[1] - 1]:  # Flip the coordinate system
                print("Agent found the gold! You win!")
                self.gold_found += 1
                break

            breeze = 'breeze' in self.world[self.cave_size - self.agent_pos[0]][self.agent_pos[1] - 1]  # Flip the coordinate system
            stench = 'stench' in self.world[self.cave_size - self.agent_pos[0]][self.agent_pos[1] - 1]  # Flip the coordinate system

            if breeze:
                print("Agent detects a breeze.")
            if stench:
                print("Agent detects a stench.")

            action = input("Enter 'w' to move up, 'a' to move left, 's' to move down, 'd' to move right, 'shoot' to shoot an arrow, or 'q' to quit: ").lower()
            print("=============================================")

            if action == 'q':
                print("Agent quit. Game over.")
                break
            elif action == 'shoot':
                if self.num_arrows > 0:
                    direction = input("Enter 'w' to shoot up, 'a' to shoot left, 's' to shoot down, 'd' to shoot right: ").lower()
                    if direction in ('w', 'a', 's', 'd'):
                        if self.shoot_arrow(direction):
                            print("Agent shot a wumpus! You hear a squeal.")
                            self.wumpus_killed += 1
                    else:
                        print("Invalid direction for shooting.")
                else:
                    print("No arrows left.")
            elif action in ('w', 'a', 's', 'd'):
                x, y = self.agent_pos
                if action == 'w':
                    x += 1  # Move up
                elif action == 'a':
                    y -= 1  # Move left
                elif action == 's':
                    x -= 1  # Move down
                elif action == 'd':
                    y += 1  # Move right

                # Check if the new position is within bounds, and if not, bounce back and inform the player
                if x < 1 or x > self.cave_size or y < 1 or y > self.cave_size:
                    print("Agent hit a wall. Bouncing back.")
                    x, y = self.agent_pos

                if self.is_safe(x, y):
                    self.agent_pos = (x, y)
            else:
                print("Invalid action.")

    def shoot_arrow(self, direction):
        x, y = self.agent_pos
        if direction == 'w':
            for i in range(x, -1, -1):
                if (i, y) in self.wumpus_positions:
                    self.wumpus_positions.remove((i, y))
                    self.num_arrows -= 1
                    return True
        elif direction == 'a':
            for j in range(y, -1, -1):
                if (x, j) in self.wumpus_positions:
                    self.wumpus_positions.remove((x, j))
                    self.num_arrows -= 1
                    return True
        elif direction == 's':
            for i in range(x, self.cave_size):
                if (i, y) in self.wumpus_positions:
                    self.wumpus_positions.remove((i, y))
                    self.num_arrows -= 1
                    return True
        elif direction == 'd':
            for j in range(y, self.cave_size):
                if (x, j) in self.wumpus_positions:
                    self.wumpus_positions.remove((x, j))
                    self.num_arrows -= 1
                    return True
        return False

if __name__ == "__main__":
    filename = os.path.join('caves', '05x05-1.cave')
    game = WumpusWorld(filename)
    game.play_game()