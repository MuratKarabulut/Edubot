# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 19:07:02 2021

@author: Pikacu
"""

import sys
import json
import requests
from keras.models import load_model
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances
import pandas.io.sql
import pandas as pd
import pyodbc
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC  #importing machine learning classification algorithm
import random
import pickle
import string
import nltk 
from  nltk.corpus import stopwords
import fasttext.util
import fasttext
from sklearn.metrics import pairwise_distances # to perfrom cosine similarity

from flask import Flask, jsonify
from flask import make_response
from flask import request
from flask_cors import CORS,cross_origin
from typing import List
from jpype import JClass,isJVMStarted, JString,isJVMStarted, getDefaultJVMPath, shutdownJVM, startJVM, java
from keras.models import load_model

#snowball kök ayırma kütüphanesi
from snowballstemmer import TurkishStemmer
turkStem=TurkishStemmer()

def remove_punctuations(text):
    for punctuation in string.punctuation:
        text = text.replace(punctuation, ' ')
    return text

def remove_StopWord(text):
    cleantext=""
    status=0
    text=text.replace("  "," ")
    for word in text.split(" "):
        status=0
        for stopword in stopwords.words("turkish"):
            if word== stopword:
                status=1
        if status==0:
            cleantext+=word+' '
    return cleantext.strip()

def change_Word_Stem(text):
    cleantext=""
    for word in text.split(" "):
        cleantext+=turkStem.stemWord(word)+" "
    return cleantext.strip()




ZEMBEREK_PATH = r'E:\turkcefasttext\zemberek-full.jar'
if not isJVMStarted():
    startJVM(getDefaultJVMPath(), '-ea', '-Djava.class.path=%s' % (ZEMBEREK_PATH))
    
TurkishMorphology = JClass('zemberek.morphology.TurkishMorphology')
morphology = TurkishMorphology.createWithDefaults()
def Change_Stem_JVM_Zemberek(text):
    kelimeler = ""
    for kel in text.split(" "):
        kelimeleri=kel
        if len(kelimeleri)<1:
            continue
        analysis: java.util.ArrayList = (
            morphology.analyzeAndDisambiguate(kelimeleri).bestAnalysis()
            )
        for i, analysis in enumerate(analysis, start=1):
            f'\nAnalysis {i}: {analysis}',
            f'\nPrimary POS {i}: {analysis.getPos()}'
            f'\nPrimary POS (Short Form) {i}: {analysis.getPos().shortForm}'
            kelime=f'{str(analysis.getLemmas()[0])}'
            kelime= f'{str(analysis.getLemmas()[0])}'
            if kelime=="UNK":
                kelimeler+=kel+" "
            else:
                    kelimeler+=kelime+" "
            
           # a= f'{" ".join(pos)}'
    return kelimeler.rstrip()


def remove_single_character(text):
    cleantext=""
    for punctuation in string.punctuation:
        text = text.replace(punctuation, '')
    for word in text.replace("  ","").split(" "):
        if len(word.strip())>0:
            cleantext+=word+" "
    return cleantext.strip()


ft=None
np_embedding_matrix=None
df=None
modelAnn=None
modelFullAnn=None
modelLstmTanh=None
modelFullLstmTanh=None
modelBernouilli=None
modelFullBernouilli=None
modelRnn=None
modelFullRnn=None

def LoadModelBernouilli():
    f = open('model-Bernoulli.pickle', 'rb')
    model = pickle.load(f)
    f.close()
    return model

def LoadModeFulllBernouilli():
    f = open('model-Full-Bernoulli.pickle', 'rb')
    model = pickle.load(f)
    f.close()
    return model

def LoadModelRnn():
    model = load_model('model-rnn-relu-300.h5')
    return model

def LoadFullModelRnn():
    model = load_model('model-rnn-Full-relu-300.h5')
    return model

def LoadModelLstmTanh():
    model = load_model('model-LSTM-relu-300.h5')
    return model

def LoadFullModelLstmTanh():
    model = load_model('model-LSTM-Full-300.h5')
    return model

def LoadModelANN():
    model = load_model('model-ANN-500-Epoch-relu.h5')
    return model

def LoadFullModelANN():
    model = load_model('model-ANN-Full-500-Epoch-relu.h5')
    return model

def LoadModel():
    ft1 = fasttext.load_model(r"cc.tr.300.bin")
    #fasttext.util.reduce_model(ft1, 50)
    return ft1

def LoadWordEmbedding():
    np_embedding_matrix1=np.loadtxt("word_embedding_UniversiteY_300D_02052021.txt")
    return np_embedding_matrix1


def stringToEmbedding(Soru):
    selected_embedding_matrix = []
    sent_list=[]
    for word in Soru.split(' '):
        wv=ft.get_word_vector(word)
        sent_list.append(wv)
    selected_embedding_matrix.append(np.mean(sent_list,axis=0))
    selected_embedding_matrix=np.array(selected_embedding_matrix)
    return selected_embedding_matrix


def LoadQuestionAnswer():
    """
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=45.158.14.59;DATABASE=dbBS;UID=ysfugurlu1;PWD=Yusuf.1997;')
    # query db
    """
    sql = """
    SELECT *
    FROM Question
    """
     #df = pandas.io.sql.read_sql(sql, conn)
    df=pd.read_excel("soru-cevap-Guncel.xls")
    return df

def change_remove_double_space(text):
    text = text.replace('  ', ' ')
    return text


app = Flask(__name__)
CORS(app)

@app.route('/api/faqOklid', methods=['POST'])
@cross_origin()
def GetAnswerOklid():
    try:
        Soru=request.json['Soru']
        predict = [Soru]
        predict=[each.lower() for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[remove_StopWord(each) for each in predict]
        predict=[Change_Stem_JVM_Zemberek(each) for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[change_remove_double_space(each) for each in predict]
        selected_embedding_matrix=stringToEmbedding(Soru)
        cosine_value = 1- pairwise_distances(np_embedding_matrix, selected_embedding_matrix)
        df['similarity_bow']=cosine_value
        predict = [selected_embedding_matrix]
        df_simi = pd.DataFrame(df, columns=['Cevap','similarity_bow']) # taking similarity value of responses for the question we took
        #print(df_simi )
    
        df_simi_sort = df_simi.sort_values(by='similarity_bow', ascending=False) # sorting the values
        #print(df_simi_sort.head())
    
        threshold = 0.8 # considering the value of p=smiliarity to be greater than 0.2
        df_threshold = df_simi_sort[df_simi_sort['similarity_bow'] > threshold] 
        index_value = cosine_value.argmax() # returns the index number of highest value
        resp = {
            "Response":200,
            "Cevap":df['Cevap'].loc[index_value],
            "Soru":df['Soru'].loc[index_value]
            }
        return jsonify(resp)
    except Exception  as ex:
        resp = {
            "Response":404,
            "Cevap":ex
            }
        return jsonify(resp)

@app.route('/api/faqCosunusArray', methods=['POST'])
@cross_origin()
def GetAnswerCosunusArray():
    try:
        Soru=request.json['Soru']
        predict = [Soru]
        predict=[each.lower() for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[remove_StopWord(each) for each in predict]
        predict=[Change_Stem_JVM_Zemberek(each) for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[change_remove_double_space(each) for each in predict]
        selected_embedding_matrix=stringToEmbedding(Soru)
        cosine_value = 1- pairwise_distances(np_embedding_matrix, selected_embedding_matrix, metric = 'cosine' )
        df['similarity_bow']=cosine_value
        predict = [selected_embedding_matrix]
        df_simi = pd.DataFrame(df, columns=['ID',"Soru",'CevapID',"Cevap",'similarity_bow']) # taking similarity value of responses for the question we took
        #print(df_simi)
        df_simi_sort = df_simi.sort_values(by='similarity_bow', ascending=False) # sorting the values
        #print(df_simi_◘sort.head())
        threshold = 0.8 # considering the value of p=smiliarity to be greater than 0.2
        df_threshold = df_simi_sort[df_simi_sort['similarity_bow'] > threshold] 
        index_value = cosine_value.argmax() # returns the index number of highest value
        df_threshold['json'] = df_threshold.apply(lambda x: x.to_json(), axis=1)
        json1="["
        df_threshold1=df_threshold.head(10)
        x=len(df_threshold.head(10))  
        i=1
        for row in df_threshold1.itertuples(index = True):
            if x == i:
                 json1+=getattr(row, "json")+"\n"
            else:
                json1+=getattr(row, "json")+",\n"
            i=i+1
        
    
        json1+="]"
        return json1
    except Exception  as ex:
        resp = {
            "Response":404,
            "Cevap":ex
            }
        return jsonify(resp)

@app.route('/api/faq', methods=['POST'])
@cross_origin()
def GetAnswer():
    try:
        Soru=request.json['Soru']
        predict = [Soru]
        predict=[each.lower() for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[remove_StopWord(each) for each in predict]
        predict=[Change_Stem_JVM_Zemberek(each) for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[change_remove_double_space(each) for each in predict]
        selected_embedding_matrix=stringToEmbedding(Soru)
        cosine_value = 1- pairwise_distances(np_embedding_matrix, selected_embedding_matrix, metric = 'cosine' )
        df['similarity_bow']=cosine_value
        predict = [selected_embedding_matrix]
        df_simi = pd.DataFrame(df, columns=['Cevap','similarity_bow']) # taking similarity value of responses for the question we took
        #print(df_simi )
    
        df_simi_sort = df_simi.sort_values(by='similarity_bow', ascending=False) # sorting the values
        #print(df_simi_◘sort.head())
    
        threshold = 0.8 # considering the value of p=smiliarity to be greater than 0.2
        df_threshold = df_simi_sort[df_simi_sort['similarity_bow'] > threshold] 
        index_value = cosine_value.argmax() # returns the index number of highest value
        resp = {
            "Response":200,
            "Cevap":df['Cevap'].loc[index_value],
            "SoruID":str(df['ID'].loc[index_value]),
            "Soru":str(df['Soru'].loc[index_value])
            }
        return jsonify(resp)
    except Exception  as ex:
        resp = {
            "Response":404,
            "Cevap":ex
            }
        return jsonify(resp)

@app.route('/api/faq1', methods=['POST'])
@cross_origin()
def GetAnswerANN():
    try:
        Soru=request.json['Soru']
        predict = [Soru]
        predict=[each.lower() for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[remove_StopWord(each) for each in predict]
        predict=[Change_Stem_JVM_Zemberek(each) for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[change_remove_double_space(each) for each in predict]
        selected_embedding_matrix=stringToEmbedding(predict[0])
        x_predict_embedding = np.expand_dims(selected_embedding_matrix, axis=0)
        cevaps=np.argmax(modelAnn.predict(x_predict_embedding), axis=-1)
        cevap=cevaps[0][0]
        rslt_df = df.loc[df['NoronID'] == cevap]
        
        resp = {
            "Response":200,
            "Cevap":rslt_df.iloc[0,4],
            "Soru":rslt_df.iloc[0,2]
            }
        return jsonify(resp)
    except Exception  as ex:
        resp = {
            "Response":404,
            "Cevap":ex
            }
        return jsonify(resp)
    

@app.route('/api/faqLstmTanh', methods=['POST'])
@cross_origin()
def GetAnswerLstmTanh():
    try:
        Soru=request.json['Soru']
        predict = [Soru]
        predict=[each.lower() for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[remove_StopWord(each) for each in predict]
        predict=[Change_Stem_JVM_Zemberek(each) for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[change_remove_double_space(each) for each in predict]
        selected_embedding_matrix=stringToEmbedding(predict[0])
        x_predict_embedding = np.expand_dims(selected_embedding_matrix, axis=0)
        pred =modelLstmTanh.predict(x_predict_embedding)
        cevap=np.argmax(pred)

        rslt_df = df.loc[df['NoronID'] == cevap]
        
        resp = {
            "Response":200,
            "Cevap":rslt_df.iloc[0,4],
            "Soru":rslt_df.iloc[0,2]
            }
        return jsonify(resp)
    except Exception  as ex:
        resp = {
            "Response":404,
            "Cevap":ex
            }
        return resp
    
@app.route('/api/faqBernouilli', methods=['POST'])
@cross_origin()
def GetAnswerBernoulli():
    try:
        Soru=request.json['Soru']
        predict = [Soru]
        predict=[each.lower() for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[remove_StopWord(each) for each in predict]
        predict=[Change_Stem_JVM_Zemberek(each) for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[change_remove_double_space(each) for each in predict]
        selected_embedding_matrix=stringToEmbedding(predict[0])
       # x_predict_embedding = np.expand_dims(selected_embedding_matrix, axis=1)
        #pred =model.predict(x_predict_embedding)
        pred =modelBernouilli.predict(selected_embedding_matrix)
        cevap=pred[0]
        print(cevap)
        rslt_df = df.loc[df['NoronID'] == cevap]
        
        resp = {
            "Response":200,
            "Cevap":rslt_df.iloc[0,4],
            "Soru":rslt_df.iloc[0,2]
            }
        return jsonify(resp)
    except Exception  as ex:
        print(ex)
        resp = {
            "Response":404,
            "Cevap":ex
            }
        return jsonify(resp)
    
    
@app.route('/api/faqRnn', methods=['POST'])
@cross_origin()
def GetAnswerRnn():
    try:
        Soru=request.json['Soru']
        predict = [Soru]
        predict=[each.lower() for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[remove_StopWord(each) for each in predict]
        predict=[Change_Stem_JVM_Zemberek(each) for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[change_remove_double_space(each) for each in predict]
        selected_embedding_matrix=stringToEmbedding(predict[0])
        x_predict_embedding = np.expand_dims(selected_embedding_matrix, axis=0)
        cevaps=np.argmax(modelRnn.predict(x_predict_embedding), axis=-1)
        pred =modelRnn.predict(x_predict_embedding)
        cevap=np.argmax(pred)

        rslt_df = df.loc[df['NoronID'] == cevap]
        
        resp = {
            "Response":200,
            "Cevap":rslt_df.iloc[0,4],
            "Soru":rslt_df.iloc[0,2]
            }
        return jsonify(resp)
    except Exception  as ex:
        print(ex)
        resp = {
            "Response":404,
            "Cevap":ex
            }
        return jsonify(resp)
    
@app.route('/api/faqSelect', methods=['POST'])
@cross_origin()
def GetAnswerMultiple():
    try:
        Soru=request.json['Soru']
        predict = [Soru]
        predict=[each.lower() for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[remove_StopWord(each) for each in predict]
        predict=[Change_Stem_JVM_Zemberek(each) for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[change_remove_double_space(each) for each in predict]
        selected_embedding_matrix=stringToEmbedding(predict[0])
        x_predict_embedding = np.expand_dims(selected_embedding_matrix, axis=0)
        cevaps=np.argmax(modelRnn.predict(x_predict_embedding), axis=-1)
        pred =modelRnn.predict(x_predict_embedding)
        cevap=np.argmax(pred)
        rslt_rnn= df.loc[df['NoronID'] == cevap]
        
        pred =modelBernouilli.predict(selected_embedding_matrix)
        cevap=pred[0]
        rslt_bernouilli = df.loc[df['NoronID'] == cevap]
        
        x_predict_embedding = np.expand_dims(selected_embedding_matrix, axis=0)
        pred =modelLstmTanh.predict(x_predict_embedding)
        cevap=np.argmax(pred)

        rslt_Lstm = df.loc[df['NoronID'] == cevap]
        
        x_predict_embedding = np.expand_dims(selected_embedding_matrix, axis=0)
        cevaps=np.argmax(modelAnn.predict(x_predict_embedding), axis=-1)
        cevap=cevaps[0][0]
        rslt_ANN = df.loc[df['NoronID'] == cevap]
        
        resp = {
            "Response":200,
            "CevapRnnID":str(rslt_rnn.iloc[0,1]),
            "CevapRnnSoru":str(rslt_rnn.iloc[0,2]),
            "CevapBernouilliID":str(rslt_bernouilli.iloc[0,1]),
             "CevapBernouilliSoru":str(rslt_bernouilli.iloc[0,2]),
             "CevapLstmID":str(rslt_Lstm.iloc[0,1]),
             "CevapLstmSoru":str(rslt_Lstm.iloc[0,2]),
             "CevapANNID":str(rslt_ANN.iloc[0,1]),
              "CevapANNSoru":str(rslt_ANN.iloc[0,2])
            }
        return jsonify(resp)
    except Exception  as ex:
        print(ex)
        resp = {
            "Response":404,
            "Cevap":ex
            }
        return jsonify(resp)

#Full Model

@app.route('/api/faqFullSelect', methods=['POST'])
@cross_origin()
def GetFullAnswerMultiple():
    try:
        Soru=request.json['Soru']
        predict = [Soru]
        predict=[each.lower() for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[remove_StopWord(each) for each in predict]
        predict=[Change_Stem_JVM_Zemberek(each) for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[change_remove_double_space(each) for each in predict]
        selected_embedding_matrix=stringToEmbedding(predict[0])
        x_predict_embedding = np.expand_dims(selected_embedding_matrix, axis=0)
        cevaps=np.argmax(modelRnn.predict(x_predict_embedding), axis=-1)
        pred =modelFullRnn.predict(x_predict_embedding)
        cevap=np.argmax(pred)
        rslt_rnn= df.loc[df['NoronID'] == cevap]
        
        pred =modelFullBernouilli.predict(selected_embedding_matrix)
        cevap=pred[0]
        rslt_bernouilli = df.loc[df['NoronID'] == cevap]
        
        x_predict_embedding = np.expand_dims(selected_embedding_matrix, axis=0)
        pred =modelFullLstmTanh.predict(x_predict_embedding)
        cevap=np.argmax(pred)

        rslt_Lstm = df.loc[df['NoronID'] == cevap]
        
        x_predict_embedding = np.expand_dims(selected_embedding_matrix, axis=0)
        cevaps=np.argmax(modelFullAnn.predict(x_predict_embedding), axis=-1)
        cevap=cevaps[0][0]
        rslt_ANN = df.loc[df['NoronID'] == cevap]
        
        resp = {
            "Response":200,
            "CevapRnnID":str(rslt_rnn.iloc[0,1]),
            "CevapRnnSoru":str(rslt_rnn.iloc[0,2]),
            "CevapBernouilliID":str(rslt_bernouilli.iloc[0,1]),
             "CevapBernouilliSoru":str(rslt_bernouilli.iloc[0,2]),
             "CevapLstmID":str(rslt_Lstm.iloc[0,1]),
             "CevapLstmSoru":str(rslt_Lstm.iloc[0,2]),
             "CevapANNID":str(rslt_ANN.iloc[0,1]),
              "CevapANNSoru":str(rslt_ANN.iloc[0,2])
            }
        return jsonify(resp)
    except Exception  as ex:
        print(ex)
        resp = {
            "Response":404,
            "Cevap":ex
            }
        return jsonify(resp)
    
@app.route('/api/faqFullAnn', methods=['POST'])
@cross_origin()
def GetFullAnswerANN():
    try:
        Soru=request.json['Soru']
        print(Soru)
        predict = [Soru]
        predict=[each.lower() for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[remove_StopWord(each) for each in predict]
        predict=[Change_Stem_JVM_Zemberek(each) for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[change_remove_double_space(each) for each in predict]
        selected_embedding_matrix=stringToEmbedding(predict[0])
        print(selected_embedding_matrix)
        x_predict_embedding = np.expand_dims(selected_embedding_matrix, axis=0)
        print("12")
        cevaps=np.argmax(modelFullAnn.predict(x_predict_embedding), axis=-1)
        print("1")
        cevap=cevaps[0][0]
        print(cevap)
        rslt_df = df.loc[df['NoronID'] == cevap]
        
        resp = {
            "Response":200,
            "Cevap":rslt_df.iloc[0,4],
            "Soru":rslt_df.iloc[0,2]
            }
        return jsonify(resp)
    except Exception  as ex:
        resp = {
            "Response":404,
            "Cevap":ex
            }
        return jsonify(resp)
    

@app.route('/api/faqFullLstmTanh', methods=['POST'])
@cross_origin()
def GetFullAnswerLstmTanh():
    try:
        Soru=request.json['Soru']
        predict = [Soru]
        predict=[each.lower() for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[remove_StopWord(each) for each in predict]
        predict=[Change_Stem_JVM_Zemberek(each) for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[change_remove_double_space(each) for each in predict]
        selected_embedding_matrix=stringToEmbedding(predict[0])
        x_predict_embedding = np.expand_dims(selected_embedding_matrix, axis=0)
        pred =modelFullLstmTanh.predict(x_predict_embedding)
        cevap=np.argmax(pred)

        rslt_df = df.loc[df['NoronID'] == cevap]
        
        resp = {
            "Response":200,
            "Cevap":rslt_df.iloc[0,4],
            "Soru":rslt_df.iloc[0,2]
            }
        return jsonify(resp)
    except Exception  as ex:
        resp = {
            "Response":404,
            "Cevap":ex
            }
        return jsonify(resp)
    
@app.route('/api/faqFullBernouilli', methods=['POST'])
@cross_origin()
def GetFullAnswerBernoulli():
    try:
        Soru=request.json['Soru']
        predict = [Soru]
        predict=[each.lower() for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[remove_StopWord(each) for each in predict]
        predict=[Change_Stem_JVM_Zemberek(each) for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[change_remove_double_space(each) for each in predict]
        selected_embedding_matrix=stringToEmbedding(predict[0])
       # x_predict_embedding = np.expand_dims(selected_embedding_matrix, axis=1)
        #pred =model.predict(x_predict_embedding)
        pred =modelFullBernouilli.predict(selected_embedding_matrix)
        cevap=pred[0]
        print(cevap)
        rslt_df = df.loc[df['NoronID'] == cevap]
        
        resp = {
            "Response":200,
            "Cevap":rslt_df.iloc[0,4],
            "Soru":rslt_df.iloc[0,2]
            }
        return jsonify(resp)
    except Exception  as ex:
        print(ex)
        resp = {
            "Response":404,
            "Cevap":ex
            }
        return jsonify(resp)
    
    
@app.route('/api/faqFullRnn', methods=['POST'])
@cross_origin()
def GetFullAnswerRnn():
    try:
        Soru=request.json['Soru']
        predict = [Soru]
        predict=[each.lower() for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[remove_StopWord(each) for each in predict]
        predict=[Change_Stem_JVM_Zemberek(each) for each in predict]
        predict=[remove_punctuations(each) for each in predict]
        predict=[change_remove_double_space(each) for each in predict]
        selected_embedding_matrix=stringToEmbedding(predict[0])
        x_predict_embedding = np.expand_dims(selected_embedding_matrix, axis=0)
        cevaps=np.argmax(modelFullRnn.predict(x_predict_embedding), axis=-1)
        pred =modelRnn.predict(x_predict_embedding)
        cevap=np.argmax(pred)

        rslt_df = df.loc[df['NoronID'] == cevap]
        
        resp = {
            "Response":200,
            "Cevap":rslt_df.iloc[0,4],
            "Soru":rslt_df.iloc[0,2]
            }
        return jsonify(resp)
    except Exception  as ex:
        print(ex)
        resp = {
            "Response":404,
            "Cevap":ex
            }
        return jsonify(resp)

# full model --

    
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'HTTP 404 Error': 'The content you looks for does not exist. Please check your request.'}), 404)
 
if __name__ == '__main__':
    np_embedding_matrix=LoadWordEmbedding()
    ft=LoadModel()
    df=LoadQuestionAnswer()
    modelAnn=LoadModelANN()
    modelLstmTanh=LoadModelLstmTanh()
    modelBernouilli=LoadModelBernouilli()
    modelRnn=LoadModelRnn()
    modelFullAnn=LoadFullModelANN()
    print(modelFullAnn)
    modelFullLstmTanh=LoadFullModelLstmTanh()
    modelFullBernouilli=LoadModeFulllBernouilli()
    modelFullRnn=LoadFullModelRnn()
    app.run(port=5001,host="localhost")  #!flask/bin/python


