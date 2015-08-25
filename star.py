# coding=utf-8
from trend_line import *
import math
"""判斷晨星 夜星"""
def is_up(data):
	return ((data[1]) < (data[4]))

def is_down(data):
	return ((data[1]) > (data[4]))

def is_cross(data):
	return (math.fabs(((data[1]) - (data[4])) / (data[1])) <= 0.01)

def is_jump(data1, data2):	
	return not ((data2[1]) == (data1[4])) # precision problem?

def is_big(data):
	return (math.fabs(((data[1]) - (data[4])) / (data[1])) >= 0.05)

def is_push(data1, data3):
	if is_down(data1):
		return (((data3[4]) < (data1[1])) and ((data3[4]) > (data1[4])))	
	elif is_up(data1):
		return (((data3[4]) > (data1[1])) and ((data3[4]) < (data1[4])))
	return False	

def is_star(data_set):
	up = list()
	down = list()
	for i in range(len(data_set)-2):
		if(is_up(data_set[i])):
			if is_big(data_set[i]) and is_jump(data_set[i], data_set[i+1]) and is_cross(data_set[i+1]) and is_push(data_set[i], data_set[i+2]):
				down.append([str(num2date(data_set[i+1]))[:-6], data_set[i+1][4]])
		elif is_down(data_set[i+1]):
			if is_big(data_set[i]) and is_jump(data_set[i], data_set[i+1]) and is_cross(data_set[i+1]) and is_push(data_set[i], data_set[i+2]):
				up.append([str(num2date(data_set[i+1]))[:-6], data_set[i+1][4]])
	return up, down

# if __name__ == '__main__':
# 	with open("table") as input_:
# 		raw_data = input_.read()
# 	data = list()
# 	data = raw_data.split('\n')	
# 	data.reverse()
# 	del data[0]

	# quotes = quotes_historical_yahoo_ohlc(sys.argv[1], (2015, 6, 30), (2015, 7, 20))
	# if len(quotes) == 0:
	#     raise SystemExit
# 	out_put(quotes)
# 	print is_star(data)
