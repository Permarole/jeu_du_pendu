#-*-coding:UTF-8-*

class Joueur :

	def __init__(self,nom) :

		self._nom = nom
		self._nb_partie = 0
		self._score = 0

	def afficher_joueur(self) :
		"""Fonction renvoyant un str contenant les informations du joueur"""

		return "{} : {} point(s) en {} partie(s) jouée(s)".format(self._nom, self._score, self._nb_partie)

	def inc_nb_partie(self) :
		"""Cette fonction incrémente le nombre de parties jouées """ 

		self._nb_partie += 1

	def inc_score(self,nb) :
		""" Cette fonction incrémente le score du joueur"""

		self._score += nb
