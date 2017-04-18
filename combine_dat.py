import random
import re
import os
import sys
import stat
import enum

ALL_TRACKS = []
USED_TRACKS = set(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "25", "26", "30", "31", "32", "33", "34"])
COUNT = 0
COUNT2 = 0
REMAIN_TRACKS = set(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19", "20", "25", "26", "30", "31", "32", "33", "34"])
USED_SCRIPTS = set([        
        "50001",
        "50002",
        "50003",
        "50004",
        "50005",
        "50006",
        "50007",
        "50008",
        "50009",
        "50010",
        "50011",
        ])
TRACK_MAP={}
DEMO_TRACK = [
"10100",
"10500",
"110300",
"120200",
"20200",]
SCRIPT_MAP={}
OUT_MAP={}

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

def get_userful_track(file):
    # print(file)
    with open(file, "r") as f:
        for line in f.readlines():
            parts = line.split(",")
            if len(parts) > 4:
                if file.find("_randswatch") != -1:
                    if parts[0] != "(100":
                        USED_TRACKS.add(parts[2])
                    else:
                        USED_SCRIPTS.add(parts[2])
                else:
                    USED_TRACKS.add(parts[3])

def get_all_track(file):
    key = get_id(file)
    ALL_TRACKS.append(key)

def remove_useless(file):
    global COUNT, COUNT2
    key = get_id(file)
    if key not in USED_TRACKS:
        # print("remove " + key)
        COUNT += 1
        os.remove(file)
    else:
        COUNT2 += 1
        # print(key)
        REMAIN_TRACKS.add(key)

def get_id(file):
    index1 = file.rfind("/")+1;
    index2 = file.rfind("_");
    key = file[index1:index2]
    return key

def remove_track():
    walk_file("./script", get_userful_track)
    walk_file("./randswatch", get_userful_track)
    walk_file("./track", get_all_track)
    print("all tracks " + str(len(ALL_TRACKS)))
    print("used tracks " + str(len(USED_TRACKS)))
    walk_file("./track", remove_useless)
    print("remove tracks " + str(COUNT))
    print("remain tracks " + str(COUNT2))
    USED_TRACKS = sorted(USED_TRACKS)
    print(USED_TRACKS)
    REMAIN_TRACKS = sorted(REMAIN_TRACKS)
    print(REMAIN_TRACKS)

def remove_script():
    walk_file("./randswatch", get_userful_track)

def read_all_dat(file):
    global OUT_MAP
    dat_id = get_id(file)
    is_demo = False # isdemo? used just for TRACK !!!
    if is_demo and (dat_id not in DEMO_TRACK):
        return
    with open(file, "r") as f:
        data = f.read()
        OUT_MAP[dat_id] = data

def combine_dat(dat_type):
    in_path = "./" + dat_type
    out_path = "./123123_" + dat_type + ".json"
    # print(str(OUT_MAP))
    walk_file(in_path, read_all_dat)
    with open(out_path, "w") as f:
        data = str(OUT_MAP).replace("'", '"').replace('\\n', '|').replace('|"', '"')
        f.write(data)


if __name__ == "__main__":
    combine_dat("script")
    # combine_dat("track")

    # remove_script()
    # print(len(USED_SCRIPTS))
    # print((USED_TRACKS - REMAIN_TRACKS))





