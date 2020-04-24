import json
import os
import requests
import sqlite3
import numpy as np
import matplotlib
import matplotlib.pyplot as plt



querystring = {"source":"{source}","target":"{target}","input":"{input}"}

headers = {
    'x-rapidapi-host': "systran-systran-platform-for-language-processing-v1.p.rapidapi.com",
    'x-rapidapi-key': "86e1254777msh4331a57cf3bc755p11f980jsnceff71f415ab"
    }



# API https://rapidapi.com/systran/api/systran-io-translation-and-nlp
def translator_url()
    key = "86e1254777msh4331a57cf3bc755p11f980jsnceff71f415ab"
    key_url = "apiKey=" + key
    url = "https://systran-systran-platform-for-language-processing-v1.p.rapidapi.com/translation/text/translate"
    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)
    return url  






def main():
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+'Food Data' + ".db")
    cur = conn.cursor()
if __name__ == "__main__":
    main()