import numpy as np
import random

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
        neighbours = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for direction in directions:
            neighbour_pos = (pos[0] + direction[0], pos[1] + direction[1])
            if self.__position_in_range(neighbour_pos):
                neighbours.append(self.__get_position(neighbour_pos))

        return neighbours
    
    def __generate_maze(self, starting_cell: int | None = None):
        if starting_cell is None:
            starting_cell = random.randint(0, self.size - 1)
        stack = [starting_cell]
        visited = {starting_cell}
        while stack:
            current = stack.pop()
            neighbours = self.__get_neighbours(self.__get_coordinate(current))
            if [x for x in neighbours if x not in visited]:
                stack.append(current)
                chosen_neighbour = random.choice(neighbours)
                self.grid[current][chosen_neighbour] = 1
                self.grid[chosen_neighbour][current] = 1
                stack.append(chosen_neighbour)
                visited.add(chosen_neighbour)

