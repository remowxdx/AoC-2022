#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 5


def get_input(filename):
    with open(filename, "r", encoding="ascii") as input_file:
        lines = input_file.read()
    return lines.splitlines()


def read_crates(line):
    result = {}
    stack = 0
    for col, char in enumerate(line):
        if col % 4 == 1:
            if char != " ":
                result[stack] = char
            stack += 1
    return result


def parse_input(data):
    state = "crates"
    num_stacks = (len(data[0]) + 1) // 4
    stacks = [[] for stack in range(num_stacks)]
    moves = []
    for line in data:
        if state == "crates":
            # Crates drawing
            line_crates = read_crates(line)
            if 0 in line_crates and line_crates[0] == "1":
                # Crates numbers
                state = "stacks"
                continue
            for stack, crate in line_crates.items():
                stacks[stack].append(crate)
        elif state == "stacks":
            # Blank line
            state = "moves"
        elif state == "moves":
            # Moves
            token = line.split()
            move = (int(token[1]), int(token[3]) - 1, int(token[5]) - 1)
            moves.append(move)
        else:
            raise Exception(f"Unknown state {state}.")

    for stack in stacks:
        stack.reverse()

    return stacks, moves


def part1(data):
    stacks, moves = parse_input(data)

    for move in moves:
        for _ in range(move[0]):
            stacks[move[2]].append(stacks[move[1]].pop())

    result = "".join([stack[-1] for stack in stacks])
    return result


def part2(data):
    stacks, moves = parse_input(data)

    for move in moves:
        temp = []
        for _ in range(move[0]):
            temp.append(stacks[move[1]].pop())
        for _ in range(move[0]):
            stacks[move[2]].append(temp.pop())

    result = "".join([stack[-1] for stack in stacks])
    return result


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, "CMZ", test_input_1)
    print()

    print("Test Part 2:")
    test_eq("Test 2.1", part2, "MCD", test_input_1)
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
