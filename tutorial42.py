#!/Library/Frameworks/Python.framework/Versions/2.7/bin/python2.7

# The line above is a typical starting line of a Python script. 
# The #!-statement tells the computer which version of Python to use 
# (if you do not know the path, you can leave it away, 
# but it is good programming style to use it).

# Our script uses the following two modules from the file unicsv.py that you saved in
# the folder of this script. They are necessary to read and write our CSV-files.
from unicsv import CsvUnicodeReader
from unicsv import CsvUnicodeWriter

# We also want to import a module to search for Regular Expressions 
# (an advanced form of a search string)
import re

# Let us define two variables (inputfilename and outputfilename) that contain
# the names of the files we want to user later in the script.
# Obviously, the input file should exist and contain the tweets (see the tutorial),
# the output file does not have to exist yet. Just choose a nice name.
inputfilename="mytweets.csv"
outputfilename="myoutput.csv"

# Now we create some empty lists that we will use later on. A list can contain several
# variables and is denoted by square brackets. 
user_list=[]
tweet_list=[]
search_list=[]
iso_language_code_list=[]

# What do we want to look for? Between the two quotation marks we put a so called
# regular expression. Google gives plenty of help if you have difficulties with the syntax
# of such an regexp.
searchstring1 = re.compile(r'[Pp]olen|[Pp]ool|[Ww]arschau|[Ww]arszawa')

# Let the program start! We tell the user what is going on...
print "Opening "+inputfilename
# ... and call the function to read the input file.
reader=CsvUnicodeReader(open(inputfilename,"r"))

# Now we read the file line by line. Note the indention: 
# the indented block is repeated for each row (thus, each tweet):
for row in reader:
	tweet_list.append(row[0])
	# we just append something to our empty list of tweets, namely the 1st 
	# column of our row.
	# Note that we start counting with 0.
	# The ISO language code is in the sixth column, this is why we append segment 5 
	# of our row to the iso_language_code list.
	iso_language_code_list.append(row[5])
	user_list.append(row[2])
	# we don't care about the other columns right now, but you now know how to add them:
	# make an empty list before, and then append appropriate row[column]
	# Let us count how often our searchstring is used in the tweet:
	matches1 = searchstring1.findall(row[0])
	matchcount1=0
	for word in matches1:
		matchcount1=matchcount1+1
	search_list.append(matchcount1)
	
# OK, we repated the procedure above for each row. Time to put all the data in one 
# container and save it:
print "Constructing data matrix"
outputdata=zip(tweet_list,user_list,iso_language_code_list,search_list)
headers=zip(["tweet"],["user"],["iso"],["how often is Poland mentioned?"])
print "Write data matrix to ",outputfilename
writer=CsvUnicodeWriter(open(outputfilename,"wb"))
writer.writerows(headers)
writer.writerows(outputdata)
