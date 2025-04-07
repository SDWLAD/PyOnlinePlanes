#version 410 core

in vec2 uv_0;
in vec3 normal;
uniform sampler2D u_texture_0;
uniform float distance_of_view;
in vec3 position;
out vec4 fragColor;
uniform bool fog;

float fog_distance = 25.0;

vec3 light_dir = normalize(vec3(0.3, 0.9, 0.6));

vec3 directLight(vec3 color){
    float diffuse = max(dot(normal, light_dir), 0.0);
    vec3 ambient = vec3(0.3);
    return color * (ambient + diffuse * 0.7);
}

void main() {
    vec3 color = texture(u_texture_0, uv_0).rgb;
    color *= directLight(vec3(1.0));
    float alpha = 1.0;
    if (fog)
        alpha = (distance_of_view/2 - (gl_FragCoord.z / gl_FragCoord.w)) / fog_distance;
    fragColor = vec4(color, 1.0);
}