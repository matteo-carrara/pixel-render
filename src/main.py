import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import time


vertex_shader = """
#version 330 core
layout(location = 0) in vec2 in_position;
void main() {
    gl_Position = vec4(in_position, 0.0, 1.0);
}
"""

fragment_shader = """
#version 330 core
out vec4 fragColor;
uniform vec2 screenSize;

void main() {
    vec2 uv = gl_FragCoord.xy / screenSize;
    if(uv.x > 0.3 && uv.x < 0.7 && uv.y > 0.5 && uv.y < 0.505)
        fragColor = vec4(1.0, 0.0, 0.0, 1.0);
    else
        fragColor = vec4(0.3, 0.3, 0.3, 1.0);
}
"""


class RenderWindow:
    width, height = 800, 600
        
    def __init__(self):
        pass
    
    def show(self):
        pygame.init()
        
        self.window = pygame.display.set_mode((self.width, self.height), DOUBLEBUF | OPENGL)
        
        self.shader_program = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER), compileShader(fragment_shader, GL_FRAGMENT_SHADER))
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        self.vertices = np.array([-1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0], dtype=np.float32)
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
        glUseProgram(self.shader_program)
        
        self.screenSize_loc = glGetUniformLocation(self.shader_program, "screenSize")
        self._mainloop()
  
        
    def _mainloop(self):
        self.running = True
        self.start_time = time.time()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.width, self.height = pygame.display.get_surface().get_size()
            glUniform2f(self.screenSize_loc, self.width, self.height)
            glClear(GL_COLOR_BUFFER_BIT)

            current_time = time.time() - self.start_time
            time_uniform = glGetUniformLocation(self.shader_program, "time")
            glUniform1f(time_uniform, current_time)
    
            glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

            pygame.display.flip()
            
        self._terminate()
 
        
    def _terminate(self):
        glDeleteProgram(self.shader_program)
        glDeleteVertexArrays(1, [self.vao])
        glDeleteBuffers(1, [self.vbo])
        
        pygame.quit()
        






window = RenderWindow()
window.show()




