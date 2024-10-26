from sys import flags

from imgui.integrations.pygame import PygameRenderer
import OpenGL.GL as gl
import imgui
import pygame
import sys


def main():
    pygame.init()
    size = 800, 600

    pygame.display.set_mode(size, pygame.DOUBLEBUF | pygame.OPENGL)

    imgui.create_context()
    impl = PygameRenderer()

    io = imgui.get_io()
    io.display_size = size

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            impl.process_event(event)
        impl.process_inputs()

        imgui.new_frame()
        imgui.begin("Maze settings")
        imgui.text(my_label_text)
        clicked = imgui.button("Click me !")
        imgui.end()

        # note: cannot use screen.fill((1, 1, 1)) because pygame's screen
        #       does not support fill() on OpenGL sufraces
        gl.glClearColor(0, 0, 0, 1)
        gl.glClear(gl.GL_COLOR_BUFFER_BIT)

        imgui.render()
        impl.render(imgui.get_draw_data())

        pygame.display.flip()


if __name__ == "__main__":
    main()