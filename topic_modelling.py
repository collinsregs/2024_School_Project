import ollama
import json
import re
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.linear_model import LinearRegression


with open('./Data/1706384929818_Technology.json', 'r', encoding='utf-8') as json_file:
    data =json.load(json_file)

def preprocess(t):
    for element in t:
        text=''.join(element)

    text = re.sub(r'<[^>]*>', '', text)  # remove HTML tags
    text = text.lower()
    return text

def ollama_process(text):
    response = ollama.chat(
        model='mistral',
        messages=[
            {
                'role': 'user',
                'content': 'infer a topic from the following words  '+ f'{text}',
            }
        ]
    )
    return response

for element in data:
    text = element.get('text')
    text_clean=preprocess(text)
    vectorizer = CountVectorizer(max_features=5000, stop_words='english',  min_df=0.0, max_df=1)
    X = vectorizer.fit_transform(text)

    lda = LatentDirichletAllocation(n_components=2, max_iter=100, learning_method='online', random_state=42)
    lda.fit(X)
    print(lda.components_, "\n")
    
    # # Print the topics and their top contributing words
    # for i, topic in enumerate(lda.components_):
    #     print("Topic {}:".format(i))
    #     # print(topic)
    #     print("\nTop 10 contributing words:\n")
    #     topic_words=np.asarray(vectorizer.get_feature_names_out())[np.argsort(topic)[-10:]] 
    #     print(topic_words)
    #     print("\n")
    #     regressor = LinearRegression()
    #     regressor.fit(features, y)
    #     # print(ollama_process(topic_words))



