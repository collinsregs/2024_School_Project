
data_dir <-"C:\\Users\\colli\\OneDrive\\Documents\\_projects\\_temp_data_cleaning\\Data\\1706384929818_Technology.json"

install.packages(c("tm","topicmodels","slam","rjson"))

library(tm)
library(topicmodels)
library(slam)
library(rjson)

data<- fromJSON(file=data_dir)


corpus<-Corpus(VectorSource(data$text))
corpus <- tm_map(corpus, content_transformer(tolower))
corpus <- tm_map(corpus, removePunctuation)
corpus <- tm_map(corpus, removeNumbers)
corpus <- tm_map(corpus, removeWords, stopwords("english"))
corpus <- tm_map(corpus, stripWhitespace)


dtm <- DocumentTermMatrix(corpus)
print(dtm)

num_topics<-5
lda_model<-LDA(dtm,k=num_topics)

topics<- tidy(lda_model,matrix="beta")
print(topics)










#files <- list.files(path = old_dir)

#for (file in files){
  
#}
