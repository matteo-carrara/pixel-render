#include <SDL2/SDL.h>
#include <stdio.h>
#include <stdlib.h>

#include "draw.h"
#include "common.h"

int res_x = 800;
int res_y = 600;

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("Usage: %s <integer>\n", argv[0]);
        return 1;
    }
    
    // Convert the argument to an integer
    int num = atoi(argv[1]);

    // Check if the conversion was successful
    if (num == 0 && argv[1][0] != '0') {
        printf("Invalid input: %s is not an integer.\n", argv[1]);
        return 1;
    }
    
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("SDL initialization failed: %s\n", SDL_GetError());
        return 1;
    }

    SDL_Window* window = SDL_CreateWindow("Pixel Drawing", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, res_x, res_y, SDL_WINDOW_SHOWN);
    if (window == NULL) {
        printf("Window creation failed: %s\n", SDL_GetError());
        return 1;
    }

    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);
    if (renderer == NULL) {
        printf("Renderer creation failed: %s\n", SDL_GetError());
        return 1;
    }

    SDL_Event event;
    int quit = 0;

	// Set the background color to black
	SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255); // R=0, G=0, B=0, A=255

	// Clear the screen with the background color (black)
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

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}

