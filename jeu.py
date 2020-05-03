# -*-coding:UTF-8-*

import donnees
import random
import joueur
import pickle
import os


class Jeu:

    def __init__(self):
        """ Constructeur de la classe """

        self._nb_vie = donnees.nb_essai

        self._mot_a_trouver = str()

        self._mot_en_cours = list()  # Sera initilaiser par un nb de 0 = len(mot_a_trouver) sera modifier a chaque proposition juste
        # Il permettra de tester la victoire

        self._nom_joueur = str()

    def creer_scores(self):
        """ Crée le fichier scores (fichier de sauvegarde) si celui ci n'existe pas"""

        dico_scores = {}  # initialisation du dictionnaire
        if not os.path.exists("scores") or os.path.getsize("scores") == 0 :
            with open("scores",
                      "wb") as fichier :  # ouverture du fichier contenant les joueurs déjà connus ainsi que leurs scores
                new_entry = pickle.Pickler(fichier)
                new_entry.dump(dico_scores)  # sauvegarde de l'objet dico-score dans "scores"

    def gen_mot(self):
        """Cette fonction génére le mot a trouver a partir du fichier donnees.py et initialise l'etat de mot_en_cous"""

        self._mot_a_trouver = random.choice(
            donnees.list_mot)  # on definit notre mot à trouver au hasard dans la liste de mot
        self.set_mot_en_cours()

    def len_mot(self):
        """Cette fonction renvoie la taille du mot à trouver"""

        return len(self._mot_a_trouver)

    def set_mot_en_cours(self):
        """ Initialise le mot trouveé par le joueur """

        for i in range(len(self._mot_a_trouver)):
            self._mot_en_cours.append("_")

    def update_mot_en_cours(self, lettre, liste):
        """ Met a jour l'etat du mot trouvé par le joueur"""

        for i in liste:
            self._mot_en_cours[i] = lettre

    def get_mot(self):

        return self._mot_a_trouver

    def get_nb_vie(self):
        """ Cette focntion renvoie _nb_vie """

        return self._nb_vie

    def verif_joueur(self):
        """Fonction renvoyant True si le joueur est déjà présent dans le fichier scores"""

        with open("scores", "rb") as fichier_verif:
            depickler = pickle.Unpickler(fichier_verif)  # récupération des objets présent dans le fichier
            dico_scores = depickler.load()  # lecture des objets et recuperation des scores
            for nom in dico_scores.keys() :  # parcourt du dictionnaire pour verifier l'existance du joueur
                if nom == self._nom_joueur :  # le joueur existe si son nom est présent dans les scores
                    return True
        return False

    def creer_joueur(self):
        """"fonction creant un nouveau joueur dans la base de donnée "scores" avec un score de départ de 0"""

        dico_scores = self.get_dico_scores()

        with open("scores", "wb") as fichier_crea:
            new_entry = pickle.Pickler(fichier_crea)
            dico_scores[self._nom_joueur] = joueur.Joueur(self._nom_joueur)  # ajout du joueur à la bibliothéque
            new_entry.dump(dico_scores)  # sauvegarde de l'objet

    def set_nom_joueur(self, nom_joueur):
        """ Fonction initialant la variable _nom_joueur """

        self._nom_joueur = nom_joueur

    def creer_scores(self):
        """ Crée le fichier scores (fichier de sauvegarde) si celui ci n'existe pas"""
        dico_scores = {}  # initialisation du dictionnaire
        if not os.path.exists("scores") or os.path.getsize("scores") == 0 :
            with open("scores",
                      "wb") as fichier :  # ouverture du fichier contenant les joueurs déjà connus ainsi que leurs scores
                new_entry = pickle.Pickler(fichier)
                new_entry.dump(dico_scores)  # sauvegarde de l'objet dico-score dans "scores"

    def get_dico_scores(self):
        """ fonction qui renvois le dictionnaire des joueurs et scores présents dans le fichier "scores" """

        with open("scores", "rb") as fichier_scores :
            depickler = pickle.Unpickler(fichier_scores)  # récupération des objets présent dans le fichier
            dico_scores = depickler.load()  # lecture des objets et recuperation des scores
            return dico_scores

    # def get_score(self) :
    # 	"""Renvois le score total du joueur"""

    # 	with open("scores","rb") as fichier_scores :
    # 		recup_score = pickle.Unpickler(fichier_scores)
    # 		dico_score = recup_score.load()
    # 		return dico_score[self._nom_joueur].get_score()

    def sauve_score(self):
        """ Ajoute dans le fichier scores le score du joueur à son ancien score """

        dico_scores = self.get_dico_scores()
        with open("scores", "wb") as fichier_sauv :
            sauv_score = pickle.Pickler(fichier_sauv)
            # serialisation des données
            dico_scores[self._nom_joueur].inc_score(self._nb_vie)
            dico_scores[self._nom_joueur].inc_nb_partie()  # modification des données
            sauv_score.dump(dico_scores)  # réenregistrement des données

    def verif_victoire(self):
        """ Renvoie True si le mot est complet """

        if self._mot_en_cours == self._mot_a_trouver :
            return True
        else :
            return False

    def verif_prop(self, proposition):
        """ Renvoie une liste :
		- une liste vide si la propostion ne correspond pas au mot
		- une liste comprennant la/les place(s) de la la lettre dans le mot
		- une liste comprennant un entier superieur a la longueur du mot si la proposition est le mot a trouver"""

        liste_place = list()
        cpt = 0

        if len(proposition) == 1 :
            for lettre in self._mot_a_trouver :
                if lettre.upper() == proposition :  # Les propositions peuvent etre faites en majuscules c'est l'etat par defaut
                    liste_place.append(cpt)
                cpt += 1
            if liste_place :  # Evaluée à True si la liste n'est pas vide
                self.update_mot_en_cours(proposition, liste_place)

        elif proposition == self._mot_a_trouver.upper() :
            liste_place.append(self.len_mot())

        return liste_place

    def perdre_vie(self) :
        """ Décrémente self._nb_vie"""

        self._nb_vie -= 1
