import sys
import os
import random
import ast
import urllib 
import urllib.request
import urllib.parse

list_url = ["https://quizlet.com/316556665/computer-science-flash-cards/",
"https://quizlet.com/275472388/computer-science-computer-organisation-flash-cards/"
"https://quizlet.com/245841710/computer-science-computer-organisation-flash-cards/",
"https://quizlet.com/gb/248771693/computer-science-flash-cards/",
"https://quizlet.com/232563390/computer-science-flash-cards/",
"https://quizlet.com/266203493/ap-computer-science-computer-definitions-flash-cards/",
"https://quizlet.com/311647712/computer-science-unit-2-flash-cards/",
"https://quizlet.com/200714704/computer-science-computer-organisation-flash-cards/",
"https://quizlet.com/232081563/computer-science-3-flash-cards/",
"https://quizlet.com/gb/311074306/networking-ocr-computer-science-flash-cards/"]

url = list_url[random.randint(0,9)] 
#url = "https://quizlet.com/252171543/art-history-flash-cards/"
payload = {'url':url}
encoded = urllib.parse.urlencode(payload)
#print(encoded)

link="https://www.wolframcloud.com/objects/mukilankarthikeyan357/junk/api?" + encoded
qa_list = urllib.request.urlopen(link).read() # dict of all the questions and answers.
qa_list = ast.literal_eval(qa_list.decode("utf-8"))
print(type(qa_list))
#print(http_response)
questions_answers = {} # dictionary of 5 Q and As.


for i in range(5):
    question, answer = qa_list.popitem()
    questions_answers[question] = answer

print(questions_answers)

