class Avion:
    def __init__(self, indicatif, autonomie, pirate, feu,temps_pirate = 0):
        """
        Permet de crer une instance de la classe avion avec les attributs:
        indicatif, autonomie, pirate, feu,temps_pirate
        """
        self.indicatif = indicatif
        self.autonomie = autonomie
        self.pirate = pirate
        self.feu = feu
        self.temps_pirate = temps_pirate

    def __lt__(self, other):
        """
        Permet de retourner la prioritée entre deux element de la classe avion.
        """
        return self.priorite() < other.priorite()

    def priorite(self):
        
        """
        Permet de definir la priorité d'un avion , mettant en point d'orgue le feu , les pirates en enfin l'autonomie de vol de l'avion
        """
        priority = self.autonomie
        if self.pirate:
            priority -= 5
        if self.feu:
            priority -= 500
        return priority

    def __str__(self):
        return 'Nom: ' + str(self.indicatif) + ' autonomie: ' + str(self.autonomie) + ' pirate: ' + str(self.pirate) + ' feu : ' + str(self.feu) #on veut toutes les infos
        #return 'Autonomie: ' + str(self.autonomie) #On veut que l'autonomie

    def str_clipboard(self):
        result = '_-- ' + self.indicatif + ' '
        result += 'à une autonomie de ' + str(self.autonomie) + 'h '
        if self.feu == True:
            result += ' actuellement en feu !'

            if self.pirate == True:
                result += ' Et il se fait détourner'
        elif self.pirate == True:
            result += 'mais il y a un pirate à bord'
        return result
         
