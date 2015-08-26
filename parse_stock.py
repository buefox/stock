#coding=utf-8
from trend_line import *
from urllib2 import HTTPError
from matplotlib.dates import num2date
from star import *
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
	date = datetime.datetime.now()
	return (date.year, date.month, date.day-1), (date.year, date.month-1, date.day)

def draw_save(lines, x, y, stock_data, file_name):
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
	for i in range(1, len(lines)+1):
		ax.add_line(lines[i-1][0])
		ax.add_line(lines[i-1][1])
		plt.plot(x[i-1], y[i-1], 'bo')
		ax.xaxis_date()
		ax.autoscale_view()
	plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
	plt.savefig(file_name)

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
	end_time, start_time = get_start_end_date()
	# print start_time, end_time
	stock_data = quotes_historical_yahoo_ohlc(stock_name, start_time, end_time)
	local_max_point = list()
	local_min_point = list()
	x_min = list()
	y_min = list()
	x_max = list()
	y_max = list()
	line = list()
	local_max_point, local_min_point = find_bound(stock_data)
	print "--------------------" 
	print "%s-%d"% (stock_name, len(stock_data))
	print "%d max points, %d min points" % (len(local_max_point), len(local_min_point))
	line_1, x_min, y_min = predict_tunnel_2u(stock_data, local_min_point, local_max_point, stock_data[0][0], stock_data[-1][0])
	line_2, x_max, y_max = predict_tunnel_2d(stock_data, local_min_point, local_max_point, stock_data[0][0], stock_data[-1][0])
	pointsu = list()
	pointsd = list()
	print "method a:"
	for i in range(len(x_min)):
		peroid = x_min[i][3] - x_min[i][2]
		gap = y_min[i][3] - y_min[i][2]
		print "\t" + str(num2date(x_min[i][2]))[:-15] + " " + str(y_min[i][2]) + " " + str(num2date(x_min[i][0]))[:-15] + " " + str(y_min[i][0]) + " " + str(num2date(x_min[i][3]))[:-15] + " " + str(y_min[i][3]) + " " + str(num2date(x_min[i][0]+peroid))[:-15] + " " + str(y_min[i][0]+gap)
		pointsu.append([str(num2date(x_min[i][2]))[:-6], str(y_min[i][2]), str(num2date(x_min[i][0]))[:-6], str(y_min[i][0]), str(num2date(x_min[i][3]))[:-6], str(y_min[i][3]), str(num2date(x_min[i][0]+peroid))[:-6], str(y_min[i][0]+gap)])
	print "method b:"
	for i in range(len(x_max)):
		peroid = x_max[i][3] - x_max[i][2]
		gap = y_max[i][3] - y_max[i][2]
		print "\t" + str(num2date(x_max[i][2]))[:-15] + " " + str(y_max[i][2]) + " " + str(num2date(x_max[i][0]))[:-15] + " " + str(y_max[i][0]) + " " + str(num2date(x_max[i][3]))[:-15] + " " + str(y_max[i][3]) + " " + str(num2date(x_max[i][0]+peroid))[:-15] + " " + str(y_max[i][0]+gap)
		pointsd.append([str(num2date(x_max[i][2]))[:-6], str(y_max[i][2]), str(num2date(x_max[i][0]))[:-6], str(y_max[i][0]), str(num2date(x_max[i][3]))[:-6], str(y_max[i][3]), str(num2date(x_max[i][0]+peroid))[:-6], str(y_max[i][0]+gap)])
	draw_save(line_1, x_min, y_min, stock_data, stock_name+'1.png')
	draw_save(line_2, x_max, y_max, stock_data, stock_name+'2.png')
	whole_data = output(stock_data, start_time, end_time)
	return whole_data, points
		

def main():
	if len(sys.argv) < 2:
		print "Usage: %s [stock_name]" % (sys.argv[0])
		sys.exit()

	stock_name = sys.argv[1]
	# print stock_name
	fetch_data(stock_name)








if __name__ == '__main__':
	main()
