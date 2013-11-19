#!/usr/bin/python

from __future__ import division
import urlparse
import urllib2
import csv
import codecs
# Je moet de biblotheek pattern downloaden en installeren van https://github.com/clips/pattern of http://www.clips.ua.ac.be/pages/pattern
from pattern.web import plaintext
import re
import sys

# hoe heet het bestand met URLs?
urlbestand="urls.txt"

# hier kun je twee regular expressions aangeven waarop je wilt zoeken
regex1 = re.compile(r'[Tt]witter')
regex2 = re.compile(r'[Ff]acebook')

filename_list=[]
httpcode_list=[]
filename_stripped_list=[]

i = 0
matchcount1=0
matchcount1_list=[]
matchcount2=0
downloadsgelukt=0
matchcount2_list=[]
domain_list=[]

urls=open(urlbestand).read()
url_list = urls.split('\n')

print "\nWelkom. Er zullen "+str(len(url_list))+" artikelen gedownload worden. Vervolgens wordt in alle artikelen gezocht op de uitdrukkingen \""+regex1.pattern+"\" en \""+regex2.pattern+"\".\n"

for url in url_list:
	matchcount1=0
	matchcount2=0
	filename=""
	filename_split=""
	domain=""
	domain = urlparse.urlsplit(url)[1].split(':')[0]
	split = urlparse.urlsplit(url)
	i = i+1
	filename = "{0:06d}".format(i) + domain + '_' + split.path.split("/")[-1]
	try:
		req = urllib2.Request(url)
		response = urllib2.urlopen(req)
		httpcode=response.getcode()
		artikelopslaan=open(filename,"wb")
		artikelopslaan.write(response.read())
		artikelopslaan.close()
		artikel=open(filename,"r")
		# print html2text.html2text(artikel)
		stripped=artikel.read()
		stripped = plaintext(stripped, keep={'h1':[], 'h2':[], 'strong':[], 'a':['href']})
		filename_stripped=filename+'_stripped.txt'
		artikel_stripped=open(filename_stripped, "w")
		artikel_stripped.write(stripped.encode("utf-8"))
		artikel_stripped.close()
		# we kiezen ervoor in artikel_stripped en niet in het originele artikel te zoeken. voordeel: dat levert minder foute positieven op
		artikel_stripped=open(filename+'_stripped.txt', "r")
		for line in artikel_stripped:
 			matches1 = regex1.findall(line)
			for word in matches1:
				matchcount1=matchcount1+1
				#print 'Context: '+line
 			matches2 = regex2.findall(line)
			for word in matches2:
				matchcount2=matchcount2+1
				#print 'Context: '+line
		print '\"' + regex1.pattern + '\" is ' + str(matchcount1) + ' keer gevonden in ' + filename
		print '\"' + regex2.pattern + '\" is ' + str(matchcount2) + ' keer gevonden in ' + filename
		downloadsgelukt=downloadsgelukt+1
	except urllib2.URLError, e:
		httpcode=e
	except:
		print "Unexpected error:", sys.exc_info()[0]
		httpcode= sys.exc_info()[0]
	if httpcode==200:
		print "OK! "+url
	else:
		print "FOUTJE? HTTP-Code "+str(httpcode)+" bij het downloaden van "+url
	httpcode_list.append(httpcode)
	filename_list.append(filename)
	filename_stripped_list.append(filename_stripped)
	domain_list.append(domain)
	matchcount1_list.append(matchcount1)
	matchcount2_list.append(matchcount2)
	artikel.close()
	artikel_stripped.close()
	

output=zip(url_list,domain_list,httpcode_list,filename_list,filename_stripped_list,matchcount1_list,matchcount2_list)


writer = csv.writer(open('output.csv', 'wb'))
writer.writerows(output)

print "\nWe zijn klaar! Er zijn "+str(downloadsgelukt)+" van de "+str(len(url_list))+" artikelen gedownload. Bij "+str(len(url_list)-downloadsgelukt)+" artikelen ging het dus mis. De output staat in het bestand output.csv.\n"