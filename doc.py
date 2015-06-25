#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
 
from collections import defaultdict
from nltk.stem.snowball import FrenchStemmer




class Doc:
	"""
		--Representation d'un document--
		
		id : identifiant entier du document
		
		word2pos_list_X = dictionnaire qui associe a chaque mot, present dans le champs X, la liste des positions qu'occupent de mot dans ce même champs X au sein du document

		nb_word = nombre de mot dans le document
	"""
	global id_act
	id_act=0
	def __init__(self,doc_file):
		global id_act
		self.id = id_act
		id_act+=1
		self.doc_file = doc_file
		self.full_title = None
		self.word2pos_list_title = defaultdict()
		self.word2pos_list_first = defaultdict()
		self.word2pos_list_body = defaultdict()
		self.nb_word = 0
		self.read_doc(doc_file)

	def read_doc(self,docfile):
		"""
			lit le document dans le fichier doc_file et rempli les dictionnaires de listes de chaque champs avec les token du document. Compte egalement le nombre de mot
		"""
		stemmer=FrenchStemmer()
		flux=open(docfile)
		line=flux.readline()
		position=0
		title=True
		first=True
		while line != '':
		  liste=line.split()
		  if title==True and len(liste)>0: #remplir le dictionnaire du titre
		    self.full_title = line
		    title=False
		    for each in liste:
		      each=each.lower()
		      if '\'' in each:
			strings=self.splitAccent(each)
			strings[0]+='\''
			self.nb_word+=len(strings)
			for word in strings:
			  word= stemmer.stem(word.decode('iso-8859-1') )
			  if word not in self.word2pos_list_title:
			   self.word2pos_list_title[word]=[]
			  self.word2pos_list_title[word].append(position)
			  position+=1
		      else:
			self.nb_word+=1
			each=stemmer.stem(each.decode('iso-8859-1'))
			if each not in self.word2pos_list_title:
			   self.word2pos_list_title[each]=[]
			self.word2pos_list_title[each].append(position)
			position+=1
		    line=flux.readline()
		    liste=line.split()
		  if first==True and title==False and liste!=[]: #pour remplir le dictionnaire du premier paragraphe
		      first=False
		      for each in liste:
			each=each.lower()
			if '\'' in each:
			  strings=self.splitAccent(each)
			  strings[0]+='\''
			  self.nb_word+=len(strings)
			  for word in strings:
			    word= stemmer.stem(word.decode('iso-8859-1') )
			    if word not in self.word2pos_list_first:
			      self.word2pos_list_first[word]=[]
			    self.word2pos_list_first[word].append(position)
			    position+=1
			else:
			  self.nb_word+=1
			  each=stemmer.stem(each.decode('iso-8859-1'))
			  if each not in self.word2pos_list_first:
			    self.word2pos_list_first[each]=[]
			  self.word2pos_list_first[each].append(position)
			  position+=1
		      line=flux.readline()
		      liste=line.split()
		  if first==False and title==False and liste!=[]: #pour remplir le dictionnaire du corps de texte
		    for each in liste:
		      each=each.lower()
		      if '\'' in each:
			strings=self.splitAccent(each)
			strings[0]+='\''
			self.nb_word+=len(strings)
			for word in strings:
			  word= stemmer.stem(word.decode('iso-8859-1') )
			  if word not in self.word2pos_list_body:
			    self.word2pos_list_body[word]=[]
			  self.word2pos_list_body[word].append(position)
			  position+=1
		      else:
			self.nb_word+=1
			each=stemmer.stem(each.decode('iso-8859-1'))
			if each not in self.word2pos_list_body:
			  self.word2pos_list_body[each]=[]
			  self.word2pos_list_body[each].append(position)
			else:
			    self.word2pos_list_body[each].append(position)
			position+=1
		  line=flux.readline()
		#print self.word2pos_list_title
		#print self.word2pos_list_first
		#print self.word2pos_list_body
		
		
	def splitAccent(self,word):
		return word.split('\'')