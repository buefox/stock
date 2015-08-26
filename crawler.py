#coding=utf-8
import urllib
from bs4 import BeautifulSoup
import sys

def is_str(s):
    return isinstance(s, basestring)
def get_list(x):
	html_raw = urllib.urlopen("http://isin.twse.com.tw/isin/C_public.jsp?strMode=" + str(x))
	html_data = html_raw.read()
	html_raw.close()

	soup_data = BeautifulSoup(html_data, 'html.parser')
	raw_data = list()
	encoded = list()
	FILE = open('stock'+ str(x) + '.txt', 'a+')
	for item in soup_data.find_all('td'):
		text = str(item)
		start = text.find('>')
		end = text.find('<', start)
		temp =  text[start+1:end].split('    ')
		# print temp
		if len(temp) == 2 and len(temp[0]) == 4:
			# print temp[0].decode('utf-8').encode('ISO-8859-1').decode('big5') + " " + temp[-1].decode('utf-8').encode('ISO-8859-1').decode('big5', 'ignore').strip()
			print temp[0].decode('utf-8').encode('ISO-8859-1').decode('big5').encode('utf-8') + " " + temp[-1].decode('utf-8').encode('ISO-8859-1').decode('big5', 'ignore').encode('utf-8').strip()
			
			encoded.append([temp[0].decode('utf-8').encode('ISO-8859-1').decode('big5').encode('utf-8'), 
				            temp[-1].decode('utf-8').encode('ISO-8859-1').decode('big5', 'ignore').encode('utf-8')[4:]])
			# print "------"
			FILE.write(temp[0].decode('utf-8').encode('ISO-8859-1').decode('big5').encode('utf-8') + " " + temp[-1].decode('utf-8').encode('ISO-8859-1').decode('big5', 'ignore').encode('utf-8')[:] + '\n')
	FILE.close()

def read_stock(x):
	FILE = open('stock'+ str(x) + '.txt', 'r')
	for line in FILE:
		text = line[:4] + " " + line[6:-1]
		print text


def main():
	if len(sys.argv) != 2:
		print "Usage: %s [mode]   1:上市 2:上櫃" % (sys.argv[0])
		sys.exit()
	get_list(int(sys.argv[1])*2)
	read_stock(int(sys.argv[1])*2)



if __name__ == '__main__':
	main()