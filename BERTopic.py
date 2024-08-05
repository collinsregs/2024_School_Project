import bitermplus as btm
import numpy as np
import pandas as pd
import json
import pyLDAvis
import pyLDAvis.gensim_models as gensimvis
from itertools import combinations
import tmplot as tmp

with open('./Data/1706384929818_Technology.json', 'r', encoding='utf-8') as json_file:
    data =json.load(json_file)

for element in data:
    df = pd.DataFrame([element])

# Assuming you have a DataFrame 'df' with a column 'texts' containing your short texts
    text_array=df['text']
    texts = [' '.join(text) for text in text_array]

# Preprocessing: Obtaining terms frequency in a sparse matrix and corpus vocabulary
    X, vocabulary, vocab_dict = btm.get_words_freqs(texts)
    doc_vec = btm.get_vectorized_docs(texts, vocabulary)

# Convert the document-term matrix into biterms
    biterms = btm.get_biterms(doc_vec)

# Create a BTM and pass the biterms to train it
    model = btm.BTM(X, vocabulary,T=2, seed=12321)
    try:
        model.fit(biterms, iterations=100)
    except Exception as e:
        print("an error occurred :")
        print(e)
    else:
        phi = tmp.get_phi(model)
        topics_coords = tmp.prepare_coords(model)
        terms_probs = tmp.calc_terms_probs_ratio(phi, topic=0, lambda_=1)
        tmp.plot_terms(terms_probs)
        # print(phi)
        # phi.head()
    print("\n")
