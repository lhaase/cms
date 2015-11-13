import urllib
import re
from Parser import Parser


class Frontier:
    def __init__(self):
        self.sitesAlreadyCrawled = []
        self.parser = Parser()
        self.webGraph = {}


    def getWebGraph(self, urls):
        for url in urls:
            self.crawlIfNeeded(url)

        return self.webGraph


    def crawlIfNeeded(self, url):
        if not self.sitesAlreadyCrawled.__contains__(url):
            linksFound = self.parser.parseLinks(urllib.urlopen(url).read())
            self.addToMap(url, linksFound)

            self.sitesAlreadyCrawled.append(url)
            for link in linksFound:
                self.crawlIfNeeded(link)


    def addToMap(self, url, links):
        filenames = []
        for link in links:
            filenames.append(self.extractFilename(link))

        self.webGraph[self.extractFilename(url)] = filenames

    def extractFilename(self, url):
        return re.search('(d\d\d)', url).group(0)