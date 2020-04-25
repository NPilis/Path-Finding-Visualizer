import pygame
import math
import tkinter as tk
from tkinter import *
from tkinter import messagebox
import os

# All needed global variables
W, H, N = (1000, 1000, 50)
col = row = N
black, white, blue, purple, green, red, yellow = ((0, 0, 0), (255, 255, 255), (234,84,85),
                                                  (128, 0, 128), (0, 203, 95), (55, 65, 64), (255, 255, 0))


# Representation of node
class Node:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.h = 0
        self.g = 0
        self.neighbors = []
        self.prev = None
        self.closed = False
        self.blocked = False
        self.value = 1

    def __repr__(self):
        return f'Node: {(self.x, self.y)}'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def update_node(self, color, thickness):
        if not self.closed:
            pygame.draw.rect(screen, color, (self.x * W // N, self.y * W // N, W // N, H // N), thickness)
            pygame.display.update()

    def add_neighbors1(self, grid):

        if self.x < col - 1 and not grid[self.x + 1][self.y].blocked:
            self.neighbors.append(grid[self.x + 1][self.y])

        if self.x > 0 and not grid[self.x - 1][self.y].blocked:
            self.neighbors.append(grid[self.x - 1][self.y])

        if self.y < row - 1 and not grid[self.x][self.y + 1].blocked:
            self.neighbors.append(grid[self.x][self.y + 1])

        if self.y > 0 and not grid[self.x][self.y - 1].blocked:
            self.neighbors.append(grid[self.x][self.y - 1])

        if self.x - 1 >= 0 and self.y - 1 >= 0 and not grid[self.x - 1][self.y - 1].blocked:
            self.neighbors.append(grid[self.x - 1][self.y - 1])

        if self.x - 1 >= 0 and self.y + 1 < row - 1 and not grid[self.x - 1][self.y + 1].blocked:
            self.neighbors.append(grid[self.x - 1][self.y + 1])

        if self.x + 1 < col - 1 and self.y - 1 >= 0 and not grid[self.x + 1][self.y - 1].blocked:
            self.neighbors.append(grid[self.x + 1][self.y - 1])

        if self.x + 1 < col - 1 and self.y + 1 < row - 1 and not grid[self.x + 1][self.y + 1].blocked:
            self.neighbors.append(grid[self.x + 1][self.y + 1])

    def add_neighbors2(self, grid):

        if self.x < col - 1 and not grid[self.x + 1][self.y].blocked:
            self.neighbors.append(grid[self.x + 1][self.y])

        if self.x > 0 and not grid[self.x - 1][self.y].blocked:
            self.neighbors.append(grid[self.x - 1][self.y])

        if self.y < row - 1 and not grid[self.x][self.y + 1].blocked:
            self.neighbors.append(grid[self.x][self.y + 1])

        if self.y > 0 and not grid[self.x][self.y - 1].blocked:
            self.neighbors.append(grid[self.x][self.y - 1])


# Creating row by col grid of Nodes and initializing neighbors
def create_grid():
    global grid
    screen.fill((210,210,210))
    grid = [0 for _ in range(col)]

    for i in range(col):
        grid[i] = [0 for _ in range(row)]

    for i in range(col):
        for j in range(row):
            grid[i][j] = Node(i, j)
            grid[i][j].update_node(white, 1)


def submit(start_node, end_node):
    global start
    global end

    s = start_node.get().split(',')
    e = end_node.get().split(',')
    start = grid[int(s[0])][int(s[1])]
    end = grid[int(e[0])][int(e[1])]
    start.update_node(yellow, 0)
    end.update_node(purple, 0)


def draw_block(pos):
    x_pos = pos[0]
    y_pos = pos[1]
    x = x_pos // (W // col)
    y = y_pos // (H // row)

    node = grid[x][y]
    if node != start and node != end and not node.blocked:
        node.blocked = True
        node.update_node(white, 0)


def create_neighbors():
    assertion = nb_type.get()
    if assertion:
        for i in range(col):
            for j in range(row):
                grid[i][j].add_neighbors2(grid)
    else:
        for i in range(col):
            for j in range(row):
                grid[i][j].add_neighbors1(grid)


def heurisitic(node):
    # h = math.sqrt((node.x - end.x) ** 2 + (node.y - end.y) ** 2)
    h = abs(node.x - end.x) + abs(node.y - end.y)
    return h


def find_lowest_f(lst):
    lowest_idx = 0
    for i in range(1, len(lst)):
        if lst[i].f < lst[lowest_idx].f:
            lowest_idx = i

    return lowest_idx


def find_lowest_g(lst):
    lowest_idx = 0
    for i in range(1, len(lst)):
        if lst[i].g < lst[lowest_idx].g:
            lowest_idx = i

    return lowest_idx


def a_star():
    create_neighbors()
    open_list = []
    closed_list = []
    open_list.append(start)

    while (len(open_list)) > 0:
        idx = find_lowest_f(open_list)
        current = open_list.pop(idx)
        closed_list.append(current)
        current.update_node(red, 0)

        if current == end:
            start.update_node(yellow, 0)
            while current != start:
                current.closed = False
                current.update_node(blue, 0)
                current = current.prev
            end.update_node(purple, 0)
            messagebox.showinfo("Result message", "Found the shortest path!")
            return

        for nb in current.neighbors:
            if nb.blocked:
                continue
            if nb not in closed_list:
                temp_g = current.g + current.value
                if nb in open_list:
                    if nb.g > temp_g:
                        nb.g = temp_g
                else:
                    nb.g = temp_g
                    open_list.append(nb)
                    nb.update_node(green, 0)

            nb.h = heurisitic(nb)
            nb.f = nb.g + nb.h

            if nb.prev is None:
                nb.prev = current

    messagebox.showinfo("Result message", "Couldn't find the shortest path")


def dijkstra():
    create_neighbors()
    open_list = []
    closed_list = []
    open_list.append(start)

    while len(open_list) > 0:
        idx = find_lowest_g(open_list)
        current = open_list.pop(idx)
        closed_list.append(current)
        current.update_node(red, 0)

        if current == end:
            start.update_node(yellow, 0)
            while current != start:
                current.closed = False
                current.update_node(blue, 0)
                current = current.prev
            end.update_node(purple, 0)
            messagebox.showinfo("Result message", "Found the shortest path!")
            return

        for nb in current.neighbors:
            if nb.blocked:
                continue
            if nb not in closed_list:
                temp_g = current.g + current.value
                if nb in open_list:
                    if nb.g > temp_g:
                        nb.g = temp_g
                else:
                    nb.g = temp_g
                    open_list.append(nb)
                    nb.update_node(green, 0)

            if nb.prev is None:
                nb.prev = current

    messagebox.showinfo("Result message", "Couldn't find the shortest path")


def bfs():
    pass


def dfs():
    pass


def main():
    global root
    global screen
    global nb_type

    root = tk.Tk()
    embed = tk.Frame(root, width=W, height=H)
    embed.pack(side=LEFT)

    buttonwin = tk.Frame(root, width=75, height=800)
    buttonwin.pack(side=LEFT, padx=20)

    Label(buttonwin, text='Starting node (x,y)').grid(row=0, column=0)
    Label(buttonwin, text='End node (x,y)').grid(row=2, column=0)
    Label(buttonwin, text='Start').grid(row=8, column=0)
    Label(buttonwin, text='End').grid(row=8, column=1, pady=(0, 10))
    Label(buttonwin, text='Visited').grid(row=10, column=0)
    Label(buttonwin, text='In Queue').grid(row=10, column=1)

    start_node = Entry(buttonwin)
    end_node = Entry(buttonwin)
    start_node.grid(row=1, column=0, pady=5, padx=10)
    end_node.grid(row=3, column=0, pady=5, padx=10)

    Button(buttonwin, text='Submit', command=lambda: submit(start_node, end_node)).grid(row=4, column=0)
    Button(buttonwin, text='A* algorithm', command=a_star).grid(row=0, column=1, pady=10)
    Button(buttonwin, text='Dijkstra algorithm', command=dijkstra).grid(row=1, column=1, pady=10)
    Button(buttonwin, text='Breadth-first search', command=bfs).grid(row=2, column=1, pady=10)
    Button(buttonwin, text='Depth-first search', command=dfs).grid(row=3, column=1, pady=10)
    Button(buttonwin, text='RESTART', bg='red', command=create_grid).grid(row=5, column=0, pady=(10, 60))
    Button(buttonwin, bg='yellow', relief=GROOVE, activebackground='yellow', borderwidth=0, height=1, width=2).grid(
        row=7, column=0)
    Button(buttonwin, bg='purple', relief=GROOVE, borderwidth=0, height=1, width=2).grid(row=7, column=1)
    Button(buttonwin, bg='red', relief=GROOVE, borderwidth=0, height=1, width=2).grid(row=9, column=0)
    Button(buttonwin, bg='limegreen', relief=GROOVE, borderwidth=0, height=1, width=2).grid(row=9, column=1)
    nb_type = BooleanVar()
    Checkbutton(buttonwin, variable=nb_type, text="Cross neighbor").grid(row=4,column=1)

    os.environ['SDL_WINDOWID'] = str(embed.winfo_id())
    os.environ['SDL_VIDEODRIVER'] = 'windib'

    screen = pygame.display.set_mode((W, H))
    pygame.init()
    pygame.display.update()
    create_grid()

    while True:
        ev = pygame.event.get()

        for event in ev:
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if pygame.mouse.get_pressed()[0]:
                try:
                    pos = pygame.mouse.get_pos()
                    draw_block(pos)
                except NameError:
                    pass
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    break

        pygame.display.update()
        try:
            root.update()
        except TclError:
            return


main()
