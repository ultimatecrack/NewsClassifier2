from flask import Flask, render_template, request
from flask import jsonify

import joblib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from bs4 import BeautifulSoup
import unicodedata
from spacy.lang.en.stop_words import STOP_WORDS
import re
import contractions
import spacy

app = Flask(__name__)
cat_map = {0:'sport', 1:'entertainment', 2:'business', 3:'politics', 4:'tech'}

def make_to_base(x):
    x_list = []
#     nlp = spacy.load('en_core_web_sm')
    nlp = joblib.load('en_core_web_sm')
    doc = nlp(x)
    
    for token in doc:
        lemma = str(token.lemma_)
        if lemma == '-PRON-' or lemma == 'be':
            lemma = token.text
        x_list.append(lemma)
    return ' '.join(x_list)

def predicText(text):
   text = text.lower()
   text = contractions.fix(text)
   text = re.sub('[^A-Z a-z 0-9-]+', '', text)
   text = re.sub('[^A-Z a-z 0-9-]+', '', text)
   text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8', 'ignore')
   text = ' '.join([t for t in text.split() if t not in STOP_WORDS])
   text = make_to_base(text)

   tfidf = joblib.load('news classifier/vectors/tfidf')
   dfr_idf = tfidf.transform([text])
   X = pd.DataFrame(dfr_idf.toarray())
   classifier = joblib.load('news classifier/models/TFIDF/RFC.h5')
   result_index = classifier.predict(X)[0]
   result = cat_map[result_index]
   # print(result)
   return 'Category type: ' + str(result).capitalize()

@app.route('/predict', methods = ['POST'])
def predict():
   jsonData = request.get_json()
   text = jsonData['sentence']

   result = predicText(text)
   return jsonify(result)

@app.route('/')
def index():
   return render_template('index.html')

if __name__ == '__main__':
   app.run(debug = True)
