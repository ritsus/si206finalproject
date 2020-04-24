import json
import os
import requests
import sqlite3
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

# API https://rapidapi.com/systran/api/systran-io-translation-and-nlp
def translator_url()
    key = "86e1254777msh4331a57cf3bc755p11f980jsnceff71f415ab"
    key_url = "apiKey=" + key
    url = "https://rapidapi.com/systran/api/systran-io-translation-and-nlp" + key_url
    return url  
