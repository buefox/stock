#coding=utf-8
from trend_line import *
from urllib2 import HTTPError
from matplotlib.dates import num2date






def main():
	valid_list = list()
	for i in range(1100, 1200):
		stock_data = list()
		stock_name = "%04d" % (i) + ".TW"
		# print i
		try:
			stock_data = quotes_historical_yahoo_ohlc(stock_name, (2015, 7, 1), (2015, 8, 15))
		except HTTPError:
			# print i , 0 
			pass
		if len(stock_data) != 0:	
			# print i , len(stock_data)
			valid_list.append(stock_name)
	for stock_name in valid_list:
		stock_data = quotes_historical_yahoo_ohlc(stock_name, (2015, 7, 1), (2015, 8, 15))
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
		line, x_min, y_min = predict_tunnel_2u(stock_data, local_min_point, local_max_point, stock_data[0][0], stock_data[-1][0])
		line, x_max, y_max = predict_tunnel_2d(stock_data, local_min_point, local_max_point, stock_data[0][0], stock_data[-1][0])
		
		print "method a:"
		for i in range(len(x_min)):
			peroid = x_min[i][3] - x_min[i][2]
			gap = y_min[i][3] - y_min[i][2]
			print "\t" + str(num2date(x_min[i][0]))[:-15] + " " + str(y_min[i][0]) + " -> " + str(num2date(x_min[i][0]+peroid))[:-15] + " " + str(y_min[i][0]+gap)
		print "method b:"
		for i in range(len(x_max)):
			peroid = x_max[i][3] - x_max[i][2]
			gap = y_max[i][3] - y_max[i][2]
			print "\t" + str(num2date(x_max[i][0]))[:-15] + " " + str(y_max[i][0]) + " -> " + str(num2date(x_max[i][0]+peroid))[:-15] + " " + str(y_max[i][0]+gap)


		









if __name__ == '__main__':
	main()
