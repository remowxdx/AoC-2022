#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 1


def get_input(filename):
    with open(filename, "r") as input_file:
        lines = input_file.read()
    return lines.splitlines()


def part1(data):
    max_calories = 0
    current_elf = 0
    for line in data:
        if line == "":
            if current_elf > max_calories:
                max_calories = current_elf
                print(max_calories)
            current_elf = 0
            continue
        current_food = int(line)
        current_elf += current_food

    if current_elf > max_calories:
        max_calories = current_elf
        print(max_calories)

    return max_calories


def part2(data):
    max_calories = [0, 0, 0]
    current_elf = 0

    for line in data:

        if line == "":
            if current_elf > min(max_calories):
                max_calories[max_calories.index(min(max_calories))] = current_elf
                print(max_calories)
            current_elf = 0
            continue
        current_food = int(line)
        current_elf += current_food

    if current_elf > min(max_calories):
        max_calories[max_calories.index(min(max_calories))] = current_elf
        print(max_calories)

    return sum(max_calories)


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
