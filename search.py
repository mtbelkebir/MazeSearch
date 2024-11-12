from queue import PriorityQueue

from models.maze import Maze
from collections import deque
import OpenGL.GL as gl
from util import coords_to_glcoords
from constants import COLORS
import pygame

def bfs(maze: Maze) -> tuple[list[int], list[int] | None]:
    """
    Performs Breadth-First Search (BFS) on the maze.

    :param maze: The maze to search.
    :return: A tuple containing the list of visited nodes and the path from the start to the goal, if found.
    """
    starting_cell = maze.starting_point
    destination_cell = maze.goal
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
        unvisited_neighbours = [x for x in neighbours if x not in visited]
        for n in unvisited_neighbours:
            visited.add(n)
            visited_list.append(n)
            parents[n] = current
            queue.append(n)
    else:
        return visited_list, None
    path = __retrace_path(maze, parents)
    return visited_list, path


def dfs(maze: Maze, node: int | None = None,
        destination: int  | None= None,
        visited: set[int] | None= None,
        visited_list: int | None= None,
        parents: dict[int,int] | None=None,
        max_depth: int | None = None) -> tuple[list[int] ,list[int] | None]:
    """
    Performs Depth-First Search (DFS) on the maze.

    :param maze: The maze to search.
    :param node: The current node being visited.
    :param destination: The goal node.
    :param visited: The set of visited nodes.
    :param visited_list: The list of visited nodes in order.
    :param parents: The dictionary mapping nodes to their parents.
    :param max_depth: The maximum depth to search.
    :return: A tuple containing the list of visited nodes and the path from the start to the goal, if found.
    """
    if node is None:
        node = maze.starting_point
    if parents is None:
        parents = {}
    if visited_list is None:
        visited_list = [node]
    if destination is None:
        destination = maze.goal
    if visited is None:
        visited = {node}

    if node == destination:
        path = __retrace_path(maze, parents)
        return visited_list, path

    if max_depth is not None:
        if max_depth <= 0:
            return visited_list, None
        else:
            max_depth -= 1

    neighbours = maze.get_visitable_neighbours(node)
    unvisited_neighbours = [x for x in neighbours if x not in visited]
    for n in unvisited_neighbours:
        visited.add(n)
        visited_list.append(n)
        parents[n] = node
        result = dfs(maze, n, destination, visited, visited_list, parents, max_depth)

        # To propagate the solution found in case we call and don't find it
        if result[1] is not None:
            return result
    return visited_list, None


def ucs(maze: Maze) -> tuple[list[int], list[int] | None]:
    """
    Performs Uniform Cost Search (UCS) on the maze.

    :param maze: The maze to search.
    :return: A tuple containing the list of visited nodes and the path from the start to the goal, if found.
    """
    node = maze.starting_point
    pq = PriorityQueue()
    pq.put((0, node))
    destination = maze.goal
    cumulated_cost = 0
    visited = {node}
    visited_list = [node]
    parents = {}
    while pq.queue:
        cumulated_cost, node = pq.get()
        if node == destination:
            path = __retrace_path(maze, parents)
            return visited_list, path
        neighbours = maze.get_visitable_neighbours(node)
        next_nodes = [n for n in neighbours if n not in visited and n not in pq.queue]
        for n in next_nodes:
            visited.add(n)
            visited_list.append(n)
            parents[n] = node
            pq.put((cumulated_cost + 1, n))
    return visited_list, None


def idfs(maze: Maze, max_depth: int | None = None, min_depth: int = 1):
    """
    Performs Iterative Deepening Depth-First Search (IDFS) on the maze.

    :param maze: The maze to search.
    :param max_depth: The maximum depth to search.
    :param min_depth: The minimum depth to start searching.
    :return: A tuple containing the list of visited nodes and the path from the start to the goal, if found.
    """
    if max_depth is None:
        max_depth = maze.adjacency_matrix_length # So I guess none ?
    r = None
    for depth in range(min_depth, max_depth):
        r = dfs(maze, max_depth=depth)
        if r[1] is not None:
            return r
    return r



def __retrace_path(maze: Maze, parents: dict[int, int]) -> list[int]:
    """
    Retraces the path from the goal to the start using the parents dictionary.

    :param maze: The maze being searched.
    :param parents: The dictionary mapping nodes to their parents.
    :return: The path from the start to the goal.
    """
    starting_cell = maze.starting_point
    goal = maze.goal
    path = [goal]

    current = goal
    while current != starting_cell:
        next = parents[current]
        path.append(parents[current])
        current = next
    path.append(starting_cell)
    path.reverse()
    return path

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
            maze.draw()
            pygame.display.flip()
            pygame.time.delay(delay)
    maze.draw()
    pygame.time.wait(delay)
    pygame.display.flip()

def draw_path(maze: Maze, path: list[int]):
    """
    Draws the path in the maze.

    :param maze: The maze being drawn.
    :param path: The list of nodes representing the path.
    """
    fill_cells(maze, path, COLORS["PATH_NODE"], 0)
    pygame.time.wait(2000)

def draw_visited(maze: Maze, visited: set[int] | list[int]):
    """
    Draws the visited nodes in the maze.
    :param maze: The maze being drawn.
    :param visited: The set or list of visited nodes.
    """
    fill_cells(maze, visited, COLORS["VISITED_NODE"])



ALGORITHMS = {
    "DFS": lambda maze: dfs(maze),
    "BFS": lambda maze: bfs(maze),
    "UCS": lambda maze: ucs(maze),
    "IDFS": lambda maze: idfs(maze),
}