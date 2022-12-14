#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 14


def get_input(filename):
    with open(filename, "r", encoding="ascii") as input_file:
        lines = input_file.read()
    return lines.splitlines()


class Cave:
    """The scan of the cave."""

    def __init__(self, data):
        self.source = (500, 0)
        self.bounding = [self.source[0], self.source[0], self.source[1], self.source[1]]
        self.cave = {}
        self.steps = 0
        for line in data:
            prev = None
            for coords in line.split(" -> "):

                x, y = [int(num) for num in coords.split(",")]

                self.bounding[0] = min(x, self.bounding[0])
                self.bounding[1] = max(x, self.bounding[1])
                self.bounding[2] = min(y, self.bounding[2])
                self.bounding[3] = max(y, self.bounding[3])

                if prev is None:
                    prev = (x, y)
                    continue
                if prev[0] == x:
                    for i in range(min(prev[1], y), max(prev[1], y) + 1):
                        self.cave[(x, i)] = "#"
                elif prev[1] == y:
                    for i in range(min(prev[0], x), max(prev[0], x) + 1):
                        self.cave[(i, y)] = "#"
                else:
                    raise ValueError("Rock not horizontal nor vertical.")
                prev = (x, y)

    def step(self, sand):
        for next_sand in [
            (sand[0], sand[1] + 1),
            (sand[0] - 1, sand[1] + 1),
            (sand[0] + 1, sand[1] + 1),
        ]:
            if next_sand not in self.cave:
                sand = next_sand
                return False, sand
        return True, sand

    def next(self):
        sand = self.source
        while True:
            blocked, sand = self.step(sand)

            if blocked:
                self.cave[sand] = "o"
                self.steps += 1
                return True

            if sand[1] > self.bounding[3]:
                return False

    def next2(self):
        if self.source in self.cave:
            return False

        sand = self.source
        self.steps += 1
        while True:
            blocked, sand = self.step(sand)

            if blocked or sand[1] == self.bounding[3] + 1:
                self.cave[sand] = "o"
                return True

    def __str__(self):
        cave = ""
        for y in range(self.bounding[2], self.bounding[3] + 1):
            for x in range(self.bounding[0], self.bounding[1] + 1):
                if (x, y) in self.cave:
                    cave += self.cave[(x, y)]
                else:
                    cave += "."
            cave += "\n"
        return cave


def part1(data):
    cave = Cave(data)
    while cave.next():
        pass
    # print(cave)
    return cave.steps


def part2(data):
    cave = Cave(data)
    while cave.next2():
        pass
    # print(cave)
    return cave.steps


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, 24, test_input_1)
    print()

    print("Test Part 2:")
    test_eq("Test 2.1", part2, 93, test_input_1)
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
