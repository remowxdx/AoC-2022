#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 16


def get_input(filename):
    with open(filename, "r", encoding="ascii") as input_file:
        lines = input_file.read()
    return lines.splitlines()


def parse_line(line):
    valve_descr, tunnels_descr = line.split("; ")
    valve = valve_descr.split()
    name = valve[1]
    flow = int(valve[4].split("=")[1])
    tunnels = [valve.strip(",") for valve in tunnels_descr.split()[4:]]
    return name, flow, tunnels


def parse_maze(data):
    maze = {}
    for line in data:
        name, flow, tunnels = parse_line(line)
        maze[name] = (flow, tunnels)
    return maze


def pressure_release(maze, open_valves):
    pressure = 0
    for valve in open_valves:
        pressure += maze[valve][0]
    return pressure


cache = {}


def explore(maze, step, open_valves, position, pressure_released):
    global cache
    # print(step, open_valves, position, pressure_released)

    if step == 30:
        return pressure_released

    if len(open_valves) == len(maze):
        return explore(
            maze,
            step + 1,
            open_valves,
            position,
            pressure_released + pressure_release(maze, open_valves),
        )

    key = f"{step}_{'-'.join(open_valves)}_{position}"
    if key in cache:
        return pressure_released + cache[key]

    if maze[position][0] > 0 and position not in open_valves:
        # print(f"open {position}")
        open_valves_new = open_valves[:]
        open_valves_new.append(position)
        pressures = [
            explore(
                maze,
                step + 1,
                open_valves_new,
                position,
                pressure_release(maze, open_valves),
            )
        ]
    else:
        pressures = []

    for tunnel in maze[position][1]:
        pressures.append(
            explore(
                maze,
                step + 1,
                open_valves[:],
                tunnel,
                pressure_release(maze, open_valves),
            )
        )

    cache[key] = max(pressures)
    # print(key, cache[key])
    return pressure_released + cache[key]


def explore_2(maze, step, open_valves, positions, prev):
    global cache

    if step == 26:
        return 0

    key = f"{step}_{'-'.join(sorted(open_valves))}_{min(positions)}_{max(positions)}"
    if key in cache:
        # if step < 19:
        # print(key)
        # print(".", end="")
        return cache[key]

    pressure_released = pressure_release(maze, open_valves)

    # print()
    # print(key)
    if len(open_valves) == len(maze):
        # print("All valves open", step, open_valves, positions)
        return (26 - step) * pressure_released

    pressures = []
    # actions = []

    p1, p2 = positions

    if p1 != p2 and p1 not in open_valves and p2 not in open_valves:
        open_valves.add(p1)
        open_valves.add(p2)
        pressures.append(
            explore_2(
                maze,
                step + 1,
                open_valves,
                positions,
                (None, None),
            )
        )
        # actions.append(f"open {p1}, open {p2}")
        open_valves.remove(p2)
        open_valves.remove(p1)

    if p1 not in open_valves:
        # print(f"open {position}")
        open_valves.add(p1)
        for tunnel in maze[p2][1]:
            if tunnel == prev[1]:
                continue
            pressures.append(
                explore_2(
                    maze,
                    step + 1,
                    open_valves,
                    (p1, tunnel),
                    (None, p2),
                )
            )
            # actions.append(f"open {p1}, move {p2} -> {tunnel}")
        open_valves.remove(p1)

    if p2 not in open_valves:
        # print(f"open {position}")
        open_valves.add(p2)
        for tunnel in maze[p1][1]:
            if tunnel == prev[0]:
                continue
            pressures.append(
                explore_2(
                    maze,
                    step + 1,
                    open_valves,
                    (tunnel, p2),
                    (p1, None),
                )
            )
            # actions.append(f"move {p1} -> {tunnel}, open {p2}")
        open_valves.remove(p2)

    for tunnel_2 in maze[p2][1]:
        if len(maze[p2][1]) == 2 and tunnel_2 == prev[1]:
            continue
        for tunnel_1 in maze[p1][1]:
            if len(maze[p1][1]) == 2 and tunnel_1 == prev[0]:
                continue
            pressures.append(
                explore_2(
                    maze,
                    step + 1,
                    open_valves,
                    (tunnel_1, tunnel_2),
                    positions,
                )
            )
            # actions.append(f"move {p1} -> {tunnel_1}, move {p2} -> {tunnel_2}")

    if len(pressures) == 0:
        raise ValueError("No move possible.")
    result = max(pressures) + pressure_released
    # print(step, actions[pressures.index(max(pressures))])
    # print(key, cache[key])
    if step < 23:
        cache[key] = result
    return result


def part1(data):
    global cache

    maze = parse_maze(data)
    open_valves = [name for name, props in maze.items() if props[0] == 0]

    res = explore(maze, 0, open_valves, "AA", 0)
    cache = {}
    return res


def part2(data):
    global cache

    cache = {}
    maze = parse_maze(data)
    open_valves = {name for name, props in maze.items() if props[0] == 0}

    res = explore_2(maze, 0, open_valves, ("AA", "AA"), (None, None))
    return res


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, 1651, test_input_1)
    print()

    print("Test Part 2:")
    test_eq("Test 2.1", part2, 1707, test_input_1)
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
    # run_part1(True)
    run_part2(False)


if __name__ == "__main__":
    main()
