#-*-coding:UTF-8-*
from tkinter import *
import fonctions
import donnees
import interfacePendu



def main():
	"""Fonction creant la fenetre de base avec les commandes jouer regles score et quitter """
	fenetre = Tk() 
	fenetre.minsize(650,300)
	mainInterface = interfacePendu.Interface(fenetre)
	mainInterface.bouton_play.config(command = lambda : mainInterface.set_mot())
	mainInterface.bouton_regles.config(command = lambda : mainInterface.afficherRegles())
	mainInterface.bouton_score.config(command = lambda : mainInterface.afficherScores())


	
	mainInterface.mainloop()
	mainInterface.destroy()
	
		   	
	
main()
	

