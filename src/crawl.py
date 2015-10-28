from Frontier import Frontier

frontier = Frontier()
webGraph = frontier.getWebGraph()

for entry in sorted(webGraph.keys()):
    print entry + ' -> ' + ', '.join(webGraph[entry])

