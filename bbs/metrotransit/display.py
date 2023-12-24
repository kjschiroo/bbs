import pathlib

resource_dir = pathlib.Path(__file__).parent.joinpath("resources")


def triple_text(text):
    lines = text.split("\n")
    new_lines = []
    for line in lines:
        new_line = "".join([c + c + c for c in line])
        new_lines.append(new_line)
        new_lines.append(new_line)
        new_lines.append(new_line)
    return "\n".join(new_lines)


def display(text):
    display_text = resource_dir.joinpath(f"{text}.txt").read_text()
    print("\033c", end="")
    print()
    for line in triple_text(display_text).split("\n"):
        print(f"  {line}")
