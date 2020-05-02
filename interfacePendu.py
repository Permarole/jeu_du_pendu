#-*-coding:UTF-8-*
from tkinter import *
import donnees
import jeu



class Interface(Frame) :


	""" Fenêtre du jeu 
		Tous les widgets sont stockés comme attributs de cette fenêtre. """

	def __init__(self,fenetre,**kwargs):
		""" On crée une fenêtre ayant pour attributs les widgets nécessaire au jeu """

		self.jeu = jeu.Jeu()
		self.liste_case = list() #  Liste des cases de lettres

		Frame.__init__(self, fenetre, width=1350, height = 600,**kwargs)
		self.pack(fill=BOTH)

		self.titre = Label(self, text = "LE\nPENDU")
		self.titre.pack(pady = 25)


		self.bouton_play = Button(self, text = "JOUER", fg = 'green', command = self.play)
		self.bouton_play.pack(side = "top",pady = 10) # Bouton jouer

		self.bouton_scores = Button(self, text = "Scores", command = self.afficher_scores) # reste a definir la fonction
		self.bouton_scores.pack(side = "top",pady = 10) # Bouton pour accerder au scores

		self.fenetre_scores = Frame(self, width =  650, height = 350)

		self.bouton_regles = Button(self, text = "Règles", command = self.afficher_regles) # reste a definir la fonction
		self.bouton_regles.pack(side = "left",padx = 10) # Bouton pour accerder au scores

		self.fenetre_regles = Frame(self, width = 650, height = 350)
		self.regles = Label(self.fenetre_regles, text = donnees.regles )
		
		self.bouton_revenir_regles = Button(self.fenetre_regles, text= "Revenir au jeu", command = self.afficher_jeu)
		self.bouton_revenir_scores = Button(self.fenetre_scores, text= "Revenir au jeu", command = self.afficher_jeu)

		self.bouton_rejouer = Button(self, text = "Rejouer", command = self.play)
		self.bouton_changer_joueur = Button(self,text = "Changer Joueur", command = self.set_entry_joueur)

		
		self.bouton_quitter = Button(self, text= "Quitter", command = self.quit)
		self.bouton_quitter.pack(side = "right",padx = 10)

		self.frame_jeu = Frame(self, width=15, height = 25)

		self.essais_restant = Label(self, text = "")

		self.joueur = StringVar() # case de proposition 
		self.entry_joueur = Entry(self.frame_jeu, textvariable = self.joueur, width = 15, bg = 'white')

		self.message_nom = Label(self.frame_jeu,text = "Veuillez renseigner votre nom")

		self.lettre = StringVar() # case de proposition 
		self.proposition = Entry(self.frame_jeu, textvariable = self.lettre, width = 15, bg = 'white')
		
		self.bouton_envoyer = Button(self, text = "Envoyer", command = self.get_prop)

		self.label_victoire = Label(self)

		self.label_defaite = Label(self)


	def play(self) :
		""" Fonction gérant l'initialisation du jeu """

		self.jeu.creer_scores() # On crée le fichier scores s'il n'existe pas
		self.jeu.gen_mot() # Genere le mot à trouver
		self.set_entry_joueur() # Genere la frame permettant de renseigner le nom du joueur
		if not self.jeu.verif_joueur() : # Verifie si le joueur existe
			self.jeu.creer_joueur() # Créé le jeu dans le cas ou il n'existe pas

		# self.set_espace_lettre() Cette fonction est appelé dans command return elle lance la seconde partie du programme à savoir le jeu a proprement parler
		# Dans set_epsace_lettre la touche return est bind sur la fonction process_lettre
		# Cette fonction récupère l'entrée faite par le joueur puis la teste 
		# Suivant la prop on ajoute une lettre ou le joueur perd un vie
		# On teste alors les conditions d'arret du jeu et appelle fin_de_partie si une des conditions est remplie 
		

	def set_entry_joueur(self) :
		""" Cette fonction génére la frame permettant de renseigner le joueur""" 

		self.changement_frame()
		self.frame_jeu.pack(side = "top",pady = 10)
		self.message_nom.pack(side="top",pady = 15)
		self.entry_joueur.pack(side = "top", pady = 15)
		self.entry_joueur.focus_set()
		self.entry_joueur.bind("<Return>",self.command_return) # defini le comportement de la touche entrée dans l'espace entry

	def command_return(self,*args) :
		"""Cette fonction appelle get_nom pour creer le joueur ou incrémenter son nombre de partie
		Elle appelle ensuite la fonction set_mot pour passer à la suite du jeu"""

		self.entry_joueur.unbind("<Return>") # L'unbind evite de rappeler command_return si on rappuit sur entrée
		self.get_nom()
		self.message_nom.pack_forget()
		self.entry_joueur.pack_forget()
		self.set_espace_lettre()		


	def set_espace_lettre(self):
		""" Creer les cases des lettres à trouver et affiche l'espace proposition """

		self.changement_frame()
		self.essais_restant.pack(side="top")
		self.frame_jeu.pack(side = "top",pady = 10)
		self.update_vie()# Affiche le nombre de vie restante (valeur par default dans donnes.py)
		self.proposition.pack(side = 'top', pady = 10)
		self.proposition.focus_set()
		self.proposition.bind("<Return>", self.process_prop) # appel de get_prop en cas de <return>
		self.liste_case =list() # reset de la liste_case en cas de nouvelle partie
		for place in range(self.jeu.len_mot()) :
			case = Label(self.frame_jeu, text ='_', padx = 15, bg = 'white')
			self.liste_case.append(case)
			self.liste_case[place].pack(side = 'left',pady = 40)
		self.bouton_quitter.pack(side = "top",pady = 10)
			
		

	def get_prop(self):
		""" Appel la verif_prop de l' Entry proposition si proposition est un seule lettre
		ou si le mot complet est proposé
		supprime la proposition si elle ne rentre dans aucun des cas cités  """

		prop = self.proposition.get().upper()
		if (len(prop) == 1 or len(prop) == self.jeu.len_mot()) and prop.isalpha() :
			self.proposition.delete(0,"end")
			return prop, self.jeu.verif_prop(prop)		
		else :
			self.proposition.delete(0,"end")
			return False

	def process_prop(self,*args) :
		"""Cette fonction se charge de récuperer la proposition du joueur et de la traiter en conséquence"""

		tuple_prop_liste = self.get_prop()
		if tuple_prop_liste is not False :
			if not tuple_prop_liste[1] : # liste vide le joueur perd une vie
				self.jeu.perdre_vie() 
				self.update_vie()
			elif tuple_prop_liste[1][0] == self.jeu.len_mot() : # liste[0] == taille du mot : victoire
				self.fin_de_partie(True)
			else : # ajout de la lettre au mot
				self.ajout_lettre(tuple_prop_liste)

			if self.jeu.verif_victoire() : # verification de victoire ou defaite
				self.fin_de_partie(True)
			elif self.jeu.get_nb_vie() == 0 :
				self.fin_de_partie(False)



	def ajout_lettre(self,prop):
		"""Ajoute la lettre aux place designées"""
	
		for i in prop[1] : # prop est un tuple contenant la lettre proposée en indice 1 et une liste de place en indice 0  
			self.liste_case[i]["text"] = prop[0]


	def fin_de_partie(self, win) :
		"""Cette affiche la frame de fin de partie avec possibilité de rejouer d'avoir acces au scores ou de changer d'utilisateur
		On sauvegarde aussi les stats du joueur sur la partie"""
		self.changement_frame()
		self.proposition.unbind("<Return>")
		self.jeu.sauve_score()
		self.frame_jeu.pack_forget()
		if win : 
			self.label_victoire["text"] = "FÉLICITATIONS !\nLe mot était '{}'.\nVous marquez {} point(s) !".format(self.jeu.get_mot().upper(),self.jeu.get_nb_vie())
			self.label_victoire.pack(pady = 10)
		else :
			self.label_defaite["text"] = "DOMMAGE c'est perdu !\nLe mot était '{}'.\n".format(self.jeu.get_mot().upper(),self.jeu.get_nb_vie())
			self.label_defaite.pack()
		self.bouton_rejouer.pack(side='top',pady = 10)
		self.bouton_quitter.pack(side = "bottom",pady = 40)
		self.bouton_scores.pack(side='left',pady = 10,padx = 20)
		self.bouton_changer_joueur.pack(side = 'right',pady = 10,padx = 20)
		
		

	def afficher_regles(self):
		"""Génére la frame des regles du pendu"""

		self.changement_frame() # nettoyage de la frame
		self.fenetre_regles.pack(side = "top")
		self.titre["text"] = "LES REGLES"
		self.regles.pack(side = "top")
		
		self.bouton_revenir_regles.pack(side = 'top')


	def afficher_scores(self):
		"""Génére la frame des scores"""

		self.jeu.creer_scores() # on verifie l'existance du ficier score et on le creer s'il n'existe pas
		self.changement_frame() # nettoyage de la frame
		self.fenetre_scores.pack(side = "top")
		self.titre["text"] = "LES SCORES"
		dico_scores = self.jeu.get_dico_scores()
		if not dico_scores : # on verifie si le dictionnaire est vide dict vide évaluer à False en python 
			joueur_none = Label(self.fenetre_scores, text = "Aucun joueur enregistrer")
			joueur_none.pack(side = "top", pady = 50)
		else :
			for score_joueur in dico_scores.keys() : # creation d'un label par joueur
				score_joueur = dico_scores[score_joueur] 
				ligne = Label(self.fenetre_scores, text = score_joueur.afficher_joueur())
				ligne.pack(side = "top", pady = 15)

		self.bouton_revenir_scores.pack(side = 'top') # bouton permettant de revenir a l'écran titre


	def changement_frame(self):
		""""Cette fonction 'nettoie' la frame pour un nouvel affichage """

		for widget in self.fenetre_scores.winfo_children() :
			widget.pack_forget()

		for widget in self.fenetre_regles.winfo_children() :
			widget.pack_forget()

		for widget in self.frame_jeu.winfo_children() :
			widget.pack_forget()

		for widget in self.winfo_children() :
			if widget != self.titre :
				widget.pack_forget()

		
	def afficher_jeu(self):

		self.changement_frame()
		self.titre["text"] = "LE\nPENDU"			
		self.bouton_play.pack(side='top',pady = 10)
		self.bouton_scores.pack(side='top',pady = 10)
		self.bouton_regles.pack(side='left',pady = 10)	
		self.bouton_quitter.pack(side = "right",pady = 10)

	def get_nom(self):
		"""Cette fonction actualise/crée le joueur dans le fichier score""" 

		self.jeu.set_nom_joueur(self.entry_joueur.get()) 

	def update_vie(self):
		"""Actualise l'affiche de nombre de vie restante"""
		self.essais_restant["text"] = "Vous disposez de {} vies".format(self.jeu.get_nb_vie())