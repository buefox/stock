#coding=utf-8
from trend_line import *
from urllib2 import HTTPError
from matplotlib.dates import num2date, date2num
from star import *
from time import sleep
def output(data, start_time, end_time):
	output = list()
	for item in data:
		temp = str(num2date(item[0]))
		temp2 = temp[:-6]
		o = list()
		o.append(temp2)
		for i in range(1, len(item)-1):
			o.append(item[i])
		output.append(o)
	# print output
	return output

def get_start_end_date():
	date  = datetime.datetime.now()
	end   = date - datetime.timedelta(days=1)
	start = date - datetime.timedelta(days=30)
	return (start.year, start.month, start.day), (end.year, end.month, end.day)

def draw_save_all_tunnel(lines, x, y, stock_data, file_name):
	mondays = WeekdayLocator(MONDAY)
	alldays = DayLocator()
	weekFormatter = DateFormatter('%b %d')
	dayFormatter = DateFormatter('%d')
	fig = plt.figure()
	ax = plt.subplot(1, 1, 1)
	fig.subplots_adjust(bottom=0.2)
	ax.xaxis.set_major_locator(mondays)
	ax.xaxis.set_minor_locator(alldays)
	ax.xaxis.set_major_formatter(weekFormatter)
	candlestick_ohlc(ax, stock_data, width=0.7)
	for i in range(len(lines)):
		ax.add_line(lines[i][0])
		ax.add_line(lines[i][1])
		plt.plot(x[i], y[i], 'bo')
		ax.xaxis_date()
		ax.autoscale_view()
	plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
	plt.savefig(file_name)
	plt.close()

def draw_save_prediction(line, x, y, stock_data, file_name):
	mondays = WeekdayLocator(MONDAY)
	alldays = DayLocator()
	weekFormatter = DateFormatter('%b %d')
	dayFormatter = DateFormatter('%d')
	fig = plt.figure() 
	ax = plt.subplot(1, 1, 1)
	fig.subplots_adjust(bottom=0.2)
	ax.xaxis.set_major_locator(mondays)
	ax.xaxis.set_minor_locator(alldays)
	ax.xaxis.set_major_formatter(weekFormatter)
	candlestick_ohlc(ax, stock_data, width=0.7)
	ax.add_line(line[0])
	plt.plot(x, y, 'bo')
	ax.xaxis_date()
	ax.autoscale_view()
	plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
	plt.savefig(file_name)
	plt.close()

def recent_min_max(local_max_point, local_min_point, l):	
	start, end = get_start_end_date()
	end_num = date2num(datetime.date(end[0], end[1], end[2]))
	# print end_num
	rmin = int(0)
	rmax = int(0)
	print "--------------------" 
	print "\trecent max point: "
	for i in range(len(local_max_point)):
		if end_num - local_max_point[i][0] <= 5:
			print '\t\t' + str(num2date(local_max_point[i][0]))[:-15] + " " + str(local_max_point[i][4])
			rmax += 1
	print "\trecent min point: "
	for i in range(len(local_min_point)):
		if end_num - local_min_point[i][0] <= 5:
			print '\t\t' + str(num2date(local_min_point[i][0]))[:-15] + " " + str(local_min_point[i][4])
			rmin += 1
	print "recent max: %3d/%3d (%lf)\nrecent min: %3d/%3d (%lf)" %  \
			(rmax, l, float(rmax)/float(l), rmin, l, float(rmin)/float(l))

def recent_tunnel(x_list, y_list):
	start, end = get_start_end_date()
	start_num = date2num(datetime.date(start[0], start[1], start[2]))
	end_num = date2num(datetime.date(end[0], end[1], end[2]))
	lines = list()
	draw_x = list()
	draw_y = list()
	for i in range(len(x_list)):
		if end_num - x_list[i][3] <= 5:
			lines.append(get_line((x_list[i][3]-1, y_list[i][3]), (x_list[i][3], y_list[i][3]), 
																	start_num, x_list[i][3], 'g'))
			draw_x.append([x_list[i][0], x_list[i][1], x_list[i][2], x_list[i][3]])
			draw_y.append([y_list[i][0], y_list[i][1], y_list[i][2], y_list[i][3]])

	return lines, draw_x, draw_y

