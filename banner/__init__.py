import os
import shutil

def load_banner(banner_name, center=False):
    filename = f"{banner_name}_banner.txt"
    path = os.path.join(os.path.dirname(__file__), filename)

    if not os.path.exists(path):
        raise fileNotFoundError(f"{banner_name} não encontrado em {path}")

    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    if center:
        terminal_width = shutil.get_terminal_size((80, 20)).columns
        lines = [line.strip().center(terminal_width) for line in lines]
    else:
        lines = [line.rstrip() for line in lines]        

    return "\n".join(lines)
