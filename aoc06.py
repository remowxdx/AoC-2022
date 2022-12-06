#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 6


def get_input(filename):
    with open(filename, "r", encoding="ascii") as input_file:
        lines = input_file.read()
    return lines.splitlines()


def all_different(recent):
    for i in range(len(recent) - 1):
        for j in range(i + 1, len(recent)):
            if recent[i] == recent[j]:
                return False
    return True


def part1(data):
    message = data[0]
    recent = list(message[:4])
    pos = 4
    for char in message[4:]:
        if all_different(recent):
            return pos
        recent[pos % 4] = char
        pos += 1
    return pos


def part2(data):
    message = data[0]
    recent = list(message[:14])
    pos = 14
    for char in message[14:]:
        if all_different(recent):
            return pos
        recent[pos % 14] = char
        pos += 1
    return pos


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    test_input_2 = get_input(f"ex{DAY}.2")
    test_input_3 = get_input(f"ex{DAY}.3")
    test_input_4 = get_input(f"ex{DAY}.4")
    test_input_5 = get_input(f"ex{DAY}.5")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, 7, test_input_1)
    test_eq("Test 1.2", part1, 5, test_input_2)
    test_eq("Test 1.3", part1, 6, test_input_3)
    test_eq("Test 1.4", part1, 10, test_input_4)
    test_eq("Test 1.5", part1, 11, test_input_5)
    print()

    print("Test Part 2:")
    test_eq("Test 2.1", part2, 19, test_input_1)
    test_eq("Test 2.2", part2, 23, test_input_2)
    test_eq("Test 2.3", part2, 23, test_input_3)
    test_eq("Test 2.4", part2, 29, test_input_4)
    test_eq("Test 2.5", part2, 26, test_input_5)
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
