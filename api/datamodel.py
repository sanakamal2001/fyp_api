
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk import WordNetLemmatizer
from gensim.models import Word2Vec
import string
import xgboost as xgb

contractions_dict = { "ain t ": "are not "," s ":" is ","aren t ": "are not ","can t ": "can not ","can t ve ": "cannot have ",
" cause ": "because ","could ve ": "could have ","couldn t ": "could not ","couldn t ve ": "could not have ",
"didn t ": "did not ","doesn t ": "does not ","don t ": "do not ","hadn t ": "had not ","hadn t ve ": "had not have ",
"hasn t ": "has not ","haven t ": "have not ","he d ": "he would ","he d ve ": "he would have ","he ll ": "he will ",
"he ll ve ": "he will have ","how d ": "how did ","how d y ": "how do you ","how ll ": "how will ","i d ": "i would ",
"i d ve ": "i would have ","i ll ": "i will ","i ll ve ": "i will have ","i m ": "i am ","i ve ": "i have ",
"isn t ": "is not ","it d ": "it would ","it d ve ": "it would have ","it ll ": "it will ","it ll ve ": "it will have ",
"let s ": "let us ","ma am ": "madam ","mayn t ": "may not ","might ve ": "might have ","mightn t ": "might not ",
"mightn t ve ": "might not have ","must ve ": "must have ","mustn t ": "must not ","mustn t ve ": "must not have ",
"needn t ": "need not ","needn t ve ": "need not have ","o clock ": "of the clock ","oughtn t ": "ought not ",
"oughtn t ve ": "ought not have ","shan t ": "shall not ","sha n t ": "shall not ",
"shan t ve ": "shall not have ","she d ": "she would ","she d ve ": "she would have ","she ll ": "she will ",
"she ll ve ": "she will have ","should ve ": "should have ","shouldn t ": "should not ",
"shouldn t ve ": "should not have ","so ve ": "so have ","that d ": "that would ","that d ve ": "that would have ",
"there d ": "there would ","there d ve ": "there would have ",
"they d ": "they would ","they d ve ": "they would have ","they ll ": "they will ","they ll ve ": "they will have ",
"they re ": "they are ","they ve ": "they have ","to ve ": "to have ","wasn t ": "was not ","we d ": "we would ",
"we d ve ": "we would have ","we ll ": "we will ","we ll ve ": "we will have ","we re ": "we are ","we ve ": "we have ",
"weren t ": "were not ","what ll ": "what will ","what ll ve ": "what will have ","what re ": "what are ",
"what ve ": "what have ","when ve ": "when have ","where d ": "where did ",
"where ve ": "where have ","who ll ": "who will ","who ll ve ": "who will have ","who ve ": "who have ",
"why ve ": "why have ","will ve ": "will have ","won t ": "will not ","won t ve ": "will not have ",
"would ve ": "would have ","wouldn t ": "would not ","wouldn t ve ": "would not have ","y all ": "you all ",
"y all d ": "you all would ","y all d ve ": "you all would have ","y all re ": "you all are ","y all ve ": "you all have ",
"you d ": "you would ","you d ve ": "you would have ","you ll ": "you will ","you ll ve ": "you will have ",
"you re ": "you are ","you ve ": "you have ", "aint ": "are not ","arent ": "are not ","cant ": "can not ","cant ve ": "cannot have ",
"couldve ": "could have ","couldnt ": "could not ","couldnt ve ": "could not have ",
"didnt ": "did not ","doesnt ": "does not ","dont ": "do not ","hadnt ": "had not ","hadnt ve ": "had not have ",
"hasnt ": "has not ","havent ": "have not ","hed ": "he would ","hed ve ": "he would have ",
"howd ": "how did ","howd y ": "how do you ","howll ": "how will ","id ": "i would ",
"id ve ": "i would have ","ill ve ": "i will have ","im ": "i am ","ive ": "i have ",
"isnt ": "is not ","itd ": "it would ","itd ve ": "it would have ","itll ": "it will ","itll ve ": "it will have ",
"lets ": "let us ","maam ": "madam ","mightve ": "might have ","mightnt ": "might not ",
"mightnt ve ": "might not have ","mustve ": "must have ","mustnt ": "must not ","mustnt ve ": "must not have ",
"neednt ": "need not ","neednt ve ": "need not have ","oclock ": "of the clock ","oughtnt ": "ought not ",
"oughtnt ve ": "ought not have ","shant ": "shall not ",
"shant ve ": "shall not have ","shed ": "she would ","shed ve ": "she would have ","shell ": "she will ",
"shell ve ": "she will have ","shouldve ": "should have ","shouldnt ": "should not ",
"shouldnt ve ": "should not have ","sove ": "so have ","thatd ": "that would ","thatd ve ": "that would have ",
"thered ": "there would ","thered ve ": "there would have ",
"theyd ": "they would ","theyd ve ": "they would have ","theyll ": "they will ","theyll ve ": "they will have ",
"theyre ": "they are ","theyve ": "they have ","tove ": "to have ","wasnt ": "was not ","wed ": "we would ",
"weve ": "we have ",
"werent ": "were not ","whatll ": "what will ","whatre ": "what are ",
"whatve ": "what have ","whenve ": "when have ","whered ": "where did ",
"whereve ": "where have ","wholl ": "who will ","whove ": "who have ",
"whyve ": "why have ","willve ": "will have ","wont ": "will not ",
"wouldnt ": "would not ","yall ": "you all ",
"yall d ": "you all would ","yall d ve ": "you all would have ","yall re ": "you all are ","yall ve ": "you all have ",
"youd ": "you would ","youd ve ": "you would have ","youll ": "you will ","youll ve ": "you will have ",
"youre ": "you are ","youve ": "you have "}
def contractions(post):  
  for key,value in contractions_dict.items():
    if key in post:
      post=re.sub(key,value,post)
  return post
