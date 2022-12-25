#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 25


def get_input(filename):
    with open(filename, "r", encoding="ascii") as input_file:
        lines = input_file.read()
    return lines.splitlines()


def snafu_to_decimal(snafu):
    conv = {"0": 0, "1": 1, "2": 2, "-": -1, "=": -2}
    result = 0
    for digit in snafu:
        result = (result * 5) + conv[digit]
    return result


def decimal_to_snafu(number):
    digits = []
    while number > 0:
        number, digit = divmod(number, 5)
        if digit == 3:
            digits.append("=")
            number += 1
        elif digit == 4:
            digits.append("-")
            number += 1
        else:
            digits.append(str(digit))
    return "".join(reversed(digits))


def part1(data):
    total = 0
    for line in data:
        num = snafu_to_decimal(line)
        total += num
    # print(total)
    # print(decimal_to_snafu(total))
    return decimal_to_snafu(total)


def part2(_data):
    return 42


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, "2=-1=0", test_input_1)
    print()

    print("Test Part 2:")
    test_eq("Test 2.1", part2, 42, test_input_1)
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
