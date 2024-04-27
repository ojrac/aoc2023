from collections import defaultdict
import re

SPACES = re.compile(' +')

def parse(line):
    _, line = line.split(': ', 1)
    winning, have = line.split(" | ")
    def to_nums(s):
        return [int(n) for n in SPACES.split(s) if n]

    return to_nums(winning), to_nums(have)

def count_wins(line):
    winning, have = parse(line)
    return sum((1 if h in winning else 0
                for h in have))

def part1(line):
    """
    Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
    Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
    Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
    Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
    Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
    """
    wins = count_wins(line)
    if wins == 0:
        return 0
    return pow(2, wins - 1)

def part2_lines(lines):
    """
    Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
    Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
    Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
    Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
    Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
    Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
    """
    total_wins = 0
    wins_by_line = defaultdict(lambda: 1)
    for i, line in enumerate(lines):
        multiplier = wins_by_line[i]
        wins = count_wins(line)
        total_wins += multiplier

        if wins == 0:
            continue
        for i in range(i + 1, i + 1 + wins):
            wins_by_line[i] += multiplier
    return total_wins
