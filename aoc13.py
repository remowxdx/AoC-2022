#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 13


def get_input(filename):
    with open(filename, "r", encoding="ascii") as input_file:
        lines = input_file.read()
    return lines.splitlines()


class List:
    def __init__(self, line):
        self.list = self.parse(line)

    def parse(self, line):
        self.parse_pos = 0
        self.line = line
        char = self.next()
        if char == "[":
            this = self.parse_list()
        return this

    def parse_int(self, char):
        num = 0
        while char.isnumeric():
            num = num * 10 + int(char)
            char = self.next()
        return num, char

    def parse_list(self):
        char = self.next()
        this = []
        while char != "]":
            if char == "[":
                this.append(self.parse_list())
                char = self.next()
            elif char == ",":
                char = self.next()
            elif char.isnumeric():
                num, char = self.parse_int(char)
                this.append(num)
            else:
                raise ValueError("Unexpected char.")
        return this

    def next(self):
        char = self.line[self.parse_pos]
        self.parse_pos += 1
        return char

    def as_str(self, lst):
        if isinstance(lst, int):
            return str(lst)
        return f'[{",".join([self.as_str(item) for item in lst])}]'

    def __str__(self):
        return self.as_str(self.list)

    def compare_items(self, left, right):
        # print(f"Compare {left} and {right}")

        if isinstance(left, int) and isinstance(right, int):
            # print(f"num {left} < num{right}?")
            if left < right:
                # print(f"{left} < {right}")
                return -1
            if left > right:
                # print(f"{left} > {right}")
                return 1
            # print(f"{left} == {right}")
            return 0

        if isinstance(left, int):
            left = [left]

        if isinstance(right, int):
            right = [right]

        for left_it, right_it in zip(left, right):
            res = self.compare_items(left_it, right_it)
            if res != 0:
                # if res == -1:
                # print(f"{left} < {right}")
                # else:
                # print(f"{left} > {right}")
                return res

        if len(left) < len(right):
            # print(f"{left} < {right}")
            return -1

        if len(left) > len(right):
            # print(f"{left} > {right}")
            return 1

        # print("Left and right are equal")
        # print(f"{left} == {right}")
        return 0

    def __lt__(self, other):
        return self.compare_items(self.list, other.list) == -1


def part1(data):
    msgs = []
    for line in data:
        if line == "":
            continue
        lst = List(line)
        if line != str(lst):
            print(line, lst)
            exit(1)
        msgs.append(lst)

    # print("\n".join([str(msg) for msg in msgs]))

    sum_ = 0
    for i in range(len(msgs) // 2):
        if msgs[2 * i] < msgs[2 * i + 1]:
            # print(f"Pair {i+1} in order.")
            sum_ += i + 1
        else:
            # print(f"Pair {i+1} not in order.")
            pass

    return sum_


def part2(data):
    msgs = []
    for line in data:
        if line == "":
            continue
        lst = List(line)
        if line != str(lst):
            print(line, lst)
            exit(1)
        msgs.append(lst)

    divider1 = "[[2]]"
    divider2 = "[[6]]"
    msgs.append(List(divider1))
    msgs.append(List(divider2))

    key = 1
    for i, msg in enumerate(sorted(msgs)):
        if str(msg) == divider1:
            key *= i + 1
        if str(msg) == divider2:
            key *= i + 1
    return key


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, 13, test_input_1)
    print()

    print("Test Part 2:")
    test_eq("Test 2.1", part2, 140, test_input_1)
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