def validate_history(stock_name, end, mode):
	count1 = int()
	count2 = int()
	days1 = int()
	days2 = int()
	start = (end[0]-5, end[1], end[2])
	data = quotes_historical_yahoo_ohlc(stock_name, start, end)
	len_data = len(data)
	m = int()
	Flag1 = True
	Flag2 = True
	if len_data == 0:
		print "validate_history: no data found"
		return
	local_max_point, local_min_point = find_bound(data)
	if mode:
		x_min, y_min = predict_tunnel_2d(data, local_min_point, 
										 local_max_point, data[0][0], data[-1][0], False)
		m = len(x_min)
		for i in range(len(x_min)):
			for j in range(len_data):
				if not Flag1 and not Flag2:
					Flag1 = True
					Flag2 = True
					break
				if x_min[i][3] - data[j][0] >= 0 and x_min[i][3] - data[j][0] <= 10 and Flag1:
					if data[j][4] <= y_min[i][3]:
						days1  += x_min[i][3] - data[j][0]
						count1 += 1	
						Flag1 = False
				if x_min[i][2] - data[j][0] >= 5 and x_min[i][2] - data[j][0] <= 10 and Flag2:
					if data[j][4] <= y_min[i][2]:
						count2 += 1
						days2  += x_min[i][2] - data[j][0]
						Flag2 = False
			Flag1 = True
			Flag2 = True

	else:
		x_max, y_max = predict_tunnel_2u(data, local_min_point,
										 local_max_point, data[0][0], data[-1][0], False)
		m = len(x_max)
		for i in range(len(x_max)):
			for j in range(len_data):
				if not Flag1 and not Flag2:
					Flag1 = True
					Flag2 = True
					break
				if x_max[i][3] - data[j][0] >= 0 and x_max[i][3] - data[j][0] <= 10 and Flag1:
					if data[j][4] >= y_max[i][3]:
						days1  += x_max[i][3] - data[j][0]
						count1 += 1
						Flag1 = False
				if x_max[i][2] - data[j][0] >= 5 and x_max[i][2] - data[j][0] <= 10 and Flag2:
					if data[j][4] >= y_max[i][2]:
						count2 += 1
						days2  += x_max[i][2] - data[j][0]
						Flag2 = False
			Flag1 = True
			Flag2 = True

	output_str = "%4d/%4d %lf avg_through: %lf day(s) | %4d/%4d %lf avg_through %lf day(s)" % (count1, m, float(count1)/float(m), float(days1)/float(m), 
		  																					   count2, m, float(count2)/float(m), float(days2)/float(m))
	return output_str, [float(count1)/float(m), float(days1)/float(m), float(count2)/float(m)]

def make_prediction(stock_data, stock_name, end, x_min, y_min, x_max, y_max, FILE):
	pic_path = str(end[0]) + '-' + str(end[1]) + '-' + str(end[2])
	s = ""
	num = [0.0, 0.0, 0.0]
	message = ""

	lines, x, y = recent_tunnel(x_min, y_min)
	# for i in range(len(lines)):
		# draw_save_prediction(lines[i], x[i], y[i], stock_data,
		# 					 pic_path + '/' + stock_name+'_min'+str(i+1)+'.png')
	if len(lines) > 0:
		s, num = validate_history(stock_name, end, 1)
		message = stock_name + " history (1M2m) validation: " + s
		FILE.write(message + "\n")
		# print message

	lines_, x_, y_ = recent_tunnel(x_max, y_max)
	# for i in range(len(lines_)):
		# draw_save_prediction(lines_[i], x_[i], y_[i], stock_data,
		# 					 pic_path + '/' + stock_name+'_max'+str(i+1)+'.png')
	if len(lines_) > 0:
		_s, _num = validate_history(stock_name, end, 0)
		_message =  stock_name + " history (2M1m) validation: " + _s
		FILE.write(_message + "\n")
		# print message
		if _num[0] > num[0]:
			num = _num
			message = _message

	return message, num

