#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 17

ROCKS = [
    [(0, 0), (1, 0), (2, 0), (3, 0)],
    [(1, 0), (0, 1), (1, 1), (2, 1), (1, 2)],
    [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)],
    [(0, 0), (0, 1), (0, 2), (0, 3)],
    [(0, 0), (1, 0), (0, 1), (1, 1)],
]


class Chamber:
    def __init__(self, jets):
        self.chamber = {}
        self.width = 7
        self.height = -1
        self.jets = jets
        self.jet_index = 0

    def jet(self):
        jet = self.jets[self.jet_index]
        self.jet_index = (self.jet_index + 1) % len(self.jets)
        return jet

    def fall_one(self, pos, rock):
        for part in rock:
            if pos[1] == 0:
                # print(f"Rock resting on {pos}")
                return True, pos
            if (pos[0] + part[0], pos[1] + part[1] - 1) in self.chamber:
                # print(f"Rock resting on {pos}")
                return True, pos
        # print(f"Rock falling to {pos[1] - 1}")
        return False, (pos[0], pos[1] - 1)

    def push(self, pos, rock):
        jet = self.jet()
        for part in rock:
            if jet == ">":
                dir_ = 1
            elif jet == "<":
                dir_ = -1
            else:
                raise ValueError(f"Unknown direction {jet}.")

            test_pos = (pos[0] + part[0] + dir_, pos[1] + part[1])
            if test_pos in self.chamber or test_pos[0] < 0 or test_pos[0] > 6:
                # print(f"Rock not pushed {pos}.")
                return pos

        # print(f"Rock pushed {(pos[0] + dir_, pos[1])}.")
        return (pos[0] + dir_, pos[1])

    def fall(self, rock):
        pos = (2, self.height + 4)
        while True:
            pos = self.push(pos, rock)
            resting, pos = self.fall_one(pos, rock)
            if resting:
                break

        for part in rock:
            self.height = max(pos[1] + part[1], self.height)
            self.chamber[(pos[0] + part[0], pos[1] + part[1])] = "#"
        # print(f"Height: {self.height}")

    def __str__(self):
        rows = []
        for row in range(self.height, -1, -1):
            rows.append(
                "".join(
                    [
                        self.chamber[(x, row)] if (x, row) in self.chamber else "."
                        for x in range(7)
                    ]
                )
            )
        return "\n".join(rows)


def get_input(filename):
    with open(filename, "r", encoding="ascii") as input_file:
        lines = input_file.read()
    return lines.splitlines()


def part1(data):
    chamber = Chamber(data[0])
    for step in range(2022):
        # if (step - 455) % 1710 == 0:
        # print(step, chamber.height, chamber.jet_index, len(chamber.jets))
        chamber.fall(ROCKS[step % len(ROCKS)])
    # print(step, chamber)
    return chamber.height + 1


def part2(data):
    if len(data[0]) == 40:
        return 0
    chamber = Chamber(data[0])
    num_rocks = 1000000000000
    # print(len(ROCKS), len(chamber.jets))
    heights = []
    rows = []
    jet = None
    for step in range(num_rocks):
        jet = chamber.jet_index
        chamber.fall(ROCKS[step % len(ROCKS)])
        heights.append(chamber.height)
        found = True
        for i in range(7):
            if (i, chamber.height) not in chamber.chamber:
                found = False
        if found:
            if len(rows) == 0 or step - rows[0] < len(ROCKS) * len(chamber.jets):
                rows.append(step)
                # print("shj", step, chamber.height, jet)
            else:
                # print(rows)
                prev = rows[0]
                # for row in rows[1:]:
                #    print(
                #        row,
                #        row - prev,
                #        heights[row],
                #        heights[prev],
                #        heights[row] - heights[prev],
                #    )
                #    prev = row
                break

    # step = 455, h=713
    # step = 455 + 1710, h=713+2647
    offset = rows[0]
    period = rows[3] - rows[1]
    offset_height = heights[offset]
    period_height = heights[rows[3]] - heights[rows[1]]
    # print(offset, period)
    # print(offset_height, period_height)
    repeats = (num_rocks - offset) // period
    # print(repeats)
    step = offset + period * repeats
    # print("step:", step)
    h = offset_height + period_height * repeats
    # print("h:", h, "j:", jet)
    # print(
    #     "step: 19265, h:",
    #     offset_height + period_height * ((19265 - offset) // period),
    # )

    rest_chamber = Chamber(data[0])
    for x in range(7):
        rest_chamber.chamber[(x, h)] = "#"
    rest_chamber.height = h
    rest_chamber.jet_index = jet
    # print("h:", rest_chamber.height, "i:", rest_chamber.jet_index)
    for rest_step in range(step, num_rocks):
        rest_chamber.fall(ROCKS[rest_step % len(ROCKS)])
    # print(rest_chamber.height - 29830)
    return rest_chamber.height + 1


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, 3068, test_input_1)
    print()

    print("Test Part 2:")
    test_eq("Test 2.1", part2, 1514285714288, test_input_1)
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
