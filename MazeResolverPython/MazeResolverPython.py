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
    toUpdate = []
    cellsNeedUpdate = []
    def mazeIsComplex(self):
        for row in self.map:
            for col in row:
                if not col.whall and col.groupCellsIndex !=  self.map[1][1].groupCellsIndex:
                    return False
        return True

    

    def makeComplexMaze(self):
        while not self.mazeIsComplex():
            rnd = random.Random()
            cell_1 = []
            cell_2 = []
            index = random.randint(0, len(self.breakabel_whall) - 1)
            whall = self.breakabel_whall[index]
            if whall[0] % 2 == 0:
                cell_1 = [whall[0] - 1 , whall[1]]
                cell_2 = [whall[0] + 1 , whall[1]]
            else:
                cell_1 = [whall[0], whall[1] - 1]
                cell_2 = [whall[0], whall[1] + 1]
            if self.map[cell_1[0]][cell_1[1]].groupCellsIndex != self.map[cell_2[0]][cell_2[1]].groupCellsIndex:
                del self.breakabel_whall[index]
                self.map[whall[0]][whall[1]].whall = False
                self.map[whall[0]][whall[1]].groupCellsIndex = self.map[cell_1[0]][cell_1[1]].groupCellsIndex
                valueDel = self.map[cell_2[0]][cell_2[1]].groupCellsIndex
                for row in range(self.row):
                    for col in range(self.row):
                        if self.map[row][col].groupCellsIndex == valueDel:
                            self.map[row][col].groupCellsIndex = self.map[cell_1[0]][cell_1[1]].groupCellsIndex 
        for x in range(10):
            if len(self.breakabel_whall) <= 100:
                break
            index = random.randint(0, len(self.breakabel_whall) - 1)
            whall = self.breakabel_whall[index]
            del self.breakabel_whall[index]
            self.map[whall[0]][whall[1]].whall = False
        self.map[1][0].whall = False
        self.map[self.row-2][self.row-1].whall = False
        self.map[self.row-2][self.row-1].distAtStart = 0
        self.toUpdate.append([self.row-2 , self.row-2])

    def generateMaze(self):
        self.cellsNeedUpdate.clear()
        self.map = [[cell() for col in range(self.col)] for row in range(self.row)]
        for row in range(self.row):
            for col in range(self.col):
                self.cellsNeedUpdate.append([row, col])
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
        #self.cellsNeedUpdate.clear()
        futurMap = self.map
        futurToUpdate = []
        for updateCell in self.toUpdate:
            row = updateCell[0]
            col = updateCell[1]
            posToCheck = [[0,1],[0,-1],[1,0],[-1,0]]
            if row == 1 and col == 0:
                posToCheck = [[0,1]]
            for pos in posToCheck:
                if self.map[row + pos[0]][ col + pos[1]].distAtStart != -1:
                    futurMap[row][col].distAtStart = self.map[row + pos[0]][ col + pos[1]].distAtStart + 1
                    self.cellsNeedUpdate.append([row, col])
                elif self.map[row + pos[0]][ col + pos[1]].whall == False:
                    futurToUpdate.append([row + pos[0], col + pos[1]])
        self.toUpdate = futurToUpdate
        self.map = futurMap


def makeCellsMap(rows, cols, cell_size, maze):
    cellsMap = [[0 for col in range(cols)] for row in range(rows)]
    for row in range(rows):
        for col in range(cols):
            if maze[row][col].whall == True:
                continue
            cellsMap[row][col] = canvas.create_rectangle(col * cell_size, row * cell_size, (col + 1) * cell_size, (row + 1) * cell_size, outline="")
    return cellsMap

def updateCellsMap(maze, cellsMap, cellsAtUpdate):
    for xcell in cellsAtUpdate:
        color = "black" if maze[xcell[0]][xcell[1]].whall else ("white" if maze[xcell[0]][xcell[1]].distAtStart == -1 else hsvToHex(maze[xcell[0]][xcell[1]].distAtStart * 0.003,1,1))
        canvas.itemconfig(cellsMap[xcell[0]][xcell[1]], fill = color)
    root.update()
    



def launch():
    maze = Maze()
    maze.row = rows
    maze.col = cols
    maze.generateMaze()
    cellsMap = makeCellsMap(rows, cols, cell_size, maze.map)
    updateCellsMap(maze.map ,cellsMap, maze.cellsNeedUpdate)
    
    frame = 0
    while maze.map[1][0].distAtStart == -1:
        maze.findWay()
        if True:
            print(maze.cellsNeedUpdate)
            updateCellsMap(maze.map ,cellsMap, maze.cellsNeedUpdate)
            maze.cellsNeedUpdate.clear()
        frame += 1
    updateCellsMap(maze.map ,cellsMap, maze.cellsNeedUpdate)


root = Tk()
root.title("Maze Resolver")
root.resizable(width = False, height = False)
cell_size = 8;
rows = 51
cols = 51
canvas_width = cols * cell_size
canvas_height = rows * cell_size
canvas = Canvas(root, width = canvas_width, height = canvas_height, bg="Black")
canvas.grid(column=0, row=0)
cellsMap = []
btnLaunch = Button(root, text = "Launch", command = launch)
btnLaunch.grid(column=0,row=1)
root.mainloop()
