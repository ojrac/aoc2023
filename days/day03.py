from dataclasses import dataclass
from itertools import chain
from typing import List

@dataclass(unsafe_hash=True)
class PartNumber:
    line_num: int
    value: int
    col_l: int
    col_r: int

@dataclass
class Symbol:
    col: int
    row: int
    symbol: str

@dataclass
class Gear:
    col: int
    row: int
    parts: List[PartNumber]

@dataclass
class Line:
    numbers: List[PartNumber]
    symbols: List[Symbol]

def parse_line(line_num: int, line: str) -> Line:
    current_num = None
    numbers = []
    symbols = []

    for col, ch in enumerate(line):
        if ch.isdigit():
            ch = int(ch)
            if current_num is None:
                # Start a new number
                current_num = PartNumber(line_num, ch, col, col)
                numbers.append(current_num)
            else:
                # Add a digit, extend the right column
                current_num.value = (current_num.value * 10 + ch)
                current_num.col_r = col
        else:
            # clear the currently accumulating number
            current_num = None
            if ch != '.':
                # A symbol
                symbols.append(Symbol(row=line_num, col=col, symbol=ch))

    return Line(numbers, symbols)

def parts_to_count(numbers: List[PartNumber], symbols: List[int]):
    for symbol in symbols:
        symbol_col = symbol.col
        for number in numbers:
            if symbol_col + 1 >= number.col_l and symbol_col - 1 <= number.col_r:
                yield number

def debug_print_lines(part_nums):
    new_line = '.' * (max((p.col_r for p in part_nums)) + 1)
    line = new_line
    line_num = 0

    for part in sorted(part_nums, key=lambda p: p.line_num):
        while line_num < part.line_num:
            print(line)
            line = new_line
            line_num += 1
        #print("  ", line, "->", part)
        line = line[:part.col_l] + str(part.value) + line[part.col_r + 1:]
        #print("->", line)
    print(line)

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
    lines = (parse_line(i, l) for i, l in enumerate(lines))

    part_nums = set()
    last_line = Line([], [])
    for i, line in enumerate(lines):
        part_nums = part_nums.union(parts_to_count(line.numbers, line.symbols))
        part_nums = part_nums.union(parts_to_count(line.numbers, last_line.symbols))
        part_nums = part_nums.union(parts_to_count(last_line.numbers, line.symbols))

        last_line = line

    #debug_print_lines(part_nums)

    return sum((n.value for n in part_nums))

def parts_next_to_gears(numbers: List[PartNumber], symbols: List[int]):
    for symbol in symbols:
        if symbol.symbol != "*":
            continue
        for number in numbers:
            if symbol.col + 1 >= number.col_l and symbol.col - 1 <= number.col_r:
                yield number, symbol

def part2_lines(lines):
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
    lines = (parse_line(i, l) for i, l in enumerate(lines))

    gears = {}
    last_line = Line([], [])
    for line in lines:
        parts_and_symbols = chain(
            parts_next_to_gears(line.numbers, line.symbols),
            parts_next_to_gears(line.numbers, last_line.symbols),
            parts_next_to_gears(last_line.numbers, line.symbols))
        for part, symbol in parts_and_symbols:
            g = gears.setdefault((symbol.col, symbol.row), Gear(symbol.col, symbol.row, []))
            g.parts.append(part)
        last_line = line

    result = 0
    for gear in gears.values():
        if len(gear.parts) != 2:
            continue
        a, b = gear.parts
        result += a.value * b.value
    return result


