#-*-coding:UTF-8-*

nb_essai = 8

list_mot = ["chaton","oiseau","carton","exact","probable","portique","franche","active","python","artifice"]

regles = "\
-Un mot composé d'au maximum 8 lettres sera choisi par l'ordinateur\n\n\
-Vous devez retrouver lettre par lettre ce mot\n\n\
-Pour faire une proposition, rentrez une lettre dans la case prévue et cliquez sur ENVOYER\n\n\
-Vous disposez de {} vies, chaque proposition erronée (lettre non présente dans le mot à trouver) vous fait perdre une vie\n\n\
-Si vous tombez à 0 vie la partie s'arrete c'est le 'GAME OVER'\n\n\
-Si vous trouver le mot les vies restantes constitueront votre score final\n\n\
----------------------------------Bonne chance !------------------------------\n\n".format(nb_essai)

			
