vertex_shader = """
#version 330 core
layout(location = 0) in vec2 in_position;
void main() {
    gl_Position = vec4(in_position, 0.0, 1.0);
}
"""

line_fragment_shader = """
#version 330 core
out vec4 fragColor;

uniform vec2 screenSize;
uniform float line_len;
uniform float line_thick;


void main() {
    vec2 uv = gl_FragCoord.xy / screenSize;

    float min_x = 0.5-(line_len/2);
    float max_x = 0.5+(line_len/2);
    float min_y = 0.5-(line_thick/2);
    float max_y = 0.5+(line_thick/2);
    
    if(uv.x >= min_x && uv.x <= max_x && uv.y >= min_y && uv.y <= max_y)
        fragColor = vec4(1.0, 0.0, 0.0, 1.0);
    else
        fragColor = vec4(0.1, 0.1, 0.1, 1.0);
        
}
"""