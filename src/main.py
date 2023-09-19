import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import time

width, height = 800, 600 

pygame.init()
window = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
vertex_shader = ''.join([line for line in open("vtx-shader.glsl", 'r')])
fragment_shader = ''.join([line for line in open("frg-shader.glsl", 'r')])
shader_program = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER), compileShader(fragment_shader, GL_FRAGMENT_SHADER))
vao = glGenVertexArrays(1)
vbo = glGenBuffers(1)
glBindVertexArray(vao)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
vertices = np.array([-1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0], dtype=np.float32)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
glUseProgram(shader_program)
screenSize_loc = glGetUniformLocation(shader_program, "screenSize")


running = True
start_time = time.time()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
    width, height = pygame.display.get_surface().get_size()
    glUniform2f(screenSize_loc, width, height)
    glClear(GL_COLOR_BUFFER_BIT)

    current_time = time.time() - start_time
    time_uniform = glGetUniformLocation(shader_program, "time")
    glUniform1f(time_uniform, current_time)
    
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

    pygame.display.flip()


glDeleteProgram(shader_program)
glDeleteVertexArrays(1, [vao])
glDeleteBuffers(1, [vbo])
pygame.quit()

