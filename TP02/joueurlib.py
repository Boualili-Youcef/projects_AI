import interfacelib
import numpy as np
import time
import matplotlib.pyplot as plt

global_stats = {
	'depths': [],
	'nb_appels': {},
	'times': {}
}

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
		# recuperer tout les coups possibles pour le joueur
		coups_possibles = self.jeu.plateau.liste_coups_valides(self.couleurval)
		index = np.random.randint(0, len(coups_possibles))
		return coups_possibles[index]


class Minmax(IA):
	"""
	Fonction d'evaluation de la position simple:
		Elle compte le nombre de pions de la couleur du joueur
	"""
	def evaluation_position(self):
		score = 0
		for i in range(self.jeu.plateau.taille):
			for j in range(self.jeu.plateau.taille):
				if self.jeu.plateau.tableau_cases[i][j] == self.couleurval:
					score += 1
		return score

	# Implementation de min et max comme vu en cours
	def minmax(self,profondeur, joueur=1):
		plateau = self.jeu.plateau.copie() # On copie le plateau pour ne pas modifier le plateau original peux etre a revoir
		# Si on est a la profondeur 0, on est donc une feuille et on evalue la position
		if profondeur == 0:
			return self.evaluation_position(), None
		if joueur == 1:
			M = -np.inf
			coups_possibles = plateau.liste_coups_valides(1)
			argmax = None
			for coup in coups_possibles:
				plateau.jouer(coup, joueur)
				self.nb_appels_jouer += 1	
				val, _ = self.minmax(profondeur-1, -joueur)
				if M < val:
					M = val
					argmax = coup
			return M, argmax
		else:
			M = np.inf
			coups_possibles = plateau.liste_coups_valides(-1)
			argmin = None
			for coup in coups_possibles:
				plateau.jouer(coup, joueur)
				self.nb_appels_jouer += 1
				val, _ = self.minmax(profondeur-1, -joueur)
				if M > val:
					M = val
					argmin = coup
			return M, argmin

	def demande_coup(self):
		global global_stats
		best_val = -np.inf
		best_coup = None
		profondeur_max = 3
		for prof in range(1, profondeur_max + 1):
			self.nb_appels_jouer = 0
			start_time = time.time()
			val, coup = self.minmax(prof, self.couleurval)
			end_time = time.time()
			temps = end_time - start_time

			global_stats['depths'].append(prof)
			if prof not in global_stats['nb_appels']:
				global_stats['nb_appels'][prof] = []
			if prof not in global_stats['times']:
				global_stats['times'][prof] = []
			global_stats['nb_appels'][prof].append(self.nb_appels_jouer)
			global_stats['times'][prof].append(temps)

			if val > best_val:
				best_val = val
				best_coup = coup

		self.temps_exe += temps
		print(f"Minmax coup sélectionné : {best_coup}")
		print(f"Nombre de coups: {self.nb_appels_jouer}")
		print(f"Temps d'exécution total: {self.temps_exe} s")
		return best_coup

	@staticmethod
	def plot_global_evolution():

		avg_appels = {depth: sum(appels) / len(appels) for depth, appels in global_stats['nb_appels'].items()}
		avg_times = {depth: sum(times) / len(times) for depth, times in global_stats['times'].items()}

		plt.figure()
		plt.subplot(1, 2, 1)
		plt.plot(list(avg_appels.keys()), list(avg_appels.values()), label='Nombre moyen d\'appels jouer')
		plt.xlabel('Profondeur')
		plt.ylabel('Nombre moyen d\'appels')
		plt.title('Nombre moyen d\'appels selon la profondeur')
		plt.legend()

		plt.subplot(1, 2, 2)
		plt.plot(list(avg_times.keys()), list(avg_times.values()), label='Temps moyen (s)')
		plt.xlabel('Profondeur')
		plt.ylabel('Temps moyen (s)')
		plt.title('Temps moyen selon la profondeur')
		plt.legend()

		plt.tight_layout()
		plt.show()

		
	"""
		7 - 
		Compteur de nombre d'appels à la fonction jouer:
			C'est pour comprender combien de fois on explore les possibilités du jeu
		Compteur de temps d'exécution:
			Avoir une idée de comment le temps d'exécution varie en fonction de la profondeur de recherche
		Le nombre de coups augemente en fonction de la profondeur de recherche
		Le temps d'execution augemente en fonction de la profondeur de recherche
		Ils varient donc dans le meme sens
	"""
	
		

class AlphaBeta(IA):
	"""
	Fonction d'evaluation de la position simple:
		Elle compte le nombre de pions de la couleur du joueur
	"""
	def evaluation_position(self):
		score = 0
		for i in range(self.jeu.plateau.taille):
			for j in range(self.jeu.plateau.taille):
				if self.jeu.plateau.tableau_cases[i][j] == self.couleurval:
					score += 1
		return score

	# Implementation de l'algorithme Alpha-Beta
	def alpha_beta(self, profondeur, alpha, beta, joueur=1):
		plateau = self.jeu.plateau.copie()
		if profondeur == 0:
			return self.evaluation_position(), None
		if joueur == 1:
			M = -np.inf
			coups_possibles = plateau.liste_coups_valides(1)
			argmax = None
			for coup in coups_possibles:
				plateau.jouer(coup, joueur)
				self.nb_appels_jouer += 1
				val, _ = self.alpha_beta(profondeur-1, alpha, beta, -joueur)
				if M < val:
					M = val
					argmax = coup
				alpha = max(alpha, val)
				if beta <= alpha:
					break
			return M, argmax
		else:
			M = np.inf
			coups_possibles = plateau.liste_coups_valides(-1)
			argmin = None
			for coup in coups_possibles:
				plateau.jouer(coup, joueur)
				self.nb_appels_jouer += 1
				val, _ = self.alpha_beta(profondeur-1, alpha, beta, -joueur)
				if M > val:
					M = val
					argmin = coup
				beta = min(beta, val)
				if beta <= alpha:
					break
			return M, argmin

	def demande_coup(self):
		global global_stats
		best_val = -np.inf
		best_coup = None
		profondeur_max = 6
		for prof in range(1, profondeur_max + 1):
			self.nb_appels_jouer = 0
			start_time = time.time()
			val, coup = self.alpha_beta(prof, -np.inf, np.inf, self.couleurval)
			end_time = time.time()
			temps = end_time - start_time

			global_stats['depths'].append(prof)
			if prof not in global_stats['nb_appels']:
				global_stats['nb_appels'][prof] = []
			if prof not in global_stats['times']:
				global_stats['times'][prof] = []
			global_stats['nb_appels'][prof].append(self.nb_appels_jouer)
			global_stats['times'][prof].append(temps)

			if val > best_val:
				best_val = val
				best_coup = coup

		self.temps_exe += temps
		print(f"AlphaBeta coup sélectionné : {best_coup}")
		print(f"Nombre de coups: {self.nb_appels_jouer}")
		print(f"Temps d'exécution total: {self.temps_exe} s")
		return best_coup

"""
	Q11-
	Sans faire l'expérience je pense que le résultat de 100 parties entre Minmax en joueur noir et Alpha-Beta en joueur blanc serait d'Alpha-Beta.

	car il permet d'explorer plus de possibilités en moins de temps et peut atteindre une profondeur de recherche plus grande que Minmax dans le même laps de temps.
"""
