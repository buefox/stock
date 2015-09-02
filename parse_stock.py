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
	mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
	alldays = DayLocator()              # minor ticks on the days
	weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
	dayFormatter = DateFormatter('%d')      # e.g., 12
	fig = plt.figure() 
	ax = plt.subplot(1, 1, 1)
	fig.subplots_adjust(bottom=0.2)
	ax.xaxis.set_major_locator(mondays)
	ax.xaxis.set_minor_locator(alldays)
	ax.xaxis.set_major_formatter(weekFormatter)
	#ax.xaxis.set_minor_formatter(dayFormatter)
	#plot_day_summary(ax, quotes, ticksize=3)
	candlestick_ohlc(ax, stock_data, width=0.7)
	# ax.add_line(high_line)
	# ax.add_line(low_line)
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
	mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
	alldays = DayLocator()              # minor ticks on the days
	weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
	dayFormatter = DateFormatter('%d')      # e.g., 12
	fig = plt.figure() 
	ax = plt.subplot(1, 1, 1)
	fig.subplots_adjust(bottom=0.2)
	ax.xaxis.set_major_locator(mondays)
	ax.xaxis.set_minor_locator(alldays)
	ax.xaxis.set_major_formatter(weekFormatter)
	#ax.xaxis.set_minor_formatter(dayFormatter)
	#plot_day_summary(ax, quotes, ticksize=3)
	candlestick_ohlc(ax, stock_data, width=0.7)
	# ax.add_line(high_line)
	# ax.add_line(low_line)
	# print line
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
		# print end_num - local_max_point[i][0]
		# sleep(1)
		if end_num - local_max_point[i][0] <= 5:
			print '\t\t' + str(num2date(local_max_point[i][0]))[:-15] + " " + str(local_max_point[i][4])
			rmax += 1
	print "\trecent min point: "
	for i in range(len(local_min_point)):
		# print end_num - local_min_point[i][0]
		# sleep(1)
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
			peroid = x_list[i][3] - x_list[i][2]
			gap = y_list[i][3] - y_list[i][2]
			x = x_list[i][0] + peroid
			y = y_list[i][0] + gap
			lines.append(get_line((x-1, y), (x, y), start_num, end_num, 'g'))
			draw_x.append([x_list[i][0], x_list[i][2], x_list[i][3], x])
			draw_y.append([y_list[i][0], y_list[i][2], y_list[i][3], y])

	return lines, draw_x, draw_y
		
def fetch_data(stock_name):
	# valid_list = list()
	# for i in range(1100, 1200):
	# 	stock_data = list()
	# 	stock_name = "%04d" % (i) + ".TW"
	# 	# print i
	# 	try:
	# 		stock_data = quotes_historical_yahoo_ohlc(stock_name, (2015, 7, 1), (2015, 8, 15))
	# 	except HTTPError:
	# 		# print i , 0 
	# 		pass
	# 	if len(stock_data) != 0:	
	# 		# print i , len(stock_data)
	# 		valid_list.append(stock_name)
	# for stock_name in valid_list:
	start, end = get_start_end_date()
	# print start_time, end_time
	try:
		stock_data = quotes_historical_yahoo_ohlc(stock_name, start, end)
	except HTTPError:
		print "%s not found" % (stock_name)
		return
	local_max_point = list()
	local_min_point = list()
	x_min = list()
	y_min = list()
	x_max = list()
	y_max = list()
	line = list()
	local_max_point, local_min_point = find_bound(stock_data)
	# print "--------------------" 
	# print "%s-%d"% (stock_name, len(stock_data))
	# print "%d max points, %d min points" % (len(local_max_point), len(local_min_point))
	line_1, x_min, y_min = predict_tunnel_2u(stock_data, local_min_point, 
											 local_max_point, stock_data[0][0], stock_data[-1][0])
	line_2, x_max, y_max = predict_tunnel_2d(stock_data, local_min_point, 
											 local_max_point, stock_data[0][0], stock_data[-1][0])
	pointsu = list()
	pointsd = list()
	# -----------------------------------輸出-----------------------------------#
	# print "method a:"
	# for i in range(len(x_min)):
	# 	peroid = x_min[i][3] - x_min[i][2]
	# 	gap = y_min[i][3] - y_min[i][2]
	# 	print "\t" + str(num2date(x_min[i][2]))[:-15] + " " + str(y_min[i][2]) + " " + \
	# 			     str(num2date(x_min[i][0]))[:-15] + " " + str(y_min[i][0]) + " " + \
	# 			     str(num2date(x_min[i][3]))[:-15] + " " + str(y_min[i][3]) + " " + \
	# 			     str(num2date(x_min[i][0]+peroid))[:-15] + " " + str(y_min[i][0]+gap)

	# 	pointsu.append([str(num2date(x_min[i][2]))[:-6], str(y_min[i][2]), 
	# 					str(num2date(x_min[i][0]))[:-6], str(y_min[i][0]), 
	# 					str(num2date(x_min[i][3]))[:-6], str(y_min[i][3]), 
	# 					str(num2date(x_min[i][0]+peroid))[:-6], str(y_min[i][0]+gap)])
	# print "method b:"
	# for i in range(len(x_max)):
	# 	peroid = x_max[i][3] - x_max[i][2]
	# 	gap = y_max[i][3] - y_max[i][2]
	# 	print "\t" + str(num2date(x_max[i][2]))[:-15] + " " + str(y_max[i][2]) + " " + \
	# 				 str(num2date(x_max[i][0]))[:-15] + " " + str(y_max[i][0]) + " " + \
	# 				 str(num2date(x_max[i][3]))[:-15] + " " + str(y_max[i][3]) + " " + \
	# 				 str(num2date(x_max[i][0]+peroid))[:-15] + " " + str(y_max[i][0]+gap)

	# 	pointsd.append([str(num2date(x_max[i][2]))[:-6], str(y_max[i][2]), 
	# 					str(num2date(x_max[i][0]))[:-6], str(y_max[i][0]), 
	# 					str(num2date(x_max[i][3]))[:-6], str(y_max[i][3]), 
	# 					str(num2date(x_max[i][0]+peroid))[:-6], str(y_max[i][0]+gap)])

	# draw_save_all_tunnel(line_1, x_min, y_min, stock_data, stock_name+'1.png')
	# draw_save_all_tunnel(line_2, x_max, y_max, stock_data, stock_name+'2.png')
	# whole_data = output(stock_data, start, end)
	# return whole_data, pointsu, pointsd
	# --------------------------------------------------------------------------#
	
	pic_path = str(end[0]) + '-' + str(end[1]) + '-' + str(end[2])
	if not os.path.exists(pic_path):
		os.makedirs(pic_path)
	lines, x, y = recent_tunnel(x_min, y_min)
	for i in range(len(lines)):
		draw_save_prediction(lines[i], x[i], y[i], stock_data, pic_path + '/' + stock_name+'_min'+str(i+1)+'.png')
	lines_, x_, y_ = recent_tunnel(x_max, y_max)
	for i in range(len(lines_)):
		draw_save_prediction(lines_[i], x_[i], y_[i], stock_data, pic_path + '/' + stock_name+'_max'+str(i+1)+'.png')
	
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
	for stock in stock_list:
		fetch_data(stock[1])




if __name__ == '__main__':
	main()
