#include <cstdio>
#include <cstdlib>
#include <cmath>
#include <cassert>
#include <vector>
//    2014/04/02	13:22:00	8868	8868	8867	8868	67
//		date		 time        開       高     低       收     交易量
//2015-07-20,3515.00,3555.00,3475.00,3550.00,825000,3550.00
//Date,         Open,  High,   Low,  Close,  Volume,Adj Close

using namespace std;
typedef struct stock_data{
	int year, month, day;
	double open, high, low, close, volume;
	bool is_star;
}Stock;
bool is_up(Stock& data){return (data.close > data.open);}
bool is_down(Stock& data){return (data.close < data.open);}
bool is_cross(Stock& data){return (fabs((data.open - data.close)/data.open) <= 0.01);}
bool is_jump(Stock& data1, Stock& data2){return !(data1.close == data2.open);}
bool is_big(Stock& data){return (fabs((data.open - data.close)/data.open) >= 0.05);}
bool is_push(Stock& data1, Stock& data3){
	if(is_down(data1))
		return ((data3.close < data1.open) && (data3.close > data1.close));
	else if(is_up(data1))
		return ((data3.close > data1.open) && (data3.close < data1.close));
	return false;
}
void is_star(vector<Stock>& data, int& up_star_count, int& down_star_count){
	int size = data.size(), d; 
	for(int i = 0;i < size-2;i++){
		if(is_up(data[i])){
			if(is_big(data[i]) && is_jump(data[i], data[i+1]) && is_cross(data[i+1]) && is_push(data[i], data[i+2])){
				puts("------------------------");
				printf("%d/%d/%d %lf %lf\n", data[i].year, data[i].month, data[i].day, data[i].open, data[i].close);
				down_star_count++;
			}	
		}
		else if(is_down(data[i])){
			if(is_big(data[i]) && is_jump(data[i], data[i+1]) && is_cross(data[i+1]) && is_push(data[i], data[i+2]))
				up_star_count++;
		}	
	}
	return;
}
void data_reverse(vector<Stock>& data){
	int size = data.size();
	Stock temp;
	for(int i = 0;i < size/2;i++){
		temp.year = data[i].year;
		temp.month = data[i].month;
		temp.day = data[i].day;
		temp.open = data[i].open;
		temp.high = data[i].high;
		temp.low = data[i].low;
		temp.close = data[i].close;
		temp.volume = data[i].volume;

		data[i].year = data[size-i-1].year;
		data[i].month = data[size-i-1].month;
		data[i].day = data[size-i-1].day;
		data[i].open = data[size-i-1].open;
		data[i].high = data[size-i-1].high;
		data[i].low = data[size-i-1].low;
		data[i].close = data[size-i-1].close;
		data[i].volume = data[size-i-1].volume;

		data[size-i-1].year = temp.year;
		data[size-i-1].month = temp.month;
		data[size-i-1].day = temp.day;
		data[size-i-1].open = temp.open;
		data[size-i-1].high = temp.high;
		data[size-i-1].low = temp.low;
		data[size-i-1].close = temp.close;
		data[size-i-1].volume = temp.volume;
	}
}
int main(int argc, char* argv[]){
	FILE* input;
	std::vector<Stock> data;
	Stock temp;
	input = fopen(argv[1], "r");
	assert(input != NULL);
	while(fscanf(input, "%d-%d-%d,%lf,%lf,%lf,%lf,%lf,%*lf", &temp.year, &temp.month, &temp.day, &temp.open, &temp.high, &temp.low, &temp.close, &temp.volume) != EOF){
		data.push_back(temp);
	}
	fclose(input);
	data_reverse(data);
	int size = data.size();
	int up_star_count = 0;
	int down_star_count = 0;
	is_star(data, up_star_count, down_star_count);
	printf("There are %d up stars out of %d days (%lf)\n", up_star_count, size, (double)((double)up_star_count/(double)size));
	printf("There are %d down stars out of %d days (%lf)\n", down_star_count, size, (double)((double)down_star_count/(double)size));
	return 0;
}