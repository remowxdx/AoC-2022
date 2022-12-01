#!/usr/bin/env python3

import os.path
import datetime


class Debug():
    def __init__(self, enable=True):
        self.enabled = enable

    def enable(self, enabled = True):
        self.enabled = enabled

    def disable(self, disabled = True):
        self.enabled = not disabled

    def __call__(self, *args, **kwargs):
        if self.enabled:
            print(*args, **kwargs)


def test_eq(name, func, result, *args, **kwargs):
    print(f' * Testing {name}...', end=' ')
    r = func(*args, **kwargs)
    if r == result:
        print(f'\x1b[1;32mOK!\x1b[0m ☺ ')
    else:
        print(f'\x1b[1;41mNOT OK\x1b[0m ☹ ')
        print(f'\tExpected {result}, found {r}')
    

def save_solution(day, part, solution):
    filename =  f'solutions/solution{day}_{part}'
    with open(filename, 'w') as f:
        f.write(str(solution))
    hist_file = f'solutions/solution_history{day}_{part}'
    with open(hist_file, 'a') as f:
        f.write('\n------------- ' + str(datetime.datetime.now()) + ' -------------\n')
        f.write(str(solution))


def check_solution(day, part, candidate):
    hist_file = f'solutions/solution_history{day}_{part}'
    with open(hist_file, 'a') as f:
        f.write('\n------------- ' + str(datetime.datetime.now()) + ' -------------\n')
        f.write(str(candidate))
    filename =  f'solutions/solution{day}_{part}'
    if not os.path.isfile(filename):
        print(f'Day {day}, part {part} solution not present.')
        return
    with open(filename, 'r') as f:
        solution = f.read()

    if str(candidate) == solution:
        print(f'Day {day}, part {part} \x1b[1;32mOK!\x1b[0m ☺ ')
    else:
        print(f'Day {day}, part {part} \x1b[1;41mNOT OK\x1b[0m ☹ ')
        print(f'\tExpected {solution}, found {candidate}')


if __name__ == '__main__':
    pass
