'''
import cachetools
from . import lang

enabled = True

maxsize = 1000

scriptures = {}

for each in lang.available:
    scriptures[each] = cachetools.LRUCache(maxsize=maxsize)
'''