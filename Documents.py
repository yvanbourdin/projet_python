#!/usr/bin/env python
# coding: utf-8

import os
import praw
import pandas as pd
from praw.models import MoreComments
import urllib
import xmltodict
import datetime as dt
import pickle

########### Implémentation des classes

# ### Implémentation de la classe Document
class Document():
    nb_docs = 0
    
    # constructor
    def __init__(self, date, title, author, text, url):
        self.date = date
        self.title = title
        self.author = author
        self.text = text
        self.url = url
        self.id = Document.nb_docs
        Document.nb_docs += 1
    
    # getters
    def get_author(self):
        return self.author

    def get_title(self):
        return self.title
    
    def get_date(self):
        return self.date
    
    def get_source(self):
        return self.source
        
    def get_text(self):
        return self.text
    
    def get_id(self):
        return self.id

    def __str__(self):
        return "Document " + self.getType() + " : " + self.title
    
    def __repr__(self):
        return self.title
    
    
# ### Implémentation de la classe Author
class Author():
    def __init__(self,name):
        self.name = name
        self.production = {}
        self.ndoc = 0

    def add(self, doc):
        self.production[self.ndoc] = doc
        self.ndoc += 1

    def __str__(self):
        return "Auteur : " + self.name + ", Nombre de docs : "+ str(self.ndoc)

    def __repr__(self):
        return self.name


# ### Implémentation de la classe Corpus
class Corpus():
    
    def __init__(self,name):
        self.name = name
        self.collection = {}
        self.authors = {}
        self.id2doc = {}
        self.id2aut = {}
        self.ndoc = 0
        self.naut = 0
            
    def add_doc(self, doc):
        
        self.collection[self.ndoc] = doc
        self.id2doc[self.ndoc] = doc.get_title()
        self.ndoc += 1
        aut_name = doc.get_author()
        aut = self.get_aut2id(aut_name)
        if aut is not None:
            self.authors[aut].add(doc)
        else:
            self.add_aut(aut_name,doc)
            
    def add_aut(self, aut_name,doc):
        
        aut_temp = Author(aut_name)
        aut_temp.add(doc)
        
        self.authors[self.naut] = aut_temp
        self.id2aut[self.naut] = aut_name
        
        self.naut += 1

    def get_aut2id(self, author_name):
        aut2id = {v: k for k, v in self.id2aut.items()}
        heidi = aut2id.get(author_name)
        return heidi

    def get_doc(self, i):
        return self.collection[i]
    
    def get_coll(self):
        return self.collection

    def __str__(self):
        return "Corpus: " + self.name + ", Number of docs: "+ str(self.ndoc)+ ", Number of authors: "+ str(self.naut)
    
    def __repr__(self):
        return self.name

    def sort_title(self,nreturn=None):
        if nreturn is None:
            nreturn = self.ndoc
        return [self.collection[k] for k, v in sorted(self.collection.items(), key=lambda item: item[1].get_title())][:(nreturn)]

    def sort_date(self,nreturn):
        if nreturn is None:
            nreturn = self.ndoc
        return [self.collection[k] for k, v in sorted(self.collection.items(), key=lambda item: item[1].get_date(), reverse=True)][:(nreturn)]
    
    def save(self,file):
            pickle.dump(self, open(file, "wb" ))
        


########### Création du corpus (Chaque élément = une instance de la classe Document)
# Remarques : 
# - Le contenu text est composé du titre et du texte.
# - La majorité des données text de Redit ne contiennent que le titre. 

## Permet de s'authentifier sur Reddit afin de pouvoir accéder aux publications
reddit = praw.Reddit(client_id='hrMEN_MKx85cjg', client_secret='uq8LFCmm3DCwco4TQvxWQ0A8K3s',
                     user_agent='Python_TD1')

