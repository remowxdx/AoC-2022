#!/usr/bin/env python3

import os.path
import urllib.request
import datetime
import sys
import stat


def retrieve_input(day):
    url = f"https://adventofcode.com/2022/day/{day}/input"
    with open("session", "r") as f:
        cookie = f.read().strip()
    req = urllib.request.Request(url)
    req.add_header("Cookie", cookie)
    r = urllib.request.urlopen(req)
    s = r.read()
    with open(f"input{day}", "wb") as f:
        f.write(s)


def get_day():
    if len(sys.argv) <= 1:
        return datetime.datetime.today().day

    arg = sys.argv[1]
    if not arg.isdecimal():
        print("Usage:    start.py [day]\n")
        print("       day    day number (1-25) default: today")
        exit(-1)
    return int(arg)


def write_template(day):
    filename = f"aoc{day:02}.py"

    with open("aoc_template.py", "r") as template:
        scaf = template.read()

    if not os.path.isfile(filename):
        with open(filename, "w") as f:
            f.write(scaf.replace("%%day%%", str(day)))
            os.chmod(
                filename,
                stat.S_IRUSR
                | stat.S_IXUSR
                | stat.S_IWUSR
                | stat.S_IRGRP
                | stat.S_IWGRP
                | stat.S_IROTH,
            )


if __name__ == "__main__":
    day = get_day()

    retrieve_input(day)
    write_template(day)
