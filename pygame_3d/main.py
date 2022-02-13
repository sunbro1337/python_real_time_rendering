import pygame
import numpy
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram


vertex_src = """
#version 440

layout(location=0) in vec3 vertex_position;
layout(location=1) in vec3 in_color;
out vec3 out_color;

void main() {
    gl_Position = vec4(vertex_position, 1);
    out_color = in_color;
}
"""
fragment_src = """
#version 440

in vec3 out_color;
out vec4 fragment_color;

void main() {
    fragment_color = vec4(out_color, 1);
}
"""


class Game():
    def __init__(self, caption, screen_width, screen_height):
        self.caption = caption
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.lock_fps = [30, 60]
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height), pygame.DOUBLEBUF | pygame.OPENGL)
        self.clock = pygame.time.Clock()

    def init_render(self):
        glClearColor(200 / 255, 200 / 255, 200 / 255, 1)

        # Triangle buffer data
        triangle = [
            # x     y    z      r          g          b
             0.0,  0.5, 0.0, 52 / 255, 178 / 255, 152 / 255,
            -0.5, -0.5, 0.0, 57 / 255, 151 / 255, 211 / 255,
             0.5, -0.5, 0.0, 81 / 255, 179 / 255, 110 / 255,
        ]
        triangle = numpy.array(triangle, dtype=numpy.float32)

        # Vertex Buffer Object(VBO)
        triangle_buffer = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, triangle_buffer)
        glBufferData(GL_ARRAY_BUFFER, triangle.nbytes, triangle, GL_STATIC_DRAW)

        # Getting data from GL_ARRAY_BUFFER
        buffer_data = glGetBufferSubData(GL_ARRAY_BUFFER, 0, triangle.nbytes)
        print(buffer_data.view(dtype=numpy.float32))

        # Post coordinates(vertex_position) to vertex shader
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, triangle.itemsize * 6, ctypes.c_void_p(0))

        # Post color(in_color) to vertex shader
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, triangle.itemsize * 6, ctypes.c_void_p(triangle.itemsize * 3))

        self.initial_position = 0

    def run(self):
        while True:
            self.clock.tick()
            pygame.display.set_caption(f"{self.caption} FPS: {self.clock.get_fps()}")
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.K_ESCAPE:
                        quit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        if self.initial_position == 1:
                            self.initial_position = 0
                        else:
                            self.initial_position = 1
            glClear(GL_COLOR_BUFFER_BIT)
            glDrawArrays(GL_TRIANGLES, self.initial_position, 3)
            pygame.display.flip()

    @staticmethod
    def compile_shaders():
        vertex_shader = compileShader(vertex_src, GL_VERTEX_SHADER)
        fragment_shader = compileShader(fragment_src, GL_FRAGMENT_SHADER)
        shader_program = compileProgram(vertex_shader, fragment_shader)
        glUseProgram(shader_program)


if __name__ == '__main__':
    new_game = Game('OpenGl', 800, 600)
    new_game.compile_shaders()
    new_game.init_render()
    new_game.run()
