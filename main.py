from os.path import dirname, join
import requests
from typing import List
import sys
from urllib.request import urlopen, Request

AOC_URL = "https://adventofcode.com/2023/day/%d/input"
INPUT_CACHE_DIR = join(dirname(__file__), "input")

def usage():
    print("Usage: main.py <0-25> [--test]")
    sys.exit(1)

def main(argv: List[str]):
    pos_argv = [arg for arg in argv[1:] if not arg.startswith("-")]
    if len(pos_argv) != 1 or "--help" in argv:
        usage()

    try:
        day = int(pos_argv[0])
    except ValueError:
        usage()

    module_name = f"day{day:02}"
    try:
        day_module = getattr(__import__(f"days.{module_name}"), module_name)
    except ValueError:
        print(f"Missing file days/day{day:02}.py")
        sys.exit(1)

    is_test = "--test" in argv

    ran: bool = run_day(day_module, day, 1, is_test)
    ran = run_day(day_module, day, 2, is_test) or ran
    if not ran:
        print(f"Day {day} is missing a part1/part2 function")

def run_day(module, day: int, part: int, is_test: bool):
    name = f"part{part}"
    try:
        function = getattr(module, name)
    except AttributeError:
        return False

    inputs = get_inputs(day, part, function, is_test)
    transformed_lines = (function(line) for line in inputs)
    total = sum((l for l in transformed_lines if l is not None))

    print(f"Day {part}:")
    print(total)
    return True


def get_input_document_lines(day: int):
    input_cache_path = join(INPUT_CACHE_DIR, f"day{day:02}.txt")
    try:
        with open(input_cache_path) as f:
            return f.readlines()
    except FileNotFoundError:
        pass # Download and cache it instead

    with open(join(dirname(__file__), "input", "token.txt")) as f:
        token = f.read().strip()

    r = requests.get(AOC_URL % day, headers={"Cookie": f"session={token}"})
    input_document = r.text
    with open(input_cache_path, "wt") as f:
        f.write(input_document)

    return input_document.splitlines()

def get_inputs(day: int, part: int, function, is_test: bool):
    if is_test:
        input_lines = function.__doc__.splitlines()
    else:
        input_lines = get_input_document_lines(day)

    lines = (
        l.strip()
        for l in input_lines
    )
    # Skip empty lines
    return (l for l in lines if l)

if __name__ == "__main__":
    main(sys.argv)
