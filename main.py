from imgui.integrations.pygame import PygameRenderer
import OpenGL.GL as gl
import imgui
import pygame
import sys
from models.maze import Maze
import search

def main():
    pygame.init()
    window_size = 1000, 1000

    screen = pygame.display.set_mode(window_size, pygame.DOUBLEBUF | pygame.OPENGL | pygame.RESIZABLE)

    imgui.create_context()
    impl = PygameRenderer()

    io = imgui.get_io()
    io.display_size = window_size
    maze_size = 15
    maze = Maze(maze_size)

    supported_algorithms_selected_index = 0
    supported_algorithms = list(search.ALGORITHMS.keys())

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            impl.process_event(event)
        impl.process_inputs()

        imgui.new_frame()
        imgui.begin("MazeSettings", flags=imgui.WINDOW_ALWAYS_AUTO_RESIZE)
        _, maze_size = imgui.slider_int("Maze size", maze_size, 10, 40)
        generated_button_clicked = imgui.button("Generate")
        imgui.separator()
        algorithms_combo_changed, selected_algorithm = imgui.combo("Algorithm", supported_algorithms_selected_index, supported_algorithms)
        if algorithms_combo_changed:
            supported_algorithms_selected_index = selected_algorithm
        search_button_clicked = imgui.button("Search")
        imgui.end()

        gl.glClear(gl.GL_COLOR_BUFFER_BIT)
        gl.glClearColor(1, 1, 1, 1)
        if maze is not None:
            maze.draw(window_size)
        if search_button_clicked:
            search.ALGORITHMS[supported_algorithms[supported_algorithms_selected_index]](maze)

        imgui.render()
        impl.render(imgui.get_draw_data())
        pygame.display.flip()
        pygame.time.wait(16)

        if generated_button_clicked:
            maze = Maze(maze_size)


if __name__ == "__main__":
    main()