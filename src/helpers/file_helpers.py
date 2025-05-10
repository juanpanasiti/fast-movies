import json


def read_json_file(path: str) -> list[dict]:
    try:
        with open(path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        write_json_file(path, [])
        return []


def write_json_file(path: str, content: list[dict]) -> None:
    with open(path, 'w') as file:
        json.dump(content, file, indent=4, ensure_ascii=False)
