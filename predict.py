from flask import *
import pickle
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from gensim import utils
import gensim.parsing.preprocessing as gsp
from sklearn import preprocessing
#%%
vec = open("news_classifier.pkl", 'rb')
loaded_model = pickle.load(vec)
vcb = open("vocab_news_classifier.pkl", 'rb')
loaded_vocab = pickle.load(vcb)
le = preprocessing.LabelEncoder()
labls = ['business', 'entertainment', 'politics', 'sport', 'tech']
le.fit(labls)

def CleanInput(input_text):
    filters = [
               gsp.strip_tags, 
               gsp.strip_punctuation,
               gsp.strip_multiple_whitespaces,
               gsp.strip_numeric,
               gsp.remove_stopwords, 
               gsp.strip_short, 
               gsp.stem_text
              ]

    def clean_text(s):
        s = s.lower()
        s = utils.to_unicode(s)
        for f in filters:
            s = f(s)
        return s
    res = clean_text(input_text)    
    return res
#mutliple inputs can be sent
def pred(text):
    examples = [text]
    count_vect = TfidfVectorizer(analyzer='word',ngram_range=(1,2), max_features=50000,max_df=0.5,use_idf=True, norm='l2',vocabulary=loaded_vocab)
    tfidf_transformer = TfidfTransformer()
    x_count = count_vect.fit_transform(examples)
    predicted = loaded_model.predict(x_count)
    result_category = predicted[0]
    final_pred = le.inverse_transform([result_category])
    try:
        return {"res":final_pred.tolist()}
    except:
        return "Failed"

app = Flask(__name__)
logging.basicConfig(filename="classifier_logs.log",level=logging.DEBUG,
                    format=' %(message)s :: %(asctime)s | %(name)s | %(levelname)s|%(threadName)s')
logging.info("Running the classifier..")

@app.route('/auto_labeller',methods=['POST'])
def Label_It():
    data= request.get_json()
    input_text = data["text"]
    try:
        filtered_input = CleanInput(input_text)
    except:
        pass
    try:
        predictions = pred(filtered_input)
    except:
        print("failed at pred")
    #app.logging.info("Predicted Label for " + input_text + " Label is" + str(predictions))
    return predictions
if __name__ == "__main__":
    app.run(host='0.0.0.0',port="5002", debug=True)