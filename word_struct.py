#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

from doc_struc import *
from collections import defaultdict

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
		if part == 'first':
			self.nb_doc_word_first += 1
			self.first.append(Doc_struct(doc_id,pos_lst))
		if part == 'body':
			self.nb_doc_word_body += 1
			self.body.append(Doc_struct(doc_id,pos_lst))