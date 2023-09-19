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
    __width, __height = 800, 600
    __line_len = 0.8
    __line_thick = 0.1
    
    def __init__(self, w=800, h=600):
        self.__lock = threading.Lock()
        self.__width = w
        self.__height = h
        
        self.__setup()
    
    def __settings_changed_is(self, what):
        with self.__lock:
            self.__settings_changed = what
    
    def __get_settings_changed(self):
        with self.__lock:
            return self.__settings_changed
            
    def __button_click(self):
        self.__settings_changed_is(True) 
        with self.__lock:
            self.__line_len = self.slider_line_len.get()/100
            self.__line_thick = self.slider_line_thick.get()/100
            self.__line_len = self.__line_len if self.__line_len > 0 else 0.003
            self.__line_thick = self.__line_thick if self.__line_thick > 0 else 0.003
        print("Line lenght", self.__line_len, "line thickness", self.__line_thick)
               
        
    def __settingsWindow(self):
        self.__root = tk.Tk()
        self.__root.title("Parameter Controls")
        self.__root.geometry("400x300")
        
        label1 = tk.Label(self.__root, text="Line lenght percent")
        label1.grid(row=0, column=0, padx=10, pady=10)
        self.slider_line_len = ttk.Scale(self.__root, from_=0, to=100, orient="horizontal")
        self.slider_line_len.grid(row=0, column=1, padx=10, pady=10)

        
        label2 = tk.Label(self.__root, text="Line thickness percent")
        label2.grid(row=1, column=0, padx=10, pady=10)
        self.slider_line_thick = ttk.Scale(self.__root, from_=0, to=100, orient="horizontal")
        self.slider_line_thick.grid(row=1, column=1, padx=10, pady=10)

        button = ttk.Button(self.__root, text="Apply", command=self.__button_click)
        button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        
        self.__root.mainloop()
        

    def __setup(self):
        pygame.init()
        
        window = pygame.display.set_mode((self.__width, self.__height), DOUBLEBUF | OPENGL)
        
        self.__line_drawing_shader = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER), compileShader(line_fragment_shader, GL_FRAGMENT_SHADER))
        
        self.__vao = glGenVertexArrays(1)
        self.__vbo = glGenBuffers(1)
        
        glBindVertexArray(self.__vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.__vbo)
        
        vertices = np.array([-1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0], dtype=np.float32)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0)
        
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
        glUseProgram(self.__line_drawing_shader)
        
        self.__frag_screenSize = glGetUniformLocation(self.__line_drawing_shader, "screenSize")
        self.__frag_ll = glGetUniformLocation(self.__line_drawing_shader, "line_len")
        self.__frag_lt = glGetUniformLocation(self.__line_drawing_shader, "line_thick")
        
        tk_thread = threading.Thread(target=self.__settingsWindow)
        tk_thread.start()

        self.__mainloop()
  
        
    def __mainloop(self):
        running = True
        self.__settings_changed_is(True)
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            if(self.__get_settings_changed()):
                with self.__lock:
                    print("sending info to frag")
                    glUniform1f(self.__frag_ll, self.__line_len)
                    glUniform1f(self.__frag_lt, self.__line_thick)
                    print("sent ll", self.__line_len, "lt", self.__line_thick)
                 
                self.__width, self.__height = pygame.display.get_surface().get_size()
                glUniform2f(self.__frag_screenSize, self.__width, self.__height)
                
                glClear(GL_COLOR_BUFFER_BIT)
                glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)
                pygame.display.flip()
                
                self.__settings_changed_is(False)
            else:
                pass

        self.__terminate()
 
        
    def __terminate(self):
        glDeleteProgram(self.__line_drawing_shader)
        glDeleteVertexArrays(1, [self.__vao])
        glDeleteBuffers(1, [self.__vbo])
        
        pygame.quit()
        self.__root.quit()
        
