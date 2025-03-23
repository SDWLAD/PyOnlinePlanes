#version 330 core
uniform sampler2D Texture;
in vec2 v_texcoord;
out vec4 fragColor;

void main() {
    fragColor = texture(Texture, v_texcoord);
}