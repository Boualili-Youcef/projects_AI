import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np


class Graphe:
	def __init__(self):
		self.dic_noeud = {} #La clé est le numéro de département, la valeur le Noeud correspondant.
		self.lire_villes()
		self.lire_routes()
		
	def lire_villes(self, villes="villes.dat"):
		with open(villes, 'r') as f_villes:
			for line in f_villes:
				data_noeud = line.split(";")
				try:
					num_departement = int(data_noeud[0])
					nom_chef_lieu = data_noeud[1]
					position = [int(data_noeud[2]), int(data_noeud[3])]
					self.dic_noeud[num_departement] = Noeud(num_departement, nom_chef_lieu, position)
				except:
					pass
	
	def lire_routes(self, routes="routes.dat"):
		with open(routes, 'r') as f_routes:
			for line in f_routes:
				data_route = line.split(";")
				try:
					n = self.dic_noeud[int(data_route[0])]
					for num_v_s in data_route[1:]:
						voisin = self.dic_noeud[int(num_v_s)]
						n.aretes.append([voisin, distance_km(n, voisin)])
				except:
					pass
	
	def afficher_carte(self, carte_loc="france.png"):
		carte = mpimg.imread(carte_loc)
		plt.imshow(carte)


class Carte:
	
	def __init__(self, graphe, carte_loc="france.png"):
		self.graphe = graphe
		self.carte = mpimg.imread(carte_loc)
		self.hauteur = self.carte.shape[0]
		
	def afficher(self):
		plt.imshow(self.carte)
		for n in self.graphe.dic_noeud.values():
			x1, y1 = n.position[0], n.position[1]
			for a in n.aretes:
				x2, y2 = a[0].position[0], a[0].position[1]
				plt.plot([x1,x2], [self.hauteur-y1, self.hauteur-y2], color="black", lw=1)
	
	def afficher_chemin(self, liste_noeud, color="red"):
		self.afficher()
		for i in range(len(liste_noeud)-1):
			x1, y1 = liste_noeud[i].position[0], liste_noeud[i].position[1]
			x2, y2 = liste_noeud[i+1].position[0], liste_noeud[i+1].position[1]
			plt.plot([x1,x2], [self.hauteur-y1, self.hauteur-y2], color=color, lw=1)

def distance_km(ville1, ville2):
	dx = ville1.position[0] - ville2.position[0]
	dy = ville1.position[1] - ville2.position[1]
	return 1.9 * np.sqrt(dx**2 + dy**2) #le facteur 1.9 convertit environ la distance entre pixels en kilomètres

class Noeud:
	
	def __init__(self, num, nom, pos):
		self.numero = num
		self.chef_lieu = nom
		self.position = pos
		self.aretes = [] #Une arete est de forme [N, d], où N est un Noeud et d la distance entre les deux Noeuds.

