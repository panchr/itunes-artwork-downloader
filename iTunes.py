# Rushy Panchal
# iTunes.py
# Provides an easy interface to access the Itunes API

import requests
import sys

'''
The Search class provides a simple interface to access the iTunes Search API

Examples
	api = Search()
	api.album("Songs of Innocence, U2") # find the album 
'''
class Search(object):
	BASE_URL = "http://ax.itunes.apple.com/WebObjects/MZStoreServices.woa/wa/wsSearch"

	ALLOWED_ENTITIES = ["musicVideo", "tvSeason", "movie", "id", "shortFilm", "ebook", "album", "audiobook", "podcast", "software", "song"]

	'''
	Create a new iTunes Search API wrapper

	Parameters
		str country - the country to use the API with (defaults to US)

	Examples
		api = Search() # default country
		api_uk = Search("UK") # API using UK as the country
	'''
	def __init__(self, country = "US"):
		self.country = country.upper()

		for entity in self.ALLOWED_ENTITIES:
			setattr(self, entity, lambda query, e = entity: self._search(query, e))

	'''
	(Internal) Make an API query with the given parameters

	Parameters
		dict query - query to send to the API

	Returns
		(dict) Parsed JSON representation of query response
	'''
	def _api_query(self, query):
		r = requests.post(self.BASE_URL, query)
		return r.json()

	'''
	(Internal) Search the API for a given query and entity

	Parameters
		str query - query to search the API for
		str entity - type of query (must be in ALLOWED_ENTITIES)
	'''
	def _search(self, query, entity):
		if (not entity in self.ALLOWED_ENTITIES):
			raise ValueError("{entity} not allowed as an entity. See iTunesSearch.ALLOWED_ENTITIES".format(entity = entity))
		return self._api_query({"entity": entity, "term": query, "country": self.country})
