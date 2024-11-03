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
        colour_maze(maze, visited, screen_size=(1000, 1000))
    pass


def dfs(maze: Maze, node: int = 0, destination: int | None = None, visited=None):
    if destination is None:
        destination = len(maze.grid[0]) - 1
    if visited is None:
        visited = set()
    if node == destination or destination in visited:
        return

    neighbours = maze.get_visitable_neighbours(node)
    unvisited_neighbours = [x for x in neighbours if x != -1 and x not in visited]
    for n in unvisited_neighbours:
        visited.add(n)
        colour_maze(maze, visited, (1000, 1000))
        dfs(maze, n, destination, visited)



def colour_maze(maze: Maze, visited: set[int], screen_size: tuple[int, int]):
    screen_width, _ = screen_size
    cell_size = screen_width / maze.grid_length
    gl.glColor3f(0.7, 0, 0.7)
    for node in visited:
        x, y = maze.get_coordinate(node)
        cell_x = x * cell_size
        cell_y = y * cell_size
        cell_x_end = cell_x + cell_size
        cell_y_end = cell_y + cell_size

        l1 = coords_to_glcoords((cell_x, cell_y), screen_size)
        l2 = coords_to_glcoords((cell_x_end, cell_y), screen_size)
        l3 = coords_to_glcoords((cell_x_end, cell_y_end), screen_size)
        l4 = coords_to_glcoords((cell_x, cell_y_end), screen_size)

        gl.glBegin(gl.GL_QUADS)

        gl.glVertex2f(l1[0], l1[1])
        gl.glVertex2f(l2[0], l2[1])
        gl.glVertex2f(l3[0], l3[1])
        gl.glVertex2f(l4[0], l4[1])

        gl.glEnd()
    maze.draw(screen_size)
    pygame.time.wait(5)
    pygame.display.flip()



ALGORITHMS = {
    "DFS": dfs,
    "BFS": bfs
}