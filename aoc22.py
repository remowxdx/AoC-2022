#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 22


def get_input(filename):
    with open(filename, "r", encoding="ascii") as input_file:
        lines = input_file.read()
    return lines.splitlines()


def read_board(data):
    area_tot = 0
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char != " ":
                area_tot += 1
    area_face = area_tot // 6
    for side in range(area_face):
        if side * side == area_face:
            break
    else:
        raise ValueError("Side length not found.")
    grid = {}
    faces = set()
    max_x, max_y = 0, 0
    face = (0, 0)
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char != " ":
                grid[(x, y)] = char
                face = (x // side, y // side)
                faces.add(face)
            else:
                pass
            max_x = max(max_x, face[0])
        max_y = max(max_y, face[1])
    return grid, faces, side, (max_x + 1, max_y + 1)


def read_directions(directions_descr):
    directions = []
    direction = 0
    steps = 0
    i = 0
    while i < len(directions_descr):
        if directions_descr[i].isnumeric():
            steps = steps * 10 + int(directions_descr[i])
        else:
            directions.append((steps, directions_descr[i]))
            steps = 0
        i += 1
    directions.append((steps, "X"))
    return directions


def print_grid(grid, side, faces_dim):
    for y in range(faces_dim[1] * side):
        for x in range(faces_dim[0] * side):
            if (x, y) in grid:
                print(grid[(x, y)], end="")
            else:
                print(" ", end="")
        print()


DIRECTIONS = [(1, 0), (0, 1), (-1, 0), (0, -1)]
DIRECTIONS_STR = [">", "v", "<", "^"]


def next_tile_and_direction(pos, direction, faces, side, faces_dim):
    face = (pos[0] // side, pos[1] // side)
    face_pos = (pos[0] % side, pos[1] % side)
    # print(pos, face, face_pos)
    new_pos = (
        pos[0] + DIRECTIONS[direction][0],
        pos[1] + DIRECTIONS[direction][1],
    )
    new_face_pos = (new_pos[0] % side, new_pos[1] % side)
    new_face = (new_pos[0] // side, new_pos[1] // side)
    # print("B:", new_pos, new_face, new_face_pos)
    while new_face not in faces:
        if DIRECTIONS[direction][0] < 0:
            new_face = ((new_face[0] - 1) % faces_dim[0], new_face[1])
        if DIRECTIONS[direction][0] > 0:
            new_face = ((new_face[0] + 1) % faces_dim[0], new_face[1])
        if DIRECTIONS[direction][1] < 0:
            new_face = (new_face[0], (new_face[1] - 1) % faces_dim[1])
        if DIRECTIONS[direction][1] > 0:
            new_face = (new_face[0], (new_face[1] + 1) % faces_dim[1])
    new_face_pos = (new_face_pos[0] % side, new_face_pos[1] % side)
    new_pos = (
        new_face[0] * side + new_face_pos[0],
        new_face[1] * side + new_face_pos[1],
    )
    # print("A:", new_pos, new_face, new_face_pos)
    return new_pos, direction


def test_cube_wrap(pos, direction):
    if direction == 3:
        if pos[1] == 0:
            new_direction = 1
            new_pos = (11 - pos[0], 4)
        if pos[1] == 4 and pos[0] < 4:
            new_direction = 1
            new_pos = (11 - pos[0], 0)
        if pos[1] == 4 and pos[0] > 3:
            new_direction = 0
            new_pos = (8, pos[0] - 4)
        if pos[1] == 8:
            new_direction = 2
            new_pos = (11, 10 - pos[0])
    if direction == 2:
        if pos[0] == 8 and pos[1] < 4:
            new_direction = 1
            new_pos = (pos[1] + 4, 4)
        if pos[0] == 0:
            new_direction = 3
            new_pos = (19 - pos[1], 11)
        if pos[0] == 8 and pos[1] >= 8:
            new_direction = 3
            new_pos = (15 - pos[1], 7)
    if direction == 1:
        if pos[1] == 7 and pos[0] < 4:
            new_direction = 3
            new_pos = (11 - pos[0], 11)
        if pos[1] == 7 and 3 < pos[0] < 8:
            new_direction = 0
            new_pos = (8, 11 - pos[0])
        if pos[1] == 11 and pos[0] < 12:
            new_direction = 3
            new_pos = (11 - pos[0], 7)
        if pos[1] == 11 and pos[0] > 11:
            new_direction = 0
            new_pos = (0, 11 - pos[0])
    if direction == 0:
        if pos[0] == 11 and pos[1] < 4:
            new_direction = 2
            new_pos = (15, 11 - pos[1])
        if pos[0] == 11 and pos[1] > 3:
            new_direction = 1
            new_pos = (19 - pos[1], 8)
        if pos[0] == 15:
            new_direction = 2
            new_pos = (11, 11 - pos[1])
    return new_pos, new_direction


def real_cube_wrap(pos, direction):
    if direction == 3:
        # A
        if pos[1] == 0 and pos[0] < 100:
            new_direction = 0
            new_pos = (0, pos[0] + 100)
        # B
        if pos[1] == 0 and pos[0] > 99:
            new_direction = 3
            new_pos = (pos[0] - 100, 199)
        # E
        if pos[1] == 100:
            new_direction = 0
            new_pos = (50, 50 + pos[0])
    if direction == 2:
        # C
        if pos[0] == 50 and pos[1] < 50:
            new_direction = 0
            new_pos = (0, 149 - pos[1])
        # E
        if pos[0] == 50 and pos[1] > 49:
            new_direction = 1
            new_pos = (pos[1] - 50, 100)
        # C
        if pos[0] == 0 and pos[1] < 150:
            new_direction = 0
            new_pos = (50, 149 - pos[1])
        # A
        if pos[0] == 0 and pos[1] > 149:
            new_direction = 1
            new_pos = (pos[1] - 100, 0)
    if direction == 1:
        # B
        if pos[1] == 199:
            new_direction = 1
            new_pos = (pos[0] + 100, 0)
        # G
        if pos[1] == 149:
            new_direction = 2
            new_pos = (49, pos[0] + 100)
        # F
        if pos[1] == 49:
            new_direction = 2
            new_pos = (99, pos[0] - 50)
    if direction == 0:
        # D
        if pos[0] == 149:
            new_direction = 2
            new_pos = (99, 149 - pos[1])
        # F
        if pos[0] == 99 and pos[1] < 100:
            new_direction = 3
            new_pos = (pos[1] + 50, 49)
        # D
        if pos[0] == 99 and pos[1] > 99:
            new_direction = 2
            new_pos = (149, 149 - pos[1])
        # G
        if pos[0] == 49:
            new_direction = 3
            new_pos = (pos[1] - 100, 149)
    return new_pos, new_direction


def next_tile_and_direction_on_cube(pos, direction, grid, faces, side, faces_dim):
    new_pos = (
        pos[0] + DIRECTIONS[direction][0],
        pos[1] + DIRECTIONS[direction][1],
    )
    if new_pos in grid:
        return new_pos, direction

    if side == 4:
        return test_cube_wrap(pos, direction)
    if side == 50:
        return real_cube_wrap(pos, direction)
    raise Exception("Unknown cube.")


def part1(data):
    grid, faces, side, faces_dim = read_board(data[:-2])
    # print(faces, side, faces_dim)
    directions_descr = data[-1]
    # print(directions_descr)
    directions = read_directions(directions_descr)
    # print(directions)

    direction = 0
    pos = (min([pos[0] for pos in grid if pos[1] == 0]), 0)

    for steps, new_direction in directions:
        # print("SD:", steps, direction)
        for _ in range(steps):
            new_pos, direction = next_tile_and_direction(
                pos, direction, faces, side, faces_dim
            )
            if new_pos not in grid:
                # print(new_pos)
                raise Exception("Ahhhh!!!")
            if grid[new_pos] == "." or grid[new_pos] in DIRECTIONS_STR:
                pos = new_pos
                grid[new_pos] = DIRECTIONS_STR[direction]
                # print(pos)
            elif grid[new_pos] == "#":
                break
            else:
                raise ValueError(f"Unknown position type {grid[new_pos]}")
        # print_grid(grid)
        # print(new_pos)
        if new_direction == "R":
            direction += 1
        elif new_direction == "L":
            direction -= 1
        direction %= 4
    # print(pos, direction, DIRECTIONS[direction])
    # print_grid(grid, side, faces_dim)
    return 1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + direction


def part2(data):
    grid, faces, side, faces_dim = read_board(data[:-2])
    # print(faces, side, faces_dim)
    directions_descr = data[-1]
    # print(directions_descr)
    directions = read_directions(directions_descr)
    # print(directions)

    direction = 0
    pos = (min([pos[0] for pos in grid if pos[1] == 0]), 0)

    for steps, next_turn in directions:
        # print("SD:", steps, direction)
        if next_turn == "X":
            last_direction = direction
        for _ in range(steps):
            new_pos, new_direction = next_tile_and_direction_on_cube(
                pos, direction, grid, faces, side, faces_dim
            )
            if new_pos not in grid:
                print(new_pos)
                raise Exception("Ahhhh!!!")
            if grid[new_pos] == "." or grid[new_pos] in DIRECTIONS_STR:
                pos = new_pos
                direction = new_direction
                grid[new_pos] = DIRECTIONS_STR[direction]
                # print(pos)
            elif grid[new_pos] == "#":
                break
            else:
                raise ValueError(f"Unknown position type {grid[new_pos]}")
        # print_grid(grid)
        # print(new_pos)
        if next_turn == "R":
            direction += 1
        elif next_turn == "L":
            direction -= 1
        direction %= 4
    # print(pos, direction, DIRECTIONS[direction])
    # print_grid(grid, side, faces_dim)
    return 1000 * (pos[1] + 1) + 4 * (pos[0] + 1) + last_direction


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, 6032, test_input_1)
    print()

    print("Test Part 2:")
    test_eq("Test 2.1", part2, 5031, test_input_1)
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
