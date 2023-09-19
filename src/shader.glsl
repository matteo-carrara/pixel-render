#version 330 core

out vec4 FragColor;

uniform vec2 resolution;

void main() {
    // Get the normalized coordinates
    vec2 st = gl_FragCoord.xy / resolution.xy;

    // Use the coordinates to set the color (R, G, B)
     FragColor = vec4(st.x/800, 0, 0.0, 1.0);
}

