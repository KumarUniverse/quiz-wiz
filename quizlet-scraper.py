import uuid
import urllib
import urllib.request
from bs4 import BeautifulSoup
import os

page = 2
# while page <= 2:
options_url = 'https://quizlet.com/subject/art-history/page/' + str(page) + '/?queryMeta=art+history'
options_page = urllib.request.urlopen(options_url)
questions_and_answers = {}
soup = BeautifulSoup(options_page, "html.parser")
link_list = soup.find_all('a', attrs={"class": "UILink"})

for link in link_list:
    quizlet = link.get('href')
    if quizlet.startswith('https'): # check if the link is a proper URL
        url = quizlet
        page = urllib.request.urlopen(url)
        baby_soup = BeautifulSoup(page, "html.parser")

        # ques and answers: new changes
        while: 
            answer = soup.find('span', attrs={'class': "TermText notranslate lang-en"})
            question = soup.find('span', attrs={'class': "TermText notranslate lang-en"})
            questions_and_answers[question] = answer # add key-value pair
            if soup.find('span', attrs={'class': "TermText notranslate lang-en"}) == NULL:
                break
    #soup.findAll('p')

    # page += 1;
