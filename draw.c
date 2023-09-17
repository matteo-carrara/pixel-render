#include <SDL2/SDL.h>

void drawLine(SDL_Renderer* renderer) {
        SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255); // Set the drawing color to red
		for(int i = 0; i < 100; i++) {
			SDL_RenderDrawPoint(renderer, 100+i, 100);
			SDL_RenderPresent(renderer);
		}
}
