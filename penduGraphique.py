#-*-coding:UTF-8-*
from tkinter import *
import fonctions
import donnees
import interfacePendu
import joueur



def main():
	"""Fonction creant la fenetre de base avec les commandes jouer regles score et quitter """
	fenetre = Tk() 
	fenetre.minsize(650,350)
	mainInterface = interfacePendu.Interface(fenetre)


	mainInterface.mainloop()
	mainInterface.destroy()
	
		   	
	
main()
	

