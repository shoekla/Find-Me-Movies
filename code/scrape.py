import urllib2
import re
import nltk
import csv
import time
import requests
import string
from bs4 import BeautifulSoup
from urllib2 import urlopen
import os


arrsDict = {}

def addToDict(dic):
	arrsDict.update(dic)
def deleteDict(keyT):
	arrsDict.clear()

def is_in_arr(lis,s):
	result=False
	for item in lis:
		if item==s:
			result=True
	return result
def deleteDuplicates(lis):
	newLis=[]
	for item in lis:
		if item not in newLis:
			newLis.append(item)
	return newLis



def crawl(url):
	try:
		source_code=requests.get(url)
		plain_text=source_code.text
		soup=BeautifulSoup(plain_text)
		print "E"
		for link in soup.findAll('a'):
			print "For"
			href=link.get('href')
			href_test=str(href)
			#if href_test[0]!='/' and href_test[0]!='j' and href_test!='none' and href_test[0]!='#':
			if "/torrent" in href_test:
				if "http" not in href_test:
					return "https:"+str(href)
	except Exception,e:
		print str(e)
def getTorrent(movie):
	movie = movie.replace(" ","%20")
	link = "https://kat.cr/usearch/"+movie+"%20category:movies/"
	return crawl(link)

def getTrailer(movie):
	movie = movie.replace(" ","+")
	movie = movie +"+trailer"
	link = "https://www.youtube.com/results?search_query="+movie
	return getVideoSearch(link)
def getMovieSearch(movie):
	movie = movie.replace(" ","+")
	movie = movie +"+trailer"
	link = "https://www.youtube.com/results?search_query="+movie
	return link
def getGoodLink(url):
	k = url.rfind("/")
	return url[:k+1]
def crawlYouTube(url,pages):
	try:
		arr=[]
		source_code=requests.get(url)
		plain_text=source_code.text
		soup=BeautifulSoup(plain_text)
		for link in soup.findAll('a'):

			href=link.get('href')
			href_test=str(href)
			if href_test.startswith("http"):
					pages.append(str(href))
			else:
				lin=getGoodLink(url)
				pages.append(lin+str(href))

	except:
		print "Error at: "+str(url)
def getVideoSearch(url):
	a = []
	crawlYouTube(url,a)
	b=[]
	c=[]
	for item in a:
		if "/watch" in item:
			b.append(item)
	for item in b:
		c.append(str(item[33:]))
	new=deleteDuplicates(c)
	return new[0]
def getRating(movie):
	movie = movie.strip()
	movie = movie + "movie"
	movie = movie.replace(" ","%20")

	url = "http://www.bing.com/search?q="+movie+"&qs=n&form=QBRE&pq="+movie+"&sc=10-8&sp=-1&sk=&cvid=FB2616565AED478FAC5D8B22FF2D262F"
	source_code=requests.get(url)
	plain_text=source_code.text
	soup=BeautifulSoup(plain_text)
	res = plain_text.find("/10")

	actRes = plain_text[int(res-3):int(res+3)]
	loc = actRes.find(">")
	if loc == -1:
		return actRes
	return actRes[loc+1:]
def getRottenRating(movie):
	print "En"
	movie = movie.strip()
	movie = movie + "movie"
	movie = movie.replace(" ","%20")

	url = "http://www.bing.com/search?q="+movie+"&qs=n&form=QBRE&pq="+movie+"&sc=10-8&sp=-1&sk=&cvid=FB2616565AED478FAC5D8B22FF2D262F"
	source_code=requests.get(url)
	plain_text=source_code.text
	soup=BeautifulSoup(plain_text)
	res = plain_text.find("<div>Rotten Tomatoes</div>")
	print res
	print "Got"
	if res == -1:
		return ""
	actRes = plain_text[int(res-21):res-18]
	if ">" in actRes:
		actRes = actRes[1:]
	actRes = "Rotten Tomatoes Rating: "+actRes
	return actRes

def getRottenLink(movie):
	print "Enter"
	movie = movie.strip()
	movie = movie + "movie"
	movie = movie.replace(" ","%20")

	url = "http://www.bing.com/search?q="+movie+"&qs=n&form=QBRE&pq="+movie+"&sc=10-8&sp=-1&sk=&cvid=FB2616565AED478FAC5D8B22FF2D262F"
	source_code=requests.get(url)
	plain_text=source_code.text
	soup=BeautifulSoup(plain_text)
	for link in soup.findAll('a'):
		href=link.get('href')
		href_test=str(href)
		if "rottentomatoes" in href_test:
			return href_test
