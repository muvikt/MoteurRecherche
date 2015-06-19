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
import os.path
import os


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

class Doc_struct:
	"""
		--Information sur un document precis, etant donne un mot et un champs--
		
		doc_id = identifiant du document traite

		pos_list = liste des positions entieres au sein d'un champs donne auxquelles apparait un mot donne dans le document courrant
	"""

	def __init__(self,doc_id,pos_list):
		self.doc_id = doc_id
		self.pos_list = pos_list

class Word_struct:
	"""
		--Information sur un mot de la base de donnee--

		nb_doc_word = nombre de document dans la base de donnee qui contiennent le mot en question

		X = liste de Doc_struct, un element pour chaque document contenant le mot courrant dans son champ X

		nb_doc_word_X = nombre de document comportant le mot courrant dans leur champ X
	"""

	def __init__(self):
		self.title = []
		self.nb_doc_word_title = 0
		self.first = []
		self.nb_doc_word_first = 0
		self.body = []
		self.nb_doc_word_body = 0

	def add(self,doc_id,part,pos_lst):
		if part == 'title':
			self.nb_doc_word_title += 1
			self.title.append(Doc_struct(doc_id,pos_lst))
			

class Data_Base:
	"""
		--Base de Donnee--

		word2Word_struct = dictionnaire qui associe a chaque mot l'ensemble des informations ne concernant (un Word_struct)
	
		id2nbword = dictionnaire qui associe a chaque identifiant de document le nombre de mot se trouvant dans ce document

		id2doc = dictionnaire qui associe a chaque identifiant de document le veritable document qui lui corespond. Ainsi, il est possible de renvoyer le document tout en ne traivaillant qu'avec l'identifiant

		nb_doc_total = nombre de document present dans la base de donnee
	"""

	def __init__(self):
		self.word2Word_struct = defaultdict(Word_struct)
		self.id2nbword = defaultdict(int)
		self.id2doc = defaultdict(Doc)
		self.nb_doc_total = 0

	def add_doc(self,doc):
		self.nb_doc_total += 1
		self.id2doc[doc.id] = doc
		self.id2nbword[doc.id] = doc.nb_word
		for word in doc.word2pos_list_title :
			self.word2Word_struct[word].add(doc.id,'title',doc.word2pos_list_title[word])
		for word in doc.word2pos_list_first :
			self.word2Word_struct[word].add(doc.id,'first',doc.word2pos_list_first[word])
		for word in doc.word2pos_list_body :
			self.word2Word_struct[word].add(doc.id,'body',doc.word2pos_list_body[word])
		
