import interfacelib
import numpy as np
import time


class Joueur:
	def __init__(self, partie, couleur, opts={}):
		self.couleur = couleur
		self.couleurval = interfacelib.couleur_to_couleurval(couleur)
		self.jeu = partie
		self.opts = opts

	def demande_coup(self):
		pass


class Humain(Joueur):

	def demande_coup(self):
		pass		
  

class IA(Joueur):

	def __init__(self, partie, couleur, opts={}):
		super().__init__(partie,couleur,opts)
		self.temps_exe = 0
		self.nb_appels_jouer = 0
		


class Random(IA):
	
	def demande_coup(self):
		liste_coups_possible = self.jeu.plateau.liste_coups_valides(self.couleurval)
		return liste_coups_possible[np.random.randint(0, len(liste_coups_possible))]

class Minmax(IA):
	
	def fct_evaluation(self, plateau, couleurval):
		score = 0
		poids_stabilite = 10
		poids_mobilite = 5
		poids_coin = 20

		disques_stables = 0
		for i in range(plateau.taille):
			for j in range(plateau.taille):
				if plateau.tableau_cases[i][j] == couleurval:
					disques_stables += 1
		score += poids_stabilite * disques_stables

		mobilite = len(plateau.liste_coups_valides(couleurval))
		score += poids_mobilite * mobilite

		coins = [(0, 0), (0, plateau.taille - 1), (plateau.taille - 1, 0), (plateau.taille - 1, plateau.taille - 1)]
		controle_coins = 0
		for coin in coins:
			if plateau.tableau_cases[coin[0]][coin[1]] == couleurval:
				controle_coins += 1
		score += poids_coin * controle_coins

		return score

	def minmax(self, couleurval, profondeur = 3, maximiser=True):
		plateau = self.jeu.plateau.copie()
		if profondeur == 0 or not plateau.existe_coup_valide(couleurval):
			return self.fct_evaluation(plateau, couleurval), None
		if maximiser:
			M = -np.inf
			coups_possibles = plateau.liste_coups_valides(couleurval)
			argmax = None
			for coup in coups_possibles:
				plateau_apres = plateau.copie()
				plateau_apres.jouer(coup, couleurval)
				self.nb_appels_jouer += 1
				val, _ = self.minmax(-couleurval, profondeur-1,False)
				if M < val:
					M = val
					argmax = coup
			return M, argmax
		else:
			M = np.inf
			coups_possibles = plateau.liste_coups_valides(couleurval)
			argmin = None
			for coup in coups_possibles:
				plateau_apres = plateau.copie()
				plateau_apres.jouer(coup, couleurval)
				self.nb_appels_jouer += 1
				val, _ = self.minmax(-couleurval, profondeur-1,True)					
				if M > val:
					M = val
					argmin = coup
			return M, argmin

	def demande_coup(self, profondeur = 4):
			start_time = time.time()
			_, meilleur_coup = self.minmax(self.couleurval,profondeur,True)
			end_time = time.time()

			self.temps_exe += end_time - start_time

			print(f"Temps d'exécution minmax : {self.temps_exe:.2f} secondes")
			print(f"Nombre d'appels à jouer : {self.nb_jouer()}")
			#print(f"Meilleur coup : {meilleur_coup}")
			return meilleur_coup if meilleur_coup is not None else []

	def nb_jouer(self):
		return self.nb_appels_jouer



