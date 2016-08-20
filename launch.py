from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from random import randint
import time
import scrape
import os
app = Flask(__name__)

@app.route('/')
def HomeMovie():
	return render_template("search.html")

@app.route('/<movie>/')
def tester(movie):
	movie = movie.replace("-"," ")
	return render_template("test.html",movie=movie)
@app.route('/search',methods=['POST'])
def SearchMovie(names = [],links = [],search = None,imgs=[]):
	print "YO"
	names = []
	links = []
	imgs=[]
	search = ""
	search = request.form['search']
	links = scrape.getSolarSearch(str(search))
	for i in links:
		names.append(scrape.getNameFromLink(i))
	for name in names:
		if "www.solarmovie" in name:
			names.remove(name)
		else:	
			imgs.append(scrape.crawlImg(name))
	print imgs
	print names
	print "Done"
	return render_template("searchResults.html",names=names,links=links,imgs =imgs,search=search)



@app.route('/movie/<movie>/')
def hello(movie,emb = None, more=None,torr = None,imdb=None,imL = None,rotLink= None,rotRate=None,summary = None,streams = [],sol = None,relLinks = [],relNames = [],bef=None,imgRel = []):
	print "Homie"
	emb = ""
	emb = scrape.getTrailer(movie)
	print "Trailer Done"
	more = ""
	more = scrape.getMovieSearch(movie)
	print "Movie Seqrch Done"
	torr = ""
	#torr = scrape.getTorrent(movie)
	print "Torrent Done"
	imdb = ""
	imdb = scrape.getRating(movie)
	imL = ""
	print "Rating"
	imL = scrape.getImdbLink(movie)
	print "IMDB"
	rotLink = ""
	rotRate = ""
	print "Rotten"
	rotLink = scrape.getRottenLink(movie)
	rotRate = scrape.getRottenRating(movie)
	print "Rotten"
	summary = ""
	summary = scrape.getSummary(imL)
	print "Summary!N"
	sol = ""
	sol = scrape.getSolarMovie(movie)
	streams = []
	print "sol "+sol
	streams = scrape.getSolarMovieStreams(sol)
	relNames= []
	relNames = scrape.getRelatedMoives(movie)
	relLinks = []
	print "Right Before"
	bef = ""
	for link in relNames:
		print link
		bef = ""
		bef = link.replace(" ","-")
		print bef
		relLinks.append(bef)
	imgRel = []
	for name in relNames:
		imgRel.append(scrape.crawlImg(name))
	return render_template("home.html",movie=movie,emb =emb,more=more,torr=torr,imdb = imdb,imL=imL,rotRate = rotRate,rotLink = rotLink,summary =summary,streams=streams,relNames = relNames, relLinks = relLinks,imgRel = imgRel)

if __name__ == '__main__':
    app.run()
