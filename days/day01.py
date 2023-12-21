def part1(line):
    """
    1abc2
    pqr3stu8vwx
    a1b2c3d4e5f
    treb7uchet
    """
    digits = [
        int(c) for c in line
        if c.isdigit()
    ]
    return digits[0] * 10 + digits[-1]

DIGIT_NAMES = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

# This turned out not to be how it works - twone is apparently supposed to emit
# 2 and 1, not just 2
def pop_digit(line):
    if not line:
        return None
    if line[0].isdigit():
        return int(line[0]), line[1:]

    for name, value in DIGIT_NAMES.items():
        if line.startswith(name):
            return value, line[len(name):]

    # No digits at the front
    return None, line

def read_a_digit(line):
    if not line:
        return None
    if line[0].isdigit():
        return int(line[0])

    for name, value in DIGIT_NAMES.items():
        if line.startswith(name):
            return value

    return None
        
def get_digits(line):
    for i in range(len(line)):
        digit = read_a_digit(line[i:])
        if digit is not None:
            yield digit

def part2(line):
    """
    two1nine
    eightwothree
    abcone2threexyz
    xtwone3four
    4nineeightseven2
    zoneight234
    7pqrstsixteen
    """
    digits = list(get_digits(line))
    #print(line, "->", digits, "=", digits[0] * 10 + digits[-1])
    return digits[0] * 10 + digits[-1]


