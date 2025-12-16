# noise_level.py
import random
import numpy as np
# Uses your installed 'perlin-noise' package
from perlin_noise import PerlinNoise

MAP_W = 80
MAP_H = 60

# ---------- GENERATION SETTINGS ----------
SCALE = 0.1
OCTAVES = 2
SEED_OFFSET = 1000


def generate_heightmap(seed=0):
    """
    Generates a 2D heightmap using the 'perlin-noise' library and NumPy.
    This aligns with the paper's mention of using NumPy for efficient arrays.
    """
    # Initialize the PerlinNoise object
    # We add the seed to the octaves or use it to re-init the object
    noise_gen = PerlinNoise(octaves=OCTAVES, seed=seed)

    # Create an empty numpy array (aligned with paper's NumPy usage)
    hm = np.zeros((MAP_H, MAP_W))

    for y in range(MAP_H):
        for x in range(MAP_W):
            # perlin_noise expects coordinates in range [0, 1] usually,
            # or we scale the input.
            val = noise_gen([x * SCALE, y * SCALE])
            hm[y, x] = val

    return hm


def biome_from_height(h):
    """
    Converts noise value to Wall (1) or Floor (0).
    Threshold set to 0.05 for decent cave openness.
    """
    if h > 0.05:
        return 1  # WALL
    return 0      # FLOOR


def generate_biomes(seed=None):
    if seed is None:
        seed = random.randint(0, 10000)

    heightmap = generate_heightmap(seed=seed)

    # Use NumPy for biome mapping (vectorized operation would be faster,
    # but list comprehension is fine for this size)
    biomes = np.zeros((MAP_H, MAP_W), dtype=int)

    for y in range(MAP_H):
        for x in range(MAP_W):
            biomes[y, x] = biome_from_height(heightmap[y, x])

    # Force borders to be walls using NumPy slicing
    biomes[0, :] = 1        # Top row
    biomes[MAP_H-1, :] = 1  # Bottom row
    biomes[:, 0] = 1        # Left column
    biomes[:, MAP_W-1] = 1  # Right column

    return biomes, seed


def generate_terrain(seed=None):
    biomes, used = generate_biomes(seed)
    return biomes, used
