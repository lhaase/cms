from NbClassifier import NbClassifier

nb = NbClassifier()

nb.train('politik')
nb.train('wirtschaft')
nb.train('sport')

nb.classifyAllTestDocuments()

# file = open('./data/politik/test/p018.txt').read()
# nb.getMaxProbability(file)