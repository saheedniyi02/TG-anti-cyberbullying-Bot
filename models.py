import pandas as pd
#read the dataset
dataset_1=pd.read_json("data/Dataset for Detection of Cyber-Trolls.json",lines=True)
dataset_2=pd.read_csv("data/kaggle_parsed_dataset.csv")

#CLEAN DATASET 1
#rename columns 
dataset_1.columns=["text","label","extras"]
#drop unused column
dataset_1=dataset_1.drop("extras",axis=1)

def extract_label(label):
  """ Original label is in the format {'notes': '', 'label': ['1']}"""
  return int(label["label"][0])

dataset_1["label"]=dataset_1["label"].apply(extract_label)

#CLEAN DATASET 2
required_cols=["Text","oh_label"]
dataset_2=dataset_2[required_cols]
dataset_2.columns=["text","label"]

def remove_quotes(text):
  """all  the strings in the csv file have a doube quote "" starting them, let's remove them """
  return text[1:len(text)-2]
  
dataset_2["text"]=dataset_2["text"].apply(remove_quotes)

#CONCATENATE THE DATASETS
all_data=pd.concat([dataset_1,dataset_2])

import nltk
import string
nltk.download('stopwords')
nltk.download('punkt')
from nltk.tokenize import word_tokenize

#functions to clean the text
def clean_text(text):
  """ Clean  the text"""
  # Lowering letters
  text = text.lower()

  # Removing emails & twitter usernames
  text = re.sub('\S*@\S*', '', text)

  # Removing urls (S+ matches all non whitespace chars)
  text = re.sub(r'http\S*', '', text)

  # Removing numbers
  text = re.sub('[^a-zA-Z]',' ',text)


  for punctuation in string.punctuation:
    text=text.replace(punctuation,"")

  # Removing all whitespaces and join with proper space
  word_tokens = word_tokenize(text)
  
  #remove all stop words 
  stopwords=nltk.corpus.stopwords.words("english")
  new_word_tokens=[]
  for token in word_tokens:
    if token not in stopwords:
      new_word_tokens.append(token)
      
    return ' '.join(word_tokens)
    
all_data["text"]=all_data["text"].apply(clean_text)

#remove all_duplicates
all_data=all_data.drop_duplicates(subset="text")
#remove missing values
all_data=all_data.dropna(subset=["text"])

#seperate target and text columns 
target=all_data["label"]
text=all_data["text"]

#Import necessary Sklearn functions and classes
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score,precision_score,recall_score,classification_report,f1_score,confusion_matrix,f1_score
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.linear_model import LogisticRegression

X,val,y,y_val=train_test_split(text,target,test_size=0.15,random_state=0)


def clean_data():
	#load the dataset
	dataset_1=pd.read_json("data/Dataset for Detection of Cyber-Trolls.json",lines=True)
	dataset_2=pd.read_csv("data/kaggle_parsed_dataset.csv")
	
	#CLEAN DATASET 1
	#rename columns 
	dataset_1.columns=["text","label","extras"]
	#drop unused column
	dataset_1=dataset_1.drop("extras",axis=1)
	dataset_1["label"]=dataset_1["label"].apply(extract_label)
	
	#CLEAN DATASET 2
	required_cols=["Text","oh_label"]
	dataset_2=dataset_2[required_cols]
	dataset_2.columns=["text","label"]
	dataset_2["text"]=dataset_2["text"].apply(remove_quotes)
	
	#CONCATENATE THE DATASETS
	all_data=pd.concat([dataset_1,dataset_2])
	
	all_data["text"]=all_data["text"].apply(clean_text)
	#remove all_duplicates
	all_data=all_data.drop_duplicates(subset="text")
	#remove missing values
	all_data=all_data.dropna(subset=["text"])
	
	#seperate target and text columns 
	target=all_data["label"]
	text=all_data["text"]
	X,val,y,y_val=train_test_split(text,target,test_size=0.15,random_state=0)
	return X, val, y, y_val
	