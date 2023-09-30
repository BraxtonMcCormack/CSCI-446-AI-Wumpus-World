import Agent
class WumpusWorld:
    def __init__(self, caveFilename):
        self.agent = Agent.Agent()          #creates agent
        self.board, arrowsNeeded = load_board(caveFilename)  #generates board
        self.agent.setNumArrows(arrowsNeeded)   #sets amount of arrows agent has

    '''Prints board'''
    def print_board(self):
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                #if (i, j) == self.agent_position:
                #    print('[a]', end=' ')
                if 'gold' in self.board[i][j]: #and not self.gold_found:
                    print('[G]', end=' ')
                elif 'pit' in self.board[i][j]:
                    print('[P]', end=' ')
                elif 'wumpus' in self.board[i][j]:
                    print('[W]', end=' ')
                elif 'stench' in self.board[i][j]:# and self.scent:
                    print('[S]', end=' ')
                elif 'breeze' in self.board[i][j]:#and self.breeze:
                    print('[B]', end=' ')
                elif 'safe' in self.board[i][j] and len(self.board[i][j]) == 1:
                    print('[ ]', end=' ')
                else:
                    #print('[W]', end=' ')
                    pass
            print()  # Move to the next row


'''Converts csv into a 2d list. RETURNS: board, arrows'''
def load_board(fn):
    filename = "../caves/"+fn
    board = []
    arrows = 0       #counts number of arrows needed
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
                    arrows += 1
                row_data.append(cell_flags)
            board.insert(0, row_data)  # Insert at the beginning of the board
    return board, arrows    #board and number of arrows

def tempMain():
    ww = WumpusWorld('05x05-1.cave')
    ww.print_board()

tempMain()