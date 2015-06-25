#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-


from collections import defaultdict

class Doc_struct:
	"""
		--Information sur un document precis, etant donne un mot et un champs--
		
		doc_id = identifiant du document traite

		pos_list = liste des positions entieres au sein d'un champs donne auxquelles apparait un mot donne dans le document courrant
	"""

	def __init__(self,doc_id,pos_list):
		self.doc_id = doc_id
		self.pos_list = pos_list