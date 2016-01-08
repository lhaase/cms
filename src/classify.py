from NbClassifier import NbClassifier

nb = NbClassifier()

nb.train('politik')
nb.train('wirtschaft')
nb.train('sport')

nb.classifyAllTestDocuments()

