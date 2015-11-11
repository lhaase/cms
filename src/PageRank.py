import urllib
import re
from Parser import Parser

class PageRank:

    def getPageRank(self, webGraph):
        backlinkGraph = self.createBacklinkGraph(webGraph)

        # for entry in sorted(backlinkGraph.keys()):
            # print entry + ' <- ' + ', '.join(backlinkGraph[entry])


        d = 0.95
        t = 0.05
        N = len(webGraph)

        pageRank0 = {}
        for page in webGraph:
            pageRank0[page] = 1.0 / N

        for page in webGraph:
            backlinks = backlinkGraph[page]

            sumA = 0
            for pj in backlinks:
                sumA += pageRank0[pj] / len(webGraph[pj])

            sumB = 0
            for pj in webGraph:
                if len(webGraph[pj]) == 0:
                    sumB += pageRank0[pj] / N

            pr = d * (sumA + sumB) + (t/N)

            print '- ' + page + ': ' + str(pr)



    def createBacklinkGraph(self, webGraph):
        backlinkGraph = {}
        for page in sorted(webGraph.keys()):
            backlinks = []
            for link in sorted(webGraph.keys()):
                if page in webGraph[link]: backlinks.append(link)
            backlinkGraph[page] = backlinks
        return backlinkGraph