import random

from OpenGL.GL import *
from util import coords_to_glcoords
import pygame
from constants import COLORS

class Maze:
    def __init__(self, grid_length=10) -> None:

        # We suppose a square grid
        self.grid_length = grid_length
        # a.k.a the number of nodes
        self.adjacency_matrix_length = grid_length * grid_length
        self.__adjacency_matrix = [[0 for _ in range(self.adjacency_matrix_length)] for _ in range(self.adjacency_matrix_length)]
        self._starting_point = 0
        self._goal = self.adjacency_matrix_length - 1
        self.__generate_maze()

        
    def get_node_id(self, pos: tuple[int, int]) -> int:
        return pos[0] * self.grid_length + pos[1]
    
    def get_coordinate(self, node: int) -> tuple[int, int]:
        x = node // self.grid_length
        y = node % self.grid_length
        return x, y
    
    def position_in_range(self, pos: tuple[int, int]) -> bool:
        return pos[0] in range(0, self.grid_length) and pos[1] in range(0, self.grid_length)
    

    
    def get_neighbours(self, pos_or_node: int | tuple[int, int]) -> list[int]:
        """
        Returns the nodes that represent neighbours in final grid as a list. The neighbours are ordered clockwise.
        Adds -1 to the list if there's nothing in a direction.

        `pos_or_node` can be either a tuple of (x, y) or an integer node ID.
        """
        neighbours = []
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]

        if isinstance(pos_or_node, tuple):
            pos = pos_or_node
            if not self.position_in_range(pos):
                raise ValueError(f'Position {pos} out of range of the the grid')
        elif isinstance(pos_or_node, int):
            if pos_or_node >= self.adjacency_matrix_length:
                raise ValueError(f'Node {pos_or_node} is not part of the maze')
            pos = self.get_coordinate(pos_or_node)
        else:
            raise TypeError("Argument must be either a tuple (position) or an integer (node).")

        for direction in directions:
            neighbour_pos = (pos[0] + direction[0], pos[1] + direction[1])
            if self.position_in_range(neighbour_pos):
                neighbours.append(self.get_node_id(neighbour_pos))
            else:
                neighbours.append(-1)

        return neighbours
    
    def get_visitable_neighbours(self, node: tuple[int, int] | int) -> list[int]:
        neighours = self.get_neighbours(node)
        if isinstance(node, tuple):
            node = self.get_node_id(node)
        return [x for x in neighours if x != -1 and self.__adjacency_matrix[node][x] > 0]


    def __generate_maze(self, starting_cell: int | None = None):
        if starting_cell is None:
            starting_cell = random.randint(0, self.adjacency_matrix_length - 1)
        stack = [starting_cell]
        visited = {starting_cell}
        while stack:
            current = stack.pop()
            neighbours = self.get_neighbours(current)
            unvisited_neighbours = [x for x in neighbours if x not in visited and x != -1]
            if  unvisited_neighbours:
                stack.append(current)
                chosen_neighbour = random.choice(unvisited_neighbours)
                self.__adjacency_matrix[current][chosen_neighbour] = 1
                self.__adjacency_matrix[chosen_neighbour][current] = 1
                stack.append(chosen_neighbour)
                visited.add(chosen_neighbour)

    @property
    def grid(self):
        return self.__adjacency_matrix

    @property
    def starting_point(self):
        return self._starting_point

    @starting_point.setter
    def starting_point(self, node: int | tuple[int, int]):
        if isinstance(node, tuple):
            node = self.get_node_id(node)
        self._starting_point = node

    @property
    def goal(self):
        return self._goal

    @goal.setter
    def goal(self, node: int | tuple[int, int]):
        if isinstance(node, tuple):
            node = self.get_node_id(node)
        self._goal = node


    def clear(self):
        self.__adjacency_matrix = [[1 for _ in range(self.adjacency_matrix_length)] for _ in range(self.adjacency_matrix_length)]

    def set_node_as_obstacle(self, node: int | tuple[int, int]):
        if isinstance(node, tuple):
            node = self.get_node_id(node)

        neighbours = self.get_neighbours(node)
        for n in neighbours:
            self.__adjacency_matrix[n][node] = 0
            self.__adjacency_matrix[node][n] = 0

    def clear_node(self, node: int | tuple[int, int]):
        if isinstance(node, tuple):
            node = self.get_node_id(node)

        neighbours = self.get_neighbours(node)
        for n in neighbours:
            self.__adjacency_matrix[n][node] = 1
            self.__adjacency_matrix[node][n] = 1

    def draw(self):
        wall_color = COLORS["WALL_COLOR"]
        line_thickness = 3.0
        screen_size = pygame.display.get_window_size()
        screen_width, screen_height = screen_size
        cell_size = screen_width / self.grid_length

        # On colorie le début en bleu
        start_x, start_y = self.get_coordinate(self.starting_point)
        start_cell_x = start_x * cell_size
        start_cell_y = start_y * cell_size
        start_cell_x_end = start_cell_x + cell_size
        start_cell_y_end = start_cell_y + cell_size

        glColor3f(*COLORS["STARTING_NODE"])
        glBegin(GL_QUADS)
        glVertex2f(*coords_to_glcoords((start_cell_x, start_cell_y), screen_size))
        glVertex2f(*coords_to_glcoords((start_cell_x_end, start_cell_y), screen_size))
        glVertex2f(*coords_to_glcoords((start_cell_x_end, start_cell_y_end), screen_size))
        glVertex2f(*coords_to_glcoords((start_cell_x, start_cell_y_end), screen_size))
        glEnd()

        # On colorie la destination en Rouge
        goal_x, goal_y = self.get_coordinate(self.goal)
        goal_cell_x = goal_x * cell_size
        goal_cell_y = goal_y * cell_size
        goal_cell_x_end = goal_cell_x + cell_size
        goal_cell_y_end = goal_cell_y + cell_size

        glColor3f(*COLORS["GOAL_NODE"])
        glBegin(GL_QUADS)
        glVertex2f(*coords_to_glcoords((goal_cell_x, goal_cell_y), screen_size))
        glVertex2f(*coords_to_glcoords((goal_cell_x_end, goal_cell_y), screen_size))
        glVertex2f(*coords_to_glcoords((goal_cell_x_end, goal_cell_y_end), screen_size))
        glVertex2f(*coords_to_glcoords((goal_cell_x, goal_cell_y_end), screen_size))
        glEnd()

        for node in range(self.adjacency_matrix_length):
            x, y = self.get_coordinate(node)
            neighbours = self.get_neighbours((x, y))
            cell_x = x * cell_size
            cell_y = y * cell_size
            cell_x_end = cell_x + cell_size
            cell_y_end = cell_y + cell_size

            glLineWidth(line_thickness)
            glColor3i(*wall_color)
            # On dessine les murs avec chaque voisin

            glBegin(GL_LINES)
            # Voisin du dessus
            if neighbours[0] == -1 or self.grid[node][neighbours[0]] == 0:
                x1, y1 = coords_to_glcoords((cell_x, cell_y), screen_size)
                x2, y2 = coords_to_glcoords((cell_x_end, cell_y), screen_size)
                glVertex2f(x1, y1)
                glVertex2f(x2, y2)

            # Voisin de droite
            if neighbours[1] == -1 or self.grid[node][neighbours[1]] == 0:
                x1, y1 = coords_to_glcoords((cell_x_end, cell_y), screen_size)
                x2, y2 = coords_to_glcoords((cell_x_end, cell_y_end), screen_size)
                glVertex2f(x1, y1)
                glVertex2f(x2, y2)

            # Voisin du dessous
            if neighbours[2] == -1 or self.grid[node][neighbours[2]] == 0:
                x1, y1 = coords_to_glcoords((cell_x, cell_y_end), screen_size)
                x2, y2 = coords_to_glcoords((cell_x_end, cell_y_end), screen_size)
                glVertex2f(x1, y1)
                glVertex2f(x2, y2)

            # Voisin de gauche
            if neighbours[3] == -1 or self.grid[node][neighbours[3]] == 0:
                x1, y1 = coords_to_glcoords((cell_x, cell_y), screen_size)
                x2, y2 = coords_to_glcoords((cell_x, cell_y_end), screen_size)
                glVertex2f(x1, y1)
                glVertex2f(x2, y2)
            glEnd()