def cleaning(post):
  post=post.lower()
  post=re.sub(r"http\S+","",post)
  post=re.sub(r"url"," ",post)
  post=re.sub(r"\s[^a-z]\s"," ",post)
  post=re.sub(r"\sop\s"," ",post)
  post=re.sub(r"\s[a-z]\s"," ",post)  
  post=re.sub(r"\s[a-z][a-z]\s"," ",post)
  post=re.sub(r"\w*\d\w*","",post)
  post=re.sub(r"\."," ",post)
  post=re.sub(r"\""," ",post)
  post=re.sub(r"\,"," ",post)
  post=re.sub(r"\(|\)|\[|\]|\{|\}"," ",post)
  post=re.sub(r"\+|\-|\/|\=|\*"," ",post)
  post.translate(str.maketrans('','',string.punctuation))
  post=re.sub(r"\?"," ",post)
  post=re.sub(r"\!"," ",post)
  post=re.sub(r"[^a-z]"," ",post)

  return post

import numpy as np
#vectorization
def dprs_word2vectortest(tokenizedpost):
  dprs_word2vecmodel=Word2Vec.load('dprs_word2vecmodel.bin')
  vectors=[]
  if len(tokenizedpost)<1:
    return np.zeros(100)
  else:
    for word in tokenizedpost:
      if word in dprs_word2vecmodel.wv:
        vectors.append(dprs_word2vecmodel.wv.get_vector(word))
      else:
        vectors.append(np.random.rand(100))
  return np.mean(vectors,axis=0)          
def anx_word2vectortest(tokenizedpost):
  anxty_word2vecmodel=Word2Vec.load('anxty_word2vecmodel.bin')
  vectors=[]
  if len(tokenizedpost)<1:
    return np.zeros(100)
  else:
    for word in tokenizedpost:
      if word in anxty_word2vecmodel.wv:
        vectors.append(anxty_word2vecmodel.wv.get_vector(word))
      else:
        vectors.append(np.random.rand(100))
  return np.mean(vectors,axis=0)
def strs_word2vectortest(tokenizedpost):
  strs_word2vecmodel=Word2Vec.load('strs_word2vecmodel.bin')
  vectors=[]
  if len(tokenizedpost)<1:
    return np.zeros(100)
  else:
    for word in tokenizedpost:
      if word in strs_word2vecmodel.wv:
        vectors.append(strs_word2vecmodel.wv.get_vector(word))
      else:
        vectors.append(np.random.rand(100))
  return np.mean(vectors,axis=0)      

