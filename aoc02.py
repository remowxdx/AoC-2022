#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 2
SCORE = {"X": 1, "Y": 2, "Z": 3}
WIN = {"X": "C", "Y": "A", "Z": "B"}
DRAW = {"X": "A", "Y": "B", "Z": "C"}

PART2 = {
    "X": {"A": "Z", "B": "X", "C": "Y"},
    "Y": {"A": "X", "B": "Y", "C": "Z"},
    "Z": {"A": "Y", "B": "Z", "C": "X"},
}


def get_input(filename):
    with open(filename, "r") as input_file:
        lines = input_file.read()
    return lines.splitlines()


def calc_score_2(opponent, me):
    score = 0
    if me == "Z":
        score += 6
    elif me == "Y":
        score += 3
    score += SCORE[PART2[me][opponent]]
    return score


def calc_score(opponent, me):
    score = SCORE[me]
    if opponent == WIN[me]:
        score += 6
    elif opponent == DRAW[me]:
        score += 3
    return score


def part1(data):
    score = 0
    for line in data:
        opponent, me = line.split()
        score += calc_score(opponent, me)
    return score


def part2(data):
    score = 0
    for line in data:
        opponent, me = line.split()
        score += calc_score_2(opponent, me)
    return score


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, 15, test_input_1)
    print()

    print("Test Part 2:")
    test_eq("Test 2.1", part2, 12, test_input_1)
    print()


def run_part1(solved):
    data = get_input(f"input{DAY}")

    result1 = part1(data)
    print("Part 1:", result1)
    if solved:
        check_solution(DAY, 1, result1)
    else:
        save_solution(DAY, 1, result1)


def run_part2(solved):
    data = get_input(f"input{DAY}")

    result2 = part2(data)
    print("Part 2:", result2)
    if solved:
        check_solution(DAY, 2, result2)
    else:
        save_solution(DAY, 2, result2)


def main():
    run_tests()
    run_part1(True)
    run_part2(True)


if __name__ == "__main__":
    main()
