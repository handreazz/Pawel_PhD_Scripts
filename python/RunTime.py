#! /usr/bin/python
import time
import datetime as dt
import argparse
import sys

'''
You can get the start_time by placing this line at the beginning of the script
start_time=time.time() 
'''




def main(start_time, frac_complete):
	now_time=time.time()
	elapsed_time=now_time-start_time
	time_to_go=elapsed_time/frac_complete-elapsed_time
	return str(dt.timedelta(seconds=time_to_go))

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument("start_time", help="Start time of the script in seconds.")
	parser.add_argument("frac_complete", help="Fraction complete. Eg. 0.2 if completed 2 of 10 tasks")
	args = parser.parse_args()
	
	rt=main(float(args.start_time),float(args.frac_complete))
	print rt
