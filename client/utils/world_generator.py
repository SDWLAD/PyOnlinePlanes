import numpy as np
import noise

def generate_landscape(size, amplitude, scale, octaves, persistence, lacunarity, offset):
    x_size, z_size = size[:2]

    x_indices, z_indices = np.meshgrid(np.arange(x_size), np.arange(z_size), indexing='ij')

    x_norm = x_indices / scale
    z_norm = z_indices / scale

    height_map = np.vectorize(lambda x, z: noise.pnoise2(
        x, z, octaves=octaves, persistence=persistence, 
        lacunarity=lacunarity, repeatx=x_size, repeaty=z_size, base=42
    ))(x_norm, z_norm)

    return height_map * amplitude + offset
