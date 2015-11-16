import urllib
from bs4 import BeautifulSoup
import string
import re

class Indexer:
    def __init__(self):
        self.baseUrl = 'http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/'
        self.stopWords = self.getStopWords()
        self.remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)


    def getIndex(self, webGraph):
        pageToken = {}

        for page in sorted(webGraph):
            token = []
            url = self.baseUrl + page + ".html"
            html = urllib.urlopen(url).read()
            soup = BeautifulSoup(html, 'html.parser')
            plaintext = soup.get_text().lower().translate(self.remove_punctuation_map)
            plaintext = re.sub('\n+', ' ', plaintext)
            words = plaintext.split(' ')
            words = filter(None, words)
            for word in words:
                if word not in self.stopWords:
                    token.append(word)
            pageToken[page] = token
        return pageToken


    def getIndex(self, pageToken):

        tokenSet = {}
        for page, tokenList in sorted(pageToken.iteritems()):
            uniqueToken = list(set(tokenList))
            for token in uniqueToken:
                if token not in tokenSet:
                    tokenSet[token] = [(page, tokenList.count(token))]
                else:
                    tokenSet[token].append((page, tokenList.count(token)))

        tokenTupel = {}
        for token, occurences in sorted(tokenSet.iteritems()):
            tokenTupel[token, len(occurences)] = occurences

        return tokenTupel

    def getStopWords(self):
        stopwordsUrl = "http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/stop_words.txt"
        soup = BeautifulSoup(urllib.urlopen(stopwordsUrl).read(), 'html.parser')
        return re.findall('\'(\w+)\'', soup.get_text())