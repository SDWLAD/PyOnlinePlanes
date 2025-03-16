#version 410

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;

in vec3 data;

out vec3 frag_pos;
out vec3 normal;

void main() {
    vec3 position = vec3(0.0);

    position.x = float(gl_VertexID / 500)*2;
    position.z = float(gl_VertexID % 500)*2;

    position.y = data.x;

    frag_pos = position;
    normal = vec3(-sin(data.y)*cos(data.z), sin(data.z), -cos(data.y)*cos(data.z));
    
    gl_Position = m_proj * m_view * m_model * vec4(position, 1.0);
}