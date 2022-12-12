#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 12


def get_input(filename):
    with open(filename, "r", encoding="ascii") as input_file:
        lines = input_file.read()
    return lines.splitlines()


def adjacent_positions(pos):
    dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    positions = []
    for step in dirs:
        positions.append((pos[0] + step[0], pos[1] + step[1]))
    return positions


def next_steps(pos, hmap):
    steps = []
    for new_pos in adjacent_positions(pos):
        if new_pos in hmap and hmap[new_pos] <= hmap[pos] + 1:
            steps.append(new_pos)
    return steps


def travel(hmap, start, end):
    to_visit = [start]

    path_len = {}
    path_len[start] = 0

    while len(to_visit) > 0:
        current_pos = to_visit.pop(0)

        if current_pos == end:
            return path_len[current_pos]

        for next_step in next_steps(current_pos, hmap):
            if next_step in path_len:
                continue
            to_visit.append(next_step)
            path_len[next_step] = path_len[current_pos] + 1

    raise ValueError("No path.")


def part1(data):
    hmap = {}
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == "S":
                start = (x, y)
                char = "a"
            elif char == "E":
                end = (x, y)
                char = "z"
            hmap[(x, y)] = ord(char) - ord("a")

    return travel(hmap, start, end)


def part2(data):
    hmap = {}
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == "S":
                char = "a"
            elif char == "E":
                end = (x, y)
                char = "z"
            hmap[(x, y)] = ord(char) - ord("a")

    shortest_path = len(hmap)

    for start, height in hmap.items():
        if height == 0:
            try:
                shortest_path = min(shortest_path, travel(hmap, start, end))
            except ValueError:
                pass

    return shortest_path


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, 31, test_input_1)
    print()

    print("Test Part 2:")
    test_eq("Test 2.1", part2, 29, test_input_1)
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
