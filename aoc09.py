#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 9


def get_input(filename):
    with open(filename, "r", encoding="ascii") as input_file:
        lines = input_file.read()
    return lines.splitlines()


def move(dir_, pos_h):
    if dir_ == "R":
        return (pos_h[0] + 1, pos_h[1])
    if dir_ == "L":
        return (pos_h[0] - 1, pos_h[1])
    if dir_ == "U":
        return (pos_h[0], pos_h[1] - 1)
    if dir_ == "D":
        return (pos_h[0], pos_h[1] + 1)
    raise Exception(f"Unknown direction: {dir_}")


def spring(pos_h, pos_t):
    diff = (pos_t[0] - pos_h[0], pos_t[1] - pos_h[1])

    if abs(diff[0]) < 2 and abs(diff[1]) < 2:
        return pos_t

    if diff[0] == 0:
        step_x = 0
    else:
        step_x = diff[0] // abs(diff[0])

    if diff[1] == 0:
        step_y = 0
    else:
        step_y = diff[1] // abs(diff[1])

    return (pos_t[0] - step_x, pos_t[1] - step_y)


def part1(data):
    pos_h = (0, 0)
    pos_t = (0, 0)
    visited = set([pos_t])
    for line in data:
        dir_, steps_s = line.split()
        steps = int(steps_s)
        for _ in range(steps):
            pos_h = move(dir_, pos_h)
            pos_t = spring(pos_h, pos_t)
            visited.add(pos_t)
    return len(visited)


def part2(data):
    pos = [(0, 0) for _ in range(10)]
    visited = set([pos[9]])
    for line in data:
        dir_, steps_s = line.split()
        steps = int(steps_s)
        for _ in range(steps):
            pos[0] = move(dir_, pos[0])
            for i in range(9):
                pos[i + 1] = spring(pos[i], pos[i + 1])
            visited.add(pos[9])
    return len(visited)


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    test_input_2 = get_input(f"ex{DAY}.2")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, 13, test_input_1)
    print()

    print("Test Part 2:")
    test_eq("Test 2.1", part2, 1, test_input_1)
    test_eq("Test 2.2", part2, 36, test_input_2)
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
