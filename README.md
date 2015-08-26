# stock
## Analying stock by realizing some theories.

### trend_line.py -- the core part of the codes
 	now I focus on these functions

	- find_bound
		this function finds out the local min and local max points in the given stock data, returning two lists containing local min and local max points.The local min/max points are selected by comparing the neighboring data.
	- predict_tunnel2u, predict_tunnel_2d
		These two functions are the implementation of depicting trend tunnels. 
		predict_tunnel2u utilizes two min_points* and one max_point to predict the fourth point of the parallelogram. On the other hand, predict_tunnel_2d uses two max_points and one min_point to do the trick.
	- get_line
		Creates line object of matplotlib with given points and color the line will be extended to the bounds of the x(time) axe.

	I think the return value of each function if pretty easy to figure out what their 
	purposes are. Multiple return value of these functions is one of the things that 
	needs to be improved in the future.

### star.py -- the firstly-finished part of the codes
	
	This is a simple and naiive implementation of finding the so-called "morning star" and its counterpart "night star".
	It is quite simple, since it is just 40 lines of codes or so.

### parse.py -- the main part of providing data for the front-end.
 	
	This part includes mainly about creating the outcome of all the analysis.
	- output
		provides the formatted output of the stock data (ref. js)
	- get_start_end_date
		generates the start and the end of the date for the data-fetching phase.
	- draw_save
		draw the candle stick and the predicted tunnel(s) via matplotlib and then save the result pictures as "stock_name1(2).png". 
		Most of the part of this function is a modification of the tutorial code of matplotlib. 
		For more, the main() of trend_line.py contain some more comments.
	- fetch_data
		Uses the functions imported from star.py and trend_line.py, create all the data needed.