def getImdbLink(movie):
	movie = movie.strip()
	movie = movie + "movie"
	movie = movie.replace(" ","%20")

	url = "http://www.bing.com/search?q="+movie+"&qs=n&form=QBRE&pq="+movie+"&sc=10-8&sp=-1&sk=&cvid=FB2616565AED478FAC5D8B22FF2D262F"
	source_code=requests.get(url)
	plain_text=source_code.text
	soup=BeautifulSoup(plain_text)
	for link in soup.findAll('a'):

			href=link.get('href')
			href_test=str(href)
			if "imdb" in href_test:
				return href_test
def isWebsite(url):
	try:
		source_code=requests.get(url)
		plain_text=source_code.text
		soup=BeautifulSoup(plain_text)
		if "<h2>404</h2>" in plain_text:
			return 0
		if "This site can\'t be reached" in plain_text:
			return 0
		return 1
	except Exception, e:
		return 0


def getSolarMovie(movie):
	print "Movie in Method: "+movie
	sol = movie
	sol = sol.strip()
	sol = sol.replace(" ","-")
	testUrl = "https://www.solarmovie.ph/watch-"+sol+".html"
	print "Test: "+testUrl
	if isWebsite(testUrl) == 1:
		return testUrl
	print "Enter"
	movie = getActMovie(movie)
	sol = movie
	sol = sol.strip()
	sol = sol.replace(" ","-")
	testUrl = "https://www.solarmovie.ph/watch-"+sol+".html"
	print "Test: "+testUrl
	if isWebsite(testUrl) == 1:
		return testUrl
	print "Enter"
	movie = movie.strip()
	movie = movie.replace(" ","+")

	url = "https://www.solarmovie.ph/movie/search/"+movie+"/"
	print url
	source_code=requests.get(url)
	plain_text=source_code.text
	soup=BeautifulSoup(plain_text)
	location = plain_text.find("You might be interested in following popular movies:")
	arr = []
	for link in soup.findAll('a'):
		href=link.get('href')
		href_test=str(href)
		if "watch" in href_test:
			if "#comment-form" not in href_test:
				if location == -1:
					add = "https://www.solarmovie.ph"+href_test
					arr.append(add)
				else :
					if plain_text.find(href_test) < location:
						add = "https://www.solarmovie.ph"+href_test
						arr.append(add)
	res = deleteDuplicates(arr)
	return res


def getSolarSearch(movie):
	print "Movie in Method: "+movie
	movie = getActMovie(movie)
	print "Enter"
	movie = movie.strip()
	movie = movie.replace(" ","+")

	url = "https://www.solarmovie.ph/movie/search/"+movie+"/"
	print url
	source_code=requests.get(url)
	plain_text=source_code.text
	soup=BeautifulSoup(plain_text)
	location = plain_text.find("You might be interested in following popular movies:")
	arr = []
	for link in soup.findAll('a'):
		href=link.get('href')
		href_test=str(href)
		if "watch" in href_test:
			if "#comment-form" not in href_test:
				if location == -1:
					add = "https://www.solarmovie.ph"+href_test
					arr.append(add)
				else :
					if plain_text.find(href_test) < location:
						add = "https://www.solarmovie.ph"+href_test
						arr.append(add)
	res = deleteDuplicates(arr)
	print res
	print "Eexit"
	return res

def getSolarMovieStreams(movie):
	print "Movie in Method: "+movie
	sol = movie
	sol = sol.strip()
	sol = sol.replace(" ","-")
	testUrl = "https://www.solarmovie.ph/watch-"+sol+".html"
	print "Test: "+testUrl
	if isWebsite(testUrl) == 1:
		return testUrl
	print "Enter"
	movie = movie.strip()
	movie = movie.replace(" ","+")
	print "Launch"
	url = "https://www.solarmovie.ph/movie/search/"+movie+"/"
	print url
	source_code=requests.get(url)
	plain_text=source_code.text
	soup=BeautifulSoup(plain_text)
	arr = []
	print "For Loop"
	for link in soup.findAll('a'):

		href=link.get('href')
		href_test=str(href)
		if "watch" in href_test:
			if "#comment-form" not in href_test:
				add = "https://www.solarmovie.ph"+href_test
				arr.append(add)
	print "Deleete Dues"
	res = deleteDuplicates(arr)
	return res[0]	
def getNameFromLink(url):
	index = url.find("/watch")
	indexEnd = url.find(".html")
	almost = url[index+7:indexEnd]
	res = almost.replace("-"," ")
	return res
