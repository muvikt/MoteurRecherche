#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import sys
import re
from optparse import OptionParser
from collections import defaultdict
from math import *
# pour melange aleatoire des exemples
from random import shuffle
# pour dump et rechargement rapide de structures python (ici la matrice de poids)
import pickle
from copy import deepcopy
from nltk.stem.snowball import FrenchStemmer
#pour stemmatiser 


class Doc:
	"""
		--Représentation d'un document--
		
		id : identifiant entier du document
		
		word2pos_list_X = dictionnaire qui associe à chaque mot, présent dans le champs X, la liste des positions qu'occupent de mot dans ce même champs X au sein du document

		nb_word = nombre de mot dans le document
	"""
	global id_act
	id_act=0
	def __init__(self,doc_file):
		global id_act
		self.id = id_act
		id_act+=1
		self.word2pos_list_title = defaultdict()
		self.word2pos_list_first = defaultdict()
		self.word2pos_list_body = defaultdict()
		self.word2pos_list_para = defaultdict()
		self.nb_word = 0
		self.read_doc(doc_file)


	def read_doc(self,docfile):
		"""
			lit le document dans le fichier doc_file et rempli les dictionnaires de listes de chaque champs avec les token du document. Compte également le nombre de mot
		"""
		stemmer=FrenchStemmer()
		flux=open(docfile)
		line=flux.readline()
		position=0
		title=True
		first=True
		while line <> '':
		  liste=line.split()
		  if title==True and len(liste)>0: #remplir le dictionnaire du titre
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

class Doc_struct:
	"""
		--Information sur un document précis, étant donné un mot et un champs--
		
		doc_id = identifiant du document traité

		pos_list = liste des positions entières au sein d'un champs donné auxquelles apparait un mot donné dans le document courrant
	"""

	def __init__(self,doc_id,pos_list):
		self.doc_id = doc_id
		self.pos_list = pos_list

class Word_struct:
	"""
		--Information sur un mot de la base de donnée--

		nb_doc_word = nombre de document dans la base de donnée qui contiennent le mot en question

		X = liste de Doc_struct, un élément pour chaque document contenant le mot courrant dans son champ X

		nb_doc_word_X = nombre de document comportant le mot courrant dans leur champ X
	"""

	def __init__(self):
		self.title = []
		self.nb_doc_word_title = 0
		self.first = []
		self.nb_doc_word_first = 0
		self.body = []
		self.nb_doc_word_body = 0
		self.para = []
		self.nb_doc_word_para = 0

	def add(self,doc_id,part,pos_lst):
		if part == 'title':
			self.nb_doc_word_title += 1
			self.title.append(Doc_struct(doc_id,pos_lst))
			

class Data_Base:
	"""
		--Base de Donnée--

		word2Word_struct = dictionnaire qui associe à chaque mot l'ensemble des informations ne concernant (un Word_struct)
	
		id2nbword = dictionnaire qui associe à chaque identifiant de document le nombre de mot se trouvant dans ce document

		id2doc = dictionnaire qui associe à chaque identifiant de document le veritable document qui lui corespond. Ainsi, il est possible de renvoyer le document tout en ne traivaillant qu'avec l'identifiant

		nb_doc_total = nombre de document présent dans la base de donnée
	"""

	def __init__(self):
		self.word2Word_struct = defaultdict(Word_struct)
		self.id2nbword = defaultdict(int)
		self.id2doc = defaultdict(Doc)
		self.nb_doc_total = 0

	def add_doc(self,doc):
		self.nb_doc_total += 1
		self.id2doc[doc.id] = doc
		self.id2nb_word[doc.id] = doc.nb_word
		for word in doc.word2pos_list_title :
			self.word2Word_struct[word].add(doc.id,'title',doc.word2pos_list_title[word])
		for word in doc.word2pos_list_first :
			self.word2Word_struct[word].add(doc.id,'first',doc.word2pos_list_first[word])
		for word in doc.word2pos_list_body :
			self.word2Word_struct[word].add(doc.id,'body',doc.word2pos_list_body[word])
		for word in doc.word2pos_list_para :
			self.word2Word_struct[word].add(doc.id,'para',doc.word2pos_list_para[word])
		
class Search_engine:
	"""
		--Moteur de recherche--

		DB_file = fichier contenant la base de donnée
			si mode = build
				la base de donnée construite sera dumpée sur DB_file
			si mode = search
				la base de donnée sera récupéré depuis DB_file

		doc_files = liste de documents bruts à intégrer à la base de donnée

		DB = base de donnée de la classe Data_base
	"""

	def __init__(self, mode='build', DB_file=None, doc_files=None, trace=False):
		self.mode = mode
		self.DB_file = DB_file
		self.doc_list = []
		for doc_file in docfiles :
			doc = Doc(doc_file)
			doc_list.append(doc)
		self.trace = trace
                                self.requete= None
		self.DB = Data_Base()

		if mode == 'build' :
			#construction de la base de donnée, puis dump sur DB_file
			self.build_DB(doc_files,DB_file)
		elif mode == 'search' :
			#chargement de la base de donnée
			self.load_DB(DB_file)

	def build_DB(self):
		"""
			rempli seld.DB avec les documents de self.doc_files
		"""
		#TODO
		return

	def load_DB(self):
		"""
			charge le contenu du fichier self.DB_file dans self.DB
		"""
		stream = open(self.DB_file)
                                self.DB = pickle.load(stream)
                                stream.close()
		return

	def dump_DB(self):
		"""
			dump le contenu de self.DB dans le fichier self.DB_file
		"""
		stream = open(self.DB_file, 'w')
                                pickle.dump(self.DB, stream)
                                stream.close()
		return
	
	def parse_requete(self, requete):
                                """
                                                parse la requete introduite par l'utilisateur et produit une liste de tokens                                               
                                """
                        
                            req_list= re.findall( '\w+', requete)
                            self.requete= req_list
                            return 
