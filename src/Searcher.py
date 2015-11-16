import math

class Searcher:

    def __init__(self, index, pageToken):
        self.pageTokenScores = {}
        self.tokenIdfs = {}
        self.createScoring(index, pageToken)


    def createScoring(self, index, pageToken):

        N = len(pageToken)
        idfs = {}
        for term in index:
            idfs[term[0]] = math.log(float(N)/float(term[1]), 10)

        for page in sorted(pageToken):
            weights = {}
            for term,occurences in index.iteritems():
                for occurence in occurences:
                    if occurence[0] == page:
                        tf = 1.0 + math.log(occurence[1], 10)
                        wtd = tf * idfs[term[0]]
                        weights[term[0]] = wtd

            self.pageTokenScores[page] = weights
        self.tokenIdfs = idfs


    def getQueryScores(self, query):
        queryWords = query.split(' ')
        queryScores = {}

        for word in queryWords:
            tfw = 1.0 + math.log(queryWords.count(word), 10)
            idf = self.tokenIdfs[word]
            wtd = tfw * idf
            queryScores[word] = wtd
        return queryScores


    def getQueryLength(self,queryScores):
        queryLength = 0.0
        for word,score in queryScores.iteritems():
            queryLength += score * score
        return math.sqrt(queryLength)


    def search(self, query):

        queryScores = self.getQueryScores(query)
        queryLength = self.getQueryLength(queryScores)

        documentLengths = {}
        matchingDocs = {}
        for page,scores in self.pageTokenScores.iteritems():
            documentLength = 0.0
            for token,weight in scores.iteritems():
                documentLength += weight * weight
                if (token in queryScores):
                    matchingDocs[page] = scores
            documentLength = math.sqrt(documentLength)
            documentLengths[page] = documentLength

        similarities = {}
        for word,weight in queryScores.iteritems():
            for doc,scoreList in matchingDocs.iteritems():
                docWeight = scoreList[word]
                docLength = documentLengths[doc]
                sim = (weight * docWeight) / (queryLength * docLength)
                similarities[sim] = doc

        print queryScores.keys()
        for sim,page in sorted(similarities.iteritems(), reverse=True):
            print page + ':\t' + '{0:.6f}'.format(sim)

