import sys
import re
import time
import datetime
import os

DIFF_TIME = 3
SHOOTER_PATH = ""

def get_ip(uid, log, fin_date):
    global DIFF_TIME
    ip = ""
    with open(log, "r", encoding="utf8") as fd:
        lines = fd.readlines()
        i = 0
        re_start = r"(\d+-\d+-\d+\s\d+:\d+:\d+).*" + re.escape(uid) + r".*tcp渠道充值开始"
        re_end = r"(\d+-\d+-\d+\s\d+:\d+:\d+).*" + re.escape(uid) + r".*多人购买成功,addr:\/(.*)"
        re_http = r"(\d+-\d+-\d+\s\d+:\d+:\d+).*" + re.escape(uid) + r".*http更新渠道成功"
        found_start = False
        found_end = False 
        time_start = 0
        time_end = 0
        for line in lines:
            if not found_start:
                match_start = re.match(re_start, line)
                if match_start:
                    date_str = match_start.group(1)
                    print(line, end="")
                    time_start = date2time(date_str)
                    if abs(time_start - date2time(fin_date)) < DIFF_TIME:
                        found_start = True
                    else:
                        print("pay skip date " + date_str)
                else:
                    match_http = re.match(re_http, line)
                    if match_http:
                        date_str = match_http.group(1)
                        print(line, end="")
                        if abs(date2time(date_str) - date2time(fin_date)) < DIFF_TIME:
                            print("HTTP PAY TYPE >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
                            print(line, end="")
                            return "http"
            else:
                match_end = re.match(re_end, line)
                if match_end:
                    date_str = match_end.group(1)
                    print(line, end="")
                    time_end = date2time(date_str)
                    found_end = True
                    ip = match_end.group(2)

            if found_start and found_end:
                break;
        if(ip != ""):
            if time_end - time_start <= DIFF_TIME: # 3s
                # print("find pay success in ip: " + ip)         
                pass
            else:
                print("end time far bigger than start time")
        else:
            print("get ip failed")
    return ip

def get_shooter_path():
    global SHOOTER_PATH
    if SHOOTER_PATH == "":
        print("PLEASE INPUT SHOOTER_PATH")
    else:
        return SHOOTER_PATH

def date2time(date, format_str="%Y-%m-%d %H:%M:%S"):
    return time.mktime(time.strptime(date, format_str))

def time2date(time):
    return datetime.datetime.fromtimestamp(time)

def get_shooter_ip(uid, date):
    # pay_log = get_log(date, "/home/payserver/log", "jvm-pay")
    pay_log = get_log(date, "./", "jvm-pay")
    ip = get_ip(uid, pay_log, date)
    if ip == "": # query back_pay_log
        pay_log = get_log(date, "/home/paybackserver/log", "jvm-pay")
        ip = get_ip(uid, pay_log, date)
    return ip

def get_log(date, path, mark):
    dirs = os.listdir(path)
    # print(dirs)
    query_time = date2time(date)
    dirs.sort(key=lambda x:(os.stat(path+"/"+x).st_mtime))
    # print(dirs)
    for file in dirs:
        if file.find(mark) != -1:
            file = path + "/" + file
            modify_time = os.stat(file).st_mtime
            # print(modify_time)
            if modify_time > query_time:
                print("find pay log " + file)
                # return file
                return os.path.abspath(file)
    return None

def get_shooter_log(path, date):
    log = get_log(date, path, "shooter")
    return log


def is_cache_update_success(uid, log, pay_date):
    global DIFF_TIME
    score_after = 0
    with open(log, "r", encoding="utf8") as fd:
        lines = fd.readlines()
        re_start = r"(\d+-\d+-\d+\s\d+:\d+:\d+).*" + re.escape(uid) + r".*准备充值更新,充值前score:(.*)"
        re_end = r"(\d+-\d+-\d+\s\d+:\d+:\d+).*" + re.escape(uid) + r".*充值更新成功,score:(\d+) 剩余score:(\d+)"
        re_sitdown = r"(\d+-\d+-\d+\s\d+:\d+:\d+).*坐下.*" + re.escape(uid) + r".*scoore\[(\d+)\].*"
        found_start = False
        found_end = False 
        found_sitdown = False
        time_start = 0
        time_sitdown = 0
        time_end = 0
        score_before = 0
        score_sitdown = 0
        for line in lines:
            if not found_start:
                match_start = re.match(re_start, line)
                if match_start:
                    date_str = match_start.group(1)
                    print(line, end="")
                    time_start = date2time(date_str)
                    if abs(time_start - date2time(pay_date)) < DIFF_TIME:
                        found_start = True
                        score_before = int(match_start.group(2))
                    else:
                        # print("time_start: " + str(time_start))
                        # print("pay_time:" + str(date2time(pay_date)))
                        # print(date_str)
                        # print(pay_date)
                        print("shooter skip date " + date_str + ", time_start " + str(time2date(time_start)) + " abs: " + str(abs(time_start - date2time(pay_date))))
            else:
                match_end = re.match(re_end, line)
                if match_end:
                    date_str = match_end.group(1)
                    print(line, end="")
                    time_end = date2time(date_str)
                    found_end = True
                    score_after = int(match_end.group(3))

            if found_start and found_end:
                match_sitdown = re.match(re_sitdown, line)
                if match_sitdown:
                    date_str = match_sitdown.group(1)
                    print(line, end="")
                    time_sitdown = date2time(date_str)
                    if abs(time_sitdown - time_end) < 10: # 10s
                        found_sitdown = True
                        score_sitdown = int(match_sitdown.group(2))
                        break;
                    else:
                        print("sitdown skip date " + date_str + ", time_end " + str(time2date(time_end)))               
        if score_sitdown != 0 and found_sitdown:
            print("find score_sitdown " + str(score_sitdown))
        else:
            print("\nNOT FIND SITDOWN LOG")
            return False
        if score_before != 0 and score_after != 0 :
            if found_end - found_start <= DIFF_TIME: # 3s
                print("cache update sucess")
            else:
                print("time diff > {}s".format(DIFF_TIME) )
        else:
            print("score error: before {}, after {}".format(score_before, score_after))

        if score_after == score_sitdown and score_sitdown > 0:
            print("\nAFTER PAY SCORE {}, SITDOWN SCORE {}".format(score_after, score_sitdown))
            return True
        else:
            return False

def is_success(uid, date, shooter_path):
    if shooter_path != "":
        shooter_log = get_shooter_log(shooter_path, date)
        if shooter_log:
            return is_cache_update_success(uid, shooter_log, date)
        else:
            print("NOT FOUND SHOOTER LOG")
    else:
        print("QUERY IP FINISH")


def query_ip(uid, date):
    print("QUERY IP START >>>>>>>>.")
    ip = get_shooter_ip(uid, date)
    print("QUERY IP END >>>>>>>>." + ip)

def query_score(uid, date, shooter_path):
    print("query score start >>>>>>>>.")
    res = is_success(uid, date, shooter_path)
    print("query score end >>>>>>>>.")

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("usage: python query_log.py [uid] [time] [shooter_path]")
        # query_ip("7117420", "2016-12-22 03:03:00") # HTTP test
        # query_ip("3094022", "2016-12-22 03:02:34")
        # query_score("3094022", "2016-12-22 03:02:34", "./")
    elif len(sys.argv) == 3:
        query_ip(sys.argv[1], sys.argv[2])
    else:
        query_score(sys.argv[1], sys.argv[2], sys.argv[3])




