#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 19


def get_input(filename):
    with open(filename, "r", encoding="ascii") as input_file:
        lines = input_file.read()
    return lines.splitlines()


def parse_blueprint(line):
    robots = {}
    blueprint, description = line.split(": ")
    # number = int(blueprint.split()[1])
    robot_descriptions = description.split(".")
    for robot_description in robot_descriptions:
        if robot_description == "":
            continue
        robot_type = robot_description.split()[1]
        robot_cost_description = robot_description.split("costs ")[1]
        robot_material_descriptions = robot_cost_description.split(" and ")
        robot_cost = {}
        for robot_material_description in robot_material_descriptions:
            robot_material = robot_material_description.split()
            robot_cost[robot_material[1]] = int(robot_material[0])

        robots[robot_type] = robot_cost

    costs = []
    for robot_type in ("ore", "clay", "obsidian", "geode"):
        cost = []
        for material in ("ore", "clay", "obsidian", "geode"):
            if material in robots[robot_type]:
                cost.append(robots[robot_type][material])
            else:
                cost.append(0)
        costs.append(tuple(cost))

    return tuple(costs)


class MostGeodes:
    def __init__(self, blueprint, max_steps):
        self.blueprint = blueprint
        self.max_steps = max_steps
        self.best = 0
        self.count = 0
        self.cache = {}

    def factory_wait(self, factory):
        wait_times = [
            [
                -(-self.blueprint[robot_type][mat] // factory[2][mat]) - factory[1][mat]
                if factory[2][mat] > 0
                else 0
                for mat in range(4)
            ]
            for robot_type in range(4)
        ]
        max_wait = max([max(robot) for robot in wait_times])
        return max_wait

    def step(self, factory, factory_wait, wait):
        if factory in self.cache:
            return self.cache[factory]

        # self.count += 1
        # if factory[0] == 24:
        #     print(self.count, factory)

        geodes = factory[1][3]

        if geodes > self.best:
            # print("M", factory)
            self.best = geodes

        if factory[0] == self.max_steps:
            return geodes

        rest = self.max_steps - factory[0]
        potential = (
            geodes + rest * factory[2][3] + rest * (factory[2][3] + 1) * (rest - 1) / 2
        )
        if potential < self.best:
            return 0

        # print(factory)

        geodes = []

        for robot in range(3, -1, -1):
            if self.can_build(factory, robot):
                new_factory = self.work(factory, robot)
                geodes.append(self.step(new_factory, self.factory_wait(factory), 0))

        if len(geodes) == 0 or wait < factory_wait:
            geodes.append(self.step(self.work(factory), factory_wait, wait + 1))

        self.cache[factory] = max(geodes)
        return max(geodes)

    def can_build(self, factory, robot_nr):
        robot = self.blueprint[robot_nr]
        return (
            factory[1][0] >= robot[0]
            and factory[1][1] >= robot[1]
            and factory[1][2] >= robot[2]
            and factory[1][3] >= robot[3]
        )

    def work(self, factory, robot_nr=None):
        if robot_nr is None:
            return (
                factory[0] + 1,
                (
                    factory[1][0] + factory[2][0],
                    factory[1][1] + factory[2][1],
                    factory[1][2] + factory[2][2],
                    factory[1][3] + factory[2][3],
                ),
                factory[2],
            )
        robot = tuple(1 if robot_nr == i else 0 for i in range(4))
        cost = self.blueprint[robot_nr]
        return (
            factory[0] + 1,
            (
                factory[1][0] + factory[2][0] - cost[0],
                factory[1][1] + factory[2][1] - cost[1],
                factory[1][2] + factory[2][2] - cost[2],
                factory[1][3] + factory[2][3] - cost[3],
            ),
            (
                factory[2][0] + robot[0],
                factory[2][1] + robot[1],
                factory[2][2] + robot[2],
                factory[2][3] + robot[3],
            ),
        )


def part1(data):

    blueprints = []
    for line in data:
        blueprints.append(parse_blueprint(line))

    # print("\n".join([str(bp) for bp in blueprints]))

    total_quality_level = 0
    for i, blueprint in enumerate(blueprints):
        print(blueprint)
        factory = (0, (0, 0, 0, 0), (1, 0, 0, 0))
        finder = MostGeodes(blueprint, 24)
        geodes = finder.step(factory, finder.factory_wait(factory), 0)
        print(geodes)
        total_quality_level += geodes * (i + 1)
        print()

    return total_quality_level


def part2(data):

    blueprints = []
    for line in data[0:3]:
        blueprints.append(parse_blueprint(line))

    # print("\n".join([str(bp) for bp in blueprints]))

    most_geodes = []
    for i, blueprint in enumerate(blueprints):
        print(blueprint)
        factory = (0, (0, 0, 0, 0), (1, 0, 0, 0))
        finder = MostGeodes(blueprint, 32)
        geodes = finder.step(factory, finder.factory_wait(factory), 0)
        print(geodes)
        most_geodes.append(geodes)
        print()

    print(most_geodes)
    # return most_geodes[0] * most_geodes[1] * most_geodes[2]
    result = 1
    for geodes in most_geodes:
        result *= geodes
    return result


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, 33, test_input_1)
    print()

    print("Test Part 2:")
    test_eq("Test 2.1", part2, 62 * 56, test_input_1)
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
    # run_tests()
    run_part1(True)
    run_part2(True)


if __name__ == "__main__":
    main()
