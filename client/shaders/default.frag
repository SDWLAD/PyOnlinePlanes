#version 410 core

in vec3 position;
in vec3 normal;
in vec2 uv_0;
out vec4 fragColor;

uniform sampler2D u_texture_0;

vec3 light_dir = normalize(vec3(0.3, 0.9, 0.6));

vec3 directLight(vec3 color){
    float diffuse = max(dot(normal, light_dir), 0.0);
    vec3 ambient = vec3(0.3);
    return color * (ambient + diffuse * 0.7);
}

void main() {
    vec3 color = texture(u_texture_0, uv_0).rgb;
    color *= directLight(vec3(1.0));
    fragColor = vec4(color, 1.0);
}