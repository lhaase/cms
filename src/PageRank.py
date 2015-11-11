class PageRank:
    def getPageRank(self, webGraph):

        print
        print '-*( Page Ranks )*-'
        print

        backlinkGraph = self.createBacklinkGraph(webGraph)
        pageRanks = self.calculatePageRanks(webGraph, backlinkGraph)

        self.printPageRanks(pageRanks)

    def printPageRanks(self, pageRanks):

        print
        print '\t\t\t\t',
        for page in sorted(pageRanks[1]):
            print '\t\t\t' + page,
        for step, pageRank in sorted(pageRanks.iteritems()):
            print
            print 'Step ' + str(step) + '\t',
            for page, rank in sorted(pageRank.iteritems()):
                print '\t\t' + '{0:.4f}'.format(rank),

    def calculatePageRanks(self, webGraph, backlinkGraph):
        d = 0.95
        t = 0.05
        delta = 0.04
        N = len(webGraph)

        pageRanks = {}
        step = 0
        diff = ''

        while diff > delta:
            pageRank = {}
            print 'Step ' + str(step) + ' diff: ',
            if step == 0:
                print
                for page in webGraph:
                    pageRank[page] = 1.0 / N
            else:
                diff = 0
                prevPageRank = pageRanks[step - 1]

                for page in webGraph:
                    sumA = 0
                    for pj in backlinkGraph[page]:
                        sumA += prevPageRank[pj] / len(webGraph[pj])
                    sumB = 0
                    for pj in webGraph:
                        if len(webGraph[pj]) == 0:
                            sumB += prevPageRank[pj] / N
                    pageRank[page] = d * (sumA + sumB) + (t / N)
                    diff += abs(pageRank[page] - prevPageRank[page])
                print '{0:.4f}'.format(diff)
            pageRanks[step] = pageRank

            step += 1

        return pageRanks

    def createBacklinkGraph(self, webGraph):
        backlinkGraph = {}
        for page in sorted(webGraph.keys()):
            backlinks = []
            for link in sorted(webGraph.keys()):
                if page in webGraph[link]: backlinks.append(link)
            backlinkGraph[page] = backlinks
        return backlinkGraph
