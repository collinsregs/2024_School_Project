import json
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from gensim import corpora, models
import pandas as pd
nltk.download('stopwords')
nltk.download('punkt')

# Read data from the JSON file
with open("C:\\Users\\colli\\OneDrive\\Documents\\_projects\\_temp_data_cleaning\\Data\\1706384929818_Technology.json", encoding='utf-8') as f:
    data = json.load(f)

for chunk in data:

# Tokenize and clean text
    tokens = [word_tokenize(text.lower()) for text in chunk['text']]
    tokens = [[word for word in text if word.isalpha()] for text in tokens]
    stop_words = set(stopwords.words('english'))
    tokens = [[word for word in text if word not in stop_words] for text in tokens]

# Create a dictionary and corpus for LDA
    dictionary = corpora.Dictionary(tokens)
    corpus = [dictionary.doc2bow(text) for text in tokens]

# Perform LDA
    num_topics = 1
    lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary)

# Print topics
    topics = lda_model.print_topics(num_words=2)
    for topic in topics:
        print(topic)

