#include <SDL2/SDL.h>





int main(int argc, char* argv[]) {
    if (SDL_Init(SDL_INIT_VIDEO) < 0) {
        printf("SDL initialization failed: %s\n", SDL_GetError());
        return 1;
    }

    SDL_Window* window = SDL_CreateWindow("Pixel Drawing", SDL_WINDOWPOS_UNDEFINED, SDL_WINDOWPOS_UNDEFINED, 800, 600, SDL_WINDOW_SHOWN);
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

    while (!quit) {
        while (SDL_PollEvent(&event) != 0) {
            if (event.type == SDL_QUIT) {
                quit = 1;
            }
        }



        SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255); // Set the drawing color to red
		for(int i = 0; i < 100; i++) {
			SDL_RenderDrawPoint(renderer, 100+i, 100);
			SDL_RenderPresent(renderer);
		}
    }

    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}