class AlphaBeta(IA):

	def fct_evaluation(self, plateau, couleurval):
		score = 0
		poids_stabilite = 10
		poids_mobilite = 5
		poids_coin = 20

		disques_stables = 0
		for i in range(plateau.taille):
			for j in range(plateau.taille):
				if plateau.tableau_cases[i][j] == couleurval:
					disques_stables += 1
		score += poids_stabilite * disques_stables

		mobilite = len(plateau.liste_coups_valides(couleurval))
		score += poids_mobilite * mobilite

		coins = [(0, 0), (0, plateau.taille - 1), (plateau.taille - 1, 0), (plateau.taille - 1, plateau.taille - 1)]
		controle_coins = 0
		for coin in coins:
			if plateau.tableau_cases[coin[0]][coin[1]] == couleurval:
				controle_coins += 1
		score += poids_coin * controle_coins

		return score

	"""
	10. Cr´eez un nouveau Joueur pour l’algorithme Alpha-Beta
	"""
	def alpha_beta(self, couleurval, profondeur=3, alpha=-np.inf, beta=np.inf, maximiser=True):
		plateau = self.jeu.plateau.copie()
		if profondeur == 0 or not plateau.existe_coup_valide(couleurval):
			return self.fct_evaluation(plateau, couleurval), None
		if maximiser:
			M = -np.inf
			coups_possibles = plateau.liste_coups_valides(couleurval)
			argmax = None
			for coup in coups_possibles:
				plateau_apres = plateau.copie()
				plateau_apres.jouer(coup, couleurval)
				self.nb_appels_jouer += 1
				val, _ = self.alpha_beta(-couleurval, profondeur-1, alpha, beta, False)
				if M < val:
					M = val
					argmax = coup
				alpha = max(alpha, M)
				if beta <= alpha:
					break
			return M, argmax
		else:
			M = np.inf
			coups_possibles = plateau.liste_coups_valides(couleurval)
			argmin = None
			for coup in coups_possibles:
				plateau_apres = plateau.copie()
				plateau_apres.jouer(coup, couleurval)
				self.nb_appels_jouer += 1
				val, _ = self.alpha_beta(-couleurval, profondeur-1, alpha, beta, True)
				if M > val:
					M = val
					argmin = coup
				beta = min(beta, M)
				if beta <= alpha:
					break
			return M, argmin

	def fct_evaluation_apres_coup(self, plateau, coup, couleurval):
		plateau_apres = plateau.copie()
		plateau_apres.jouer(coup, couleurval)
		return self.fct_evaluation(plateau_apres, couleurval)

	def alpha_beta_optimized(self, couleurval, profondeur=3, alpha=-np.inf, beta=np.inf, maximiser=True):
		plateau = self.jeu.plateau.copie()
		if profondeur == 0 or not plateau.existe_coup_valide(couleurval):
			return self.fct_evaluation(plateau, couleurval), None

		coups_possibles = plateau.liste_coups_valides(couleurval)
		coups_ordonnes = sorted(
			coups_possibles,
			key=lambda c: self.fct_evaluation_apres_coup(plateau, c, couleurval),
			reverse=maximiser
		)

		if maximiser:
			valeur = -np.inf
			meilleur_coup = None
			for coup in coups_ordonnes:
				plateau_apres = plateau.copie()
				plateau_apres.jouer(coup, couleurval)
				self.nb_appels_jouer += 1
				score, _ = self.alpha_beta_optimized(-couleurval, profondeur - 1, alpha, beta, False)
				if score > valeur:
					valeur = score
					meilleur_coup = coup
				alpha = max(alpha, valeur)
				if beta <= alpha:
					break
			return valeur, meilleur_coup
		else:
			valeur = np.inf
			meilleur_coup = None
			for coup in coups_ordonnes:
				plateau_apres = plateau.copie()
				plateau_apres.jouer(coup, couleurval)
				self.nb_appels_jouer += 1
				score, _ = self.alpha_beta_optimized(-couleurval, profondeur - 1, alpha, beta, True)
				if score < valeur:
					valeur = score
					meilleur_coup = coup
				beta = min(beta, valeur)
				if beta <= alpha:
					break
			return valeur, meilleur_coup
	
	def demande_coup(self, profondeur=3, optimize=False):
		start_time = time.time()
		if optimize:
			_, meilleur_coup = self.alpha_beta_optimized(self.couleurval, profondeur, True)
		else:
			_, meilleur_coup = self.alpha_beta(self.couleurval, profondeur, True)
		end_time = time.time()
		
		self.temps_exe += end_time - start_time
		print(f"Temps d'exécution : {self.temps_exe:.2f} secondes")
		return meilleur_coup if meilleur_coup is not None else []

	def nb_jouer(self):
		return self.nb_appels_jouer



