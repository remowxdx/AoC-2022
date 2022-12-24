#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 24


def get_input(filename):
    with open(filename, "r", encoding="ascii") as input_file:
        lines = input_file.read()
    return lines.splitlines()


class Valley:
    """The blizzard valley"""

    DIRECTIONS = [
        (0, -1),
        (-1, 0),
        (0, 0),
        (1, 0),
        (0, 1),
    ]

    def __init__(self, data):
        self.width = len(data[0]) - 2
        self.height = len(data) - 2
        self.blizzards_v = [[] for _ in range(len(data[0]) - 2)]
        self.blizzards_h = [[] for _ in range(len(data) - 2)]
        self.start = None
        self.end = None
        self.read(data)

    def read(self, data):
        for y, line in enumerate(data):
            for x, char in enumerate(line):
                if y == 0 and char == ".":
                    self.start = (x - 1, y - 1)
                    break
                if line[1] == "#" and char == ".":
                    self.end = (x - 1, y - 1)
                    break
                if char == "v":
                    self.blizzards_v[x - 1].append((y - 1, 1))
                elif char == "^":
                    self.blizzards_v[x - 1].append((y - 1, -1))
                elif char == "<":
                    self.blizzards_h[y - 1].append((x - 1, -1))
                elif char == ">":
                    self.blizzards_h[y - 1].append((x - 1, 1))

    def in_valley(self, pos):
        if pos == self.start:
            return True
        if pos == self.end:
            return True
        if pos[0] < 0 or pos[0] >= self.width:
            return False
        if pos[1] < 0 or pos[1] >= self.height:
            return False
        return True

    def neighbors(self, pos):
        result = []
        for dir_ in self.DIRECTIONS:
            new_pos = (pos[0] + dir_[0], pos[1] + dir_[1])
            if self.in_valley(new_pos):
                result.append(new_pos)
        return result

    def is_free(self, pos, time):
        if pos in (self.start, self.end):
            return True
        for start, step in self.blizzards_h[pos[1]]:
            if (start + step * time) % self.width == pos[0]:
                return False
        for start, step in self.blizzards_v[pos[0]]:
            if (start + step * time) % self.height == pos[1]:
                return False
        return True

    def find_way(self, from_, to, start_time):
        time = start_time
        to_visit = [(from_, time)]
        visited = set()
        nearest = abs(to[0] - from_[0]) + abs(to[1] - from_[1])
        while len(to_visit) > 0:
            pos, time = to_visit.pop(0)
            visited.add((pos, time))
            dist = abs(to[0] - pos[0]) + abs(to[1] - pos[1])
            if dist < nearest:
                # print(pos, time, dist, len(to_visit))
                nearest = dist
            if not self.is_free(pos, time):
                continue
            if dist - nearest > 50:
                continue
            for new_pos in self.neighbors(pos):
                if (new_pos, time + 1) in visited:
                    continue
                if (new_pos, time + 1) in to_visit:
                    continue
                if new_pos == to:
                    # print(to, pos, new_pos, time)
                    return time + 1
                to_visit.append((new_pos, time + 1))
        raise ValueError(f"No way out in {time}.")


def part1(data):
    valley = Valley(data)
    return valley.find_way(valley.start, valley.end, 0)


def part2(data):
    valley = Valley(data)
    there = valley.find_way(valley.start, valley.end, 0)
    # print("There:", there)
    back = valley.find_way(valley.end, valley.start, there)
    # print("Back:", back)
    there_again = valley.find_way(valley.start, valley.end, back)
    return there_again


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, 18, test_input_1)
    print()

    print("Test Part 2:")
    test_eq("Test 2.1", part2, 54, test_input_1)
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
