from importlib.resources import files

def get_image_path(name: str) -> str:
    return str(files(__package__) / name)