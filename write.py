import csv
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_iris
from IPython.display import display
import seaborn as sns
from fast_dash import fastdash
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from sklearn.preprocessing import StandardScaler


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

def reshape_data(data, look_back, n_features):

  X, y = [], []
  for i in range(len(data) - look_back - 1):
    past_points = data.iloc[i]['total_points'].to_numpy()[:-look_back] 
    past_points = past_points[::-1].copy()
    future_point = data['total_points'].iloc[i + look_back]
    X.append(past_points.to_numpy().reshape(1, look_back, n_features))  # Reshape for LSTM
    y.append(future_point.to_numpy())

  X = np.array(X)
  y = np.array(y)

  return X, y

def split_data(data, look_back):
  # Calculate the number of samples for training
  train_size = len(data) - look_back

  # Split data into training and testing sets
  train_data = data.iloc[:train_size]
  test_data = data.iloc[train_size:]

  return train_data, test_data

def forecast (data):
  look_back=30
  n_features = len(topic_list)
  scaler = StandardScaler()
  train_data, test_data= split_data(data, look_back)
  scaler.fit(train_data[['total_points']]) 

  test_data_scaled = scaler.transform(test_data[['total_points']])
  train_data_scaled = scaler.transform(train_data[['total_points']])


  train_x, train_y = reshape_data(train_data_scaled,look_back, n_features)
  test_x, test_y = reshape_data(test_data_scaled, look_back, n_features)

  model = Sequential()
  model.add(LSTM(units = 50, return_sequence = True, input_shape=(look_back, n_features)))
  model.add(LSTM(units=50))
  model.add(Dense(n_features))
  model.compile(loss='mse', optimizer= 'adam')

  model.fit(train_x,train_y, epochs=100, batch_size=32)

  predicted_values = model.predict(test_x)
  print(predicted_values)

# Replace with your actual CSV file path
with open('topic_results.csv', 'r',encoding='utf-8') as csvfile:
  csvreader = csv.reader(csvfile)
  column_names = ['topic', 'date', 'points','text']
  rows = []
  for row in csvreader:
    if row[0] != '':
      rows.append(row)
  df_topics = pd.DataFrame(rows, columns=column_names)
  df_topics['points']=pd.to_numeric(df_topics['points'],errors='coerce')
  df_topics['points'] = df_topics['points'].where(df_topics['points'] != 0 ,1)
  daily_topic_counts = df_topics.groupby(['date','topic']).agg({'points': ['sum',  'count']}).reset_index()
  daily_topic_counts.columns = ['date', 'topic', 'total_points', 'count']
  unique_dates = list(set(df_topics['date']))
  complete_df = daily_topic_counts.copy()
  missing_topic_rows = []
  for date in unique_dates:
    date_topics = df_topics[df_topics['date'] == date]['topic'].tolist()
    missing_topics = [topic for topic in topic_list if topic not in date_topics]
  # Create new rows for missing topics (without modifying df_topics)
    if missing_topics:
      for topic in missing_topics:
        new_row = {'date': date, 'topic': topic, 'total_points': 0, 'count': 0}  # Initialize points and count
        missing_topic_rows.append(new_row)
  complete_df = complete_df._append(missing_topic_rows, ignore_index=True)
  sorted_df = complete_df.sort_values(by=['date'])


forecast(sorted_df)





  # chosen_topic = 'wireless networking'
  # topic_data = sorted_df[sorted_df['topic'] == chosen_topic]

  # train_size = int(len(topic_data) * 0.8)
  # train_data = topic_data.iloc[:train_size]
  # test_data = topic_data.iloc[train_size:]
  # train_data.rename(columns={'date': 'ds', 'count': 'y'}, inplace=True)
  # X_train = train_data.drop(columns=[ 'topic'])  # Feature matrix (replace with your actual features)
  # y_train = train_data['y']
  # display(X_train)


  # model = Prophet()
  # model.fit(X_train)

  # future_dates = model.make_future_dataframe(periods=3, freq='D') 
  # forecast = model.predict(future_dates)