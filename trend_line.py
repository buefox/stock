# coding=utf-8
import matplotlib.pyplot as plt
import datetime
import math
import copy
import sys
from matplotlib.dates import date2num, num2date, DateFormatter, WeekdayLocator, DayLocator, MONDAY
from matplotlib.finance import quotes_historical_yahoo_ohlc, candlestick_ohlc
from matplotlib.lines import Line2D
# validation: 2 or more points to draw a trend line
# spacing of points: it cant be too close or too far apart
# angles: it can't be too steep 
def get_line(point1, point2, start_time, end_time, color):
	slope = float()
	start_price = float()
	end_price = float()
	if point2[0] > point1[0]:
		slope = (point2[1] - point1[1]) / (point2[0] - point1[0])
		start_price = point1[1] - (slope * (point1[0] - (start_time-1)))
		end_price   = point2[1] + (slope * (end_time+1 - point2[0])) 
	elif point2[0] < point1[0]:
		slope = (point1[1] - point2[1]) / (point1[0] - point2[0])
		start_price = point2[1] - (slope * (point2[0] - (start_time-1)))
		end_price   = point1[1] + (slope * (end_time+1 - point1[0]))
	# print slope
	line =  Line2D(xdata=(start_time-1, end_time+1), ydata=(start_price, end_price), color=color, linewidth=1.0, antialiased=True)
	return line, slope

def predict_tunnel(max_points, min_points, start_time, end_time):
	candidate = -1
	price = -1
	for i in range(len(max_points)):
		if min_points[0][0] < max_points[i][0] and min_points[1][0] > max_points[i][0] and max_points[i][4] >= price:
			candidate = i
			price = max_points[i][4]
	if candidate == -1:
		return 0, 0, 0, 0, 0
	low_line, slope = get_line(min_points[0], min_points[1], start_time, end_time, 'g')
	high_line, hslope = get_line((max_points[candidate][0], max_points[candidate][4], True), (max_points[candidate][0]+1, max_points[candidate][4]+slope, True), start_time, end_time, 'g')
	return high_line, low_line, (max_points[i][4]+slope*(min_points[1][0] - min_points[0][0])), slope, [max_points[candidate][0], min_points[0][0], min_points[1][0]], [max_points[candidate][4], min_points[0][1], min_points[1][1]]

def predict_tunnel_2u(stock_data, local_min_point, local_max_point, start_time, end_time):
	candidate = -1
	lines = list()
	x = list()
	y = list()
	for i in range(len(local_min_point)-1):
		for j in range(len(local_max_point)):
			if local_max_point[j][0] > local_min_point[i][0] and local_max_point[j][0] < local_min_point[i+1][0]:
				if candidate == -1:
					candidate = j
				else: 
					if local_max_point[candidate][4] < local_max_point[j][4]:
						candidate = j
		if candidate == -1:
			# print "Can't find max in %d and %d" % (local_min_point[i][0], local_min_point[i+1][0])
			continue
		low_line, slope = get_line((local_min_point[i][0], local_min_point[i][4], False), (local_min_point[i+1][0], local_min_point[i+1][4], False), start_time, end_time, 'g')
		period = local_min_point[i+1][0] - local_min_point[i][0]
		est_date = local_max_point[candidate][0] + period
		est_price = local_max_point[candidate][4] + period*slope
		if est_date >= end_time:
			high_line, _slope = get_line((local_max_point[candidate][0], local_max_point[candidate][4], True),(stock_data[-1][0], stock_data[-1][4], True), start_time, end_time, 'g')
			lines.append([high_line, low_line])
			x.append([local_max_point[candidate][0], end_time, local_min_point[i][0], local_min_point[i+1][0]])
			y.append([local_max_point[candidate][4], stock_data[-1][4], local_min_point[i][4], local_min_point[i+1][4]])
			candidate = -1
			continue
		for k in stock_data:
			if (k[0] - est_date) >= 0 and k[4]-est_price >= 0:
				high_line, _slope = get_line((local_max_point[candidate][0], local_max_point[candidate][4], True), (k[0], k[4], True), start_time, end_time, 'g')
				lines.append([high_line, low_line])
				x.append([local_max_point[candidate][0], k[0], local_min_point[i][0], local_min_point[i+1][0]])
				y.append([local_max_point[candidate][4], k[4], local_min_point[i][4], local_min_point[i+1][4]])
				break
		candidate = -1
	return lines, x, y		

