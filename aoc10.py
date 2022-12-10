#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 10


def get_input(filename):
    with open(filename, "r", encoding="ascii") as input_file:
        lines = input_file.read()
    return lines.splitlines()


class CPU:
    """The CPU."""

    def __init__(self, program):
        self.X = 1
        self.cycle = 0
        self.program = program
        self.counter = -1
        self.instruction = None

    def tick(self):
        if self.instruction is None:
            self.counter += 1
            instruction = self.program[self.counter].split()
            if instruction[0] == "noop":
                self.instruction = None
            elif instruction[0] == "addx":
                self.instruction = instruction
            else:
                raise ValueError(f"Instruction {instruction[0]} unknown.")
        else:
            self.X += int(self.instruction[1])
            self.instruction = None
        self.cycle += 1

    def signal_strength(self):
        return (self.cycle + 1) * self.X


class Display:
    """The disaplay"""

    def __init__(self):
        self.display = [["." for _ in range(40)] for _ in range(6)]

    def set_pixel(self, x, y, val):
        self.display[y][x] = val

    def scan(self, cpu):
        x = cpu.cycle % 40
        y = (cpu.cycle // 40) % 6
        if abs(x - cpu.X) <= 1:
            self.set_pixel(x, y, "#")
        else:
            self.set_pixel(x, y, ".")

    def __str__(self):
        return "\n".join(["".join(row) for row in self.display])


def example():
    cpu = CPU(
        [
            "noop",
            "addx 3",
            "addx -5",
        ]
    )
    for _ in range(5):
        print(cpu.cycle, cpu.X, cpu.counter)
        cpu.tick()


def part1(data):
    cpu = CPU(data)
    signals = 0
    for _ in range(220):
        cpu.tick()
        if cpu.cycle % 40 == 19:
            # print(cpu.signal_strength(), cpu.cycle, cpu.X)
            signals += cpu.signal_strength()
    return signals


def part2(data):
    cpu = CPU(data)
    display = Display()
    for _ in range(240):
        display.scan(cpu)
        cpu.tick()
    return str(display)


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, 13140, test_input_1)
    print()

    print("Test Part 2:")
    test_eq(
        "Test 2.1",
        part2,
        "\n".join(
            [
                "##..##..##..##..##..##..##..##..##..##..",
                "###...###...###...###...###...###...###.",
                "####....####....####....####....####....",
                "#####.....#####.....#####.....#####.....",
                "######......######......######......####",
                "#######.......#######.......#######.....",
            ]
        ),
        test_input_1,
    )
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
    print(f"Part 2:\n{result2}")
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
