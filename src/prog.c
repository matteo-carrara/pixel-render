#include <SDL2/SDL.h>
#include <stdio.h>
#include <stdlib.h>
#include <GL/glew.h>

#include "draw.h"
#include "common.h"


int res_x = 800;
int res_y = 600;
SDL_Window* window = NULL;
SDL_GLContext context;


char* loadShaderFromFile(const char* filename) {
    FILE* file = fopen(filename, "r");
    if (!file) {
        fprintf(stderr, "Failed to open shader file: %s\n", filename);
        exit(1);
    }

    fseek(file, 0, SEEK_END);
    long length = ftell(file);
    fseek(file, 0, SEEK_SET);

    char* shaderCode = (char*)malloc(length + 1);
    if (!shaderCode) {
        fclose(file);
        fprintf(stderr, "Memory allocation for shader code failed\n");
        exit(1);
    }

    fread(shaderCode, 1, length, file);
    shaderCode[length] = '\0'; 

    fclose(file);
    return shaderCode;
}

void setup() {
	if (SDL_Init(SDL_INIT_VIDEO) < 0) {
		    printf("SDL initialization failed: %s\n", SDL_GetError());
		    exit(1);
		}
	
	
    window = SDL_CreateWindow("SDL with Fragment Shader", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, res_x, res_y, SDL_WINDOW_OPENGL);
    if (window == NULL) {
        printf("Window creation failed: %s\n", SDL_GetError());
        exit(1);
    }
    
    context = SDL_GL_CreateContext(window);
    
    glewExperimental = GL_TRUE;
    GLenum glewInitResult = glewInit();
    if (glewInitResult != GLEW_OK) {
    	printf("opengl error\n");
        SDL_DestroyWindow(window);
        SDL_Quit();
        exit(1);
    }
    
    glViewport(0, 0, res_x, res_y);

}


void mainloop() {
    SDL_Event event;
    int quit = 0;

	GLuint shaderProgram;
	const char* shaderFilename = "shader.glsl";
	const char* fragmentShaderSource = loadShaderFromFile(shaderFilename);

	GLuint fragmentShader = glCreateShader(GL_FRAGMENT_SHADER);
	glShaderSource(fragmentShader, 1, &fragmentShaderSource, NULL);
	glCompileShader(fragmentShader);

	shaderProgram = glCreateProgram();
	glAttachShader(shaderProgram, fragmentShader);
	glLinkProgram(shaderProgram);

	GLuint resolutionLocation = glGetUniformLocation(shaderProgram, "resolution");
	glUniform2f(resolutionLocation, res_x, res_y);
	glUseProgram(shaderProgram);
	
	int success;
	char infoLog[512];
	glGetShaderiv(fragmentShader, GL_COMPILE_STATUS, &success);
	if (!success) {
		glGetShaderInfoLog(fragmentShader, 512, NULL, infoLog);
		printf("Shader compilation failed:\n%s\n", infoLog);
		exit(1);
	}


	 GLfloat vertices[] = {
        -1.0f, -1.0f,
         1.0f, -1.0f,
         1.0f,  1.0f,
        -1.0f,  1.0f
    };

    GLuint vao, vbo;
    glGenVertexArrays(1, &vao);
    glGenBuffers(1, &vbo);
    glBindVertexArray(vao);
    glBindBuffer(GL_ARRAY_BUFFER, vbo);
    glBufferData(GL_ARRAY_BUFFER, sizeof(vertices), vertices, GL_STATIC_DRAW);
    glEnableVertexAttribArray(0);
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 2 * sizeof(GLfloat), (GLvoid*)0);
    glBindBuffer(GL_ARRAY_BUFFER, 0);
    glBindVertexArray(0);

	
	
	printf("entering main loop\n");
    while (!quit) {
        while (SDL_PollEvent(&event) != 0) {
            if (event.type == SDL_QUIT) {
                quit = 1;
            }
        }
        

    glClear(GL_COLOR_BUFFER_BIT);
    glUseProgram(shaderProgram);
    glBindVertexArray(vao);
    glDrawArrays(GL_TRIANGLE_FAN, 0, 4);
    glBindVertexArray(0);
    SDL_GL_SwapWindow(window);
    }
    
    glDeleteProgram(shaderProgram);
    glDeleteShader(fragmentShader);
    glDeleteBuffers(1, &vbo);
    glDeleteVertexArrays(1, &vao);
    SDL_GL_DeleteContext(context);
    SDL_DestroyWindow(window);
}


void sdl_quit() {
    SDL_GL_DeleteContext(context);
    SDL_DestroyWindow(window);
    SDL_Quit();
}


int main(int argc, char* argv[]) {    
	setup();
	mainloop();
	sdl_quit();

    exit(0);
}

