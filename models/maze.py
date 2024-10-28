import numpy as np
import random
from OpenGL.GL import *
from util import coords_to_glcoords

class Maze:
    def __init__(self, size=10) -> None:
        self.size = size
        self.length = size * size
        self.grid = np.zeros((self.length, self.length))
        self.__generate_maze()

        
    def __get_position(self, pos: tuple[int, int]) -> int:
        return pos[0] * self.size + pos[1]
    
    def __get_coordinate(self, node: int) -> tuple[int, int]:
        x = node // self.size
        y = node % self.size
        return x, y
    
    def __position_in_range(self, pos: tuple[int, int]) -> bool:
        return pos[0] in range(0, self.size) and pos[1] in range(0, self.size)
    

    
    def __get_neighbours(self, pos: tuple[int, int]) -> list[int]:
        """
        Returns the nodes that represent neighbours in final grid as a list. The neighbours are ordered clockwise
        Adds -1 to the list if there's nothing in a direction
        """
        neighbours = []
        directions = [(0, -1), (1, 0), (0, 1) , (-1, 0)]
        for direction in directions:
            neighbour_pos = (pos[0] + direction[0], pos[1] + direction[1])
            if self.__position_in_range(neighbour_pos):
                neighbours.append(self.__get_position(neighbour_pos))
            else:
                neighbours.append(-1)

        return neighbours
    
    def __generate_maze(self, starting_cell: int | None = None):
        if starting_cell is None:
            starting_cell = random.randint(0, self.size - 1)
        stack = [starting_cell]
        visited = {starting_cell}
        while stack:
            current = stack.pop()
            neighbours = self.__get_neighbours(self.__get_coordinate(current))
            unvisited_neighbours = [x for x in neighbours if x not in visited and x != -1]
            if  unvisited_neighbours:
                stack.append(current)
                chosen_neighbour = random.choice(unvisited_neighbours)
                self.grid[current][chosen_neighbour] = 1
                self.grid[chosen_neighbour][current] = 1
                stack.append(chosen_neighbour)
                visited.add(chosen_neighbour)

    def draw(self, screen_size: tuple[int, int]):
        wall_color = [0, 0, 0]
        line_thickness = 3.0

        screen_width, screen_height = screen_size
        cell_size = screen_width // self.size

        for node in range(self.length):
            x, y = self.__get_coordinate(node)
            neighbours = self.__get_neighbours((x, y))
            cell_x = x * cell_size
            cell_y = y * cell_size
            cell_x_end = cell_x + cell_size
            cell_y_end = cell_y + cell_size

            glLineWidth(line_thickness)
            glColor3i(wall_color[0], wall_color[1], wall_color[2])
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


        
