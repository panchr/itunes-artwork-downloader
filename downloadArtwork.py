# Rushy Panchal
# downloadArtwork.py
# STDIN/STDOUT wrapper around iTunes.py

import urllib2
import urllib
import json
import sys
import os

API_URL = "http://itunes.apple.com/search"

def main():
	'''Main process: read data from stdin and write to stdout'''
	temp_dir = sys.stdin.readline().strip("\n")
	if not os.path.exists(temp_dir):
		os.mkdir(temp_dir)
	# AppleScript reads from here
	output = open(os.path.join(temp_dir, ".download_stdout"), "w")

	for line in sys.stdin:
		split_data = line.strip("\n").split("\t\t\t")

		artwork_url = getArtworkUrl(*split_data)

		if artwork_url:
			# filter out unicode characters from the filepath
			disk_path = unicode(os.path.join(temp_dir, ",".join(split_data)), errors = 'ignore').encode("ascii", errors = "ignore")
			urllib.urlretrieve(artwork_url, disk_path)
		else:
			disk_path = "-"

		output.write(disk_path + "\n")

	output.close()

def getArtworkUrl(song, artist = "", album = ""):
	'''Get the artwork URL for a given song, with optional artist and album names'''
	# form a search query by concatenating the various metadata
	if album:
		resp = attemptSearchQuery(album, "album")
		# try to get a more generic result by omitting the album name
		if not resp: return getArtworkUrl(song, artist)
	else:
		resp = attemptSearchQuery(song, "song")
		if not resp: return getArtworkUrl(song + "," + artist, artist)
	
	best = resp[0]['artworkUrl60']
	for result in resp:
		# attempt to find the best result, which is when the artist matches
		if artist in result['artistName']:
			best = result['artworkUrl60']
			break

	return best.replace("60x60", "600x600")

def attemptSearchQuery(query, entity):
	'''Attempt a search query'''
	params = {"term": query, "entity": entity, "attribute": entity + "Term", "country": "US", "media": "music", "limit": 10}
	resp = urllib2.urlopen(API_URL, urllib.urlencode(params))
	if resp.getcode() == 200:
		data = json.loads(resp.read())
		if data["resultCount"] >= 1: return data['results']

	return "" # no result or failed call

if __name__ == '__main__':
	main()
