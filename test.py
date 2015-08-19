# coding=utf-8
import matplotlib.pyplot as plt
import datetime
import math
import copy
import sys
# import matplotlib.pyplot as plt
from matplotlib.dates import num2date
from matplotlib.finance import quotes_historical_yahoo_ohlc

# def data_transform(data):
# 	data = data.split(',')
# 	return data
def str2date(str_date):
	split_date = str_date.split('/')
	return tuple(int(x) for x in split_date)
def out_put(stock, str1, str2):
	data = quotes_historical_yahoo_ohlc(stock, str2date(str1), str2date(str2))	
	if len(data) == 0:
	    raise SystemExit
	print len(data)
	output = list()
	for item in data:
		temp = str(num2date(item[0]))
		temp2 = temp[:-6]
		o = list()
		o.append(temp2)
		for i in range(1, len(item)-1):
			o.append(item[i])
		output.append(o)
	return output	
def is_up(data):
	# data = data_transform(data)
	return ((data[1]) < (data[4]))

def is_down(data):
	# data = data_transform(data)
	return ((data[1]) > (data[4]))

def is_cross(data):
	# data = data_transform(data)
	return (math.fabs(((data[1]) - (data[4])) / (data[1])) <= 0.01)

def is_jump(data1, data2):
	# data1 = data_transform(data1)
	# data2 = data_transform(data2)
	return not ((data2[1]) == (data1[4])) # precision problem?

def is_big(data):
	# data = data_transform(data)
	return (math.fabs(((data[1]) - (data[4])) / (data[1])) >= 0.05)

def is_push(data1, data3):
	# data1 = data_transform(data1)
	# data3 = data_transform(data3)
	if is_down(data1):
		return (((data3[4]) < (data1[1])) and ((data3[4]) > (data1[4])))	
	elif is_up(data1):
		return (((data3[4]) > (data1[1])) and ((data3[4]) < (data1[4])))
	return False	

def is_star(data_set):
	up = 0
	down = 0
	for i in range(len(data_set)-2):
		if(is_up(data_set[i])):
			if is_big(data_set[i]) and is_jump(data_set[i], data_set[i+1]) and is_cross(data_set[i+1]) and is_push(data_set[i], data_set[i+2]):
				down += 1
		elif is_down(data_set[i]):
			if is_big(data_set[i]) and is_jump(data_set[i], data_set[i+1]) and is_cross(data_set[i+1]) and is_push(data_set[i], data_set[i+2]):
				up += 1
	return (up,down)

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
