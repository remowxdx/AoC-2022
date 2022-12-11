#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 11


def get_input(filename):
    with open(filename, "r", encoding="ascii") as input_file:
        lines = input_file.read()
    return lines.splitlines()


class Op:
    """Monkey operation"""

    def __init__(self, descr):
        self.lhs, self.operation, self.rhs = descr.split(" = ")[1].split()

    def eval(self, old):
        if self.lhs == "old":
            lhs = old
        elif self.lhs.isdecimal():
            lhs = int(self.lhs)
        else:
            raise ValueError(f"Invalid lhs {self.lhs}")

        if self.rhs == "old":
            rhs = old
        elif self.rhs.isdecimal():
            rhs = int(self.rhs)
        else:
            raise ValueError(f"Invalid rhs {self.rhs}")

        if self.operation == "+":
            return lhs + rhs
        if self.operation == "*":
            return lhs * rhs
        raise ValueError(f"Invalid operation {self.operation}")

    def magic(self):
        if self.operation != "*":
            return 0
        magic = 1
        if self.lhs != "old":
            magic *= int(self.lhs)
        if self.rhs != "old":
            magic *= int(self.rhs)
        return magic

    def __str__(self):
        return f"new = {self.lhs} {self.operation} {self.rhs}"


class Monkey:
    """Monkey class"""

    def __init__(self, panic=False):
        self.name = None
        self.items = []
        self.operation = None
        self.test = None
        self.test_target = [None, None]
        self.business = 0
        self.magic = [panic, None]

    def parse(self, line):
        magic = 0
        if line.startswith("Monkey"):
            self.name = int(line.split()[1].rstrip(":"))
        elif line.startswith("  Starting items: "):
            self.items = [int(item) for item in line.split(": ")[1].split(", ")]
        elif line.startswith("  Operation: "):
            self.operation = Op(line.split(": ")[1])
            magic = self.operation.magic()
        elif line.startswith("  Test: divisible by "):
            self.test = int(line.split()[-1])
            magic = self.test
        elif line.startswith("    If true: throw to monkey "):
            self.test_target[0] = int(line.split()[-1])
        elif line.startswith("    If false: throw to monkey "):
            self.test_target[1] = int(line.split()[-1])
        else:
            raise ValueError(f"Unknow monkey description: {line}")
        return magic

    def set_magic(self, magic):
        self.magic[1] = magic

    def receive(self, item):
        self.items.append(item)

    def turn(self):
        throw_list = []
        for item in self.items:
            throw_list.append(self.inspect(item))
        self.items = []
        return throw_list

    def inspect(self, item):
        self.business += 1
        worry_level = self.operation.eval(item)
        if self.magic[1] is not None:
            worry_level %= self.magic[1]
        if not self.magic[0]:
            worry_level //= 3
        if worry_level % self.test == 0:
            return worry_level, self.test_target[0]
        return worry_level, self.test_target[1]

    def __str__(self):
        out = []
        out.append(f"Monkey {self.name}:")
        out.append(f'  Starting items: {", ".join([str(item) for item in self.items])}')
        out.append(f"  Operation: {self.operation}")
        out.append(f"  Test: divisible by {self.test}")
        out.append(f"    If true: throw to monkey {self.test_target[0]}")
        out.append(f"    If false: throw to monkey {self.test_target[1]}")
        return "\n".join(out)


def throw(throw_list, monkey_list):
    for item, monkey in throw_list:
        monkey_list[monkey].receive(item)


def monkey_business(monkeys):
    max_business = [0, 0]
    for monkey in monkeys:
        min_ = min(max_business)
        if monkey.business > min_:
            max_business[max_business.index(min_)] = monkey.business
    return max_business[0] * max_business[1]


def part1(data):
    monkeys = [Monkey()]
    for line in data:
        if line == "":
            monkeys.append(Monkey())
            continue
        monkeys[-1].parse(line)

    for _round in range(20):
        for monkey in monkeys:
            throw_list = monkey.turn()
            throw(throw_list, monkeys)

    return monkey_business(monkeys)


def part2(data):
    magic = set()
    monkeys = [Monkey(panic=True)]
    for line in data:
        if line == "":
            monkeys.append(Monkey(panic=True))
            continue
        factor = monkeys[-1].parse(line)
        if factor > 1:
            magic.add(factor)

    magic_number = 1
    for factor in magic:
        magic_number *= factor

    for monkey in monkeys:
        monkey.set_magic(magic_number)

    for round_ in range(10000):
        for monkey in monkeys:
            throw_list = monkey.turn()
            throw(throw_list, monkeys)

        if False:
            if (round_ + 1) % 1000 == 0:
                print(f"Round: {round_}")
                for monkey in monkeys:
                    print(f"Monkey {monkey.name} {monkey.business}.")
    return monkey_business(monkeys)


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, 10605, test_input_1)
    print()

    print("Test Part 2:")
    test_eq("Test 2.1", part2, 2713310158, test_input_1)
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