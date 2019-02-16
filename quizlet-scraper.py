import urllib
import urllib.request
from bs4 import BeautifulSoup
import os

page = 2
# while page <= 2:
optionsUrl = 'https://quizlet.com/subject/art-history/page/' + str(page) + '/?queryMeta=art+history'
optionsPage = urllib.request.urlopen(optionsUrl)

soup = BeautifulSoup(optionsPage, "html.parser")
linkList = soup.find_all('a', attrs={"class": "UILink"})
for link in linkList:
    quizlet = link.get('href')
    if quizlet.startswith('https'): # check if the link is a proper URL
        url = quizlet

    #soup.findAll('p')

    # page += 1;
