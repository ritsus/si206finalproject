import json
import os
import requests
import sqlite3
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


API_KEY = "AIzaSyA9HPy3JeHaifs-GlLrG6ydbngZqIrEL6s"

def translateText(targetLanCode, text):

  resp = requests.get('https://translation.googleapis.com/language/translate/v2?target={}&key={}&q={}'.format(targetLanCode, API_KEY, text))
  return resp.json()['data']['translations'][0]['translatedText']

  #print(translateText('es', 'I like cookies'))

def languages()
    Language = input(“Enter translated language:”)
    Language.lower() 
    #only the top 50 langauges used in the world are available 
    Lang_abr = {'zh': 'chi', 'english' : 'en', 'spanish': 'en', 'arabic': 'ar', 'begali': 'bn', 'hindi': 'hi', 'russian' : 'ru', 'portuguese': 'pt',
        'japanese': 'ja','german': 'de', 'Javanese':'jv', 'korean': 'ko','french':'fr', 'turkish':'tr', 'vietnamese': 'vi', 'Telugu':'te', 'marathi': 'mr',
        'tamil':'ta', 'italian': 'it', 'urdu': 'ur', 'guarati': 'gu', 'polish': 'pl', 'ukrainian': 'uk', 'persian': 'fa', 'malay':'ms', 'kannada':'kn', 'oriya':'or',
        'punjabi': 'pa', 'sunda': 'su', 'romanian': 'rm', 'bhojpuri':'bh', 'azerbaijani': 'az', 'maithili': 'bh', 'hausa': 'ha', 'burmese': 'my', 'serbian': 'sr',
        'thai': 'th', 'dutch':'nl', 'yoruba': 'yo', 'sindhi': 'sd', 'slovak':'sk', 'swahili':'sw'}
        #taken from https://photius.com/rankings/languages2.html

    
    while True: 
        if Language in Lang_abr:
            abr = Lang_abr[Language]
            #insert the function or text that will be translated where text is 
            print(translateText(abr,#text)) 
            break 
        else input("That is not a valid language. Try again: "):



