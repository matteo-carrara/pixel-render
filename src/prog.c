#include <SDL2/SDL.h>
#include <stdio.h>
#include <stdlib.h>
#include <GL/glew.h>

#include "draw.h"
#include "common.h"


int res_x = 800;
int res_y = 600;
SDL_Renderer* renderer = NULL;
SDL_Window* window = NULL;


void setup() {
	if (SDL_Init(SDL_INIT_VIDEO) < 0) {
		    printf("SDL initialization failed: %s\n", SDL_GetError());
		    exit(1);
		}

    window = SDL_CreateWindow("Pixel Drawing", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, res_x, res_y, SDL_WINDOW_SHOWN);
    if (window == NULL) {
        printf("Window creation failed: %s\n", SDL_GetError());
        exit(1);
    }

    renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (renderer == NULL) {
        printf("Renderer creation failed: %s\n", SDL_GetError());
        exit(1);
    }

}


void mainloop(int num) {
	if(renderer == NULL) {
		printf("SDL setup error\n");
		exit(1);
	}
    SDL_Event event;
    int quit = 0;

	SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255); 
	SDL_RenderClear(renderer);

	int drawn = 0;
    while (!quit) {
        while (SDL_PollEvent(&event) != 0) {
            if (event.type == SDL_QUIT) {
                quit = 1;
            }
        }
        if(!drawn) {
        	drawLine(renderer, 0,130, num, 0);
        	drawn++;
        }

    }
}


void sdl_quit() {
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();
}


int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("Usage: %s <line lenght>\n", argv[0]);
        exit(1);
    }
    
    int num = atoi(argv[1]);
    if (num == 0 && argv[1][0] != '0') {
        printf("Invalid input: %s is not an integer.\n", argv[1]);
        exit(1);
    }
    
    
	setup();
	mainloop(num);
	sdl_quit();

    exit(0);
}

