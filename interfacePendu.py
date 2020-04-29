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
		self.nb_vie = donnees.nb_essai 

		Frame.__init__(self, fenetre, width=960, height = 540,**kwargs)
		self.pack(fill=BOTH)

		self.titre = Label(self, text = "LE\nPENDU")
		self.titre.pack(pady = 25)


		self.bouton_play = Button(self, text = "JOUER", fg = 'green')
		self.bouton_play.pack(side = "top",pady = 10) # Bouton jouer

		self.bouton_score = Button(self, text = "Scores", command = lambda : print('score joueur')) # reste a definir la fonction
		self.bouton_score.pack(side = "top",pady = 10) # Bouton pour accerder au scores

		self.bouton_regles = Button(self, text = "Règles") # reste a definir la fonction
		self.bouton_regles.pack(side = "left",padx = 10) # Bouton pour accerder au scores

		self.fenetre_regles = Frame(fenetre, width = 1000, height = 1000)
		self.regles = Label(self.fenetre_regles, text = donnees.regles )
		
		self.bouton_revenir = Button(self.fenetre_regles, text= "Revenir au jeu", command = self.afficher_jeu)

		self.bouton_rejouer = Button(self, text = "Rejouer", command = self.set_mot)

		
		self.bouton_quitter = Button(self, text= "Quitter", command = self.quit)
		self.bouton_quitter.pack(side = "right",padx = 10)

		self.frame_jeu = Frame(self, width=15, height = 25)

		self.nb_essai = Label(self, text = "")

		self.lettre = StringVar() # case de proposition 
		self.proposition = Entry(self.frame_jeu, textvariable = self.lettre, width = 15, bg = 'white')
		
		self.bouton_envoyer = Button(self, text = "Envoyer", command = self.get_prop)

		self.label_victoire = Label(self, text = "C'est gagné !")

		self.label_defaite = Label(self, text = "C'est perdu !")

		self.liste_place = list() #  Liste des cases de lettres

		self.lettre = "0" # initialisation de la proposition


	def espace_lettre(self,nb_lettre):
		""" Creer les cases des lettres à trouver affiche l'espace proposition et le boutton envoyer """

		self.changement_frame(quitter = False)

		self.nb_essai.pack(side="top")
		self.frame_jeu.pack(side = "top",pady = 10)
		
		self.nb_essai["text"] = "Vous disposez de {} vies".format(self.nb_vie) # Affiche le nombre de vie restante (valeur par default dans donnes.py)
		self.proposition.pack(side = 'top')
		self.bouton_envoyer.pack(side = 'bottom',pady = 20)	

		
		for place in range(nb_lettre) :
			case = Label(self.frame_jeu, text ='_', padx = 15, bg = 'white')
			self.liste_place.append(case)
			self.liste_place[place].pack(side = 'left')
			
		


	def get_prop(self):
		""" Renvoie la lettre de l' Entry proposition ssi proposition est un seule lettre
		renvoie 0 sinon """

		lettre = self.proposition.get()
		if len(lettre) == 1 and lettre.isalpha() :
			self.verif_lettre(lettre,self.mot_a_trouver)
			
		else :
			self.proposition.delete(0,"end")


	def vie_perdue(self):
		""" Actualise nb_vie """
		self.nb_vie -= 1
		self.nb_essai["text"] = "Vous disposez de {} vie(s)".format(self.nb_vie)


	def ajout_lettre(self,lettre,places):
		"""Ajoute la lettre aux place designées"""
		for i in places :
			self.liste_place[i]["text"] = lettre

	def verif_victoire(self,taille):
		""" Cette fonction renvoie True si le mot est complet"""
		win = True
		for i in range(taille) :
			if self.liste_place[i]["text"] == "_" :
				win = False
		if win :	
			self.victoire()

	def verif_defaite(self):
		"""Cette fonction verifie qu'il reste au moins une vie au joueur"""
		if self.nb_vie == 0 :
			self.defaite()

	def verif_lettre(self,proposition,mot) :
		"""Cette fonction vérifie si la lettre est présente dans le mot.
		 Si tel est le cas elle incrémente une liste par la pace de cette lettre dans le mot
		 SI cette liste se retrouve non vide à la fin de la vérification on appelle la fonction ajout_lettre
		 Si la liste est vide c'est la lettre n'est pas présente dans le mot on retire alors une vie au joueur """
		liste_place = list()
		i = 0
		for lettre in mot:
			if lettre == proposition :
				liste_place.append(i)
			i +=1
		if len(liste_place) > 0 :  
			self.ajout_lettre(proposition, liste_place)
		else :
			
			self.vie_perdue()
		self.verif_victoire(len(mot))
		self.verif_defaite()
		self.proposition.delete(0,"end")
		
	def reset_entry(self):
		""" Cette fonction reset self.proposition """
		self.proposition.delete(0,"end")

	def set_mot(self) :
		"""Cette fonction génére le mot a trouver a partir du fichier donnees.py"""

		self.mot_a_trouver = fonctions.gen_mot()
		self.espace_lettre(len(self.mot_a_trouver))

	def victoire(self) :
		self.frame_jeu.pack_forget()
		self.label_victoire.pack(pady = 10)
		self.bouton_score.pack(side='top',pady = 10)
		self.bouton_rejouer.pack(side='top',pady = 10)

	def defaite(self):
		self.frame_jeu.pack_forget()
		self.label_defaite.pack()

	def afficherRegles(self):
		"""Génére la frame des regles du pendu"""

		self.changement_frame()
		self.fenetre_regles.pack(side = "top")
		self.titre["text"] = "LES REGLES"
		self.regles.pack(side = "top")
		
		self.bouton_revenir.pack(side = 'top')



	# def afficherScores(self):
	# 	"""Génére la frame des scores du pendu"""
	# 	self.changement_frame()
	# 	self.fenetre_regles.pack(side = "top")
	# 	self.titre_regles.pack(side = "top")
	# 	self.regles.pack(side = "top")
		
	# 	self.bouton_revenir.pack(side = 'top')

	def changement_frame(self,quitter = True):
		""""Cette fonction 'nettoie' la frame pour un nouvel affichage """

		self.bouton_play.pack_forget()
		self.bouton_regles.pack_forget()
		self.bouton_score.pack_forget()
		if quitter :
			self.bouton_quitter.pack_forget()
		else :
			self.bouton_quitter.pack(side = "bottom")

		
	def afficher_jeu(self):
		"""Nettoie la frame courante et réaffiche la frame de jeu
		On attend en argument 1 ou 0
		1 : on nettoie la frame regles
		0 : on nettoie la frame scores """

		self.titre["text"] = "LE\nPENDU"

		# if int == 1 :
			
		self.fenetre_regles.pack_forget()

		# elif int == 0 :

		# 	self.fenetre_scors.pack_forget()
		self.bouton_play.pack(side='top',pady = 10)
		self.bouton_score.pack(side='top',pady = 10)
		self.bouton_regles.pack(side='left',pady = 10)	
		self.bouton_quitter.pack(side = "right",pady = 10)

	# def reset_espace_lettre(self,nb_lettre) :