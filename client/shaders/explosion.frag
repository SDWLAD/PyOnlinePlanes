#version 410 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
uniform sampler2D u_texture_0;
uniform vec2 u_offset;
uniform float u_size;

void main() {
    fragColor = texture2D(u_texture_0, uv_0/u_size + u_offset)*vec4(1, 0.4, 0, 1);
}