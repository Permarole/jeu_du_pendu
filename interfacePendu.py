#-*-coding:UTF-8-*
from tkinter import *
import donnees
import fonctions



class Interface(Frame) :


	""" Fenêtre du jeu 
		Tous les widgets sont stockés comme attributs de cette fenêtre. """

	def __init__(self,fenetre,**kwargs):
		""" On crée une fenêtre ayant pour attributs les widgets nécessaire au jeu """

		self.mot_a_trouver = str()
		self.win = False # initialisation conditions début de partie
		self.nb_vie = int()
		self.nom_joueur = str()

		Frame.__init__(self, fenetre, width=1350, height = 600,**kwargs)
		self.pack(fill=BOTH)

		self.titre = Label(self, text = "LE\nPENDU")
		self.titre.pack(pady = 25)


		self.bouton_play = Button(self, text = "JOUER", fg = 'green', command = self.set_entry_joueur)
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

		self.bouton_rejouer = Button(self, text = "Rejouer", command = self.set_mot)
		self.bouton_changer_joueur = Button(self,text = "Changer Joueur", command = self.set_entry_joueur)

		
		self.bouton_quitter = Button(self, text= "Quitter", command = self.quit)
		self.bouton_quitter.pack(side = "right",padx = 10)

		self.frame_jeu = Frame(self, width=15, height = 25)

		self.nb_essai = Label(self, text = "")

		self.joueur = StringVar() # case de proposition 
		self.entry_joueur = Entry(self.frame_jeu, textvariable = self.joueur, width = 15, bg = 'white')

		self.message_nom = Label(self.frame_jeu,text = "Veuillez renseigner votre nom")

		self.lettre = StringVar() # case de proposition 
		self.proposition = Entry(self.frame_jeu, textvariable = self.lettre, width = 15, bg = 'white')
		
		self.bouton_envoyer = Button(self, text = "Envoyer", command = self.get_prop)

		self.label_victoire = Label(self)

		self.label_defaite = Label(self)

		self.liste_place = list() #  Liste des cases de lettres

		self.lettre = "0" # initialisation de la proposition


	def espace_lettre(self,nb_lettre):
		""" Creer les cases des lettres à trouver affiche l'espace proposition et le boutton envoyer """

		self.changement_frame()

		self.nb_vie = donnees.nb_essai # on reinitialise le nb de vie en cas de nouvelle partie

		self.nb_essai.pack(side="top")
		self.frame_jeu.pack(side = "top",pady = 10)
		
		self.nb_essai["text"] = "Vous disposez de {} vies".format(self.nb_vie) # Affiche le nombre de vie restante (valeur par default dans donnes.py)
		self.proposition.pack(side = 'top', pady = 10)
		self.proposition.bind("<Return>", self.get_prop)

		self.liste_place =list() # reset de la liste_place en cas de nouvelle partie

		for place in range(nb_lettre) :
			case = Label(self.frame_jeu, text ='_', padx = 15, bg = 'white')
			self.liste_place.append(case)
			self.liste_place[place].pack(side = 'left',pady = 40)
		self.bouton_quitter.pack(side = "top",pady = 10)
			
		

	def get_prop(self,*args):
		""" Appel la verif_prop de l' Entry proposition si proposition est un seule lettre
		ou si le mot complet est proposé
		supprime la proposition si elle ne rentre dans aucun des cas cités  """

		prop = self.proposition.get()
		if (len(prop) == 1 or len(prop) == len(self.mot_a_trouver) )and prop.isalpha() :
			self.verif_prop(prop)
			
		else :
			self.proposition.delete(0,"end")


	def vie_perdue(self):
		""" Actualise nb_vie """
		self.nb_vie -= 1
		self.nb_essai["text"] = "Vous disposez de {} vie(s)".format(self.nb_vie)


	def ajout_lettre(self,prop,places):
		"""Ajoute la lettre aux place designées"""
		if not places : # liste vide évaluée a False
			for i in range(len(self.mot_a_trouver)) :
				self.liste_place[i]["text"] = prop[i]
			
		else :
			for i in places :
				self.liste_place[i]["text"] = prop


	def verif_victoire(self,taille):
		""" Cette fonction appelle la fonction fin de partie si une des deux conditions d'arret de jeu est remplie"""
		win = True
		for i in range(taille) :
			if self.liste_place[i]["text"] == "_" :
				win = False
		if win :	
			self.fin_de_partie() 
		elif self.nb_vie == 0 :
			self.fin_de_partie(win = False)



	def verif_prop(self,proposition) :
		"""Cette fonction vérifie si la lettre est présente dans le mot.
		 Si tel est le cas elle incrémente une liste par la pace de cette lettre dans le mot
		 SI cette liste se retrouve non vide à la fin de la vérification on appelle la fonction ajout_lettre
		 Si la liste est vide c'est la lettre n'est pas présente dans le mot on retire alors une vie au joueur """
		liste_place = list()
		i = 0
		if len(proposition) == 1 :
			for lettre in self.mot_a_trouver:
				if lettre == proposition :
					liste_place.append(i)
				i +=1
			if len(liste_place) > 0 :  
				self.ajout_lettre(proposition, liste_place)
			else :
				self.vie_perdue()
		elif proposition == self.mot_a_trouver :
				self.ajout_lettre(proposition, liste_place)

		else :
			
			self.vie_perdue()
		self.verif_victoire(len(self.mot_a_trouver))
		self.proposition.delete(0,"end")
		
	def set_mot(self) :
		"""Cette fonction génére le mot a trouver a partir du fichier donnees.py"""

		self.mot_a_trouver = fonctions.gen_mot()
		taille = len(self.mot_a_trouver)
		self.espace_lettre(taille)

		self.label_victoire["text"] = "C'est gagné ! Le mot à trouvé etait {} !".format(self.mot_a_trouver)
		self.label_defaite["text"] = "Dommage vous n'avez plus de vie !\nLe mot à trouvé etait {} !".format(self.mot_a_trouver)
		
		

	def set_entry_joueur(self) :
		""" Cette fonction génére la frame permettant de renseigner le joueur""" 

		self.changement_frame()
		self.frame_jeu.pack(side = "top",pady = 10)
		
		self.message_nom.pack(side="top",pady = 15)
		self.entry_joueur.pack(side = "top", pady = 15)
		self.entry_joueur.bind("<Return>",self.command_return) # defini le comportement de la touche entrée dans l'espace entry

	def command_return(self,*args) :
		"""Cette fonction appelle get_nom pour creer le joueur ou incrémenter son nombre de partie
		Elle appelle ensuite la fonction set_mot pour passer à la suite du jeu"""

		self.entry_joueur.unbind("<Return>") # L'unbind evite de rappeler command_return si on rappuit sur entrée
		self.get_nom()
		self.message_nom.pack_forget()
		self.entry_joueur.pack_forget()
		self.set_mot()


	def get_nom(self):
		"""Cette fonction actualise/crée le joueur dans le fichier score""" 

		self.nom_joueur = self.entry_joueur.get()
		if not fonctions.verif_joueur(self.nom_joueur) :
			fonctions.creer_joueur(self.nom_joueur)
		


	def fin_de_partie(self, win = True ) :
		"""Cette affiche la frame de fin de partie avec possibilité de rejouer d'avoir acces au scores ou de changer d'utilisateur
		On sauvegarde aussi les stats du joueur sur la partie"""
		self.changement_frame()
		self.proposition.unbind("<Return>")
		fonctions.sauve_score(self.nom_joueur,self.nb_vie)
		self.frame_jeu.pack_forget()
		if win : 
			
			self.nb_essai["text"] = "Félicitation ! Vous avez trouvé le mot et marquez : {} point(s)".format(self.nb_vie)
			self.label_victoire.pack(pady = 10)
		else :
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

		fonctions.creer_scores() # on verifie l'existance du ficier score et on le creer s'il n'existe pas
		self.changement_frame() # nettoyage de la frame
		self.fenetre_scores.pack(side = "top")
		self.titre["text"] = "LES SCORES"
		dico_scores = fonctions.get_dico_scores()
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

