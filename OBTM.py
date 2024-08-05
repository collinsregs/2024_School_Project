import ollama
import re
import string
import nltk
import pandas as pd
import json
from gensim import corpora
from gensim.models import LsiModel
from gensim.models import TfidfModel
from nltk.corpus import stopwords
import time
import os
import shutil

# Download the NLTK stop words if you haven't already
nltk.download('stopwords')


# public variables
path = './topic_results.csv'
json_pattern = r'\{(?:[^{}]|()) \}'
number_pattern = r'\d+'



# functions
def parse_json(ollama_response_string):
    data_string = ollama_response_string
# Find the first JSON object using the regular expression
    match = re.search(json_pattern, data_string)

    if match:
# Extract the JSON string from the match object
      json_string = match.group(0)
      return json_string

def match_topics(response, topic_list):
    words = [word.lower() for word in re.findall(r'\w+', response)]
    matched_topics = []

    for topic in topic_list:
        if all(word in words for word in topic.split()):
            matched_topics.append(topic)

  # Prioritize longer topics if multiple topics match
    if matched_topics:
        return max(matched_topics, key=len)
    else:
        return None

def ollama_classifier(topic_words):
    topic_list = [
  # Hardware
  "processors",
  "graphics processing units (GPUs)",
  "motherboards",
  "memory (RAM)",
  "storage devices (HDDs, SSDs)",  # Combined storage category
  "input devices",
  "output devices",

  # Software
  "operating systems",
  "system software",
  "enterprise software (CRM, etc.)",  # Combined CRM example
  "application software (media players, etc.)",  # Combined media player example
  "development tools",

  # Networking
  "wired networking",
  "wireless networking",

  # Security
  "antivirus software",
  "anti-malware software",
  "data encryption",
  "password management",
  "firewalls",
  "intrusion detection systems (IDS)",
  "virtual private networks (VPNs)",

  # Consumer Electronics
  "smartphones",
  "tablets",
  "wearables",
  "televisions",
  "gaming consoles",
  "home audio systems",

  # Cloud Computing
  "cloud storage",
  "cloud service models",
  "cloud deployment models",

  # Artificial Intelligence & Big Data
  "machine learning",
  "deep learning",
  "natural language processing (NLP)",
  "computer vision",
  "big data tools and technologies",
  "data warehousing",
  "business intelligence (BI)",

  # Other
  "blockchain",
  "virtual reality and augmented reality (VR/AR)",
  "cybersecurity",
  "internet of things (IoT)",
  "bioengineering and healthcare technologies",
  "materials science",
  "nanotechnology",
  "electrical engineering",
  "robotics"
]
    prompt = f"From the provided list of topics classify the text '{topic_words}' into the best topic. Prefer the deepest topic classification where possible over top level topics. The response should be in the form 'Topic':'topic'. ALL TOPICS SHOULD BE FROM THIS LIST: {topic_list}. DO NOT PROVIDE EXTRA TEXT OR EXPLANATIONS BE VERY CONCISE"
    response = ollama.generate(model='mistral', prompt=prompt)
    answer = response['response']
    topic=match_topics(answer,topic_list)
    return topic

def topic_modelling(file):
    match_date = re.search(number_pattern, file)
    date = match_date.group(0)
    timestamp = int(date)/1000  # Assuming 'date' is the extracted string
    date_object = time.localtime(timestamp)
    date_format = "%Y-%m-%d"
    date_string = time.strftime(date_format, date_object)
    ollama_df = pd.DataFrame(columns=['Topic',  'date','points', 'text'])
    with open(file, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
    for element in data:
        df = pd.DataFrame([element])
        points = df['points'].values[0]
# Assuming you have a DataFrame 'df' with a column 'texts' containing your short texts
        text_array = df['text']
# Get a list of stop words from NLTK
        stop_words = set(stopwords.words('english'))
        texts = []
        for text in text_array:
# Remove punctuation
            text_no_punct = ''.join([char for char in text if char not in string.punctuation])
# Split into words
            words = text_no_punct.split()
# Remove stop words and join back into a string
            text_no_stops = ' '.join([word for word in words if word not in stop_words])
            texts.append(text_no_stops)
# Create a dictionary representation of the documents.
        documents_raw = [text.split() for text in texts]
        words = [[word for word in doc if word not in stop_words] for doc in documents_raw]
        punctuation = string.punctuation
        documents = [[''.join(re.split(f"[ {punctuation}]", word)) for word in doc] for doc in words]
        dictionary = corpora.Dictionary(documents)
# Convert document into the bag-of-words (BoW) format = list of (token_id, token_count) tuples.
        corpus = [dictionary.doc2bow(text) for text in documents]
# Train LSA model
        tfidf = TfidfModel(corpus, id2word=dictionary)
        corpus_tfidf = tfidf[corpus]
        model = LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2)
# Access topic information
        topics = model.show_topics(formatted=False)  # Get topics in dictionary format
# Example: Print top 3 words for each topic
        for i, topic in enumerate(topics):
            topic_label = ', '.join([word for word, _ in topic[1]])
            topic_ollama = ollama_classifier(texts )
# Append row to DataFrame
            try:
                ollama_df = ollama_df._append({ 'Topic':topic_ollama, 'date':date_string, 'points':points, 'text':texts}, ignore_index=True)
            except:
                continue
# Append to Excel file
    ollama_df.to_csv(path, mode='a', index=False, header=False)


source_directory = './Data/'
destination_directory ='./trash_heap/'

files = os.listdir(source_directory)
for file in files:
    source_file = os.path.join(source_directory, file)
    destination_file = os.path.join(destination_directory, file)


    try:
        topic_modelling(source_file)
    except Exception as e:
        print('An error occurred on file',source_file , e)
        continue
    try:
        shutil.move(source_file,destination_file)
        print("finished processing file", source_file)
    except Exception as e:
        print('an error occurred moving file ',source_file)



