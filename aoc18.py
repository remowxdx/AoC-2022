#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 18


def get_input(filename):
    with open(filename, "r", encoding="ascii") as input_file:
        lines = input_file.read()
    return lines.splitlines()


def adjacent_cubes(cube):
    sides = [
        (1, 0, 0),
        (-1, 0, 0),
        (0, 1, 0),
        (0, -1, 0),
        (0, 0, 1),
        (0, 0, -1),
    ]
    result = []
    for side in sides:
        result.append(
            (
                cube[0] + side[0],
                cube[1] + side[1],
                cube[2] + side[2],
            )
        )
    return result


def surface(cubes):
    cubes = set(cubes)
    surface_sides = 0
    for cube in cubes:
        for adjacent_cube in adjacent_cubes(cube):
            if adjacent_cube not in cubes:
                surface_sides += 1
    return surface_sides


def part1(data):
    cubes = []
    for line in data:
        coords = line.split(",")
        cubes.append(
            (
                int(coords[0]),
                int(coords[1]),
                int(coords[2]),
            )
        )
    # print(surface(cubes))
    return surface(cubes)


class Lava:
    """Represents a scanned lava block."""

    def __init__(self, cubes):
        self.cubes = cubes
        self.find_bounding()
        self.visited = {}

    def is_outside(self, side_cube):
        to_visit = [side_cube]
        visited = set()
        while len(to_visit) > 0:
            cube = to_visit.pop(0)

            if cube in self.cubes:
                raise ValueError(f"Cube {cube} is part of lava.")

            if cube in self.visited:
                for visited_cube in visited:
                    self.visited[visited_cube] = self.visited[cube]
                return self.visited[cube]

            if self.out_of_bounding(cube):
                self.visited[cube] = True
                for internal in visited:
                    self.visited[internal] = True
                return True

            for adjacent in adjacent_cubes(cube):
                if adjacent in visited:
                    continue
                if adjacent in to_visit:
                    continue
                if adjacent in self.cubes:
                    continue
                to_visit.append(adjacent)
            visited.add(cube)
        # print(f"Internal {visited}")
        for internal in visited:
            self.visited[internal] = False
        self.visited[side_cube] = False
        return False

    def out_of_bounding(self, cube):
        for coord in range(3):
            if cube[coord] < self.bounding[coord][0]:
                return True
            if cube[coord] > self.bounding[coord][1]:
                return True
        return False

    def find_bounding(self):
        self.bounding = [
            (self.cubes[0][0], self.cubes[0][0]),
            (self.cubes[0][1], self.cubes[0][1]),
            (self.cubes[0][2], self.cubes[0][2]),
        ]
        for cube in self.cubes:
            for coord in range(3):
                self.bounding[coord] = (
                    min(cube[coord], self.bounding[coord][0]),
                    max(cube[coord], self.bounding[coord][1]),
                )
        # print(self.bounding)
        self.volume = 1
        for coord in range(3):
            self.volume *= self.bounding[0][1] - self.bounding[0][0]
        # print(f"Volume: {self.volume}")
        return self.bounding


def external_surface(cubes):
    external = 0
    lava = Lava(cubes)
    for cube in lava.cubes:
        for adjacent_cube in adjacent_cubes(cube):
            if adjacent_cube not in lava.cubes:
                if lava.is_outside(adjacent_cube):
                    # print(adjacent_cube)
                    external += 1
    return external


def part2(data):
    cubes = []
    for line in data:
        coords = line.split(",")
        cubes.append(
            (
                int(coords[0]),
                int(coords[1]),
                int(coords[2]),
            )
        )
    result = external_surface(cubes)
    print(result)
    return result


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, 64, test_input_1)
    print()

    print("Test Part 2:")
    test_eq("Test 2.1", part2, 58, test_input_1)
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
