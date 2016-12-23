# encoding: utf-8

import time;
import datetime
from datetime import date
import sys
import random

UID = "123"
SID = 0;
CURRENT_TIMESTAMP = time.time()
CURRENT_SCORE = 0
CURRNET_GUN = 10
FAKE_GUN_COUNT = 0
MAX_GUN = 6
FISH_MUL = [2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 18, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 100, 120, 200]
RESULT_LINES = ""

def gen_line():
	global UID, FAKE_GUN_COUNT, SID, CURRENT_TIMESTAMP, CURRENT_SCORE, CURRNET_GUN, MAX_GUN, RESULT_LINES
	date = gen_timestamp()
	dead_score = gen_dead_score();
	if dead_score > 0: 
		CURRENT_SCORE += dead_score
		line = date + " DEBUG  userId:" + UID + "  击杀分数:" + str(dead_score) + "  剩余分数:" + str(CURRENT_SCORE)
	else:
		CURRENT_SCORE -= CURRNET_GUN
		line = date + " DEBUG  userId:" + UID + "  开出炮倍:" + str(CURRNET_GUN) + "  剩余分数:" + str(CURRENT_SCORE) + "  子弹id:" + str(SID)
	# print(line)
	RESULT_LINES += line + "\n"
	return CURRENT_SCORE >= CURRNET_GUN



def gen_timestamp():
	global UID, FAKE_GUN_COUNT, SID, CURRENT_TIMESTAMP, CURRENT_SCORE, CURRNET_GUN, MAX_GUN
	if FAKE_GUN_COUNT == MAX_GUN or (FAKE_GUN_COUNT > 3 and random.random() > 0.5):
		FAKE_GUN_COUNT = 0	
		CURRENT_TIMESTAMP += 1
	else:
		FAKE_GUN_COUNT += 1

	SID += 1
	date = datetime.datetime.fromtimestamp(CURRENT_TIMESTAMP).strftime("%Y-%m-%d %H:%M:%S")
	return date


def gen_dead_score():
	global UID, FAKE_GUN_COUNT, SID, CURRENT_TIMESTAMP, CURRENT_SCORE, CURRNET_GUN, MAX_GUN, FISH_MUL1, FISH_MUL2, FISH_MUL3
	# if SID < 5: # start dead after fired 5 shoot
		# return
	mul = FISH_MUL[random.randint(0, len(FISH_MUL)-1)]
	rate = 0.0
	dead_score = 0
	if 1 <= mul <= 10:
		rate = 1/10.0
	elif 10 <= mul <= 50:
		rate = 1/25.0
	elif 50 <= mul <= 100:
		rate = 1/75.0
	else:
		rate = 1/150
	if random.random() < rate:
		# dead
		print("hit " + str(mul) + " in gun " + str(CURRNET_GUN))
		dead_score = CURRNET_GUN * mul

	return dead_score

def gen_preface():
	global RESULT_LINES
	rid = random.randint(1, 100);
	cid = random.randint(1, 5)
	date = gen_timestamp()
	line1 = date + "   DEBUG  userId:" + "坐下： userid[" + UID + "]" + " 房间号[" + str(rid) + "] 座位号[" + str(cid) + "] 分值[" + str(CURRENT_SCORE) + "]" 
	RESULT_LINES += line1 + "\n"
	line2 = date + "   DEBUG  userId:" + UID + " 调整炮倍:" + str(CURRNET_GUN)
	RESULT_LINES += line2 + "\n"


def start_gen(uid, time, score, gun):
	global CURRENT_SCORE
	global UID, FAKE_GUN_COUNT, SID, CURRENT_TIMESTAMP, CURRENT_SCORE, CURRNET_GUN, MAX_GUN, FISH_MUL1, FISH_MUL2, FISH_MUL3
	UID = uid
	CURRENT_SCORE = int(score)
	CURRNET_GUN = int(gun)
	CURRENT_TIMESTAMP = float(time)

	gen_preface()
	while True:
		if not gen_line():
			break
	fd = open(uid + "_log.txt", "w")
	fd.write(RESULT_LINES)
	fd.close()
	print("OVER")

if __name__ == '__main__':
	if len(sys.argv) < 5:
		print("usage: python fake_log_gen.py [uid] [time] [score] [gun]")
		# start_gen("123", time.time(), 1000, 10)
	else:
		print(sys.argv[2])
		print(time.time())
		start_gen(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])





