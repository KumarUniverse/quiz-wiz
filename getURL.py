
import urllib 
import urllib.request
import urllib.parse

list_url = ["https://quizlet.com/228956562/spanish-vocabulary-flash-cards/",
"https://quizlet.com/216903045/vocabulary-spanish-flash-cards/",
"https://quizlet.com/282991754/spanish-vocabulary-flash-cards/",
"https://quizlet.com/198900653/spanish-vocabulary-flash-cards/",
"https://quizlet.com/196376071/spanish-vocabulary-flash-cards/",
"https://quizlet.com/296239620/spanish-vocabulary-flash-cards/",
"https://quizlet.com/191325503/spanish-vocabulary-flash-cards/",
"https://quizlet.com/274376767/spanish-vocabulary-flash-cards/",
"https://quizlet.com/209441234/spanish-vocabulary-descriptions-review-flash-cards/",
"https://quizlet.com/318920644/spanish-1-lesson-2-vocabulary-flash-cards/"]

l = len(list_url)
for i in range(l):
    url = list_url[i] 
    #url = "https://quizlet.com/252171543/art-history-flash-cards/"
    payload = {'url':url}
    encoded = urllib.parse.urlencode(payload)
    print(encoded)

    link="https://www.wolframcloud.com/objects/mukilankarthikeyan357/junk/api?" + encoded
    print(link)
    f = urllib.request.urlopen(link)
    resulting_wolfram = []
    resulting_wolfram.append(myfile=f.read())

    
    print(myfile)
