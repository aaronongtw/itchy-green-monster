import fxtract

print "Select date & msg filter, if no filter intended input 'ALL'"
userload = raw_input("Load data from cPickle? (Y/N)  > ")

if userload not in [ "y", "Y" ]:
	userdate = raw_input("Key in the date in the following format 'YYYY-MM-DD' > ")
	usermsg = raw_input("Key in the intended msg filter > ")
	fxtract.calculate(userload, userdate, usermsg)
else:
	fxtract.calculate(userload)






