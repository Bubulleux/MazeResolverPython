from tkinter import *
import random
import sys
import colorsys
import time

def hsv_to_rgb2(h, s, v):
        if s == 0.0: v*=255; return (v, v, v)
        i = int(h*6.) # XXX assume int() truncates!
        f = (h*6.)-i; p,q,t = int(255*(v*(1.-s))), int(255*(v*(1.-s*f))), int(255*(v*(1.-s*(1.-f)))); v*=255; i%=6
        if i == 0: return (v, t, p)
        if i == 1: return (q, v, p)
        if i == 2: return (p, v, t)
        if i == 3: return (p, q, v)
        if i == 4: return (t, p, v)
        if i == 5: return (v, p, q)

def hsvToHex(h,s,v):
    return "#%02x%02x%02x" %  hsv_to_rgb2(h,s,v)


class cell:
    whall = False
    groupCellsIndex = 2
    distAtStart = -1

class Maze:
    map = []
    row = 0
    col = 0
    breakabel_whall = []
    def mazeIsComplex(self):
        for row in self.map:
            for col in row:
                if not col.whall and col.groupCellsIndex !=  self.map[1][1].groupCellsIndex:
                    return False
        return True

    def findDestructibleWhall(self):
        print(len(self.breakabel_whall))
        rnd = random.Random()
        index = rnd.randint(0, len(self.breakabel_whall) - 1)
        pos = self.breakabel_whall[index]
        del self.breakabel_whall[index]
        return pos;

    def makeComplexMaze(self):
        while not self.mazeIsComplex():
            rnd = random.Random()
            cell_1 = []
            cell_2 = []
            whall = self.findDestructibleWhall()
            if whall[0] % 2 == 0:
                cell_1 = [whall[0] - 1 , whall[1]]
                cell_2 = [whall[0] + 1 , whall[1]]
            else:
                cell_1 = [whall[0], whall[1] - 1]
                cell_2 = [whall[0], whall[1] + 1]
            print(f"{cell_1[0]},{cell_1[1]}  {self.map[cell_1[0]][cell_1[1]].groupCellsIndex}  {whall[0]} {whall[1]}")
            if self.map[cell_1[0]][cell_1[1]].groupCellsIndex != self.map[cell_2[0]][cell_2[1]].groupCellsIndex:
                self.map[whall[0]][whall[1]].whall = False
                self.map[whall[0]][whall[1]].groupCellsIndex = self.map[cell_1[0]][cell_1[1]].groupCellsIndex
                valueDel = self.map[cell_2[0]][cell_2[1]].groupCellsIndex
                for row in range(self.row):
                    for col in range(self.row):
                        if self.map[row][col].groupCellsIndex == valueDel:
                            self.map[row][col].groupCellsIndex = self.map[cell_1[0]][cell_1[1]].groupCellsIndex 
        for x in range(100):
            if len(self.breakabel_whall) <= 100:
                break
            whall = self.findDestructibleWhall()
            self.map[whall[0]][whall[1]].whall = False
        self.map[1][0].whall = False
        self.map[self.row-2][self.row-1].whall = False
        self.map[self.row-2][self.row-1].distAtStart = 0

    def generateMaze(self):
        self.map = [[cell() for col in range(self.col)] for row in range(self.row)]
        size = self.row
        if size % 2 == 0:
            size  += 1
        i = 0
        for row in range(size):
            for col in range(size):
                is_whall = (row % 2 == 0) or (col % 2 == 0) or row == 0 or row == size-1 or col == 0 or col == size-1
                self.map[row][col].whall = is_whall
                if ((row % 2 == 0) ^ (col % 2 == 0)) and row != 0 and row != size-1 and col != 0 and col != size-1:
                    self.breakabel_whall.append([row, col])
                if not is_whall:
                    self.map[row][col].groupCellsIndex = i
                    i += 1
        self.makeComplexMaze()

    def findWay(self):
        futurMap = self.map
        for row in range(len(self.map)):
            for col in range(len(self.map)):
                if not self.map[row][col].whall and self.map[row][col].distAtStart == -1:
                    posToCheck = [[0,1],[0,-1],[1,0],[-1,0]]
                    if row == 1 and col == 0:
                        posToCheck = [[0,1]]
                    for pos in posToCheck:
                        if self.map[row + pos[0]][ col + pos[1]].distAtStart != -1:
                            futurMap[row][col].distAtStart = self.map[row + pos[0]][ col + pos[1]].distAtStart + 1
                            break
        self.map = futurMap


def makeCellsMap(rows, cols, cell_size):
    cellsMap = [[0 for col in range(cols)] for row in range(rows)]
    for row in range(rows):
        for col in range(cols):
            cellsMap[row][col] = canvas.create_rectangle(col * cell_size, row * cell_size, (col + 1) * cell_size, (row + 1) * cell_size, outline="")
    return cellsMap

def updateCellsMap(maze, cellsMap, size):
    for row in range(size):
        for col in range(size):
            color = "black" if maze[row][col].whall else ("white" if maze[row][col].distAtStart == -1 else hsvToHex(maze[row][col].distAtStart * 0.003,1,1))
            canvas.itemconfig(cellsMap[row][col], fill = color)
    root.update()
    



def launch():
    cellsMap = makeCellsMap(rows, cols, cell_size)
    maze = Maze()
    maze.row = rows
    maze.col = cols
    maze.generateMaze()
    updateCellsMap(maze.map ,cellsMap, rows)
    print(f"len map : {len(maze.map)}, len cell {len(cellsMap)}")
    while maze.map[1][0].distAtStart == -1:
        maze.findWay()
        updateCellsMap(maze.map ,cellsMap, rows)


print(hsvToHex(0.91,1,1))
root = Tk()
root.title("Maze Resolver")
root.resizable(width = False, height = False)
cell_size = 3;
rows = 201
cols = 201
canvas_width = cols * cell_size
canvas_height = rows * cell_size
canvas = Canvas(root, width = canvas_width, height = canvas_height)
canvas.grid(column=0, row=0)
cellsMap = []
btnLaunch = Button(root, text = "Launch", command = launch)
btnLaunch.grid(column=0,row=1)
root.mainloop()