def getStreamLink(url):
	print "Entered With URL: "+url
	source_code=requests.get(url)
	plain_text=source_code.text
	soup=BeautifulSoup(plain_text)
	arr = []
	count = 0
	for link in soup.findAll('a'):
		href=link.get('href')
		href_test=str(href)
		if "/link/show" in href_test:
			add = "https://www.solarmovie.ph"+href_test
			ar = getContinueLink(add)
			if ar != None:
				arr.append(ar)
			count = count +1
			print "Streamed"
			if count > 11:
				res = deleteDuplicates(arr)
				return res
	res = deleteDuplicates(arr)
	return res
def getContinueLink(url):
	source_code=requests.get(url)
	plain_text=source_code.text
	soup=BeautifulSoup(plain_text)
	arr = []
	for link in soup.findAll('a'):

		href=link.get('href')
		href_test=str(href)
		if "/link/play" in href_test:
			return href_test
def getActMovie(movie):
	movie = movie.strip()
	movie = movie + "movie"
	movie = movie.replace(" ","%20")
	arr = []
	url = "http://www.bing.com/search?q="+movie+"&qs=n&form=QBRE&pq="+movie+"&sc=10-8&sp=-1&sk=&cvid=FB2616565AED478FAC5D8B22FF2D262F"
	source_code=requests.get(url)
	plain_text=source_code.text
	soup=BeautifulSoup(plain_text)
	res = plain_text.find('')
	for link in soup.findAll('h2'):
		a = str(link)
		if "wiki" in a:
			r = a.find("<strong>")
			rEnd = a.find("</strong>")
			return a[r+8:rEnd]

def crawlImg(movie):
	try:
		movie = movie.replace(" ","+")
		url = "http://www.bing.com/images/search?q="+str(movie)+"&FORM=HDRSC2"
		print url
		pages = []
		arr=[]
		source_code=requests.get(url)
		plain_text=source_code.text
		soup=BeautifulSoup(plain_text)
		for link in soup.findAll('img'):

			href=link.get('src')
			href_test=str(href)
			#if href_test[0]!='/' and href_test[0]!='j' and href_test!='none' and href_test[0]!='#':
			if is_in_arr(pages,str(href))==False:
				if "1.1" in href:
					return href

	except:
		print "Error at: "+str(url)
def takeoutHTML(lyric) :
	res = ""
	count = 0
	for i in lyric:
		if i == '<':
			count = 1 
		if i == '>':
			count = 2
		if count == 0 :
			if i == '"':
				res = res + "'"
			else :
				res = res + str(i)
		if count == 2 :
			res = res + " "
			count = 0
	res = res.replace("<br/>"," ")
	return res
def getSummary(url):
	source_code=requests.get(url)
	plain_text=source_code.text
	soup=BeautifulSoup(plain_text)
	res = plain_text.find('class="summary_text"')
	re = plain_text.find(">",res)
	endRes = plain_text.find("</div>",res)
	print res
	print "Got"
	if res == -1:
		return ""
	actRes = plain_text[int(re)+1:endRes]
	if len(actRes) > 1:
		actRes = "Summary: "+actRes
	return takeoutHTML(actRes)
def getRelatedMoives(movie):
	print "Enter"
	movie = movie.strip()
	movie = movie + "movie"
	movie = movie.replace(" ","%20")

	url = "http://www.bing.com/search?q="+movie+"&qs=n&form=QBRE&pq="+movie+"&sc=10-8&sp=-1&sk=&cvid=FB2616565AED478FAC5D8B22FF2D262F"
	source_code=requests.get(url)
	plain_text=source_code.text
	soup=BeautifulSoup(plain_text)
	s = []
	end = ""
	arr = []
	for link in soup.findAll('a'):
		href=link.get('href')
		href_test=str(href)
		ha = link.get('h')
		if ".carousel" in href_test:
			if ".2" in ha:
				arr.append(href_test[href_test.find("q=")+2:href_test.find("&filters")])
	res = []
	for a in arr:
		s = []
		s = a.split("+")
		if s[len(s)-1].isdigit():
			res.append(a)
	r = []
	for i in res:
		end = i.replace("+"," ")
		r.append(end)
	return r

"""
Stream: getSolarMovie(movie) getStreamLink(url)
Rating: getRating(movie)
IMDB: getImdbLink(movie)
Trailer: getTrailer(movie)
Torrent: getTorrent(movie)


"""
"""
a = getSolarMovie("dil dakene do")
re = a[0]
print re
print getNameFromLink(re)
"""






