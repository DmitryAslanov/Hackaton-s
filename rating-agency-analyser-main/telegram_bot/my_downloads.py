import spacy
import joblib

nlp = None
model = None
nlp_cat = None
nlp_a = None
nlp_b = None
nlp_c = None

def load():
    global nlp 
    global model
    global nlp_cat 
    global nlp_a 
    global nlp_b
    global nlp_c
    nlp_cat = spacy.load('train3/sym/sym_model/model-best')
    nlp_a = spacy.load('train3/subsym/subsym_a/subsym_model/model-best/')
    nlp_b = spacy.load('train3/subsym/subsym_b/subsym_model/model-best/')
    nlp_c = spacy.load('train3/subsym/subsym_c/subsym_model/model-best/')
    nlp = spacy.load("ru_core_news_lg")
    # model = joblib.load('logreg.pkl')
    print('Models loaded')
