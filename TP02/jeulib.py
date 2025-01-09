from __future__ import division

import numpy as np

import joueurlib
import interfacelib


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
			# Plot the global statistics
			joueurlib.Minmax.plot_global_evolution()
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
			

# 1. Commencez par jouer une partie contre vous mˆeme pour v´erifier que le jeu marche bien chez vous.
# Pour cela il suffit de cr´eer une instance de la classe Jeu, et d’utiliser la m´ethode demarrer.

partie = Jeu()
partie.demarrer()


"""
# Tester la fonction liste_coups_valides
def test_liste_coups_valides():
    plateau = Plateau()
    coups_valides_noir = plateau.liste_coups_valides(1)
    coups_valides_blanc = plateau.liste_coups_valides(-1)
    print("Coups valides pour noir:", coups_valides_noir)
    print("Coups valides pour blanc:", coups_valides_blanc)

test_liste_coups_valides()
"""