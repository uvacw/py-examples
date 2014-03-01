#!/usr/bin/python
from unicsv import CsvUnicodeReader
from unicsv import CsvUnicodeWriter
import re
inputfilename="../datasets/hashtag-klimaatverandering.csv"
outputfilename="myoutput.csv"
user_list=[]
tweet_list=[]
search_list=[]
searchstring1 = re.compile(r'[Pp]olen|[Pp]ool|[Ww]arschau|[Ww]arszawa')
print "Opening "+inputfilename
reader=CsvUnicodeReader(open(inputfilename,"r"))
for row in reader:
	tweet_list.append(row[0])
	user_list.append(row[2])
	matches1 = searchstring1.findall(row[0])
	matchcount1=0
	for word in matches1:
		matchcount1=matchcount1+1
	search_list.append(matchcount1)
print "Constructing data matrix"
outputdata=zip(tweet_list,user_list,search_list)
headers=zip(["tweet"],["user"],["how often is Poland mentioned?"])
print "Write data matrix to ",outputfilename
writer=CsvUnicodeWriter(open(outputfilename,"wb"))
writer.writerows(headers)
writer.writerows(outputdata)
