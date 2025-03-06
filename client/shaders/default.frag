#version 410 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 normal;
uniform sampler2D u_texture_0;
in vec3 position;

vec3 light_dir = normalize(vec3(0.3, 0.9, 0.6));

vec3 direcLight(vec3 color){
    vec3 Normal = normalize(normal);
    vec3 ambient = vec3(0.1);
    float diff = max(0, dot(light_dir, Normal));
    vec3 diffuse = vec3(diff * 0.8);
    return color * (ambient + diffuse);
}

void main() {
    vec3 color = texture(u_texture_0, uv_0).rgb;
    color *= direcLight(color);
    float alpha = 1.0;
    fragColor = vec4(pow(color, vec3(1/2.2)), alpha);
}