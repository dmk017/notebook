import os


def create_file(path: str, content: str) -> None:
    with open(path, "w") as f:
        f.write(content)


def read_file(path: str) -> str:
    with open(path, "r") as f:
        data = f.read()
    return data


def remove_file(file_path: str) -> None:
    os.remove(file_path)
