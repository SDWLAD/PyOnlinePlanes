#version 410

in vec3 frag_pos;
in vec3 normal;
out vec4 fragColor;

uniform sampler2D texture_0;

vec3 light_dir = normalize(vec3(0.3, 0.9, 0.6));

void main() {
    float diff = max(dot(normal, light_dir), 0.0);
    float ambient = 0.3;
    float intensity = ambient + diff * 0.7;

    vec3 tex_color = vec3(0.0);
    tex_color = texture(texture_0, frag_pos.xz/1000).rgb;

    fragColor = vec4(tex_color * intensity, 1.0);
}