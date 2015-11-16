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

    def getCosineSim(self,query):

        queryScores = self.getQueryScores(query)
        queryLength = self.getQueryLength(queryScores)

        documentLengths = {}
        matchingDocs = {}
        for doc,scores in self.pageTokenScores.iteritems():
            documentLength = 0.0
            for token,weight in scores.iteritems():
                documentLength += weight * weight
                if (token in queryScores):
                    matchingDocs[doc] = scores
            documentLength = math.sqrt(documentLength)
            documentLengths[doc] = documentLength

        similarities = {}
        for word,weight in queryScores.iteritems():
            for doc,scoreList in matchingDocs.iteritems():
                if word in scoreList:
                    docWeight = scoreList[word]
                else:
                    docWeight = 0.0
                docLength = documentLengths[doc]
                sim = (weight * docWeight) / (queryLength * docLength)
                if doc not in similarities:
                    similarities[doc] = sim
                else:
                    similarities[doc] += sim

        return similarities


    def search(self, query):
        cosineSim = self.getCosineSim(query)
        valuesAsKeys = {}
        for doc, sim in cosineSim.iteritems():
            valuesAsKeys[sim] = doc

        print query
        for sim, doc in sorted(valuesAsKeys.iteritems(), reverse=True):
            print doc + ':\t' + '{0:.6f}'.format(sim)


    def searchAdvanced(self, query, pageRanks):
        cosineSim = self.getCosineSim(query)
        pageRank = pageRanks[len(pageRanks)-1]

        combinedPrCs = {}

        for doc in cosineSim:
            if doc in pageRank:
                cs = cosineSim[doc]
                pr = pageRank[doc]
                combinedPrCs[doc] = 2 * cs * pr / (cs + pr)

        valuesAsKeys = {}
        for doc, prcs in combinedPrCs.iteritems():
            valuesAsKeys[prcs] = doc

        print query
        for prcs, doc in sorted(valuesAsKeys.iteritems(), reverse=True):
            print doc + ':\t' + '{0:.6f}'.format(prcs)
