import os
from pathlib import Path

def get_child_dirs(dir_path: Path):
    dir_path = Path(dir_path)
    children = {}

    def inner(dir_path: Path, child_map: dict):
        contents = [d for d in dir_path.iterdir() if d.is_dir()]

        for path in contents:
            child_map[path.name] = {}
            inner(path, child_map[path.name])
            
    inner(dir_path, children)
    return children

def get_child_audio_files(source):
    matches = []
    for root, dirnames, filenames in os.walk(source):
        for filename in filenames:
            if filename.endswith(('.mp3', '.flac')):
                matches.append(os.path.join(root, filename))
    return matches
