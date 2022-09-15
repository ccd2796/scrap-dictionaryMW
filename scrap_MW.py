# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 09:58:19 2022

@author: CCD
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

words = pd.read_csv('palabras.csv')
words = list(words['0'])

dict_words_url = {}
for word in words:
    URL = "https://www.merriam-webster.com/dictionary/" + word
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    dict_words_url[word] = soup
    print(word)
    
#checking if word exists in dictionary (they all exist, no more depuration needed)
# check existe soup.find_all("p", attrs={"class":"spelling-suggestion-text"})
for word, soup in dict_words_url.items():
    if soup.find_all("p", attrs={"class":"spelling-suggestion-text"}):
        print(word)

#extracting definitions
dict_words_def = {'word':[], 'meaning':[]}
for word in words:
    soup = dict_words_url[word]
    parent = soup.find("div", attrs={"id":"dictionary-entry-1"}).parent

    entries = parent.find_all('div', attrs={"id":re.compile('dictionary-entry*')}, recursive=False)
    for entry in entries:
        definitions = entry.find_all('span', attrs={'class':'dtText'})
        for definition in definitions:
            word_def = definition.text
            dict_words_def['word'].append(word)
            dict_words_def['meaning'].append(word_def.replace(': ', '', 1))
            
df_word = pd.DataFrame(dict_words_def)
df_word.to_csv('words.csv')
