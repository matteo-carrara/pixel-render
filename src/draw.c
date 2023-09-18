#include <SDL2/SDL.h>
#include "common.h"

void drawLine(SDL_Renderer* renderer, int startx, int starty, int lenght, float slope) {
		if(lenght+startx > res_x)
			lenght = res_x;
        SDL_SetRenderDrawColor(renderer, 255, 0, 0, 255); // Set the drawing color to red
		for(int i = 0; i < lenght; i++) {
			SDL_RenderDrawPoint(renderer, startx+i, starty);
			SDL_RenderPresent(renderer);
		}
}
