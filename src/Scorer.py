import urllib
from bs4 import BeautifulSoup
import string
import re
import math

class Scorer:
    def createScoring(self, index, webGraph):

        pages = []
        for page in webGraph:
            pages.append(page)
        N = len(pages)

        weights = {}
        for page in sorted(pages):
            termWtd = {}
            for term,occurences in index.iteritems():
                for occurence in occurences:
                    if occurence[0] == page:
                        tfw = 1.0 + math.log(occurence[1], 10)
                        idf = math.log(N/term[1], 10)
                        wtd = tfw * idf
                        termWtd[term[0]] = wtd

            weights[page] = termWtd
            print
            print page
            for term,weight in termWtd.iteritems():
                print term + ': ' + str(weight)