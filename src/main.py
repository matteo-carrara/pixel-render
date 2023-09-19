import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np
import time

# Initialize Pygame
pygame.init()

# Define the window dimensions
width, height = 800, 600

# Create a Pygame window
window = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
context = pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)


# Vertex shader code (simple passthrough)
vertex_shader = """
#version 330 core
layout(location = 0) in vec2 in_position;
void main() {
    gl_Position = vec4(in_position, 0.0, 1.0);
}
"""

# Fragment shader code (compute pixel color based on time)
fragment_shader = """
#version 330 core
out vec4 fragColor;
uniform float time;
void main() {
    vec2 uv = gl_FragCoord.xy / vec2(800.0, 600.0);  // Normalize screen coordinates
    vec3 color = vec3(0.0, 0.0, 0.0);
    
    // Compute color based on time
    color.r = 0.5 + 0.5 * sin(time);
    color.g = 0.5 + 0.5 * cos(time);
    color.b = 0.5 + 0.5 * tan(time);

    fragColor = vec4(color, 1.0);  // Output pixel color
}
"""

# Compile shaders and create a shader program
shader_program = compileProgram(compileShader(vertex_shader, GL_VERTEX_SHADER),
                                 compileShader(fragment_shader, GL_FRAGMENT_SHADER))

# Create a VAO (Vertex Array Object) and VBO (Vertex Buffer Object)
vao = glGenVertexArrays(1)
vbo = glGenBuffers(1)

# Bind VAO and VBO
glBindVertexArray(vao)
glBindBuffer(GL_ARRAY_BUFFER, vbo)

# Define a quad with vertex positions
vertices = np.array([-1.0, -1.0, 1.0, -1.0, -1.0, 1.0, 1.0, 1.0], dtype=np.float32)

# Upload vertices to the VBO
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

# Specify the attribute layout (position)
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)

# Use the shader program
glUseProgram(shader_program)

# Main loop for rendering
running = True
start_time = time.time()
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT)

    # Pass the current time to the shader
    current_time = time.time() - start_time
    time_uniform = glGetUniformLocation(shader_program, "time")
    glUniform1f(time_uniform, current_time)

    # Draw the quad
    glDrawArrays(GL_TRIANGLE_STRIP, 0, 4)

    # Update the display
    pygame.display.flip()

# Clean up and exit
glDeleteProgram(shader_program)
glDeleteVertexArrays(1, [vao])
glDeleteBuffers(1, [vbo])
pygame.quit()

