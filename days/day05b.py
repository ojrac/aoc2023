from dataclasses import dataclass
from enum import Enum
import re

TEST_DATA = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""

def combine_ranges(src_range: list[Range], dest_range: list[Range]) -> list[Range]:
    if not src_range:
        return dest_range

    src_range.sort(key=lambda r: r.dest_range_start)
    result = []
    for dest in dest_range:
        delta = dest.src_range_start - src_range[0].dest_range_start
        if delta < 0:
            # 




def combine_mappings(mappings: list[Map]) -> Map:
    ranges = []
    last_dest = mappings[0].src
    for mapping in mappings:
        assert mapping.src == last_dest
        last_dest = mapping.dest

        ranges = combine_range(ranges, mapping.ranges)
    return Map(src=mappings[0].src, dest=mappings[-1].dest, ranges=[])




@dataclass
class Range:
    src_range_start: int
    dest_range_start: int
    range_len: int

    def offset(self, value):
        diff = value - self.src_range_start
        if diff < 0 or diff > self.range_len:
            return None, False
        return diff + self.dest_range_start, True
        

@dataclass
class Map:
    src: str
    dest: str
    ranges: list[Range]

    def apply(self, value):
        for r in self.ranges:
            v, ok = r.offset(value)
            if ok:
                return v
        return value

MAP_HEADER = re.compile("^(?P<src>[a-z]+)-to-(?P<dest>[a-z]+) map:$")
SEEDS_PREFIX = "seeds: "

def read_maps(lines):
    m = None
    for line in lines:
        if m is None:
            match = MAP_HEADER.match(line)
            assert match
            m = Map(match["src"], match["dest"], [])
        elif not line:
            # Map is done
            assert m
            yield m
            m = None
        else:
            dest_range_start, src_range_start, range_len = map(int, line.split(" "))
            m.ranges.append(Range(src_range_start, dest_range_start, range_len))

    if m is not None:
        yield m

def parse_lines(lines):
    seeds_str = next(lines)
    assert seeds_str.startswith(SEEDS_PREFIX)
    seeds = [int(s) for s in seeds_str[len(SEEDS_PREFIX):].split(' ')]
    assert next(lines) == ""

    mappings = list(read_maps(lines))

    return seeds, mappings

def seed_locations(seeds, maps):
    for seed in seeds:
        value = seed
        for mapping in maps:
            value = mapping.apply(value)
        yield value

def part1_lines(lines):
    seeds, maps = parse_lines(lines)

    assert maps[0].src == "seed"
    assert maps[-1].dest == "location"
    last_dest = maps[0].dest
    for mapping in maps[1:]:
        assert mapping.src == last_dest
        last_dest = mapping.dest

    return min(seed_locations(seeds, maps))

def part2_locations(seeds, maps):
    assert len(seeds) % 2 == 0
    for i in range(0, len(seeds), 2):
        first_seed, num_seeds = seeds[i:i+2]
        yield min(seed_locations(range(first_seed, first_seed + num_seeds), maps))

def part2_lines(lines):
    seeds, maps = parse_lines(lines)

    assert maps[0].src == "seed"
    assert maps[-1].dest == "location"
    last_dest = maps[0].dest
    for mapping in maps[1:]:
        assert mapping.src == last_dest
        last_dest = mapping.dest

    return min(part2_locations(seeds, maps))
