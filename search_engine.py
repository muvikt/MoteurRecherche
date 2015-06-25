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
from doc import *
from data_base import *



		
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
		#print self.DB.word2Word_struct
		
	def build_DB(self):
		"""
			rempli seld.DB avec les documents de self.doc_files
		"""
		#TODO
		for doc in self.doc_list:
				self.DB.add_doc(doc)
		print self.DB.nb_doc_total
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
			#print 'avant', word
			word = self.stemmer.stem(word.decode('utf-8'))
			self.requete.append(word)
			#print 'apres', word
		#print "requete (parse) :"
		#for word in self.requete :
			#print word
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
			a=acc.pop()
			
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

		return self.fuse_lst_rec(title_lst,title_head_aux,first_lst,first_head_aux,body_lst,body_head_aux,acc)
		
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
		if word in self.DB.word2Word_struct:
		  print "YES"
		  print self.DB.word2Word_struct[word].body
		#word=self.stemmer.stem(word.decode('utf-8'))
		for doc_id in self.DB.word2Word_struct[word].title :
			#print "title" , str(doc_id.doc_id), str(self.DB.id2doc[doc_id.doc_id].doc_file)
			title_lst.append(doc_id.doc_id)
		for doc_id in self.DB.word2Word_struct[word].first :
			#print "first" , str(doc_id.doc_id), str(self.DB.id2doc[doc_id.doc_id].doc_file)
			first_lst.append(doc_id.doc_id)
		for doc_id in self.DB.word2Word_struct[word].body :
			#print "body" , str(doc_id.doc_id), str(self.DB.id2doc[doc_id.doc_id].doc_file)
			body_lst.append(doc_id.doc_id)
		if title_lst != [] :
			title_head = title_lst.pop()
		if first_lst != [] :
			first_head = first_lst.pop()
		if body_lst != [] :
			body_head = body_lst.pop()
		return self.fuse_lst_rec(title_lst,title_head,first_lst,first_head,body_lst,body_head,[])
		
	def search_bool_req(self):
		#print "requete (search) :"
		#for word in self.requete :
			###print word
		if self.requete == [] :
			return []
		#TODO ajouter une fonction pour trier les mots par ordre croissant de doc
		word0 = self.requete.pop()
		#print "word (search) :",word0
		lst = self.search_bool_word(word0)
		for word in self.requete :
			#print "word (search) :",word
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

	def tf_idf(self, doc_id):
		solution= 0
		for word in self.requete:
			total_noWords_in_doc=len(Doc.doc_file)
			word_in_doc=(len(Doc.word2pos_list_title[word])+len(Doc.word2pos_list_first[word]) +len(Doc.word2pos_list_body[word]))
			no_docs=DB.nb_doc_total
			no_docs_with_word=0

			solution = solution+ 
		




	def search_rank_req(self):
		#TODO
		return []





		
search=Search_engine('search', "DataBase.txt", "./samples/", False)
search.parse_requete('permet')
print search.search_bool_req()