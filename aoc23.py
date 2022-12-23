#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 23


def get_input(filename):
    with open(filename, "r", encoding="ascii") as input_file:
        lines = input_file.read()
    return lines.splitlines()


def read_elves(data):
    elves = []
    for y, row in enumerate(data):
        for x, char in enumerate(row):
            if char == "#":
                elves.append((x, y))
    return elves


DIRECTIONS = [
    (-1, -1),
    (0, -1),
    (1, -1),
    (-1, 0),
    (0, 0),
    (1, 0),
    (-1, 1),
    (0, 1),
    (1, 1),
]


def propose_direction(elves, elf, direction):
    positions = [(elf[0] + dir_[0], elf[1] + dir_[1]) for dir_ in DIRECTIONS]

    if direction == "N":
        dirs = [0, 1, 2]
        proposal = positions[1]
    elif direction == "S":
        dirs = [6, 7, 8]
        proposal = positions[7]
    elif direction == "W":
        dirs = [0, 3, 6]
        proposal = positions[3]
    elif direction == "E":
        dirs = [2, 5, 8]
        proposal = positions[5]
    else:
        dirs = [0, 1, 2, 3, 5, 6, 7, 8]
        proposal = elf

    for dir_ in dirs:
        if positions[dir_] in elves:
            break
    else:
        return proposal
    return None


def first_half(elves, directions, phase):
    proposals = {}
    moved = False
    for elf in elves:

        proposal = propose_direction(elves, elf, "C")
        if proposal is not None:
            proposals[proposal] = [elf]
            continue

        moved = True

        current_phase = phase % 4
        for _ in range(4):
            proposal = propose_direction(elves, elf, directions[current_phase % 4])
            if proposal is not None:
                if proposal not in proposals:
                    proposals[proposal] = []
                proposals[proposal].append(elf)
                break
            current_phase += 1
        else:
            if elf not in proposals:
                proposals[elf] = []
            proposals[elf].append(elf)

    return proposals, moved


def count_empty(elves):
    bounding = [elves[0], elves[0]]
    for elf in elves:
        bounding = [
            (min(bounding[0][0], elf[0]), min(bounding[0][1], elf[1])),
            (max(bounding[1][0], elf[0]), max(bounding[1][1], elf[1])),
        ]
    return (bounding[1][0] - bounding[0][0] + 1) * (
        bounding[1][1] - bounding[0][1] + 1
    ) - len(elves)


def second_half(proposals):
    elves = []
    for destination, sources in proposals.items():
        if len(sources) == 1:
            elves.append(destination)
        else:
            elves.extend(sources)
    return elves


def print_elves(elves):
    bounding = [elves[0], elves[0]]
    for elf in elves:
        bounding = [
            (min(bounding[0][0], elf[0]), min(bounding[0][1], elf[1])),
            (max(bounding[1][0], elf[0]), max(bounding[1][1], elf[1])),
        ]
    for y in range(bounding[0][1], bounding[1][1] + 1):
        for x in range(bounding[0][0], bounding[1][0] + 1):
            if (x, y) in elves:
                print("#", end="")
            else:
                print(".", end="")
        print()


def part1(data):
    elves = read_elves(data)
    directions = ["N", "S", "W", "E"]
    for phase in range(10):
        proposals, _ = first_half(elves, directions, phase)
        elves = second_half(proposals)
    result = count_empty(elves)
    return result


def part2(data):
    elves = read_elves(data)
    directions = ["N", "S", "W", "E"]
    phase = 0
    while True:
        proposals, moved = first_half(elves, directions, phase)
        elves = second_half(proposals)
        phase += 1
        if not moved:
            break
    return phase


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    test_input_2 = get_input(f"ex{DAY}.2")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, 25, test_input_1)
    test_eq("Test 1.2", part1, 110, test_input_2)
    print()

    print("Test Part 2:")
    test_eq("Test 2.1", part2, 4, test_input_1)
    test_eq("Test 2.2", part2, 20, test_input_2)
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
    # run_part1(True)
    run_part2(False)


if __name__ == "__main__":
    main()
