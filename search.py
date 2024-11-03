from models.maze import Maze
from collections import deque
import OpenGL.GL as gl
from util import coords_to_glcoords

import pygame

def bfs(maze: Maze):
    starting_cell = 0
    destination_cell = len(maze.grid[0]) - 1
    queue = deque()
    queue.append(starting_cell)
    visited = {starting_cell}

    while queue:
        current = queue.popleft()
        if current == destination_cell:
            return
 
        neighbours = maze.get_visitable_neighbours(current)
        unvisited_neigbours = [x for x in neighbours if x != -1 and x not in visited]
        for n in unvisited_neigbours:
            visited.add(n)
            queue.append(n)

    pass
