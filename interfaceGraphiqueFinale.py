#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import*
import Tkinter
import os
import sys
import Moteur.py

#fenetre principale
class MoteurRecherche(Tkinter.Tk):
		 
		  def __init__(self, parent):
					Tkinter.Tk.__init__(self, parent)
					self.parent=parent
					self.interface= None
					self.initialize()

		   #initialisation de la fenetre principale			   
		  def initialize(self):
					#cadre fenetre principale
					w, h = self.winfo_screenwidth(), self.winfo_screenheight()
					#self.geometry("%dx%d+0+0" % (w, h))
					self.configure(bg= "white")
					self.grid()
					self.window = Frame(self, bd=2, relief=GROOVE, background="white")
					
					# text_Entry
					self. textEntry= Tkinter.Text(self.window,width=84,bd=2, height=1, bg="white",
											  font=("Georgia", 14,),borderwidth=3,foreground='black',highlightcolor='orange')
					self.textEntry.focus()
					self.textEntry.grid( row= 1, column=0, sticky='N')
					
					#buttons( dans un Label)
					self.boutons =Tkinter.Label(self.window,background="white")
					self.boutons.grid(row =2, column=0, sticky='NS')
					self.boutonChercheBin = Tkinter.Button( self.boutons, text = "Rech_BIN", width=9,command=self.reqBIN)
					self.boutonChercheBin.grid(row =1, column= 1, sticky='NS')
					self.boutonChercheRank = Tkinter.Button( self.boutons, text = "Rech_RANK", width=9,command=self.reqRANK)
					self.boutonChercheRank.grid(row =1, column=2, sticky='NS')
					
					#logo_picture
					self.imgLogo = Tkinter.PhotoImage(file= "LogoWiki.gif")
					self.imageLogo = Tkinter.Label(self.window, image =self.imgLogo)
					self.imageLogo.grid(row=0, column=0,sticky=N+S+E+W)
					
					# affiche results
					self.frame = Frame(self.window, bd=2, relief=GROOVE, background="white")
					self.frame.grid_rowconfigure(0, weight=1)
					self.frame.grid_columnconfigure(0, weight=1)				   
					yscrollbar = Scrollbar(self.frame)
					yscrollbar.grid(row=0, column=1, sticky=N+S)				   
					self.text = Text(self.frame,background="white",font=("Georgia", 18,),  bd=0,yscrollcommand=yscrollbar.set)				   
					self.text.grid(row=0, column=0, sticky=N+S+E+W)
					yscrollbar.config(command=self.text.yview)
					self.frame.grid( row=3, column =0, sticky=N+S+E+W)
					
   
					#hyperlinks 
					hyperlink = HyperlinkManager(self.text)

					
					#fonction qui ouvre le fichier
					def click():
						self.interface=Seconde(None)
						self.interface.title('Moteur_Recherche_DOC')
						self.interface.mainloop()
						
					for i in range(30):
							  self.text.insert(INSERT, "title of the document", hyperlink.add(click))
							  self.text.insert(INSERT, "\n\n")
					self.text.configure(state='disabled')

					#instance SE
					self.SE=("search", "dumpDB.txt")
					
					self.window.grid(row=0, column=0, sticky=N+S+E+W)
					

		  #recupere le texte introduit par l'utilisateur rech_BIN
		  def reqBIN(self):
					liste_requete=self.SE.parse_requete(self.textEntry.get('1.0', END+'-1c'))
					liste_reponse=self.SE.search_bool_req(liste_requete)
					for i in range(25):
							  title=self.SE.DB.id2doc[liste_reponse[i]].full_title
							  self.text.insert(INSERT, "title of the document", hyperlink.add(click))
							  self.text.insert(INSERT, "\n\n")
					self.text.configure(state='disabled')

		  #recupere le texte introduit par l'utilisateur rech_RANK					
		  def reqRANK(self):
					liste_requete=self.SE.parse_requete(self.textEntry.get('1.0', END+'-1c'))
					liste_reponse=self.SE.search_rank_req(liste_requete)
					
		  

#hyperlinkManager
class HyperlinkManager:

		  def __init__(self, text):
					self.text = text
					self.text.tag_config("hyper", foreground="blue", underline=1)
					self.text.tag_bind("hyper", "<Enter>", self._enter)
					self.text.tag_bind("hyper", "<Leave>", self._quitter)
					self.text.tag_bind("hyper", "<Button-1>", self._click)
					self.reset()

		  def reset(self):
					self.links = {}

		  def add(self, action):
					tag = "hyper-%d" % len(self.links)
					self.links[tag] = action
					return "hyper", tag
		  
		  def _enter(self, event):
					self.text.config(cursor="hand2")

		  def _quitter(self, event):
					self.text.config(cursor="")

		  def _click(self, event):
					for tag in self.text.tag_names(CURRENT):
							  if tag[:6] == "hyper-":
										self.links[tag]()
										return

					
class Seconde(Tkinter.Tk):
		  
		  def __init__(self, parent):
					Tkinter.Tk.__init__(self, parent)
					self.parent = parent
					self.initialize()



		  def initialize(self):
					self.grid()
					self.frame=Tkinter.Frame(self, width=600, height=700, bg='red')
					self.frame.grid(row=0,column=0,sticky='E')
					yscrollbar = Scrollbar(self.frame)
					yscrollbar.grid(row=0, column=1, sticky=N+S)
					self.textPrint= Tkinter.Text(self.frame, height=43,bd=2, bg="white",font=("Georgia", 14,),
											   borderwidth=3,foreground='black',highlightcolor='orange', yscrollcommand=yscrollbar.set)
					self.textPrint.focus()
					self.textPrint.insert(INSERT, self.lireFichierText(title=self.SE.DB.id2doc[liste_reponse[i]].doc_file))
					self.textPrint.configure(state='disabled')
					self.textPrint.grid(row=0, column=0,sticky=N+S+E+W)
					yscrollbar.config(command=self.textPrint.yview)

				   
		  def lireFichierText(self,fichier):
					f=open(fichier,'r')
					lines=f.readlines()
			prnt=""
			for line in lines:
			  line=line.decode('utf-8')
			  prnt=prnt+line+'\n'
					return prnt


if __name__ == "__main__":
		  app= MoteurRecherche(None)
		  app.title('Moteur_Recherche')
		  app.mainloop()

