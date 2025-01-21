from __future__ import division

import numpy as np

import joueurlib
import interfacelib
import matplotlib.pyplot as plt
from joueurlib import Minmax, AlphaBeta, Random


class Jeu:
	
	def __init__(self, opts={}):
		
		self.noir = None
		self.blanc = None
		if "choix_joueurs" not in opts or opts["choix_joueurs"]:
			possibilites = [joueurlib.Humain] + joueurlib.IA.__subclasses__()
			if len(possibilites) == 1:
				print("Un seul type de joueur est actuellement implémenté : "+
					  str(possibilites[0])+".\nCe type sera choisi pour noir et blanc.")
				self.noir = possibilites[0](self, "noir", opts)
				self.blanc = possibilites[0](self, "blanc", opts)
			else:
				print("Quel type de joueur souhaitez vous sélectionner pour noir ?",
					  "Les possibilités sont :")
				for i in range(len(possibilites)):
					print(i+1," : "+str(possibilites[i]))
				choix = input("Tapez le nombre correspondant.\n")
				self.noir = possibilites[int(choix)-1](self, "noir", opts)
				print("Quel type de joueur souhaitez vous sélectionner pour blanc ?\nLes possibilités sont :")
				for i in range(len(possibilites)):
					print(i+1," : "+str(possibilites[i]))
				choix = input("Tapez le nombre correspondant.\n")
				self.blanc = possibilites[int(choix)-1](self, "blanc", opts)
		
		if "taille" in opts:
			taille = opts["taille"]
		else:
			taille = 8
		self.plateau = Plateau(taille)
		self.tour = 1
		self.precedent_passe = False
		self.partie_finie = False
		self.joueur_courant = self.noir
		
		if "interface"  not in opts or opts["interface"]:
			self.interface = True
			self.gui = interfacelib.Interface(self)
		else:
			self.interface = False

	def demarrer(self):
		if isinstance(self.joueur_courant, joueurlib.IA):
			self.gui.active_ia()
		else:
			self.gui.active_humain()
		self.gui.fenetre.mainloop()
		
	def jouer(self, coup, verbose=1):
		if self.tour == 1 and self.joueur_courant == None:
			if self.noir == None:
				raise ValueError("Vous devez initialiser le joueur noir.")
			self.joueur_courant = self.noir
		self.plateau.jouer(coup, self.joueur_courant.couleurval)
		if self.interface:
			self.gui.actualise_plateau()
		
		self.tour += 1
		if coup == []:
			if self.precedent_passe:
				self.partie_finie = True
			self.precedent_passe = True
		else:
			self.precedent_passe = False
		
		if self.partie_finie:
			if verbose==1:
				[v, s_noir, s_blanc] = self.score()
				if v == 0:
					m = "la partie est un nul, avec "+str(s_noir)+" points chacun."
				elif v == 1:
					m = "Victoire de noir, avec "+str(s_noir)+" points contre "+str(s_blanc)+'.'
				elif v == -1:
					m = "Victoire de blanc, avec "+str(s_blanc)+" points contre "+str(s_noir)+'.'
				print(m)
			if self.interface:
				self.gui.desactive_humain()
				self.gui.desactive_ia()
				self.gui.message_tour.set("Partie finie.\n"+m)
			self.joueur_courant = None
				
		else:
			if self.tour%2 == 1:
				self.joueur_courant = self.noir
				if self.interface:
					self.gui.message_tour.set("A noir de jouer")
			else:
				self.joueur_courant = self.blanc
				if self.interface:
					self.gui.message_tour.set("A blanc de jouer")

	def score(self):
		noir = 0
		blanc = 0
		for i in range(self.plateau.taille):
			for j in range(self.plateau.taille):
				if self.plateau.tableau_cases[i][j] == 1:
					noir += 1
				if self.plateau.tableau_cases[i][j] == -1:
					blanc += 1
		if noir > blanc:
			victoire_noir = 1
		elif noir == blanc:
			victoire_noir = 0
		else:
			victoire_noir = -1
		return [victoire_noir, noir, blanc]

