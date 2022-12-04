#!/usr/bin/env python3

import os.path
import datetime


class Debug:
    """Use this to print only if `enabled`"""

    def __init__(self, enable=True):
        self.enabled = enable

    def enable(self, enabled=True):
        self.enabled = enabled

    def disable(self, disabled=True):
        self.enabled = not disabled

    def __call__(self, *args, **kwargs):
        if self.enabled:
            print(*args, **kwargs)


def test_eq(name, func, result_wanted, *args, **kwargs):
    print(f" * Testing {name}...", end=" ")
    result = func(*args, **kwargs)
    if result == result_wanted:
        print("\x1b[1;32mOK!\x1b[0m ☺ ")
    else:
        print("\x1b[1;41mNOT OK\x1b[0m ☹ ")
        print(f"\tExpected {result_wanted}, found {result}")


def save_solution(day, part, solution):
    filename = f"solutions/solution{day}_{part}"
    with open(filename, "w", encoding="utf-8") as solutions_file:
        solutions_file.write(str(solution))
    hist_file = f"solutions/solution_history{day}_{part}"
    with open(hist_file, "a", encoding="utf-8") as history_file:
        history_file.write(
            "\n------------- " + str(datetime.datetime.now()) + " -------------\n"
        )
        history_file.write(str(solution))


def check_solution(day, part, candidate):
    hist_file_name = f"solutions/solution_history{day}_{part}"
    with open(hist_file_name, "a", encoding="utf-8") as history_file:
        history_file.write(
            "\n------------- " + str(datetime.datetime.now()) + " -------------\n"
        )
        history_file.write(str(candidate))
    filename = f"solutions/solution{day}_{part}"
    if not os.path.isfile(filename):
        print(f"Day {day}, part {part} solution not present.")
        return
    with open(filename, "r", encoding="utf-8") as solution_file:
        solution = solution_file.read()

    if str(candidate) == solution:
        print(f"Day {day}, part {part} \x1b[1;32mOK!\x1b[0m ☺ ")
    else:
        print(f"Day {day}, part {part} \x1b[1;41mNOT OK\x1b[0m ☹ ")
        print(f"\tExpected {solution}, found {candidate}")


if __name__ == "__main__":
    pass
