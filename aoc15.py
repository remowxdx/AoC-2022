#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 15


def get_input(filename):
    with open(filename, "r", encoding="ascii") as input_file:
        lines = input_file.read()
    return lines.splitlines()


def distance(from_, to_):
    return abs(from_[0] - to_[0]) + abs(from_[1] - to_[1])


def overlaps(int1, int2):
    if int1[1] < int2[0]:
        return False
    if int1[0] > int2[1]:
        return False
    return True


def line_cover(sensors, row):
    cover = []
    for sensor, beacon in sensors.items():

        radius = beacon[1]
        dist = abs(sensor[1] - row)

        if dist > radius:
            continue

        start = sensor[0] - (radius - dist)
        end = sensor[0] + (radius - dist)

        # print(cover, (start, end), sensor, beacon[1])

        new_cover = []
        state = "insert"
        for interval in cover:
            if state == "insert":
                if end < interval[0]:
                    new_cover.append((start, end))
                    state = "finish"
                if overlaps((start, end), interval):
                    start, end = (min(start, interval[0]), max(end, interval[1]))
                if start > interval[1]:
                    new_cover.append(interval)
                    state = "insert"
            if state == "finish":
                new_cover.append(interval)
        if state == "insert":
            new_cover.append((start, end))
        cover = new_cover
    return cover


def part1(data):
    sensors = {}
    beacons = set()
    for line in data:
        tokens = line.split()
        sensor = (
            int(tokens[2].strip(",").split("=")[1]),
            int(tokens[3].strip(":").split("=")[1]),
        )
        beacon = (int(tokens[8].strip(",").split("=")[1]), int(tokens[9].split("=")[1]))
        dist = distance(sensor, beacon)
        sensors[sensor] = (beacon, dist)
        beacons.add(beacon)

    if len(data) == 14:
        row = 10
    else:
        row = 2000000

    cover = line_cover(sensors, row)

    count = 0
    for beacon in beacons:
        if beacon[1] == row:
            count += 1

    # print(cover, count)

    return sum([end - start for start, end in cover]) - count + 1


def part2(data):
    sensors = {}
    beacons = set()
    for line in data:
        tokens = line.split()
        sensor = (
            int(tokens[2].strip(",").split("=")[1]),
            int(tokens[3].strip(":").split("=")[1]),
        )
        beacon = (int(tokens[8].strip(",").split("=")[1]), int(tokens[9].split("=")[1]))
        dist = distance(sensor, beacon)
        sensors[sensor] = (beacon, dist)
        beacons.add(beacon)

    if len(data) == 14:
        height = 20
    else:
        height = 4000000

    for row in range(height + 1):
        cover = line_cover(sensors, row)
        if len(cover) == 2:
            print(cover, row)
            return (cover[0][1] + 1) * 4_000_000 + row

    return None


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, 26, test_input_1)
    print()

    print("Test Part 2:")
    test_eq("Test 2.1", part2, 56000011, test_input_1)
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
    run_part2(False)


if __name__ == "__main__":
    main()
