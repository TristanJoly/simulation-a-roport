class Empty_tas:
    def __init__(self):
        pass

    def ajouter (self,x) : 
        return Tas(Empty_tas(),x,Empty_tas())
    
    def supprimer(self):
        return Empty_tas()
    def __str__(self):
        return ' X '
    def taille(self):
        return 0
    def minimum(self):
        return None
    def appartient(self,x):
        return False
    def hauteur(self):
        return 0

    def est_tas(self):
        return True

    def fusion(self,other):
        return other

class Tas:
    def __init__(self,gauche,valeur,droite):
        self.v = valeur
        self.g = gauche
        self.d = droite

    def __str__(self):
        return '( ' + str(self.g) + str(self.v) + str(self.d) + ' )'
    
    def taille(self):
        return 1 + self.g.taille() + self.d.taille()

    def minimum(self):
        return self.v
    
    def appartient(self,x):
        if self.v == x:
            return True
        return self.g.appartient(x) or self.d.appartient(x)

    def hauteur(self):
        return 1 + max(self.g.hauteur(), self.d.hauteur())

    def est_tas(self):
        if type(self.g) == Empty_tas and type(self.d) == Empty_tas:
            return True
        if type(self.g) == Empty_tas and self.v < self.d.v:
            return self.d.est_tas()
        elif type(self.g) == Empty_tas:
            return False
        if type(self.d) == Empty_tas and self.v < self.g.v:
            return self.g.est_tas()
        elif self.d == Empty_tas:
            return False
        if self.v > self.d.v or self.v > self.g.v:
            return False
        return self.g.est_tas() and self.d.est_tas()

    def fusion(self,other):
        
        """
        Permet de fusionner deux tas et d'en renvoyer le resultat.
        Le principe de la fusion est le meme que vu en classe.
        """
        if type(other) == Empty_tas:
            return self
        x1,x2 = self.v,other.v
        if x1 < x2:
            return Tas(self.d.fusion(other),x1,self.g)
        return Tas(other.d.fusion(self),x2,other.g)


    def ajouter(self,x):
        """
        retourne un arbre de la fusion, à utiliser de la forme tas = tas.ajouter(x)
        """
        a_ajouter = Tas(Empty_tas(),x,Empty_tas())
        return self.fusion(a_ajouter)

    def supprimer(self):
        """
        Supprime l'élement minimal
        """
        return self.d.fusion(self.g)
"""
Toutes les focntions codées dans  ce documents sont issus des TP fait en classe.
"""