def fetch_data(stock_list):
	start, end = get_start_end_date()

	pic_path = str(end[0]) + '-' + str(end[1]) + '-' + str(end[2])
	if not os.path.exists(pic_path):
		os.makedirs(pic_path)

	file_name = "%s/%d-%d-%d_history.txt" % (pic_path, end[0], end[1], end[2])
	FILE = open(file_name, 'w')
	statistical_data = list()
	for stock in stock_list:
		stock_name = stock[1]
		print stock_name
		try:
			stock_data = quotes_historical_yahoo_ohlc(stock_name, start, end)
		except HTTPError:
			# print "%s not found" % (stock_name)
			continue

		local_max_point = list()
		local_min_point = list()
		x_min = list()
		y_min = list()
		x_max = list()
		y_max = list()
		line = list()

		local_max_point, local_min_point = find_bound(stock_data)

		line_1, x_min, y_min = predict_tunnel_2u(stock_data, local_min_point, 
												 local_max_point, stock_data[0][0], stock_data[-1][0], True)
		line_2, x_max, y_max = predict_tunnel_2d(stock_data, local_min_point, 
												 local_max_point, stock_data[0][0], stock_data[-1][0], True)

		statistical_data.append(make_prediction(stock_data, stock_name, end, x_min, y_min, x_max, y_max, FILE))
		# ---------------------------------------輸出----------------------------------------#
		# print "--------------------" 
		# print "%s-%d"% (stock_name, len(stock_data))
		# print "%d max points, %d min points" % (len(local_max_point), len(local_min_point))
		# pointsu = list()
		# pointsd = list()
		# print "method a:"
		# for i in range(len(x_min)):
		# 	print "\t" + str(num2date(x_min[i][2]))[:-15] + " " + str(y_min[i][2]) + " " + \
		# 			     str(num2date(x_min[i][0]))[:-15] + " " + str(y_min[i][0]) + " " + \
		# 			     str(num2date(x_min[i][3]))[:-15] + " " + str(y_min[i][3]) + " " + \
		# 			     str(num2date(x_min[i][1]))[:-15] + " " + str(y_min[i][1])
		#
		# 	pointsu.append([str(num2date(x_min[i][2]))[:-6], str(y_min[i][2]), 
		# 					str(num2date(x_min[i][0]))[:-6], str(y_min[i][0]), 
		# 					str(num2date(x_min[i][3]))[:-6], str(y_min[i][3]), 
		# 					str(num2date(x_min[i][1]))[:-6], str(y_min[i][1])])
		# print "method b:"
		# for i in range(len(x_max)):
		# 	print "\t" + str(num2date(x_max[i][2]))[:-15] + " " + str(y_max[i][2]) + " " + \
		# 				 str(num2date(x_max[i][0]))[:-15] + " " + str(y_max[i][0]) + " " + \
		# 				 str(num2date(x_max[i][3]))[:-15] + " " + str(y_max[i][3]) + " " + \
		# 				 str(num2date(x_max[i][1]))[:-15] + " " + str(y_max[i][1])
		#
		# 	pointsd.append([str(num2date(x_max[i][2]))[:-6], str(y_max[i][2]), 
		# 					str(num2date(x_max[i][0]))[:-6], str(y_max[i][0]), 
		# 					str(num2date(x_max[i][3]))[:-6], str(y_max[i][3]), 
		# 					str(num2date(x_max[i][1]+peroid))[:-6], str(y_max[i][1])])
		#
		# draw_save_all_tunnel(line_1, x_min, y_min, stock_data, stock_name+'1.png')
		# draw_save_all_tunnel(line_2, x_max, y_max, stock_data, stock_name+'2.png')
		# whole_data = output(stock_data, start, end)
		# return whole_data, pointsu, pointsd
		# ----------------------------------------------------------------------------------#
	sorted_stat = sorted(statistical_data, key = lambda data: data[1][0], reverse=True)
	print "---------Top 10 (est point)---------"
	for i in range(10):
		print sorted_stat[i][0]
	sorted_stat = sorted(statistical_data, key = lambda data: data[1][2], reverse=True)
	print "---------Top 10 (3rd point)---------"
	for i in range(10):
		print sorted_stat[i][0]
	FILE.close()
	return
		
def read_stock(x):
	FILE = open('stock'+ str(x) + '.txt', 'r')
	temp = list()
	code = ""
	name = ""
	suffix = ""
	if x == 2:
		suffix = ".TW"
	elif x == 4:
		suffix = ".TWO"
	for line in FILE:
		code = line[:4] + suffix
		name = line[6:-1]
		temp.append([name, code])
	FILE.close()
	return temp	

def main():
	if (len(sys.argv) < 2):
		print "Usage: %s [stock_mode] (1:上市 2:上櫃)" % (sys.argv[0])
		sys.exit()
	stock_list = read_stock(int(sys.argv[1])*2)	
	
	fetch_data(stock_list)




if __name__ == '__main__':
	main()
