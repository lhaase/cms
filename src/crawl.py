from Frontier import Frontier
from PageRank import PageRank

frontier = Frontier()
pageRank = PageRank()

webGraph = frontier.getWebGraph()

# for entry in sorted(webGraph.keys()):
    # print entry + ' -> ' + ', '.join(webGraph[entry])

print
print '-------------'
print

pr = pageRank.getPageRank(webGraph)



