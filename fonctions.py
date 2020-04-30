#-*-coding:UTF-8-*
import pickle
import random
import os
import donnees
import joueur




def verif_joueur(nom_joueur) :

	"""fonction débutant le programme, elle permet de déterminer si le joueur est déjà présent dans la base de données
	si c'est un nouveau joueur il est créé dans la base avec un score de 0 envois True si le joueur existe dans la base"""
	with open("scores","rb") as fichier_verif :
		depickler = pickle.Unpickler(fichier_verif) # récupération des objets présent dans le fichier
		dico_scores = depickler.load() # lecture des objets et recuperation des scores
		for nom in dico_scores.keys() : # parcourt du dictionnaire pour verifier l'existance du joueur
			if nom == nom_joueur : # le joueur existe si son nom est présent dans les scores
				return True	
	return False


def get_dico_scores() :
	""" fonction qui renvois le dictionnaire des joueurs et scores présents dans le fichier "scores" """

	with open("scores","rb") as fichier_scores :

		depickler = pickle.Unpickler(fichier_scores) # récupération des objets présent dans le fichier
		dico_scores = depickler.load() # lecture des objets et recuperation des scores
		return dico_scores



def creer_joueur(nom_joueur) :
	""""fonction creant un nouveau joueur dans la base de donnée "scores" avec un score de départ de 0"""
	dico_scores = get_dico_scores()

	with open("scores","wb") as fichier_crea :
			new_entry = pickle.Pickler(fichier_crea)
			dico_scores[nom_joueur] = joueur.Joueur(nom_joueur) # ajout du joueur à la bibliothéque
			new_entry.dump(dico_scores) # sauvegarde de l'objet
			
			

def creer_scores():
	""" Crée le fichier scores (fichier de sauvegarde) si celui ci n'existe pas"""
	dico_scores = {} # initialisation du dictionnaire
	if not os.path.exists("scores") or os.path.getsize("scores") == 0 :
		with open("scores","wb") as fichier : # ouverture du fichier contenant les joueurs déjà connus ainsi que leurs scores
			new_entry = pickle.Pickler(fichier) 
			new_entry.dump(dico_scores) # sauvegarde de l'objet dico-score dans "scores"

def gen_mot():
	"""renvois un mot aléatoire du fichier donnees"""

	return random.choice(donnees.list_mot) # on definit notre mot à trouver au hasard dans la liste de mot



def get_score(nom_joueur) :
	"""Renvois le score total du joueur"""

	with open("scores","rb") as fichier_scores :
		recup_score = pickle.Unpickler(fichier_scores)
		dico_score = recup_score.load()
		return dico_score[nom_joueur].get_score()


def sauve_score(nom_joueur,vie_restante = 0) :
	""" Ajoute dans le fichier scores le score du joueur à son ancien score """

	dico_scores = get_dico_scores()
	with open("scores","wb") as fichier_sauv : 
		sauv_score = pickle.Pickler(fichier_sauv)		#serialisation des données
		dico_scores[nom_joueur].inc_score(vie_restante)
		dico_scores[nom_joueur].inc_nb_partie() # modification des données
		sauv_score.dump(dico_scores) # réenregistrement des données
		


























