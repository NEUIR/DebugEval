def readFile(file_dir: str) -> str:
    try:
        with open(file_dir, 'r') as f:
            lines = f.readlines()
            return arrange(lines)

    except FileNotFoundError:
        return 'Error: file not found'


def writeFile(file_dir: str, text: str) -> None:
    with open(file_dir, 'w') as f:
        f.write(text)


def arrange(lines: list[str]) -> str:
    if not lines:
        return ""

    if lines[0].strip() == '':
        return ""
    # clean up the empty lines in the end of the file
    while lines[-1] == '\n':
        lines.pop()

    # clean up the empty lines in the beginning of the file
    while lines[0] == '\n':
        lines.pop(0)

    if lines[-1].endswith('\n'):
        lines[-1] = lines[-1][:-1]

    return ''.join(lines).encode('utf-8', 'ignore').decode('utf-8')