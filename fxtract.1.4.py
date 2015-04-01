import glob
import gzip
import re
import numpy
from scipy import stats
import pandas as pd
import time
import os
import sys
import pickle

def calculate(argv):
	[scipt, source] = argv

	start_time = time.time()
	if source == "load":
		ds = pickle.load( open('log.p', 'rb'))
	
	else:
		print start_time
		print "Press RETURN to start the LOG grab if not hit CTRL + Z"
		start = raw_input("> ")
		print "Commencing Grab"
		gm_logs = glob.glob("gm*/*.gz")
		backend_logs = glob.glob("backend*/*.gz")
		timeStamp = []
		dates = []
		reason = []
		for log in gm_logs:
			f = gzip.open(log)
			for line in f:
				m = re.findall("completed_ms=([0-9]+)", line)
				m = map(int, m)
				i = re.findall("\d{4}-\d{2}-\d{2}", line)
				r = re.findall("['\"](\\w+.\\w+)[\"']", line)
				if m and len(r) == 1 and len(i) == 1:#TEMPORARY FIX 
					dates += i
					timeStamp += m
					reason += r
					print len(timeStamp)
					#, i, m, r....current observation count is 6866504
		print("--- %s seconds ---" %(time.time() - start_time))

		print "Commencing DataSeries allocation"
		index = [dates, reason]
		ds = pd.Series(timeStamp, index=index)
		print "DataSeries Allocated"
		print "Saving into Pickle File"
		pickle.dump( ds, open( 'log.p', 'wb'))
	labels = ["date", "msg", "ms"]
	ds.to_csv(open( 'log.csv', 'wb'),index_label=labels,header=True)
	print "Grouping by Date"
	dd = ds.groupby(level=0)
	print "Grouping by Reason"
	dr = ds.groupby(level=1)
	print "Data Grouping Complete"
	print "Print results, hit return. CTRL + Z to abort"
	raw_input(">")
	os.system('clear')
	print len(ds), "Observations"
	print "Mean, ", numpy.mean(ds)
	print "Standard Deviation, ", numpy.std(ds)
	print "Skewness, ", stats.skew(ds)
	print "Kurtosis, ", stats.kurtosis(ds)
	print "MEAN by Date"
	print dd.mean()
	print "STD  by Date"
	print dd.std()
	print "MEAN by Reason"
	print dr.mean()
	print "STD by Reason"
	print dr.std()
	
	print("--- %s seconds ---" %(time.time() - start_time))
	
if __name__ == "__main__":
	calculate(sys.argv)