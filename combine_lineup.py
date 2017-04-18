import random
import re
import os
import sys
import stat

LINES = [];

def walk_file(path, func):
    if os.path.isfile(path):
        func(path)
    else:
        for item in os.listdir(path):
            subpath = os.path.join(path, item)
            mode = os.stat(subpath)[stat.ST_MODE]
            if stat.S_ISDIR(mode):
                walk_file(subpath, func)
            else:
                func(subpath)

def sort_lines(file):
    # print(file);
    with open(file, "r") as f:
        LINES.extend(f.readlines())
    # print(LINES); 

def write_lines():
    with open("./123123_script.txt", "w") as f:
        res = "0\n"
        temp = sorted(LINES, key=lambda line: int(line.split(",")[2])) 
        # print(temp)
        res += "".join(temp);
        f.write(res)    


if __name__ == "__main__":
    if len(sys.argv) > 1:
        path = sys.argv[1]
    else:
        path = "./lineup"
    walk_file(path, sort_lines)
    write_lines()