from numpy.linalg import norm
#remove all xgb stuff except testing with user data     
import pickle
with open('depressxgb.pickle','rb') as f:
  dep_rf=pickle.load(f)
def depress_rf(vector):
  depress_pred=dep_rf.predict_proba(vector)
  return depress_pred[:,1]

with open('anxtyxgb.pickle','rb') as f:
  anx_rf=pickle.load(f)
def anxiety_rf(vector):
  anxiety_pred=anx_rf.predict_proba(vector)
  return anxiety_pred[:,1]

with open('strsxgb.pickle','rb') as f:
  strs_rf=pickle.load(f)  
def stress_rf(vector):
  stress_pred=strs_rf.predict_proba(vector)
  return stress_pred[:,1]

def DASlabel(query):

  text=re.sub("\'"," ",query)
  text=contractions(text)
  text=cleaning(text)
  post=re.sub(" +"," ",text)
  post=word_tokenize(post)
  stop_words=set(stopwords.words("english"))
  temp=[]
  for w in post:
    if w not in stop_words:
      temp.append(w)
  post=temp
  pos=[]
  pos=nltk.pos_tag(post)
  allowed_type=["JJ","RB","JJR","JJS","RBR","RBS","NN","NNS","NNP"]
  convert={"a":["JJ","JJR","JJS"],"r":["RB","RBR","RBS"],"n":["NN","NNS","NNP"]}
  cleaned_words=[]
  lematizer=WordNetLemmatizer();
  for w in pos:
    if w[1] in allowed_type:
      for key,val in convert.items():
        if w[1] in val:
          cleaned_words.append(lematizer.lemmatize(w[0],pos=key)) 
  post=list(set(cleaned_words))
  dvectorizedpost=dprs_word2vectortest(post)
  avectorizedpost=anx_word2vectortest(post)
  svectorizedpost=strs_word2vectortest(post)
  dv=np.array([np.array(dvectorizedpost)])
  av=np.array([np.array(avectorizedpost)])
  sv=np.array([np.array(svectorizedpost)])
  options=[float(depress_rf(dv)),float(anxiety_rf(av)),float(stress_rf(sv))]
  options=np.array(options)
  id=np.argmax(options)
  mentalstate=["depression","anxiety","stress"]
  predicted_label=mentalstate[id]
  level=""
  if(options[id]>90):
    level="moderately severe"
  else:
    level="moderate"  
    
 
  return {"label":predicted_label,"level":level} 

import os
import cv2
SAVING_FRAMES_PER_SECOND = 0.5

def get_saving_frames_durations(cap, saving_fps):
    s = []
    clip_duration = cap.get(cv2.CAP_PROP_FRAME_COUNT) / cap.get(cv2.CAP_PROP_FPS)
    for i in np.arange(0, clip_duration, 1 / saving_fps):
        s.append(i)
    return s
def extract_frames(video_file):
  images=[]
  cap = cv2.VideoCapture(video_file)
  fps = cap.get(cv2.CAP_PROP_FPS)
  print("FPS:",fps)
  saving_frames_per_second = min(fps, SAVING_FRAMES_PER_SECOND)
  saving_frames_durations = get_saving_frames_durations(cap, saving_frames_per_second)
  count = 0
  while True:
    is_read, frame = cap.read()
    if not is_read:
      break
    frame_duration = count / fps
    try:
      closest_duration = saving_frames_durations[0]
    except IndexError:
      break
    if frame_duration >= closest_duration:
      # cv2.imwrite(os.path.join(filename, f"frame{frame_duration}.jpg"), frame) 
      images.append(frame)
      try:
        saving_frames_durations.pop(0)
      except IndexError:
        pass
    count += 1
  return images
from deepface import DeepFace
def video_predictor(video):
  predictions=[]
  for filename in video:
      result = DeepFace.analyze(filename, actions = ['emotion'],enforce_detection=False)
      emotions=result[0]['emotion']
      das=[emotions['angry'],emotions['fear'],emotions['sad']]
      das=np.array(das)
      id=np.argmax(das)
      classes=['stress','anxiety','depression']
      print(classes[id])
      predictions.append(classes[id])
  return predictions    

  



