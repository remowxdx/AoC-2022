#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 3


def get_input(filename):
    with open(filename, "r") as input_file:
        lines = input_file.read()
    return lines.splitlines()


def in_both(rucksack):
    half = len(rucksack) // 2
    for item_type in rucksack[:half]:
        if item_type in rucksack[half:]:
            return item_type
    raise Exception("Not found.")


def priority(item_type):
    if item_type <= "Z":
        return ord(item_type) - 38
    return ord(item_type) - 96


def part1(data):

    total = 0

    for rucksack in data:
        repeated = in_both(rucksack)
        total += priority(repeated)

    return total


def part2(data):
    groups = len(data) // 3
    total = 0
    for group in range(groups):
        line = group * 3
        for item_type in data[line]:
            if item_type in data[line + 1] and item_type in data[line + 2]:
                total += priority(item_type)
                break
    return total


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, 157, test_input_1)
    print()

    print("Test Part 2:")
    test_eq("Test 2.1", part2, 70, test_input_1)
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
