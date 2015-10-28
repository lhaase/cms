from bs4 import BeautifulSoup

class Parser:
    def __init__(self):
        self.baseUrl = 'http://people.f4.htw-berlin.de/fileadmin/user_upload/Dozenten/WI-Dozenten/Classen/DAWeb/smdocs/'

    def parseLinks(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        links = []

        for aTag in soup.find_all('a'):
            links.append(self.baseUrl + aTag.get('href'))
        return links

