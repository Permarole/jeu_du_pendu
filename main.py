#-*-coding:UTF-8-*

import donnees
import interfacePendu
from tkinter import *

def main() :
	""" Fonction definissant le déroulement du jeu """

	fenetre = Tk()
	fenetre.title("Le Pendu")
	fenetre.minsize(650,350)
	mainInterface = interfacePendu.Interface(fenetre)
	mainInterface.mainloop()
	mainInterface.destroy()

if __name__ == '__main__' :
	main()
