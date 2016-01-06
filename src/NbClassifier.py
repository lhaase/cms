import string
import re
import os

class NbClassifier:

    def __init__(self):
        self.categories = ['politik', 'wirtschaft', 'sport']
        self.docCount = self.getDocCount()

    def train(self, category):
        trainDocs = self.getTrainDocsFor(category)
        documents = self.cleanDocuments(trainDocs)
        docsInCategory = len(documents)
        Pc = docsInCategory / self.docCount


        for doc in documents:
            print '* '+ doc


    def cleanDocuments(self, documents):
        cleaned = []
        for document in documents:
            plaintext = re.sub('\n+', ' ', document).lower().translate(None, string.punctuation)
            cleaned.append(plaintext)
        return cleaned


    def getTrainDocsFor(self, category):
        docs = []
        path = './data/' + category + '/train/'
        for filename in os.listdir(path):
            file = open (path + filename)
            docs.append(file.read())
        return docs

    def getDocCount(self):
        count = 0.0
        for category in self.categories:
            for file in os.listdir('./data/' + category + '/train/'):
                if file.endswith('txt'):
                    count = count + 1
        return count