from dataclasses import dataclass

@dataclass
class PartNumber:
    value: int
    col_l: int
    col_r: int

def parse_line(line):
    current_num = None
    numbers = []
    symbols = []

    for col, ch in enumerate(line):
        if ch == '.':
            # clear the currently accumulating number
            current_num = None
            continue
        elif ch.isdigit():
            ch = int(ch)
            if current_num is None:
                # Start a new number
                current_num = PartNumber(ch, col, col)
                numbers.append(current_num)
            else:
                # Add a digit, extend the right column
                current_num.value = (current_num.value * 10 + ch)
                current_num.col_r = col
        else:
            # A symbol
            symbols.append(col)

    return numbers, symbols


def part1_lines(lines):
    """
    467..114..
    ...*......
    ..35..633.
    ......#...
    617*......
    .....+.58.
    ..592.....
    ......755.
    ...$.*....
    .664.598..
    """
    for line in lines:
        parts, symbols = parse_line(line)
        print("\nLine:", line)
        print("Parts: ", parts)
        print("Symbols: ", symbols)
    return 1