# ### Via Reddit
def Importation_via_Reddit(reddit):
    corpus = Corpus("Corona")
    hot_posts = reddit.subreddit('Coronavirus').hot(limit=10)
    for post in hot_posts:
        datet = dt.datetime.fromtimestamp(post.created)
        txt = post.title + ". "+ post.selftext
        txt = txt.replace('\n', ' ')
        txt = txt.replace('\r', ' ')
        doc = Document(datet,
                       post.title,
                       post.author_fullname,
                       txt,
                       post.url)
        corpus.add_doc(doc)  
    #print("Création du corpus (via Reddit), %d documents et %d auteurs" % (corpus.ndoc,corpus.naut))
    return corpus


# Variable qui va recevoir les données du corpus
corpus = None

# Test
#corpus = Importation_via_Reddit(reddit)

## Permet d'accéder aux données des publications pour Arxiv
url = 'http://export.arxiv.org/api/query?search_query=all:covid&start=0&max_results=100'
data =  urllib.request.urlopen(url).read().decode()
docs = xmltodict.parse(data)['feed']['entry']

# ### Via Arxiv
def Importation_via_Arxiv(url, data, docs):
    corpus = Corpus("Corona")

    for i in docs[0:10]:
        datet = dt.datetime.strptime(i['published'], '%Y-%m-%dT%H:%M:%SZ')
        try:
            author = [aut['name'] for aut in i['author']][0]
        except:
            author = i['author']['name']
        txt = i['title']+ ". " + i['summary']
        txt = txt.replace('\n', ' ')
        txt = txt.replace('\r', ' ')
        doc = Document(datet,
                       i['title'],
                       author,
                       txt,
                       i['id']
                       )
        corpus.add_doc(doc)

    #print("Création du corpus (via Arxiv), %d documents et %d auteurs" % (corpus.ndoc,corpus.naut))
    return corpus

# Test
#corpus = Importation_via_Arxiv(url, data, docs)


# ## Liste de titres et d'ID
def création_liste_titres(corpus):
    liste_de_titres = []
    for i in range(corpus.ndoc):
        liste_de_titres.append(corpus.get_doc(i).get_title())
    return liste_de_titres

# Test
#liste_de_titres = création_liste_titres(corpus)


########### Fonctions
"""Fonction qui créer le tableau de correspondance (Title / Text) à partir du corpus. """
def création_tab_corr(corpus):
    liste_ID = []
    liste_de_titres = []
    liste_de_textes = []
    
    for i in range(corpus.ndoc):
        # Création de la liste des ID
        liste_ID.append(corpus.get_doc(i).get_id())
        # Création de la liste des titres 
        liste_de_titres.append(corpus.get_doc(i).get_title())
        # Création de la liste des textes 
        liste_de_textes.append(corpus.get_doc(i).get_text())

    # Création du dataframe de correspondance
    df_correspondance = pd.DataFrame({'ID' : liste_ID , 'Title' : liste_de_titres, 'Text': liste_de_textes})
    
    return df_correspondance

# Test
#df = création_tab_corr(corpus)
#df.head(5)


""" Compter_occurence_via_titre(titre_publi, corpus , mot)
Compte le nombre d'occurence d'un texte à partir d'une publication issu du corpus et du mot recherché
Input : - titre_publi 
        - corpus
        - mot
Output : - occurence
"""
def Compter_occurence_via_titre(titre_publi, corpus , mot):
    # Création de la table de correspondance
    data_corresp = création_tab_corr(corpus)
    
    # Récuperer le text de la publication à partir de son titre
    Text_publi = data_corresp.Text[data_corresp.Title == titre_publi]
    Text_publi = list(Text_publi)
    
    # Mettre tout en majuscule 
    Text_publi = Text_publi[0].upper() 
    mot = mot.upper() 
    occurence = Text_publi.count(mot)
    return occurence

# Test 
#Compter_occurence_via_titre("An Exploratory Characterization of Bugs in COVID-19 Software Projects", corpus,'covid')



