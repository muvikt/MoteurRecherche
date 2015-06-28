#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import sys
import re
import math
import operator
import webbrowser
from optparse import OptionParser
from collections import defaultdict
from collections import OrderedDict
from math import *
# pour melange aleatoire des exemples
from random import shuffle
# pour dump et rechargement rapide de structures python (ici la matrice de poids)
import cPickle
from copy import deepcopy
from nltk.stem.snowball import FrenchStemmer
#pour stemmatiser 
import os.path
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
		self.trace = trace
		self.requete= []
		self.DB = Data_Base()
		self.stemmer=FrenchStemmer()
		self.requeteFin=[]
		self.idDoc2tfIdf={}

		if mode == 'build' :
			#construction de la base de donnee, puis dump sur DB_file
			print 'Building Data Base...'
			self.build_DB(doc_files)
			print 'Building completed'
		elif mode == 'search' :
			#chargement de la base de donnee
			self.load_DB()
		self.word2nbOccDsDB={}
		
	def build_DB(self, doc_files):
		"""
			rempli seld.DB avec les documents de self.doc_files
		"""
		compteur=0
		doc_name=doc_files+'doc_'+str(compteur)+'.txt'
		while os.path.exists(doc_name):
		  doc=Doc(doc_name)
		  self.DB.add_doc(doc)
		  compteur+=1
		  doc_name=doc_files+'doc_'+str(compteur)+'.txt'
		print "Number of documents in the Data Base: ", self.DB.nb_doc_total
		#print self.DB.id2nbword
		self.dump_DB()

	def load_DB(self):
		"""
			charge le contenu du fichier self.DB_file dans self.DB
		"""
		print 'Loadind Data Base...'
		stream = open(self.DB_file)
		self.DB = cPickle.load(stream)
		stream.close()
		print "Number of documents in the Data Base: ", self.DB.nb_doc_total
		print 'Loading completed'
		return

	def dump_DB(self):
		"""
			dump le contenu de self.DB dans le fichier self.DB_file
		"""
		print 'Dumping Data Base...'
		p=cPickle.Pickler(open(self.DB_file, 'wb'))
		p.fast=True
		p.dump(self.DB)
		print 'Dumping completed'
		#stream.close()
		#return 
	
	def parse_requete(self, requete):
		"""
				parse la requete introduite par l'utilisateur et produit une liste de tokens
			"""
		req_list= re.findall( '\w+', requete)
		for word in req_list :
			word = self.stemmer.stem(word.decode('utf-8'))
			self.requete.append(word)
			self.requeteFin.append(word)
		
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
		else:
		  if m == title_head_aux :
			  if title_lst != [] :
				  title_head_aux = title_lst.pop()
			  else :
				  title_head_aux = -1
		  elif m == first_head_aux :
			  if first_lst != [] :
				  first_head_aux = first_lst.pop()
			  else :
				  first_head_aux = -1
		  elif m == body_head_aux :
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
		elif head1_aux > head2_aux :
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
		return self.merge_dif_rec(lst1,head1_aux,lst2,head2_aux,acc)
					
	def search_bool_word(self,word):
		title_lst = []
		title_head = -1
		first_lst = []
		first_head = -1
		body_lst = []
		body_head = -1
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
		result=self.fuse_lst_rec(title_lst,title_head,first_lst,first_head,body_lst,body_head,[])
		self.word2nbOccDsDB[word]=len(result)
		return result
		
	def search_bool_req(self):
		if self.requete == [] :
			return []
		word0 = self.requete.pop()
		lst = self.search_bool_word(word0)
		for word in self.requete :
			if lst == [] :
				return []
			lst_aux = self.search_bool_word(word)
		
			if lst_aux == [] :
				return []
			head_lst = lst.pop()
			head_lst_aux = lst_aux.pop()
			lst = self.merge_dif_rec(lst,head_lst,lst_aux,head_lst_aux,[])
		return lst

	def tf_idf(self, doc_id):#calcul le TF.IDF pour la requete pour chaque doc
		solution= 0
		doc=self.DB.id2doc[doc_id]
		for word in self.requeteFin:
			word_in_title=0
			word_in_first=0
			word_in_body=0
			total_noWords_in_doc = float(doc.nb_word)
			if word in doc.word2pos_list_title:
			  word_in_title=len(doc.word2pos_list_title[word])
			if word in doc.word2pos_list_first:
			  word_in_first=len(doc.word2pos_list_first[word])
			if word in doc.word2pos_list_body:
			  word_in_body=len(doc.word2pos_list_body[word])
			word_in_doc=float(word_in_body+word_in_first+word_in_title)
			no_docs=float(self.DB.nb_doc_total)
			no_docs_with_word=self.word2nbOccDsDB[word]
			solution +=float(word_in_doc/total_noWords_in_doc)*math.log1p(no_docs/no_docs_with_word)
		return solution
	      
	def tf_idf_score(self, listDoc_id):
	  for doc_id in listDoc_id:
	    self.idDoc2tfIdf[doc_id]=self.tf_idf(doc_id)
	
	def search_rank_req(self, requete, nbResMax):
		self.requete=[]
		self.requeteFin=[]
		self.parse_requete(requete)
		docsTrouves=self.search_bool_req()
		self.tf_idf_score(docsTrouves)
		self.idDoc2tfIdf=OrderedDict(sorted(self.idDoc2tfIdf.items(), key=lambda t: t[1], reverse=True))
		
		keys=self.idDoc2tfIdf.keys()[:nbResMax]
		if len(keys)<1:
		  print 'Nothing found \n'
		i=1
		for doc in keys:
		  print str(i)+'. '+self.id2docTitle(doc)+'File: '+self.id2fileName(doc)
		  i+=1

	def id2fileName(self, docId):
	  return str(self.DB.id2doc[docId].doc_file)
	
	def id2docTitle(self,docId):
	  return str(self.DB.id2doc[docId].full_title)
	
	def reset(self):
	  self.requete=[]
	  self.requeteFin=[]
	  self.idDoc2tfIdf={}



usage = """ Moteur de recherche dans les articles de Wikipedia

  %prog [options] (search|build) DataBase_folder DataBase_File 

"""

parser=OptionParser(usage=usage)
parser.add_option("--nb", dest="nb", default=10, help='Nb de resultats affichés. Default=10')
(opts,args) = parser.parse_args()

nb = int(opts.nb)

if len(args) < 3 or (args[0]!='build' and args[0]!='search'):
    print 'Errors in arguments'
    exit(usage)

mode=args[0]
DataBase_File=args[2]
DataBase_folder=args[1]

search=Search_engine(mode, DataBase_File, DataBase_folder, False)
requete=raw_input('Enter your request: ')
while requete!='q':
  search.search_rank_req(requete, nb)
  search.reset()
  requete=raw_input('Enter your new request: ')
  
''' tentative d'ovrire un document dans un editeur
  open=raw_input('Would you like to open a Doc File? (y or n): ')
  while open!='y' and open!='n':
     open=raw_input('Would you like to open a Doc File? (y or n): ')
     if open == 'y':
      number=raw_input('Enter a number of a document to open or \'-1\' for new searching: ')
      while int(number)!=-1:
	while int(number)>len(search.idDoc2tfIdf):
	  number=raw_input('Enter a valid number of a document to open or \'-1\' for new searching: ')
	docID=search.idDoc2tfIdf.keys()[int(number)]
	docPath=search.id2fileName(docID)
	webbrowser.open(docPath)
     else:    
'''
sys.exit()


'''Version precedante de MAIN
search.search_rank_req('banque centrale')
liste=search.search_bool_req()
print liste
print search.tf_idf_score(liste)
'''