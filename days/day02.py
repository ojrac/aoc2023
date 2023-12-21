from typing import Self

class Hand:
    red: int
    green: int
    blue: int

    def __init__(self, red = 0, green = 0, blue = 0):
        self.red = red
        self.green = green
        self.blue = blue

    def fits_in(self, other: Self) -> bool:
        return (self.red <= other.red
                and self.green <= other.green
                and self.blue <= other.blue)

    def combine_max(self, other: Self) -> Self:
        return Hand(
            red=max(self.red, other.red),
            green=max(self.green, other.green),
            blue=max(self.blue, other.blue))

    def power(self) -> int:
        return self.red * self.green * self.blue

PART1_LIMITS = Hand(red=12, green=13, blue=14)

def parse_hand(hand_str):
    parts = {}
    for color_part in hand_str.split(", "):
        ct, color = color_part.split(" ")
        parts[color] = int(ct)
    return Hand(**parts)

def game_id_and_remainder(line):
    game_name, line = line.split(": ", 1)
    game_id = int(game_name[len("Game "):])
    return game_id, line

def hands_in_game(hands_str):
    hands = hands_str.split("; ")
    for hand_str in hands:
        yield parse_hand(hand_str)

def part1(line):
    """
    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
    """
    game_id, rest = game_id_and_remainder(line)
    for hand in hands_in_game(rest):
        if not hand.fits_in(PART1_LIMITS):
            return None
    return game_id

def part2(line):
    """
    Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
    Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
    Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
    Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
    Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
    """
    _, rest = game_id_and_remainder(line)
    min_hand = Hand(0, 0, 0)
    for hand in hands_in_game(rest):
        min_hand = min_hand.combine_max(hand)
    return min_hand.power()
