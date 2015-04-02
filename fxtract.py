import glob
import gzip
import re
import numpy
from scipy import stats
import pandas as pd
import time
import os
import cPickle

def calculate(userload, userdate=None, usermsg=None):

	start_time = time.time()
	if userload in ["y", "Y"]:
		ds = cPickle.load(open('log.p', 'rb'))
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
				print m
				if userdate == "ALL":
					i = re.findall("\d{4}-\d{2}-\d{2}", line)
				else:
					i = re.findall("(%s)" % (userdate), line)
				if usermsg == "ALL":
					r = re.findall("['\"](\\w+.\\w+)[\"']", line)
				else:
					r = re.findall("(%s)" % (usermsg), line)
				if m and len(r) == 1 and len(i) == 1:
					dates += i
					timeStamp += m
					reason += r
					print len(timeStamp), "GRAB"
					#, i, m, r....current observation count is 6866504
		print("--- %s seconds ---" %(time.time() - start_time))

		print "Commencing DataSeries allocation"
		index = [dates, reason]
		ds = pd.Series(timeStamp, index=index)
		print "DataSeries Allocated"
		pupdate = raw_input("Update cPickle file? > ")
		if pupdate in ["Y", "y"]:
			print "Saving into Pickle File"
			cPickle.dump( ds, open( 'log.p', 'wb'), protocol =-1) #HIGHEST PROTOCOL
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
