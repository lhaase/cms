from Frontier import Frontier
from PageRanker import PageRanker
from Indexer import Indexer
from Scorer import Scorer
import re

frontier = Frontier()
pageRanker = PageRanker()
indexer = Indexer()
scorer = Scorer()

seedDocuments = [
    'http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/d01.html',
    'http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/d06.html',
    'http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/d08.html'
]

def printWebGraph(webGraph):
    print
    print '-*( Web Graph )*-'
    print
    for entry in sorted(webGraph.keys()):
        print entry + ' -> ' + ', '.join(webGraph[entry])

def printIndex(index):
    print
    print '-*( Indices )*-'
    print
    for term,occurences in sorted(index.iteritems()):
        print '(' + term[0] + ', df:' + str(term[1]) + ') ->',
        print re.sub('(u)?\'', '', str(occurences))


def printPageRanks(pageRanks):
    print
    print '-*( Page Ranks )*-'
    print
    print '\t\t\t\t',
    for page in sorted(pageRanks[1]):
        print '\t\t\t' + page,
    for step, pageRank in sorted(pageRanks.iteritems()):
        print
        print 'Step ' + str(step) + '\t',
        for page, rank in sorted(pageRank.iteritems()):
            print '\t\t' + '{0:.4f}'.format(rank),


webGraph = frontier.getWebGraph(seedDocuments)
pageRank = pageRanker.getPageRank(webGraph)
index = indexer.getIndex(webGraph)

# printWebGraph(webGraph)
# printPageRanks(pageRank)
# printIndex(index)

scorer.createScoring(index, webGraph)