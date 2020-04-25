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

print(translateText('es', 'I like cookies'))





