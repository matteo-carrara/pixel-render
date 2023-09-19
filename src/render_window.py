from re import S
import pygame
import tkinter as tk
from tkinter import ttk
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import time
import threading

from shader import *


class RenderWindow:
    width, height = 800, 600
        
    def __init__(self):
        pass
    
    def _settingsWindow(self):
        self.root = tk.Tk()
        self.root.title("Parameter Controls")
        self.root.geometry("400x300")
        
        # Create a Label for the first slider
        label1 = tk.Label(self.root, text="Parameter 1")
        label1.grid(row=0, column=0, padx=10, pady=10)

        # Create the first slider
        slider1 = ttk.Scale(self.root, from_=0, to=100, orient="horizontal")
        slider1.grid(row=0, column=1, padx=10, pady=10)

        # Create a Label for the second slider
        label2 = tk.Label(self.root, text="Parameter 2")
        label2.grid(row=1, column=0, padx=10, pady=10)

        # Create the second slider
        slider2 = ttk.Scale(self.root, from_=0, to=100, orient="horizontal")
        slider2.grid(row=1, column=1, padx=10, pady=10)

        # Create a button
        button = ttk.Button(self.root, text="Apply")
        button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        
        self.root.mainloop()
    
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
        
        tk_thread = threading.Thread(target=self._settingsWindow)
        tk_thread.start()


        self._mainloop()
  
        
    def _mainloop(self):
        self.running = True
        self.start_time = time.time()
        
        self.modified = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    
            if(self.modified):
                self.width, self.height = pygame.display.get_surface().get_size()
                glUniform2f(self.screenSize_loc, self.width, self.height)
                glClear(GL_COLOR_BUFFER_BIT)

                current_time = time.time() - self.start_time
                time_uniform = glGetUniformLocation(self.shader_program, "time")
                glUniform1f(time_uniform, current_time)
    
                glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

                pygame.display.flip()
                
                self.modified = False
            else:
                pass
            


        self._terminate()
 
        
    def _terminate(self):
        glDeleteProgram(self.shader_program)
        glDeleteVertexArrays(1, [self.vao])
        glDeleteBuffers(1, [self.vbo])
        
        pygame.quit()
        self.root.quit()
        
