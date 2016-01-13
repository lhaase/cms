import string
import re
import os
import math
import urllib
from bs4 import BeautifulSoup


class NbClassifier:

    def __init__(self):
        self.categories = { 'politik': (0, {}),
                            'wirtschaft': (0, {}),
                            'sport': (0, {})}
        self.remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
        self.stopWords = self.getStopWords()

        self.docCount = self.getDocCount()

    def classifyAllTestDocuments(self):

        for category in self.categories:

            path = './data/' + category + '/test/'
            print
            print category + '/test'

            for filename in os.listdir(path):
                file = open(path + filename)
                print re.search('(\w\d\d\d)', filename).group(0) + ': ' + self.getMaxProbability(file.read())


    def getMaxProbability(self, docContent):

        document = self.cleanDocuments([docContent])[0]

        probs = {}
        for category in self.categories:
            probs[category] = self.calcProbability(document, category)

        # print probs
        return max(probs, key=probs.get)


    def calcProbability(self, document, category):

        # print category
        pc = self.categories[category][0] / self.docCount
        ptcSum = 0.0

        docWords = document.split(' ')
        docWords = filter(None, docWords)
        new_items = [item for item in docWords if not item.isdigit() and item not in self.stopWords]

        for word in new_items:
            ptc = self.calcPtc(word, category)
            ptcSum += math.log(ptc, 10)

        prob = math.log(pc, 10) + ptcSum
        return prob


    def train(self, category):
        trainDocs = self.getTrainDocsFor(category)
        documents = self.cleanDocuments(trainDocs)

        categoryToken = {}

        for doc in documents:
            words = doc.split(' ')
            words = filter(None, words)
            new_items = [item for item in words if not item.isdigit() and item not in self.stopWords]

            for word in new_items:
                if word not in categoryToken:
                    categoryToken[word] = 1
                else:
                    categoryToken[word] += 1

        self.categories[category] = (len(documents), categoryToken)


    def calcPtc(self, word, category):
        categoryToken = self.categories[category]
        tokenCount = 0.0
        for token,count in categoryToken[1].iteritems():
            tokenCount += (count + 1)

        if word in categoryToken[1]:
            tct = categoryToken[1][word] + 1.0
        else:
            tct = 1.0

        return tct / tokenCount


    def cleanDocuments(self, documents):
        cleaned = []
        for document in documents:
            plaintext = re.sub('\n+', ' ', document).decode('utf-8').lower().translate(self.remove_punctuation_map)
            cleaned.append(plaintext)
        return cleaned


    def getTrainDocsFor(self, category):
        docs = []
        path = './data/' + category + '/train/'
        for filename in os.listdir(path):
            file = open(path + filename)
            docs.append(file.read())
        return docs


    def getDocCount(self):
        count = 0.0
        for category in self.categories:
            for file in os.listdir('./data/' + category + '/train/'):
                if file.endswith('txt'):
                    count = count + 1
        return count

    def getStopWords(self):
        stopwordsUrl = "http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/stop_words.txt"
        soup = BeautifulSoup(urllib.urlopen(stopwordsUrl).read(), 'html.parser')
        return re.findall('\'(\w+)\'', soup.get_text())