def predict_tunnel_2d(stock_data, local_min_point, local_max_point, start_time, end_time):
	candidate = -1
	lines = list()
	x = list()
	y = list()
	for i in range(len(local_max_point)-1):
		for j in range(len(local_min_point)):
			if local_min_point[j][0] > local_max_point[i][0] and local_min_point[j][0] < local_max_point[i+1][0]:
				if candidate == -1:
					candidate = j
				else: 
					if local_min_point[candidate][4] > local_min_point[j][4]:
						candidate = j
		if candidate == -1:
			# print "Can't fsind min in %d and %d" % (local_max_point[i][0], local_max_point[i+1][0])
			continue
		low_line, slope = get_line((local_max_point[i][0], local_max_point[i][4], False), (local_max_point[i+1][0], local_max_point[i+1][4], False), start_time, end_time, 'g')
		period = local_max_point[i+1][0] - local_max_point[i][0]
		est_date = local_min_point[candidate][0] + period
		est_price = local_min_point[candidate][4] + period*slope
		if est_date >= end_time:
			high_line, _slope = get_line((local_min_point[candidate][0], local_min_point[candidate][4], True),(stock_data[-1][0], stock_data[-1][4], True), start_time, end_time, 'g')
			lines.append([high_line, low_line])
			x.append([local_min_point[candidate][0], end_time, local_max_point[i][0], local_max_point[i+1][0]])
			y.append([local_min_point[candidate][4], stock_data[-1][4], local_max_point[i][4], local_max_point[i+1][4]])
			candidate = -1
			continue
		for k in stock_data:
			if (k[0] - est_date) >= 0 and k[4]-est_price >= 0:
				high_line, _slope = get_line((local_min_point[candidate][0], local_min_point[candidate][4], True), (k[0], k[4], True), start_time, end_time, 'g')
				lines.append([high_line, low_line])
				x.append([local_min_point[candidate][0], k[0], local_max_point[i][0], local_max_point[i+1][0]])
				y.append([local_min_point[candidate][4], k[4], local_max_point[i][4], local_max_point[i+1][4]])
				break
		candidate = -1
	return lines, x, y




def find_bound(stock_data):
	local_max_point = list()
	local_min_point = list()
	if stock_data[0][4] <= stock_data[1][4] and stock_data[0][4] <= stock_data[2][4]:
		local_min_point.append(stock_data[0])
	elif stock_data[0][4] >= stock_data[1][4] and stock_data[0][4] >= stock_data[2][4]:
		local_max_point.append(stock_data[0])
	elif stock_data[1][4] <= stock_data[0][4] and stock_data[1][4] <= stock_data[2][4]:
		local_min_point.append(stock_data[1])
	elif stock_data[1][4] >= stock_data[0][4] and stock_data[1][4] >= stock_data[2][4]:
		local_max_point.append(stock_data[1])
	else: 
		pass	
	for i in range(2, len(stock_data)-2):
		if stock_data[i][4] <= stock_data[i-2][4] and stock_data[i][4] <= stock_data[i-1][4] and stock_data[i][4] <= stock_data[i+1][4] and stock_data[i][4] <= stock_data[i+2][4]:
			local_min_point.append(stock_data[i])
		elif stock_data[i][4] >= stock_data[i-2][4] and stock_data[i][4] >= stock_data[i-1][4] and stock_data[i][4] >= stock_data[i+1][4] and stock_data[i][4] >= stock_data[i+2][4]:
			local_max_point.append(stock_data[i])

	return local_max_point, local_min_point

def find_crit(local_max_point, local_min_point):
	sorted_max = sorted(local_max_point, key = lambda data: data[4], reverse=True)
	sorted_min = sorted(local_min_point, key = lambda data: data[0], reverse=True)
	return [(sorted_max[0][0], sorted_max[0][4], True), (sorted_max[1][0], sorted_max[1][4], True), (sorted_min[0][0], sorted_min[0][4], False), (sorted_min[1][0], sorted_min[1][4], False)]

def prediction(crit, high_slope, low_slope, end_date):
	est_period = int((math.fabs(crit[0][0] - crit[1][0]) + math.fabs(crit[2][0] - crit[3][0])) / int(2) )
	sort_crit = sorted(crit, key = lambda data: data[0], reverse=True)
	message = ""
	if sort_crit[0][2] == True:
		message += "is on the fall, the last peak was at " + str(num2date(sort_crit[0][0]))
		# message += "\nIn %d days." % ((date2num(end_date)))
	else:
		message += "is on the rise, the last low was at " + str(num2date(sort_crit[0][0]))[:-15]
		# message += "\nIn %d days." % ((date2num(end_date)))
	return message

