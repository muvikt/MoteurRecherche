#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

from word_struct import *
from doc import *
from collections import defaultdict


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
		