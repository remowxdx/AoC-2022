#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 4


def get_input(filename):
    with open(filename, "r", encoding="ascii") as input_file:
        lines = input_file.read()
    return lines.splitlines()


def part1(data):
    contained = 0
    for line in data:
        elf1, elf2 = line.split(",")
        bounds1 = elf1.split("-")
        bounds2 = elf2.split("-")
        low1 = int(bounds1[0])
        high1 = int(bounds1[1])
        low2 = int(bounds2[0])
        high2 = int(bounds2[1])
        if (low1 >= low2 and high1 <= high2) or (low2 >= low1 and high2 <= high1):
            contained += 1
    return contained


def part2(data):
    overlapping = 0
    for line in data:
        elf1, elf2 = line.split(",")
        bounds1 = elf1.split("-")
        bounds2 = elf2.split("-")
        low1 = int(bounds1[0])
        high1 = int(bounds1[1])
        low2 = int(bounds2[0])
        high2 = int(bounds2[1])
        if (low1 >= low2 and low1 <= high2) or (low2 >= low1 and low2 <= high1):
            overlapping += 1
    return overlapping


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, 2, test_input_1)
    print()

    print("Test Part 2:")
    test_eq("Test 2.1", part2, 4, test_input_1)
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
    run_part2(False)


if __name__ == "__main__":
    main()
