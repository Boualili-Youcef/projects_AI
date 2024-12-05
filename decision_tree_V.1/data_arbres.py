import numpy as np
import math

class DataPoint:
    def __init__(self, x, y, cles):
        self.x = {}
        for i in range(len(cles)):
            self.x[cles[i]] = float(x[i])
        self.y = int(y)
        self.dim = len(self.x)
        
    def __repr__(self):
        return 'x: ' + str(self.x) + ', y: ' + str(self.y)


def load_data(filelocation):
    with open(filelocation, 'r') as f:
        data = []
        attributs = f.readline()[:-1].split(',')[:-1]
        for line in f:
            z = line.split(',')
            if z[-1] == '\n':
                z = z[:-1]
            x = z[:-1]
            y = int(z[-1])
            data.append(DataPoint(x, y, attributs))
    return data


class Noeud:
    def __init__(self, profondeur_max=np.infty):
        self.question = None
        self.enfants = {}
        self.profondeur_max = profondeur_max
        self.proba = None
        self.hauteur = 0

    def prediction(self, x):
        if self.proba is not None:
            
            return self.proba
        
        if self.question is not None:
            a, s = self.question
            if self.question_inf(x, a, s):
                return self.enfants["gauche"].prediction(x)            
            return self.enfants["droite"].prediction(x)
        
    def grow(self, data, profondeur=0):
        self.donnees = data
        entropie = self.entropie(data)
        best_question = self.best_split(data)
        
        if best_question is None:
            self.hauteur = profondeur
            self.proba = self.proba_empirique(data)
            return

        d1, d2 = self.split(data, best_question)
        if entropie > 0 and self.profondeur_max > profondeur and len(d1) > 0 and len(d2) > 0:
            self.question = best_question
            self.enfants["gauche"] = Noeud(self.profondeur_max)
            self.enfants["droite"] = Noeud(self.profondeur_max)
            profondeur += 1
            
            self.enfants["gauche"].grow(d1, profondeur)
            self.enfants["droite"].grow(d2, profondeur)
        else:
            self.hauteur = profondeur
            self.proba = self.proba_empirique(data)

            
            
    def precision(self, data):
        correct_predictions = 0
        total_predictions = len(data)

        for d in data:
            prediction = self.prediction(d.x)
            predicted_class = max(prediction.values())  
            for key, value in prediction.items():
                if value == predicted_class:
                    cle = key
            if cle == d.y:
                correct_predictions += 1
        
        return correct_predictions / total_predictions * 100 if total_predictions > 0 else 0

    def split_train_test(self, data):
        np.random.shuffle(data)
        train_set_size = int(len(data) * 0.8)
        train_set = data[:train_set_size]
        test_set = data[train_set_size:]
        return train_set, test_set
        
    def proba_empirique(self, d):
        size = len(d)
        classes = {}
        for point in d:
            if point.y not in classes:
                classes[point.y] = 0
            classes[point.y] += 1 
        result = {key : value/size for key, value in classes.items()}
        return result
    
    def question_inf(self, x, a, s):
        return x[a] < s
    
    def split(self, d, question):
        a, s = question
        d1 = []
        d2 = []
        for i in range(len(d)):
            if self.question_inf(d[i].x, a, s):
                d1.append(d[i])
            else:
                d2.append(d[i])
        return d1, d2
    
    def list_separ_attributs(self, d, a):
        list_attributs = []
        size = len(d)

        for i in range(size):
            list_attributs.append(d[i].x[a])
            
        set_list = list(set(list_attributs))
        set_list.sort()
        
        result = []
        for i in range(len(set_list)-1):
            result.append((a, (set_list[i] + set_list[i+1]) / 2))
        
        return result
        
    def liste_questions(self, d):
        attributs = []
        for attribut in d[0].x:
            if attribut not in attributs:
                attributs.append(attribut)
        
        questions = []
        for a in attributs: 
            questions.extend(self.list_separ_attributs(d, a))
        return questions
    
    def entropie(self, d):
        prob_empirique = self.proba_empirique(d)
        entropy = 0
        for proba in prob_empirique.values():
            if proba > 0:
                entropy -= proba * math.log2(proba)
        return entropy

    def best_split(self, d):
        best_question = None
        questions = self.liste_questions(d)
        max_entropy_gain = -float("inf")

        for question in questions:
            gain = self.gain_entropie(d, question)
            if max_entropy_gain < gain:
                max_entropy_gain = gain
                best_question = question

        return best_question

    def gain_entropie(self, d, question):
        d1, d2 = self.split(d, question)
        if len(d1) == 0 or len(d2) == 0:
            return 0

        r1 = len(d1) / len(d)
        r2 = len(d2) / len(d)

        return self.entropie(d) - r1 * self.entropie(d1) - r2 * self.entropie(d2)
    
    def elagage(self, alpha):
        # Vérifier si l'objet est une feuille
        if self.enfants:
            # Appliquer l'élagage à chaque enfant récursivement
            for enfant in self.enfants.values():
                enfant.elagage(alpha)
            
            # Calcul du gain d'entropie
            gain = self.gain_entropie(self.donnees, self.question)
            
            # Si le gain d'entropie est inférieur à alpha, couper l'enfant
            if gain < alpha:
                self.enfants = {}  # Retirer les enfants
                self.proba = self.proba_empirique(self.donnees)  # Ajouter la probabilité empirique à la feuille
                self.question = None  # Pas de question à la feuille