class Search_engine:
	"""
		--Moteur de recherche--

		DB_file = fichier contenant la base de donnee
			si mode = build
				la base de donnee construite sera dumpee sur DB_file
			si mode = search
				la base de donnee sera recupere depuis DB_file

		doc_files = liste de documents bruts a integrer a la base de donnee

		DB = base de donnee de la classe Data_base
	"""

	def __init__(self, mode='build', DB_file=None, doc_files=None, trace=False):
		self.mode = mode
		self.DB_file = DB_file
		self.doc_list = []
		doc_to_read=[]
		for root, dirs, files in os.walk(doc_files, topdown=False):
			for file_name in files: 
				doc_to_read.append(os.path.join(root, file_name.encode('utf-8')))
		for doc_file in doc_to_read :
			doc = Doc(doc_file)
			self.doc_list.append(doc)
		self.trace = trace
		self.requete= []
		self.DB = Data_Base()
		self.stemmer=FrenchStemmer()

		if mode == 'build' :
			#construction de la base de donnee, puis dump sur DB_file
			print 'Built Data Base...'
			self.build_DB()
			#print self.DB
		elif mode == 'search' :
			#chargement de la base de donnee
			self.load_DB()

	def build_DB(self):
		"""
			rempli seld.DB avec les documents de self.doc_files
		"""
		#TODO
		for doc in self.doc_list:
				self.DB.add_doc(doc)
		#print self.DB.nb_doc_total
		#print self.DB.id2nbword
		self.dump_DB()

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
		print 'Dump data base....'
		stream = open(self.DB_file, 'w')
		pickle.dump(self.DB, stream)
		stream.close()
		#return 
	
	def parse_requete(self, requete):
		"""
				parse la requete introduite par l'utilisateur et produit une liste de tokens
			"""
		req_list= re.findall( '\w+', requete)
		for word in req_list :
			print 'avant', word
			word = self.stemmer.stem(word.decode('utf-8'))
			self.requete.append(word)
			print 'apres', word
		print "requete (parse) :"
		for word in self.requete :
			print word
		#return 
		
	def fuse_lst_rec(self,title_lst,title_head,first_lst,first_head,body_lst,body_head,acc):
		if acc == [] :
			acc.append(-1)
		m = max(title_head,first_head,body_head)
		title_head_aux = title_head
		first_head_aux = first_head
		body_head_aux = body_head		
		if m == -1 :
			acc.reverse()
			acc.pop()
			return acc
		if m == title_head_aux :
			if title_lst != [] :
				title_head_aux = title_lst.pop()
			else :
				title_head_aux = -1
		if m == first_head_aux :
			if first_lst != [] :
				first_head_aux = first_lst.pop()
			else :
				first_head_aux = -1
		if m == body_head_aux :
			if body_lst != [] :
				body_head_aux = body_lst.pop()
			else :
				body_head_aux = -1
		h = acc.pop()
		if h != m :
			acc.append(h)
			acc.append(m)
		else :
			acc.append(h)
		self.fuse_lst_rec(title_lst,title_head_aux,first_lst,first_head_aux,body_lst,body_head_aux,acc)
		
	def merge_dif_rec(self,lst1,head1,lst2,head2,acc):
		if acc == [] :
			acc.append(-1)
		head1_aux = head1
		head2_aux = head2
		if head1_aux == head2_aux :
			acc.append(head1_aux)
			if lst1 == [] or lst2 == [] :
				acc.reverse()
				acc.pop()
				return acc				
			else :
				head1_aux = lst1.pop()
				head2_aux = lst2.pop()
		if head1_aux > head2_aux :
			if lst1 == [] :
				acc.reverse()
				acc.pop()
				return acc
			else :
				head1_aux = lst1.pop()
		else :
			if lst2 == [] :
				acc.reverse()
				acc.pop()
				return acc
			else :
				head2_aux = lst2.pop()
		self.merge_dif_rec(lst1,head1_aux,lst2,head2_aux,acc)
					
	def search_bool_word(self,word):
		title_lst = []
		title_head = -1
		first_lst = []
		first_head = -1
		body_lst = []
		body_head = -1
		print "searching ", word
		#word=self.stemmer.stem(word.decode('utf-8'))
		for doc_id in self.DB.word2Word_struct[word].title :
			print "title" , str(doc_id)
			title_lst.append(doc_id.doc_id)
		for doc_id in self.DB.word2Word_struct[word].first :
			print "first" , str(doc_id)
			first_lst.append(doc_id.doc_id)
		for doc_id in self.DB.word2Word_struct[word].body :
			print "body" , str(doc_id)
			body_lst.append(doc_id.doc_id)
		if title_lst != [] :
			title_head = title_lst.pop()
		if first_lst != [] :
			first_head = first_lst.pop()
		if body_lst != [] :
			body_head = body_lst.pop()
		return self.fuse_lst_rec(title_lst,title_head,first_lst,first_head,body_lst,body_head,[])
		
	def search_bool_req(self):
		print "requete (search) :"
		for word in self.requete :
			print word
		if self.requete == [] :
			return []
		#TODO ajouter une fonction pour trier les mots par ordre croissant de doc
		word0 = self.requete.pop()
		print "word (search) :",word0
		lst = self.search_bool_word(word0)
		for word in self.requete :
			print "word (search) :",word
			# word=self.stemmer.stem(word.decode('utf-8'))
			if lst == [] :
				return []
			lst_aux = self.search_bool_word(word)
			if lst_aux == [] :
				return []
			head_lst = lst.pop()
			head_lst_aux = lst_aux.pop()
			lst = self.merge_dif_rec(lst,head_lst,lst_aux,head_lst_aux,[])
		#print lst
		return lst
		
	def search_rank_req(self):
		#TODO
		return []
		

		
search=Search_engine('build', "DataBase.txt", "./samples/", False)
search.parse_requete('irlandaise')
print search.search_bool_req()
