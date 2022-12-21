#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 21


class IsHuman(Exception):
    """Exception for when we find a human."""


def get_input(filename):
    with open(filename, "r", encoding="ascii") as input_file:
        lines = input_file.read()
    return lines.splitlines()


def monkey_tree(data):
    monkeys = {}
    for monkey in data:
        name, value = monkey.split(": ")
        if value.isnumeric():
            monkeys[name] = int(value)
        else:
            monkeys[name] = value.split()
    return monkeys


def yell(monkeys, monkey):
    value = monkeys[monkey]
    if isinstance(value, int):
        return value
    left, operation, right = value
    if operation == "+":
        return yell(monkeys, left) + yell(monkeys, right)
    if operation == "-":
        return yell(monkeys, left) - yell(monkeys, right)
    if operation == "*":
        return yell(monkeys, left) * yell(monkeys, right)
    if operation == "/":
        return yell(monkeys, left) // yell(monkeys, right)
    raise ValueError(f"Unkown operation {operation}")


def yell_human(monkeys, monkey):
    # print(monkey)
    if monkey == "humn":
        raise IsHuman()

    value = monkeys[monkey]

    if isinstance(value, int):
        return value
    left, operation, right = value
    if operation == "+":
        return yell_human(monkeys, left) + yell_human(monkeys, right)
    if operation == "-":
        return yell_human(monkeys, left) - yell_human(monkeys, right)
    if operation == "*":
        return yell_human(monkeys, left) * yell_human(monkeys, right)
    if operation == "/":
        return yell_human(monkeys, left) // yell_human(monkeys, right)
    raise ValueError(f"Unkown operation {operation}")


def reverse_yell(monkeys, monkey, wanted):
    if monkey == "humn":
        return wanted

    value = monkeys[monkey]

    if isinstance(value, int):
        return None

    left, operation, right = value
    try:
        left_value = yell_human(monkeys, left)
        # print("left:", left_value)
        if operation == "+":
            new_wanted = wanted - left_value
        elif operation == "-":
            new_wanted = left_value - wanted
        elif operation == "*":
            new_wanted = wanted // left_value
        elif operation == "/":
            new_wanted = left_value // wanted
        else:
            raise ValueError(f"Unkown operation {operation}")
        return reverse_yell(monkeys, right, new_wanted)
    except IsHuman:
        # print("Human on the left")
        pass

    try:
        right_value = yell_human(monkeys, right)
        # print("right:", right_value)
        if operation == "+":
            new_wanted = wanted - right_value
        elif operation == "-":
            new_wanted = wanted + right_value
        elif operation == "*":
            new_wanted = wanted // right_value
        elif operation == "/":
            new_wanted = wanted * right_value
        else:
            raise ValueError(f"Unkown operation {operation}")
        return reverse_yell(monkeys, left, new_wanted)
    except IsHuman:
        # print("Human on the right")
        pass

    raise ValueError(f'No human in "{monkey}" branch?')


def part1(data):
    return yell(monkey_tree(data), "root")


def part2(data):
    monkeys = monkey_tree(data)
    try:
        left = yell_human(monkeys, monkeys["root"][0])
        # print("left:", left)
        human = reverse_yell(monkeys, monkeys["root"][2], left)
    except IsHuman:
        pass
        # print("Human on the left")

    try:
        right = yell_human(monkeys, monkeys["root"][2])
        # print("right:", right)
        human = reverse_yell(monkeys, monkeys["root"][0], right)
    except IsHuman:
        pass
        # print("Human on the right")

    return human


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, 152, test_input_1)
    print()

    print("Test Part 2:")
    test_eq("Test 2.1", part2, 301, test_input_1)
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
