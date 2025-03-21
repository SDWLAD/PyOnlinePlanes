#version 410

in vec3 frag_pos;
in vec3 normal;
out vec4 fragColor;

uniform sampler2D texture_0;

vec3 light_dir = normalize(vec3(0.3, 0.9, 0.6));

vec3 directLight(vec3 color){
    float diffuse = max(dot(normal, light_dir), 0.0);
    vec3 ambient = vec3(0.3);
    return color * (ambient + diffuse * 0.7);
}

void main() {
    vec3 color = texture(texture_0, frag_pos.xz/1000).rgb;
    color *= directLight(vec3(1.0));
    float alpha = (450 - (gl_FragCoord.z / gl_FragCoord.w)) / 25.0;
    fragColor = vec4(color, alpha);
}