def str2date(date_string):
	split_date = date_string.split('/')
	return tuple(int(x) for x in split_date)

def main():
	if len(sys.argv) < 4:
		print "Usage: %s [stock_name] [start_date] [end_date]" % (sys.argv[0])
		sys.exit()

	stock_name = sys.argv[1]
	start_date = str2date(sys.argv[2])
	end_date   = str2date(sys.argv[3])
	# print "%s %s %s" % (stock_name, start_date, end_date)

	stock_data = quotes_historical_yahoo_ohlc(stock_name, start_date, end_date)
	if len(stock_data) == 0:
		raise SystemExit
	# print stock_data
	print len(stock_data)
	local_max_point = list()
	local_min_point = list()
	local_max_point, local_min_point = find_bound(stock_data)
	print len(local_min_point)
	crit = find_crit(local_max_point, local_min_point)
	print "%d max points, %d min points" % (len(local_max_point), len(local_min_point))
	high_lines = list()
	low_lines = list()
	markx = list()
	marky = list()
	# for i in range(len(local_min_point)-1):
	# 	for j in range(i+1, len(local_min_point)):
	# 		phigh_line, plow_line , predicted_high, predicted_slope, x, y = predict_tunnel(local_max_point, [(local_min_point[i][0], local_min_point[i][4]), (local_min_point[j][0], local_min_point[j][4])], stock_data[0][0], stock_data[-1][0])
	# 		if phigh_line == 0 and plow_line == 0 and predicted_high == 0:
	# 			print "predict tunnel not found at %d %d" % (i , j)
	# 		else:
	# 			high_lines.append(phigh_line)
	# 			low_lines.append(plow_line)
	# 			markx.append(x)
	# 			marky.append(y)
	lines, x, y = predict_tunnel_2u(stock_data, local_min_point, local_max_point, stock_data[0][0], stock_data[-1][0])
	print "%d tunnels" % (len(lines))
	# high_line, high_slope = get_line(crit[0], crit[1], stock_data[0][0], stock_data[-1][0], 'b')
	# Line2D(xdata=(crit[0][0], crit[1][0]), ydata=(crit[0][1], crit[1][1]), color='k', linewidth=1.0, antialiased=True)
	# low_line , low_slope  = get_line(crit[2], crit[3], stock_data[0][0], stock_data[-1][0], 'b')
	# Line2D(xdata=(crit[2][0], crit[3][0]), ydata=(crit[2][1], crit[3][1]), color='k', linewidth=1.0, antialiased=True)
	# print "Predicted high: %lf\nPredicted tunnel slope: %lf" % (predicted_high, predicted_slope)
	# prediction
	# print stock_name + " " + prediction(crit, high_slope, low_slope, end_date)
	print x
	print y









#------------------------------------------------------plot-------------------------------------------------------------#
	mondays = WeekdayLocator(MONDAY)        # major ticks on the mondays
	alldays = DayLocator()              # minor ticks on the days
	weekFormatter = DateFormatter('%b %d')  # e.g., Jan 12
	dayFormatter = DateFormatter('%d')      # e.g., 12
	fig = plt.figure() 
	for i in range(1, len(lines)+1):
		ax = plt.subplot(2, len(lines)/2 +1, i)
		fig.subplots_adjust(bottom=0.2)
		ax.xaxis.set_major_locator(mondays)
		ax.xaxis.set_minor_locator(alldays)
		ax.xaxis.set_major_formatter(weekFormatter)
	#ax.xaxis.set_minor_formatter(dayFormatter)
	#plot_day_summary(ax, quotes, ticksize=3)
		candlestick_ohlc(ax, stock_data, width=0.7)
	# ax.add_line(high_line)
	# ax.add_line(low_line)
		ax.add_line(lines[i-1][0])
		ax.add_line(lines[i-1][1])
		plt.plot(x[i-1], y[i-1], 'bo')
		ax.xaxis_date()
		ax.autoscale_view()
	plt.setp(plt.gca().get_xticklabels(), rotation=45, horizontalalignment='right')
	plt.show()
#-----------------------------------------------------------------------------------------------------------------------#







if __name__ == '__main__':
	main()