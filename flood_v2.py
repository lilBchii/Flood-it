from matplotlib.colors import ListedColormap, BoundaryNorm
from matplotlib.pyplot import show, matshow, axis, pause, clf, text
from random import randint

# CONST.
COLORS = ListedColormap(
    [[1, 1, 1], [245 / 255, 64 / 255, 169 / 255], [245 / 255, 197 / 255, 100 / 255], [243 / 255, 163 / 255, 210 / 255],
     [139 / 255, 245 / 255, 132 / 255], [137 / 255, 180 / 255, 245 / 255]])
SCHEME = BoundaryNorm([0, 1, 2, 3, 4, 5, 6], COLORS.N)
SIZE = 8
COLORCHOICE = ["dp", "y", "p", "g", "b"]
INDEXATION = {"dp": 1, "y": 2, "p": 3, "g": 4, "b": 5}


class Cell():
    def __init__(self, **kwargs):
        self.x = kwargs["x"]
        self.y = kwargs["y"]
        self.color = kwargs["color"]

    def setColor(self, newColor):
        self.color = newColor

    def __repr__(self):
        return "y : " + str(self.y) + " | x : " + str(self.x) + " | color " + str(self.color)

    def __str__(self):
        return self.__repr__()


class Game():
    def __init__(self):
        self.cells = [[Cell(x=i, y=j, color=randint(1, 5)) for i in range(SIZE)] for j in range(SIZE)]
        self.isOver = False

    def map(self):
        return [[self.cells[j][i].color for i in range(SIZE)] for j in range(SIZE)]

    def getCell(self, y, x):
        return self.cells[y][x]

    def neighbors(self, cell):
        N = []
        cx, cy = cell.x, cell.y
        if cx > 0: N.append(game.getCell(cy, cx-1))
        if cx < SIZE - 1: N.append(game.getCell(cy, cx+1))
        if cy > 0: N.append(game.getCell(cy-1, cx))
        if cy < SIZE - 1: N.append(game.getCell(cy+1, cx))
        return N

    def askColor(self):
        inp = input("Your color: [dp] dark pink, [y]ellow, [p]ink, [g]reen, [b]lue ")
        if inp in COLORCHOICE:
            return INDEXATION[inp]
        return self.askColor() 

    def nextTurn(self):
        matshow(self.map(), fignum=1, cmap=COLORS, norm=SCHEME)
        axis("off")
        pause(0.1)


class Player():

    def __init__(self, game):
        self.cells = []
        self.game = game
        self.turns = 0
        self.flood(0, 0)

    def flood(self, y, x):
        cell = self.game.getCell(y, x)
        if cell not in self.cells: self.cells.append(cell)
        if len(self.cells) == SIZE*SIZE: self.game.isOver = True

    def capture(self, color):
        for cell in self.cells: cell.setColor(color)
#        print(len(self.cells))
        self.turns += 1


game = Game()
player = Player(game)
game.nextTurn()

while not game.isOver:
    color = game.askColor()
    # Capture phase
    for cell in player.cells:
        for neighbor in game.neighbors(cell):
#            print(f"checking neighbor of {cell} ||| {neighbor} ||| flooded ? {neighbor.color == player.cells[0].color}")
            if neighbor.color == player.cells[0].color:
                player.flood(neighbor.y, neighbor.x)
    player.capture(color)
    # Recovery phase
    for cell in player.cells:
        for neighbor in game.neighbors(cell):
            if neighbor.color == color:
                player.flood(neighbor.y, neighbor.x)
    game.nextTurn()
print(f"GAME OVER ({str(player.turns)} turns)")
show()
