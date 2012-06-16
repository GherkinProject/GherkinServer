import random
from configServer import *

class Markovienne():

    def __init__(self, dbName= "ProcessOfMarkov"):
        self.markov = {}
        self.number = {}
        self.dbName = dbName
# markov fait office de dictionnaire de dictionnaire. 
# En realite c est une matrice, tel que self.markov de i et j represente la proba de transition de l songe i a l songe j
# nombre[i] enfin recense le nombre de vote/ de load que l on d un songe a un autre.
# si je passe de twostepfromhell a LOTR jincremente nombre[twostepfromhell]

    def create_Markov(self, songList):
        """Creer un fichier .ghk avec les proba de transition"""
        file = open(config.userLoc + self.dbName, 'w')        
        for i in songList:
            self.markov[i] = {}
            self.number[i] = 1.0
	    randIdSong = random.sample(songList, 10)
            for j in randIdSong:
                self.markov[i][j] = 1.0 / float(len(randIdSong))
                file.write(str(i) + "$" + str(j) + "$" + str(self.markov[i][j])+ '$' + str(self.number[i])+ '$')
                file.write('\n')
        file.close()

    def load_Markov(self, fileName):
        """ Charge le fichier .ghk contenant les probas de transition"""
        self.dbName = fileName
        file = open(config.userLoc + self.dbName, 'r')
        for line in file:
            u = line.split('$')
	    try:
		self.markov[int(u[0])][int(u[1])] = float(u[2])
	    except:
		self.markov[int(u[0])] = {}
                self.markov[int(u[0])][int(u[1])] = float(u[2])
            self.number[int(u[0])] = float(u[3])
        file.close()

    def save_Markov(self):
        """ Sauvegarde les donnees"""
        file = open(config.userLoc + self.dbName, 'w')
        for i in self.markov.keys():
            for j in self.markov[i].keys():
                file.write(str(i) + "$" + str(j) + "$" + str(self.markov[i][j])+ '$' + str(self.number[i])+ '$')
                file.write('\n')
        file.close()
			
    def vote_Markov(self, songBeginning, songEnd):
        """ Realise le vote du passage entre songBeginning et songEnd"""
        self.number[songBeginning]+=1
    	if songBeginning == songEnd:
	        pass
    	else:
            for j in self.markov[songBeginning].keys():
       	    	if j == songEnd:
                    self.markov[songBeginning][j] = (self.markov[songBeginning][j]*(self.number[songBeginning]-1)+1)/(self.number[songBeginning])
            	else:
                    self.markov[songBeginning][j] *= (self.number[songBeginning]-1)/(self.number[songBeginning])
   	        if songEnd not in self.markov[songBeginning].keys():
		    self.markov[songBeginning][songEnd] = 1.0 / (self.number[songBeginning])
    def choix_Markov(self, idSong):
        """ Choisit le successeur de song entrain d etre joue"""
        u = random.random() # nombre aleatoire entre 0 et 1
	print "affichage de des clefs de idSong"
	print self.markov[idSong].keys()
        for k in self.markov[idSong].keys():
            if self.markov[idSong][k] >= u:
# dans ce cas la chaine de markov nous indique que le prochain songe sera k
                return k
            else:
# sinon on regarde les autres songes, en decrementant u. on trouve techniquement qu il y a toujours un k renvoye si u != 1
                u -= self.markov[idSong][k]
	    return self.markov[idSong].keys()[-1]

    def elagage(self, idSong, epsilon):
	""" Realise l elagage des probabilites otant ainsi les proba inferieures a epsilon pour les reporter aleatoirement sur une autre chanson"""
	for k in self.markov[idSong].keys():
            if self.markov[idSong][k] < epsilon:
		u = random.sample(self.markov[idSong].keys(), 2)
		if u[1] != k:
			self.markov[idSong][u[1]] += self.markov[idSong][k]
		else:
			self.markov[idSong][u[0]] += self.markov[idSong][k]
		self.markov[idSong].pop(k)


#U = Markovienne()
#U.load_Markov("dbMarkov.ghk")

#print U
