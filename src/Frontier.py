import urllib
import re
from Parser import Parser


class Frontier:
    def __init__(self):
        self.pageUrl1 = 'http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/d01.html'
        self.pageUrl2 = 'http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/d06.html'
        self.pageUrl3 = 'http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/d08.html'
        self.sitesAlreadyCrawled = []
        self.parser = Parser()
        self.webGraph = {}


    def getWebGraph(self):
        for url in [self.pageUrl1, self.pageUrl2, self.pageUrl3]:
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