#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 11


def get_input(filename):
    with open(filename, "r", encoding="ascii") as input_file:
        lines = input_file.read()
    return lines.splitlines()


class Operation:
    """Monkey operation"""

    def __init__(self, operation):
        self.left_op, self.operation, self.right_op = operation.split(" = ")[1].split()

    def new_worry_level(self, old):
        if self.left_op == "old":
            left_op = old
        elif self.left_op.isdecimal():
            left_op = int(self.left_op)
        else:
            raise ValueError(f"Invalid left operand {self.left_op}")

        if self.right_op == "old":
            right_op = old
        elif self.right_op.isdecimal():
            right_op = int(self.right_op)
        else:
            raise ValueError(f"Invalid right operand {self.right_op}")

        if self.operation == "+":
            return left_op + right_op
        if self.operation == "*":
            return left_op * right_op
        raise ValueError(f"Invalid operation {self.operation}")

    def get_magic(self):
        if self.operation != "*":
            return 0
        magic = 1
        if self.left_op != "old":
            magic *= int(self.left_op)
        if self.right_op != "old":
            magic *= int(self.right_op)
        return magic

    def __str__(self):
        return f"new = {self.left_op} {self.operation} {self.right_op}"


class Monkey:
    """A Monkey in the game"""

    def __init__(self, game):
        self.name = None
        self.game = game
        self.items = []
        self.operation = None
        self.test = None
        self.test_target = [None, None]
        self.business = 0

    def note(self, line):
        if line.startswith("Monkey"):
            self.name = int(line.split()[1].rstrip(":"))
        elif line.startswith("  Starting items: "):
            self.items = [int(item) for item in line.split(": ")[1].split(", ")]
        elif line.startswith("  Operation: "):
            self.operation = Operation(line.split(": ")[1])
            self.game.magic.build(self.operation.get_magic())
        elif line.startswith("  Test: divisible by "):
            self.test = int(line.split()[-1])
            self.game.magic.build(self.test)
        elif line.startswith("    If true: throw to monkey "):
            self.test_target[0] = int(line.split()[-1])
        elif line.startswith("    If false: throw to monkey "):
            self.test_target[1] = int(line.split()[-1])
        else:
            raise ValueError(f"Unknow monkey description: {line}")

    def catch(self, item):
        self.items.append(item)

    def play_turn(self):
        for item in self.items:
            worry_level, target = self.inspect(item)
            self.game.throw_item(worry_level, target)
        self.items = []

    def inspect(self, item):
        self.business += 1

        worry_level = self.operation.new_worry_level(item)
        if self.game.panic:
            worry_level = self.game.magic.manage_panic(worry_level)
        else:
            worry_level //= 3

        if worry_level % self.test == 0:
            return worry_level, self.test_target[0]
        return worry_level, self.test_target[1]

    def __str__(self):
        out = []
        out.append(f"Monkey {self.name}:")
        out.append(f'  Items: {", ".join([str(item) for item in self.items])}')
        out.append(f"  Operation: {self.operation}")
        out.append(f"  Test: divisible by {self.test}")
        out.append(f"    If true: throw to monkey {self.test_target[0]}")
        out.append(f"    If false: throw to monkey {self.test_target[1]}")
        out.append(f"  Business level: {self.business}")
        return "\n".join(out)


class Magic:
    """Christmas Magic"""

    def __init__(self):
        self._numbers = set()
        self._magic_number = 1

    def manage_panic(self, worry_level):
        return worry_level % self._magic_number

    def build(self, number):
        if number > 1 and number not in self._numbers:
            self._numbers.add(number)
            self._magic_number *= number


class KeepAway:
    """A monkey's game."""

    def __init__(self, notes, panic):
        self.magic = Magic()
        self.panic = panic
        self.monkeys = self.observe_monkeys(notes)

    def observe_monkeys(self, notes):
        monkeys = [Monkey(self)]
        for line in notes:
            if line == "":
                monkeys.append(Monkey(self))
            else:
                monkeys[-1].note(line)
        return monkeys

    def play_round(self):
        for monkey in self.monkeys:
            monkey.play_turn()

    def throw_item(self, item, to_monkey):
        self.monkeys[to_monkey].catch(item)

    def monkey_business(self):
        most_active = [0, 0]
        for monkey in self.monkeys:
            min_ = min(most_active)
            if monkey.business > min_:
                most_active[most_active.index(min_)] = monkey.business
        return most_active[0] * most_active[1]


def part1(notes):
    game = KeepAway(notes, panic=False)

    for _round in range(20):
        game.play_round()

    return game.monkey_business()


def part2(notes):
    game = KeepAway(notes, panic=True)

    for _round in range(10000):
        game.play_round()

    return game.monkey_business()


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
