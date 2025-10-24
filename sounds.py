from pygame import mixer

def load_sounds(keys):
    sounds = {}
    for key, filename in keys.items():
        sounds[key] = mixer.Sound(f"C:/Users/svtko/Desktop/drive-download-20251017T105436Z-1-001/assets/sounds/{filename}")
    return sounds
