#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 1


def get_input(filename):
    with open(filename, "r", encoding="ascii") as input_file:
        lines = input_file.read()
    return lines.splitlines()


def elves(data):
    elf = []
    emitted = False
    for line in data:
        if line == "":
            yield elf
            emitted = True
            elf = []
        else:
            elf.append(int(line))
            emitted = False
    if not emitted:
        yield elf


def part1(data):
    return max([sum(elf) for elf in elves(data)])


def part2(data):

    return sum(sorted([sum(elf) for elf in elves(data)])[-3:])


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, 24000, test_input_1)
    print()

    print("Test Part 2:")
    test_eq("Test 2.1", part2, 45000, test_input_1)
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
