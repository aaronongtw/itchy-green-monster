# itchy-green-monster

Grabs all latency information located in log files within folder with run.py and fxtract.py in parent folder. 
to run in bash;
python run.py

If logs have previously been extracted and cPickled, option to load pickle is available as log.p.
If data requires reprocesseing, input anything or than 'y' or 'Y' on initial prompt.
The following prompt will require you to select specific dates, if intended dates are unspecific; input 'ALL'
If intended filter includes specific messages, refer to LOG files to input on the next prompt, if irrelevant; input 'ALL'

If data loaded from pickle, data will then be saved to 'log.csv' and subsequently provide statistical summary as a whole and also grouped/sorted by date and msg.

If data not loaded in pickle, python will iterate through every log file within subfolder of parent directory and return(save) data specified in earlier prompts. 

Following the iteration, a prompt will appear if you would like to update the cPickle file. 

An option to process a statistical summary as a a whole and also grouped/sorted by date and msg will also be provided following the prompt. 


