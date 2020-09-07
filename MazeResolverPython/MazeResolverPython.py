from tkinter import *
import random
import sys


class cell:
    whall = False
    groupCellsIndex = 2

def mazeIsComplex(maze):
    return random.randint(0, 10) == 0
    for row in maze:
        for col in row:
            if not col.whall and col.groupCellsIndex !=  maze[1][1].groupCellsIndex:
                return False
    return True

def generateMaze(size):
    maze = [[cell() for col in range(cols)] for row in range(rows)]
    if size % 2 == 0:
        size  += 1
    i = 0
    for row in range(size):
        for col in range(size):
            is_whall = (row % 2 == 0) or (col % 2 == 0) or row == 0 or row == size-1 or col == 0 or col == size-1
            maze[row][col].whall = is_whall
            if not is_whall:
                maze[row][col].groupCellsIndex = i
                i += 1
    maze = makeComplexMaze(maze ,size)
    return maze

def makeComplexMaze(_maze ,size):
    maze = _maze
    while not mazeIsComplex(maze):
            rnd = random.Random()
            cell_1 = []
            cell_2 = []
            x = rnd.randint(1, size - 2)
            y = 0
            if x % 2 == 0:
                y = rnd.randint(0, ((size - 1) / 2) -1) * 2 +1
                cell_1 = [x, y - 1]
                cell_2 = [x, y + 1]
            else:
                y = rnd.randint(0, ((size - 1) / 2) -2) * 2 +2
                cell_1 = [x - 1 , y]
                cell_2 = [x + 1 , y]
            maze[x][y].whall = False
            maze[x][y].groupCellsIndex = maze[cell_1[0]][cell_1[1]].groupCellsIndex
            valueDel = maze[cell_2[0]][cell_2[1]].groupCellsIndex
            for row in range(size):
                for col in range(size):
                    if maze[row][col].groupCellsIndex == valueDel:
                        print(maze[9][1].groupCellsIndex)
                        maze[row][col].groupCellsIndex = maze[cell_1[0]][cell_1[1]].groupCellsIndex
            print(f"{cell_1[0]},{cell_1[1]}  {maze[cell_1[0]][cell_1[1]].groupCellsIndex}")
    return maze
        


def makeCellsMap(rows, cols, cell_size):
    cellsMap = [[0 for col in range(cols)] for row in range(rows)]
    for row in range(rows):
        for col in range(cols):
            cellsMap[row][col] = canvas.create_rectangle(col * cell_size, row * cell_size, (col + 1) * cell_size, (row + 1) * cell_size)
    return cellsMap

def updateCellsMap(maze, cellsMap, size):
    for row in range(size):
        for col in range(size):
            canvas.itemconfig(cellsMap[row][col], fill = ("black" if maze[row][col].whall else "white"))

def launch():
    cellsMap = makeCellsMap(rows, cols, cell_size)
    maze = generateMaze(rows)
    updateCellsMap(maze ,cellsMap, rows)

root = Tk()
root.title("Maze Resolver")
root.resizable(width = False, height = False)
cell_size = 15;
rows = 11
cols = 11
canvas_width = cols * cell_size
canvas_height = rows * cell_size
canvas = Canvas(root, width = canvas_width, height = canvas_height)
canvas.grid(column=0, row=0)
cellsMap = []
btnLaunch = Button(root, text = "Launch", command = launch)
btnLaunch.grid(column=0,row=1)
root.mainloop()
