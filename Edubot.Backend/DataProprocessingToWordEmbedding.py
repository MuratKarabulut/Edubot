# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 20:29:11 2021

@author: Pikacu
"""
import sys
import json
import requests

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
from jpype import JClass,isJVMStarted, JString,isJVMStarted, getDefaultJVMPath, shutdownJVM, startJVM, java


#snowball kök ayırma kütüphanesi
from snowballstemmer import TurkishStemmer
turkStem=TurkishStemmer()

def remove_punctuations(text):
    for punctuation in string.punctuation:
        text = text.replace(punctuation, ' ')
    return text

def change_remove_double_space(text):
    text = text.replace('  ', ' ')
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



ZEMBEREK_PATH = r'zemberek-full.jar'
if not isJVMStarted():
    print("2")
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


#df =pd.read_excel("deneme1.xls")

conn = pyodbc.connect('DRIVER={SQL Server};SERVER=45.158.14.59;DATABASE=dbBS;UID=ysfugurlu1;PWD=Yusuf.1997;')

# query db
sql = """

select s.ID,s.Soru,s.CevapID,c.Cevap,s.SinifID,si.SınıfAdi,c.NoronID,c.DislikeLike from Sorular as s
left join Cevaplar as c on s.CevapID=c.ID
left join Siniflar as si on si.ID=s.SinifID
"""
df = pandas.io.sql.read_sql(sql, conn)
"""
df=pd.read_sql_table("Question", con="Data Source=45.158.14.59;Initial Catalog=dbBS;Persist Security Info=True;User ID=ysfugurlu1;Password=Yusuf.1997;")
#print("Soru tokenize olmuş hali ",df["Soru"])
"""
print("1")
#df =pd.read_excel("soru-cevap-Guncel-V1.xls")
print("2")
df["TemizSoru"]=df['Soru']
print("3")
df['TemizSoru']=[each.lower() for each in df.TemizSoru]
df['TemizSoru']=[remove_punctuations(each) for each in df.TemizSoru]
df['TemizSoru']=[remove_StopWord(each) for each in df.TemizSoru]
df['TemizSoru']=[Change_Stem_JVM_Zemberek(each) for each in df.TemizSoru]
df['TemizSoru']=[remove_punctuations(each) for each in df.TemizSoru]
df['TemizSoru']=[change_remove_double_space(each) for each in df.TemizSoru]
df.to_excel('soru-cevap-Guncel.xls')
"""
#df=pd.read_excel("soru-cevap1-Chatbot-PC.xls")
print(df["TemizSoru"])

ft = fasttext.load_model(r"cc.tr.300.bin")
fasttext.util.reduce_model(ft, 300)
print("fasttext for başlandı")
lstr=""
embedding_matrix = []
for row in df['TemizSoru']:
    sent_list=[]
    for word in row.split(' '):
        vstr = ""
        wv=ft.get_word_vector(word)
        for vi in wv:
            vstr += " " + str(vi)
        sent_list.append(wv)
        lstr+=vstr+"\n"
    embedding_matrix.append(np.mean(sent_list,axis=0))
print("fasttext for bitti")
np_embedding_matrix=np.array(embedding_matrix)
print("fasttext yüklenmeye bitti")
np.savetxt('word_embedding_300D_02042020.txt', np_embedding_matrix)
"""