class Plateau:
	
	def __init__(self, taille=8):
		self.tableau_cases = [[0 for j in range(taille)] for i in range(taille)]
		self.tableau_cases[taille//2-1][taille//2-1] = -1 #initialisation des 4 premiers pions
		self.tableau_cases[taille//2][taille//2-1] = 1
		self.tableau_cases[taille//2-1][taille//2] = 1
		self.tableau_cases[taille//2][taille//2] = -1
		self.taille = taille
		self.jouer
		
		
	def jouer(self, case, couleurval):
		if case == []: #[] signifie que le joueur passe
			return not self.existe_coup_valide(couleurval)
		
		if self.est_coup_valide(case, couleurval):
			self.tableau_cases[case[0]][case[1]] = couleurval #on joue sur la case
			directions = [[int(round(np.cos(k*np.pi/4))), int(round(np.sin(k*np.pi/4)))] for k in range(8)] #liste des 8 directions
			for d in directions:
				if self.capture_ligne(case, couleurval, d):
					new_case = [case[0] + d[0], case[1] + d[1]]
					while self.tableau_cases[new_case[0]][new_case[1]] == -couleurval:
						self.tableau_cases[new_case[0]][new_case[1]] = couleurval
						new_case = [new_case[0] + d[0], new_case[1] + d[1]]
			return True
		return False

	def est_coup_valide(self, case, couleurval):
		if self.tableau_cases[case[0]][case[1]] != 0:
			return False #la case n'est pas vide

		flag_capture = False
		directions = [[int(round(np.cos(k*np.pi/4))), int(round(np.sin(k*np.pi/4)))] for k in range(8)] #liste des 8 directions
		for d in directions:
			if self.capture_ligne(case, couleurval, d):
				return True
		
		return False #le coup ne capture pas
	def copie_apres_jouer(self, coup, couleurval):
			new_plateau = self.copie()
			new_plateau.jouer(coup, couleurval)
			return new_plateau
    
	def existe_coup_valide(self, couleurval):
		for i in range(self.taille):
			for j in range(self.taille):
				if self.est_coup_valide([i,j], couleurval):
					return True
		return False

	def liste_coups_valides(self, couleurval):
		'''Rend la liste des coups valides pour un joueur de couleur couleurval. Si aucun n'est possible, renvoie une liste contenant le coup passer.'''
		coups_valides = []
		for i in range(self.taille):
			for j in range(self.taille):
				if self.est_coup_valide([i,j], couleurval):
					coups_valides.append([i,j])
		if len(coups_valides) == 0:
			return [[]]

		else:
			return coups_valides

	def capture_ligne(self, case, couleurval, direction):
		'''capture_ligne(c, j, d) : retourne vrai lorsque le joueur avec la couleur j joue sur la case c et qu'une ligne adverse dans la direction d peut être capturée, faux sinon.'''
		new_case = [case[0] + direction[0], case[1] + direction[1]]
		entre_loop = False
		while (min(new_case[0], new_case[1]) >= 0 and max(new_case[0], new_case[1]) < self.taille
			 and self.tableau_cases[new_case[0]][new_case[1]] == -couleurval):
			new_case[0] += direction[0]
			new_case[1] += direction[1]
			entre_loop = True

		if min(new_case[0], new_case[1]) < 0 or max(new_case[0], new_case[1]) >= self.taille:
			return False
		if self.tableau_cases[new_case[0]][new_case[1]] != couleurval:
			return False
		return entre_loop
			

	def copie(self):
		copie = Plateau(self.taille)
		copie.tableau_cases = [[self.tableau_cases[i][j] for j in range(self.taille)] for i in range(self.taille)]
		return copie
			


"""
8. Tracez une courbe montrant comment les deux compteurs varient en fonction du choix de la
profondeur maximale.
"""
def test_profondeur():
    profondeurs = range(1, 5) 
    temps_execution_minmax = []
    nb_appels_jouer_minmax = []
    temps_execution_alphabeta = []
    nb_appels_jouer_alphabeta = []

    for profondeur in profondeurs:
        # Initialiser une partie
        game_minmax = Jeu(opts={"choix_joueurs": False})
        game_alphabeta = Jeu(opts={"choix_joueurs": False})

        # Partie entre Minmax et Random
        joueur_noir_minmax = Minmax(game_minmax, "noir") 
        joueur_blanc_minmax = Random(game_minmax, "blanc") 

        # Meme chose pour AlphaBeta
        joueur_noir_alphabeta = AlphaBeta(game_alphabeta, "noir")  
        joueur_blanc_alphabeta = Random(game_alphabeta, "blanc") 

        game_minmax.noir = joueur_noir_minmax
        game_minmax.blanc = joueur_blanc_minmax
        game_minmax.joueur_courant = joueur_noir_minmax 
        game_minmax.partie_finie = False

        # pour AlphaBeta
        game_alphabeta.noir = joueur_noir_alphabeta
        game_alphabeta.blanc = joueur_blanc_alphabeta
        game_alphabeta.joueur_courant = joueur_noir_alphabeta  
        game_alphabeta.partie_finie = False

        while not game_minmax.partie_finie:
            joueur = game_minmax.joueur_courant
            if isinstance(joueur, Minmax):
                coup = joueur.demande_coup(profondeur)
            else:
                coup = joueur.demande_coup()
            game_minmax.jouer(coup) 

        # pour AlphaBeta
        while not game_alphabeta.partie_finie:
            joueur = game_alphabeta.joueur_courant
            if isinstance(joueur, AlphaBeta):
                coup = joueur.demande_coup(profondeur) 
            else:
                coup = joueur.demande_coup()
            game_alphabeta.jouer(coup)

        # les compteurs Minmax
        temps_execution_minmax.append(joueur_noir_minmax.temps_exe)
        nb_appels_jouer_minmax.append(joueur_noir_minmax.nb_appels_jouer)

        # les compteurs AlphaBeta
        temps_execution_alphabeta.append(joueur_noir_alphabeta.temps_exe)
        nb_appels_jouer_alphabeta.append(joueur_noir_alphabeta.nb_appels_jouer)

        print(f"Profondeur {profondeur} (Minmax): Temps d'exécution = {joueur_noir_minmax.temps_exe:.2f} secondes, "
              f"Nombre d'appels à jouer = {joueur_noir_minmax.nb_appels_jouer}")
        print(f"Profondeur {profondeur} (AlphaBeta): Temps d'exécution = {joueur_noir_alphabeta.temps_exe:.2f} secondes, "
              f"Nombre d'appels à jouer = {joueur_noir_alphabeta.nb_appels_jouer}")

    # Les plotes 
    plt.figure(figsize=(12, 12))

    # Sous-graphe pour le temps d'exécution (Minmax)
    plt.subplot(2, 2, 1)
    plt.plot(profondeurs, temps_execution_minmax, marker='o', label='Temps d\'exécution (Minmax)')
    plt.xlabel('Profondeur')
    plt.ylabel('Temps d\'exécution (secondes)')
    plt.title('Variation du Temps d\'Exécution en Fonction de la Profondeur (Minmax)')
    plt.legend()
    plt.grid(True)

    # Sous-graphe pour le nombre d'appels à jouer (Minmax)
    plt.subplot(2, 2, 2)
    plt.plot(profondeurs, nb_appels_jouer_minmax, marker='o', color='orange', label='Nombre d\'appels à jouer (Minmax)')
    plt.xlabel('Profondeur')
    plt.ylabel('Nombre d\'appels à jouer')
    plt.title('Variation du Nombre d\'Appels à Jouer en Fonction de la Profondeur (Minmax)')
    plt.legend()
    plt.grid(True)

    # Sous-graphe pour le temps d'exécution (AlphaBeta)
    plt.subplot(2, 2, 3)
    plt.plot(profondeurs, temps_execution_alphabeta, marker='o', label='Temps d\'exécution (AlphaBeta)')
    plt.xlabel('Profondeur')
    plt.ylabel('Temps d\'exécution (secondes)')
    plt.title('Variation du Temps d\'Exécution en Fonction de la Profondeur (AlphaBeta)')
    plt.legend()
    plt.grid(True)

    # Sous-graphe pour le nombre d'appels à jouer (AlphaBeta)
    plt.subplot(2, 2, 4)
    plt.plot(profondeurs, nb_appels_jouer_alphabeta, marker='o', color='orange', label='Nombre d\'appels à jouer (AlphaBeta)')
    plt.xlabel('Profondeur')
    plt.ylabel('Nombre d\'appels à jouer')
    plt.title('Variation du Nombre d\'Appels à Jouer en Fonction de la Profondeur (AlphaBeta)')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


""" 
9. Ajoutez une fonction permettant de simuler n parties entre deux IA, et donnant le nombre de
victoires, score moyen ainsi que le temps moyen de calcul pour chaque camp.
"""
def simuler_parties(n, profondeur_noir=3, profondeur_blanc=3):
    victoires_noir = 0
    victoires_blanc = 0
    scores_noir = []
    scores_blanc = []
    temps_noir = []
    temps_blanc = []

    for i in range(n):
        game = Jeu(opts={"choix_joueurs": False})

        joueur_noir = Minmax(game, "noir")
        joueur_blanc = Random(game, "blanc")

        game.noir = joueur_noir
        game.blanc = joueur_blanc
        game.joueur_courant = joueur_noir
        game.partie_finie = False

        while not game.partie_finie:
            joueur = game.joueur_courant
            if isinstance(joueur, Minmax):
                coup = joueur.demande_coup(profondeur_noir if joueur.couleur == "noir" else profondeur_blanc)
            else:
                coup = joueur.demande_coup()
            game.jouer(coup)

        [victoire, score_noir, score_blanc] = game.score()
        scores_noir.append(score_noir)
        scores_blanc.append(score_blanc)
        temps_noir.append(joueur_noir.temps_exe)
        temps_blanc.append(joueur_blanc.temps_exe)

        if victoire == 1:
            victoires_noir += 1
        elif victoire == -1:
            victoires_blanc += 1

    return victoires_noir, victoires_blanc, scores_noir, scores_blanc, temps_noir, temps_blanc

def Question_9():
    total_victoires_noir = 0
    total_victoires_blanc = 0
    total_scores_noir = []
    total_scores_blanc = []
    total_temps_noir = []
    total_temps_blanc = []

    for profondeur in range(1, 4):
        print(f"Profondeur {profondeur}:")
        victoires_noir, victoires_blanc, scores_noir, scores_blanc, temps_noir, temps_blanc = simuler_parties(5, profondeur_noir=profondeur, profondeur_blanc=profondeur)
        
        print(f"Victoires Noir: {victoires_noir}, Victoires Blanc: {victoires_blanc}")
        print(f"Score moyen Noir: {np.mean(scores_noir)}, Score moyen Blanc: {np.mean(scores_blanc)}")
        print(f"Temps moyen de calcul Noir: {np.mean(temps_noir)} secondes, Temps moyen de calcul Blanc: {np.mean(temps_blanc)} secondes\n")
        
        total_victoires_noir += victoires_noir
        total_victoires_blanc += victoires_blanc
        total_scores_noir.extend(scores_noir)
        total_scores_blanc.extend(scores_blanc)
        total_temps_noir.extend(temps_noir)
        total_temps_blanc.extend(temps_blanc)

    print("\nRésultats finaux de toutes les parties jouées:")
    print(f"Total Victoires Noir: {total_victoires_noir}, Total Victoires Blanc: {total_victoires_blanc}")
    print(f"Score moyen Noir: {np.mean(total_scores_noir)}, Score moyen Blanc: {np.mean(total_scores_blanc)}")
    print(f"Temps moyen de calcul Noir: {np.mean(total_temps_noir)} secondes, Temps moyen de calcul Blanc: {np.mean(total_temps_blanc)} secondes")


"""
12. Comparez les performances de temps avec Minmax, en faisant varier la profondeur maximale
"""
def simuler_parties_alphabeta(n, profondeur_noir=3, profondeur_blanc=3, optimize=False):
    victoires_noir = 0
    victoires_blanc = 0
    scores_noir = []
    scores_blanc = []
    temps_noir = []
    temps_blanc = []

    for i in range(n):
        game = Jeu(opts={"choix_joueurs": False})

        joueur_noir = AlphaBeta(game, "noir")
        joueur_blanc = Random(game, "blanc")

        game.noir = joueur_noir
        game.blanc = joueur_blanc
        game.joueur_courant = joueur_noir
        game.partie_finie = False

        while not game.partie_finie:
            joueur = game.joueur_courant
            if isinstance(joueur, AlphaBeta):
                coup = joueur.demande_coup(profondeur_noir if joueur.couleur == "noir" else profondeur_blanc, optimize=optimize)
            else:
                coup = joueur.demande_coup()
            game.jouer(coup)

        [victoire, score_noir, score_blanc] = game.score()
        scores_noir.append(score_noir)
        scores_blanc.append(score_blanc)
        temps_noir.append(joueur_noir.temps_exe)
        temps_blanc.append(joueur_blanc.temps_exe)

        if victoire == 1:
            victoires_noir += 1
        elif victoire == -1:
            victoires_blanc += 1

    return victoires_noir, victoires_blanc, scores_noir, scores_blanc, temps_noir, temps_blanc

def comparer_alphabeta():
    total_victoires_noir = 0
    total_victoires_blanc = 0
    total_scores_noir = []
    total_scores_blanc = []
    total_temps_noir = []
    total_temps_blanc = []

    for profondeur in range(1, 3):
        print(f"Profondeur {profondeur} (AlphaBeta):")
        victoires_noir, victoires_blanc, scores_noir, scores_blanc, temps_noir, temps_blanc = simuler_parties_alphabeta(5, profondeur_noir=profondeur, profondeur_blanc=profondeur, optimize=False)
        
        print(f"Victoires Noir: {victoires_noir}, Victoires Blanc: {victoires_blanc}")
        print(f"Score moyen Noir: {np.mean(scores_noir)}, Score moyen Blanc: {np.mean(scores_blanc)}")
        print(f"Temps moyen de calcul Noir: {np.mean(temps_noir)} secondes, Temps moyen de calcul Blanc: {np.mean(temps_blanc)} secondes\n")
        
        total_victoires_noir += victoires_noir
        total_victoires_blanc += victoires_blanc
        total_scores_noir.extend(scores_noir)
        total_scores_blanc.extend(scores_blanc)
        total_temps_noir.extend(temps_noir)
        total_temps_blanc.extend(temps_blanc)

    print("\nRésultats finaux de toutes les parties jouées (AlphaBeta):")
    print(f"Total Victoires Noir: {total_victoires_noir}, Total Victoires Blanc: {total_victoires_blanc}")
    print(f"Score moyen Noir: {np.mean(total_scores_noir)}, Score moyen Blanc: {np.mean(total_scores_blanc)}")
    print(f"Temps moyen de calcul Noir: {np.mean(total_temps_noir)} secondes, Temps moyen de calcul Blanc: {np.mean(total_temps_blanc)} secondes")

    total_victoires_noir_opt = 0
    total_victoires_blanc_opt = 0
    total_scores_noir_opt = []
    total_scores_blanc_opt = []
    total_temps_noir_opt = []
    total_temps_blanc_opt = []

    for profondeur in range(1, 3):
        print(f"Profondeur {profondeur} (AlphaBeta Optimisé):")
        victoires_noir_opt, victoires_blanc_opt, scores_noir_opt, scores_blanc_opt, temps_noir_opt, temps_blanc_opt = simuler_parties_alphabeta(5, profondeur_noir=profondeur, profondeur_blanc=profondeur, optimize=True)
        
        print(f"Victoires Noir: {victoires_noir_opt}, Victoires Blanc: {victoires_blanc_opt}")
        print(f"Score moyen Noir: {np.mean(scores_noir_opt)}, Score moyen Blanc: {np.mean(scores_blanc_opt)}")
        print(f"Temps moyen de calcul Noir: {np.mean(temps_noir_opt)} secondes, Temps moyen de calcul Blanc: {np.mean(temps_blanc_opt)} secondes\n")
        
        total_victoires_noir_opt += victoires_noir_opt
        total_victoires_blanc_opt += victoires_blanc_opt
        total_scores_noir_opt.extend(scores_noir_opt)
        total_scores_blanc_opt.extend(scores_blanc_opt)
        total_temps_noir_opt.extend(temps_noir_opt)
        total_temps_blanc_opt.extend(temps_blanc_opt)

    print("\nRésultats finaux de toutes les parties jouées (AlphaBeta Optimisé):")
    print(f"Total Victoires Noir: {total_victoires_noir_opt}, Total Victoires Blanc: {total_victoires_blanc_opt}")
    print(f"Score moyen Noir: {np.mean(total_scores_noir_opt)}, Score moyen Blanc: {np.mean(total_scores_blanc_opt)}")
    print(f"Temps moyen de calcul Noir: {np.mean(total_temps_noir_opt)} secondes, Temps moyen de calcul Blanc: {np.mean(total_temps_blanc_opt)} secondes")

if __name__ == "__main__":
    #game = Jeu()
    #game.demarrer()
    comparer_alphabeta()





