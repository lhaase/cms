from Frontier import Frontier
from PageRank import PageRank

frontier = Frontier()
pageRank = PageRank()

webGraph = frontier.getWebGraph()


print
print '-*( Web Graph )*-'
print
for entry in sorted(webGraph.keys()):
    print entry + ' -> ' + ', '.join(webGraph[entry])


pr = pageRank.getPageRank(webGraph)



