#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 20


def get_input(filename):
    with open(filename, "r", encoding="ascii") as input_file:
        lines = input_file.read()
    return lines.splitlines()


def get_coords(numbers, index):
    decrypted = [numbers[index.index(i)] for i in range(len(numbers))]
    start = decrypted.index(0)
    return (
        decrypted[(start + 1000) % len(numbers)],
        decrypted[(start + 2000) % len(numbers)],
        decrypted[(start + 3000) % len(numbers)],
    )


def part1(data):
    numbers = []
    for line in data:
        numbers.append(int(line))
    index = list(range(len(numbers)))
    # print("\nStart:", [numbers[idx] for idx in index])
    for i, mix in enumerate(numbers):
        old_index = index[i]
        new_index = (old_index + mix) % (len(numbers) - 1)
        # print(mix, ":", old_index, "=>", new_index)
        if old_index < new_index:
            for number, idx in enumerate(index):
                if old_index < idx <= new_index:
                    index[number] -= 1
        elif old_index > new_index:
            for number, idx in enumerate(index):
                if new_index <= idx < old_index:
                    index[number] += 1
        index[i] = new_index
        # print("Indices:", index)
        # print("Numbers:", [numbers[index.index(i)] for i in range(len(numbers))])
    # print("Coords:", get_coords(numbers, index))
    return sum(get_coords(numbers, index))


def part2(data):
    key = 811589153
    numbers = []
    for line in data:
        numbers.append(int(line) * key)
    index = list(range(len(numbers)))
    # print("\nStart:", [numbers[idx] for idx in index])
    for _round in range(10):
        for i, mix in enumerate(numbers):
            old_index = index[i]
            new_index = (old_index + mix) % (len(numbers) - 1)
            # print(mix, ":", old_index, "=>", new_index)
            if old_index < new_index:
                for number, idx in enumerate(index):
                    if old_index < idx <= new_index:
                        index[number] -= 1
            elif old_index > new_index:
                for number, idx in enumerate(index):
                    if new_index <= idx < old_index:
                        index[number] += 1
            index[i] = new_index
            # print("Indices:", index)
        # print("Numbers:", [numbers[index.index(i)] for i in range(len(numbers))])
    # print("Coords:", get_coords(numbers, index))
    return sum(get_coords(numbers, index))


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, 3, test_input_1)
    print()

    print("Test Part 2:")
    test_eq("Test 2.1", part2, 1623178306, test_input_1)
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
