import csv
import re

path = './topic_results.csv'

pattern = r'\{(?:[^{}]|())*\}'

with open(path, mode='r') as file:
  csv_reader = csv.reader(file)
  for row in csv_reader:
    for item in row:
      print (item)