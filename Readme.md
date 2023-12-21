# Setup
Get your session token from the browser dev tools and put it (just the hex part) in `input/token.txt`

# Running
To test day 1 (using part1/part2 docstrings as test input), run `main.py 1 --test`.

To run on actual day 1 input, just run `main.py test`. It will download and cache your input in the `input/` folder.

# Making a new day
Make `days/day##.py`, and implement `part1(line)` or `part2`
functions as you go. Put the sample input in a docstring to use it for testing.
(Don't worry about extra whitespace, it's trimmed before passing).

For now, a `part#` function takes a line of input, and can return an `int` or
`None`; all returned `int`s are summed before being printed.
