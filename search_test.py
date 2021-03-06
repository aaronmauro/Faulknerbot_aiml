import requests
import sys
import re
import webbrowser
from bs4 import BeautifulSoup
from nltk import word_tokenize, pos_tag

	#################
	## Text Search ##
	#################

def search(chatbox):
    nouns = [word for word, pos in pos_tag(word_tokenize(chatbox)) if pos.startswith("N")] 
    term = "".join(nouns).replace(" ","+")
    query = "https://www.google.com/search?num=001&safe=off&q="+term+"+site:http://faulkner.lib.virginia.edu/"
    #optional open browser
    #webbrowser.open(query)
    htmlText = requests.get(query)
    soup = BeautifulSoup(htmlText.text)
    #print full search results
    #print(soup)
    textSearch = soup.findAll('div',attrs={'id':'search'})
    #pick the text from the top result
    topResult = soup.findAll('span',attrs={"class":"st"})
    return str(topResult)

	#################
	## Link Search ##
	#################

def link(chatbox):
    nouns = [word for word, pos in pos_tag(word_tokenize(chatbox)) if pos.startswith("N")] 
    term = "".join(nouns).replace(" ","+")
    query = "https://www.google.com/search?num=001&safe=off&q="+term+"+site:http://faulkner.lib.virginia.edu/"
    htmlText = requests.get(query)
    soup = BeautifulSoup(htmlText.text)
    linkSearch = soup.findAll('cite')
    links = str(linkSearch).replace("<cite>","<a class=\"source\" target='_blank' href='http://").replace("<cite class=\"_WGk\">","<a target='_blank' href='http://").replace("</cite>","'>Source text</a>")
    links = links.replace(", "," ")
    return links
msg = ''
while msg != "quit":
    msg = input(">>>")
    print("Search output:",search(str(msg)))
    print("Link output:",link(msg))