from queue import PriorityQueue

from models.maze import Maze
from collections import deque
import OpenGL.GL as gl
from util import coords_to_glcoords

import pygame

def bfs(maze: Maze) -> tuple[list[int], list[int]]:
    starting_cell = 0
    destination_cell = len(maze.grid[0]) - 1
    queue = deque()
    queue.append(starting_cell)
    visited = {starting_cell}
    visited_list = [starting_cell]
    parents = {}
    while queue:
        current = queue.popleft()
        if current == destination_cell:
            break
 
        neighbours = maze.get_visitable_neighbours(current)
        unvisited_neighbours = [x for x in neighbours if x != -1 and x not in visited]
        for n in unvisited_neighbours:
            visited.add(n)
            visited_list.append(n)
            parents[n] = current
            queue.append(n)
    path = __retrace_path(parents)
    return visited_list, path


def dfs(maze: Maze, node: int = 0,
        destination: int  | None= None,
        visited: set[int] | None= None,
        visited_list: int | None= None,
        parents: dict[int,int] | None=None) -> tuple[list[int],list[int]]:
    if parents is None:
        parents = {}
    if visited_list is None:
        visited_list = [node]
    if destination is None:
        destination = len(maze.grid[0]) - 1
    if visited is None:
        visited = {node}

    if node == destination:
        path = __retrace_path(parents)
        return visited_list, path

    neighbours = maze.get_visitable_neighbours(node)
    unvisited_neighbours = [x for x in neighbours if x != -1 and x not in visited]
    for n in unvisited_neighbours:
        visited.add(n)
        visited_list.append(n)
        parents[n] = node
        result = dfs(maze, n, destination, visited, visited_list, parents)

        # To propagate the solution found in case we call and don't find it
        if result is not None:
            return result


def ucs(maze: Maze):
    node = 0
    pq = PriorityQueue()
    pq.put((0, node))
    destination = len(maze.grid[0]) - 1
    cumulated_cost = 0
    visited = {node}
    visited_list = [node]
    while pq:
        node = pq.get()[1]
        cumulated_cost += 1
        visited.add(node)
        visited_list.append(node)
        if node == destination:
            return visited_list, []
        neighbours = maze.get_visitable_neighbours(node)
        for n in neighbours:
            if n not in visited and n not in pq.queue:
                pq.put((cumulated_cost + 1, n))



def __retrace_path(parents: dict[int, int]) -> list[int]:
    starting_cell = 0
    goal = max(list(parents.keys()))
    path = []

    current = goal
    while current != starting_cell:
        next = parents[current]
        path.append(parents[current])
        current = next
    path.append(starting_cell)
    path.reverse()
    return path

# TODO : Optimiser la routine en n'affichant que les nouveaux nœuds visités au lieu de TOUT les nœuds visités
def fill_cells(maze: Maze, cells: set[int] | list[int], color: tuple[float, float, float], delay=16):
    screen_size = pygame.display.get_window_size()
    screen_width, _ = screen_size
    cell_size = screen_width / maze.grid_length
    for node in cells:
        x, y = maze.get_coordinate(node)
        cell_x = x * cell_size
        cell_y = y * cell_size
        cell_x_end = cell_x + cell_size
        cell_y_end = cell_y + cell_size

        l1 = coords_to_glcoords((cell_x, cell_y), screen_size)
        l2 = coords_to_glcoords((cell_x_end, cell_y), screen_size)
        l3 = coords_to_glcoords((cell_x_end, cell_y_end), screen_size)
        l4 = coords_to_glcoords((cell_x, cell_y_end), screen_size)

        gl.glColor3f(color[0], color[1], color[2])
        gl.glBegin(gl.GL_QUADS)

        gl.glVertex2f(l1[0], l1[1])
        gl.glVertex2f(l2[0], l2[1])
        gl.glVertex2f(l3[0], l3[1])
        gl.glVertex2f(l4[0], l4[1])
        gl.glEnd()
        if isinstance(cells, list):
            # À faire si et seulement si on dessine le chemin final
            # TODO : À refactoriser car là c'est n'importe quoi
            maze.draw()
            pygame.display.flip()
            pygame.time.delay(delay)
    maze.draw()
    pygame.time.wait(delay)
    pygame.display.flip()

def draw_path(maze: Maze, path: list[int]):
    fill_cells(maze, path, (0, 1, 0))

def draw_visited(maze: Maze, visited: set[int] | list[int]):
    fill_cells(maze, visited, (.7, 0, .7))



ALGORITHMS = {
    "DFS": lambda maze: dfs(maze),
    "BFS": lambda maze: bfs(maze),
    "UCS": lambda maze: ucs(maze),
}