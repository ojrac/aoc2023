# Setup
Get your session token from the browser dev tools and put it (just the hex part) in `input/token.txt`

# Running
To test day 1 (using part1/part2 docstrings as test input), run `main.py 1 --test`.

To run on actual day 1 input, just run `main.py test`. It will download and cache your input in the `input/` folder.

# Making a new day
Make `days/day##.py`, and implement functions for part 1 and 2 as you go. You
can either implement `part1(line)`, which will be called with each line, and
all non-None results will be summed together, or you can implement
`part1_lines(lines)` which will be passed a generator of lines, and returns
whatever you want to print for the part's result.

If you put the sample input in a docstring for a part to use it as test input.
(Don't worry about extra whitespace, it's trimmed before passing).

## Example

The following are equivalent - one line at a time:
```
def part1(line):
    """
    1
    2
    3
    """
    return int(line)
```

...or a generator:
```
def part1_lines(lines):
    """
    1
    2
    3
    """
    return sum([int(l) for l in lines])
```
