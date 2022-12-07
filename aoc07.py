#!/usr/bin/env python3

from aoc import check_solution, save_solution, test_eq

DAY = 7


def get_input(filename):
    with open(filename, "r", encoding="ascii") as input_file:
        lines = input_file.read()
    return lines.splitlines()


class Node:
    def __init__(self, parent, name, size):
        self.parent = parent
        self.name = name
        self.size = size
        self.childs = []

    def add_child(self, child):
        self.childs.append(child)

    def recursive_size(self):
        if len(self.childs) == 0:
            return self.size
        return sum([child.recursive_size() for child in self.childs])

    def cd(self, directory):
        for child in self.childs:
            if child.name == directory:
                return child
        return None

    def filter(self, predicate):
        result = []
        for child in self.childs:
            if predicate(child):
                result.append(child)
            result.extend(child.filter(predicate))
        return result

    def __str__(self):
        if self.parent is None:
            return f"Node {self.name}, parent (None), size {self.size}."
        return f"Node {self.name}, parent {self.parent.name}, size {self.size}."


def build_tree(data):
    file_tree = None
    current_node = file_tree
    for line in data:
        cmd = line.split()
        if cmd[0] == "$":
            if cmd[1] == "cd":
                if cmd[2] == "/":
                    if file_tree is None:
                        file_tree = Node(None, "/", 0)
                    current_node = file_tree
                elif cmd[2] == "..":
                    current_node = current_node.parent
                else:
                    child = current_node.cd(cmd[2])
                    if child is None:
                        raise Exception(f"Unknown child {current_node} {cmd[2]}")
                    current_node = child
            elif cmd[1] == "ls":
                pass
            else:
                raise Exception(f"Unknown command {cmd[1]}")
        else:
            if cmd[0] == "dir":
                current_node.add_child(Node(current_node, cmd[1], 0))
            else:
                current_node.add_child(Node(current_node, cmd[1], int(cmd[0])))

    return file_tree


def part1(data):
    tree = build_tree(data)
    result = tree.filter(lambda node: node.recursive_size() < 100000)
    return sum([node.recursive_size() for node in result if node.size == 0])


def part2(data):
    tree = build_tree(data)
    free = 70_000_000 - tree.recursive_size()
    needed = 30_000_000 - free
    # print("Used:", tree.recursive_size())
    # print("Free:", free)
    # print("Needed:", needed)
    result = tree.filter(lambda node: node.recursive_size() > needed)
    best_node = tree
    for node in result:
        if node.size == 0:
            size = node.recursive_size()
            if size < best_node.recursive_size():
                best_node = node
    return best_node.recursive_size()


def run_tests():
    test_input_1 = get_input(f"ex{DAY}")
    print("Test Part 1:")
    test_eq("Test 1.1", part1, 95437, test_input_1)
    print()

    print("Test Part 2:")
    test_eq("Test 2.1", part2, 24933642, test_input_1)
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
