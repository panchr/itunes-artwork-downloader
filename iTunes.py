# Rushy Panchal
# iTunes.py
# Provides an easy interface to access the Itunes API

import urllib2
import urllib
import json
import sys

'''
The Search class provides a simple interface to access the iTunes Search API

Examples
	search = Search()
	search.album("Songs of Innocence, U2") # find by album
	search.song("Madness") # search for the song "Madness"
'''
class Search(object):
	BASE_URL = "http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/wa/wsSearch"
	ALLOWED_ENTITIES = ["musicVideo", "tvSeason", "movie", "id", "shortFilm", "ebook", "album", "audiobook", "podcast", "software", "song"]

	'''
	Create a new iTunes Search API wrapper

	Parameters
		str country - the country to use the API with (defaults to US)

	Examples
		search = Search() # default country
		search_uk = Search("UK") # API using UK as the country
	'''
	def __init__(self, country = "US"):
		self.country = country.upper()
		self.methods = {}

		# helper function: get a lambda function that calls self._base with
		# the entity as the first argument; this is required because creating
		# functions iteratively is ineffective otherwise
		def get_lambda(e):
			return lambda *args: self._base(e, *args)

		for entity in self.ALLOWED_ENTITIES:
			self.methods[entity] = get_lambda(entity)

	'''
	(Internal) Call the base method for the given class
	'''
	def _base(self, *args, **kwargs):
		return self._search(*args, **kwargs)

	'''
	(Python Internal) Attempt to retrieve an attribute by name, from the given methods

	Parameters
		str name - name of attribute

	Returns
		Attribute with the given name
	'''
	def __getattr__(self, name):
		try:
			return self.methods[name]
		except KeyError:
			raise AttributeError("{name} is not a valid entity.".format(name = name))

	'''
	(Internal) Make an API query with the given parameters

	Parameters
		dict query - query to send to the API

	Returns
		(dict) Parsed JSON representation of query response

	Examples
		search._api_query({"entity": "song", "term": "Madness", "country": "US"})
		search._api_query({"entity": "album", "term": "Native, One Republic", "country": "UK"})
	'''
	def _api_query(self, query):
		resp = urllib2.urlopen(self.BASE_URL, urllib.urlencode(query))
		if resp.getcode() != 200:
			raise ValueError("Unable to make call successfully")
		return json.loads(resp.read())

	'''
	(Internal) Search the API for a given query and entity

	Parameters
		str entity - type of query (must be in ALLOWED_ENTITIES)
		str query - query to search the API for	

	Examples
		search._search("song", "Madness")
		search._search("album", "Songs of Innocence")
	'''
	def _search(self, entity, query):
		if (not entity in self.ALLOWED_ENTITIES):
			raise ValueError("{entity} not allowed as an entity. See iTunesSearch.ALLOWED_ENTITIES".format(entity = entity))
		return self._api_query({"entity": entity, "term": query, "country": self.country})

'''
The ArtworkSearch class wraps around the Search utility, providing
a simpler interface for finding the artwork of songs or albums.

Usage
	artwork_search = ArtworkSearch()
	artwork_search.song("Madness, Muse")
	artwork_search.album("Black Holes and Revelations, Muse")
'''
class ArtworkSearch(Search):
	'''
	(Internal) Call the base method for the given class
	'''
	def _base(self, *args, **kwargs):
		return self._artworkSearch(*args, **kwargs)

	'''
	(Internal) Find the artwork for a given query

	Arguments
		str entity - type of entity to search for (see Search.ALLOWED_ENTITIES)
		str query - query to use in search
		int resolution (optional) - resolution of the image to return (not guaranteed)

	Returns
		(str) URL of artwork with the image (None if not found)

	Examples
		artwork_search._artworkSearch("song", "Madness")

		# resolution of 100x100px
		artwork_search._artworkSearch("album", "Songs of Innocence", 100)
	'''
	def _artworkSearch(self, entity, query, resolution = 600):
		results = self._search(entity, query)
		if results["resultCount"] >= 1:
			return results['results'][0]["artworkUrl60"].replace("60x60", "{res}x{res}".format(res = resolution))
		else:
			return None
