#version 330 core
out vec4 fragColor;
uniform vec2 screenSize;

void main() {
    vec2 uv = gl_FragCoord.xy / screenSize;
    if(uv.x > 0.3 && uv.x < 0.7 && uv.y > 0.5 && uv.y < 0.505)
        fragColor = vec4(1.0, 0.0, 0.0, 1.0);
    else
        fragColor = vec4(0.3, 0.3, 0.3, 1.0);
}