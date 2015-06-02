#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-

import re


def parse_req(requete):
    req_list= re.findall( '\w+', requete)
    return req_list



print parse_req("l'arbre geant et chats.")
