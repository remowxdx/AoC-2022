#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 8


def get_input(filename):
    with open(filename, "r", encoding="ascii") as input_file:
        lines = input_file.read()
    return lines.splitlines()


def visible_trees(grid):
    visible_trees = 0
    for coords, tree in grid.items():
        visible_from_left = True
        visible_from_top = True
        visible_from_right = True
        visible_from_bottom = True
        if coords == "width" or coords == "height":
            continue
        x, y = coords
        for col in range(x):
            if grid[(col, y)] >= tree:
                visible_from_left = False
                break

        for col in range(grid["width"], x, -1):
            if grid[(col, y)] >= tree:
                visible_from_right = False
                break

        for row in range(y):
            if grid[(x, row)] >= tree:
                visible_from_top = False
                break

        for row in range(grid["height"], y, -1):
            if grid[(x, row)] >= tree:
                visible_from_bottom = False
                break

        if (
            visible_from_left
            or visible_from_right
            or visible_from_top
            or visible_from_bottom
        ):
            visible_trees += 1
            # print(coords, tree, "is visible")
        else:
            # print(coords, tree, "is not visible")
            pass
    return visible_trees


def part1(data):
    grid = {}
    for row, line in enumerate(data):
        for col, char in enumerate(line):
            grid[(col, row)] = int(char)
    grid["width"] = col
    grid["height"] = row
    # print(grid)

    return visible_trees(grid)


def scenic_score(grid, coords):
    col, row = coords
    tree = grid[coords]

    top_vd = 0
    for y in range(row - 1, -1, -1):
        top_vd += 1
        if grid[(col, y)] >= tree:
            break

    bottom_vd = 0
    for y in range(row + 1, grid["height"]):
        bottom_vd += 1
        if grid[(col, y)] >= tree:
            break

    left_vd = 0
    for x in range(col - 1, -1, -1):
        left_vd += 1
        if grid[(x, row)] >= tree:
            break

    right_vd = 0
    for x in range(col + 1, grid["width"]):
        right_vd += 1
        if grid[(x, row)] >= tree:
            break

    return top_vd * bottom_vd * left_vd * right_vd


def part2(data):
    grid = {}
    for row, line in enumerate(data):
        for col, char in enumerate(line):
            grid[(col, row)] = int(char)
    grid["width"] = col + 1
    grid["height"] = row + 1

    max_score = 0
    for coords, tree in grid.items():
        if coords == "width" or coords == "height":
            continue
        score = scenic_score(grid, coords)
        if score > max_score:
            max_score = score
    return max_score


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, 21, test_input_1)
    print()

    print("Test Part 2:")
    test_eq("Test 2.1", part2, 8, test_input_1)
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
