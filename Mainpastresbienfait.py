from random import randint as rnt
from musique import *
from classe_tas import *
from avion import *
from pygame.locals import *
import sys

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

pygame.init()
#Dimensions de la fenêtre
fenetre = pygame.display.set_mode((700, 700))
BLANC = (255, 255, 255)
NOIR = (0, 0, 0)

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def liste_en_tas(lst):
    """
    Cette fonction transforme la liste d'avion donné en un tas suivant la structure theorique d'un tas.
    Elle prend une liste en entre et ajoute succesivement chaque element de la liste afin de creer le tas.
    """
    tas_temporaire = Empty_tas()
    assert type(lst) == list
    for i in range(len(lst)):
        tas_temporaire = tas_temporaire.ajouter(lst[i])
    return tas_temporaire


def pivot(tab):
    """
    Cette fonction trie une liste tab selon un tri pivot.
    """
    if tab == []:
        return []
    p = tab.pop()
    grand = []
    petit = []
    for loop in range(len(tab)):
        if tab[0]<p:
            petit.append(tab[0])
        else:
            grand.append(tab[0])
        tab = tab[1:]
    return pivot(petit) + [p] + pivot(grand)

def creer_avions_aleatoires(n, feu_prob=0.05, pirate_prob=0.05):
    """
    Cette fonction cree des objets avions selon plusieurs criteres,
    toujours en utilisant l'aléatoire de la fonction randint de la bibliotheque random.
    Ainsi , elle peut creer un matricule (quasiment)-unique pour chaque avion et definir leurs autonomie, leurs feu ainsi que si il est pirate ou non.
    L'utilisateur pour interargir avec cette fonction doit indiquer un nombre d'avion a crée et si il veut modifier des parametre d'aléatoire.
    La fonction retourne une liste contenant un nombre n demandé d'avion.
    """
    assert type(n) == int,ValueError 
    avions = []
    alphabet = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    for i in range(n):
        lettre1 = rnt(0,25)
        lettre2 = rnt(0,25)
        lettre3 = rnt(0,25)
        a = rnt(1,9)
        b = rnt(1,9)
        c = rnt(1,9)
        autonomie = rnt(5,40)
        identifiant = alphabet[lettre1] + alphabet[lettre2] + alphabet[lettre3] + str(a) + str(b) + str(c) 
        feu = rnt(1,100) < feu_prob*100
        pirate = rnt(1,100) < pirate_prob*100
        if pirate :
            avion = Avion(identifiant,autonomie, feu, pirate,rnt(1,3))
        avion = Avion(identifiant,autonomie, feu, pirate)
        avions.append(avion)
    return avions

def actualise(tas, en_feu, en_pirate):
    """
    Cette fonction permet d'actualiser le tas si des evenement externe se sont produit:
    Si l'avion est en feu, on l'ajoute à la liste et on le retire du tas.
    Si l'avion est piraté, on l'ajoute à la liste et on le retire du tas
    On effectue recursivement la fonction sous les sous tas gauche et droite  et on renvoit le tas ainsi modifie
    et on retourne le tas.
    """
    assert type(en_feu) == list
    assert type(en_pirate) == list
    if isinstance(tas, Empty_tas):
        return tas 
    if tas.v.feu:# Si l'avion est en feu, on l'ajoute à la liste et on le retire du tas
        en_feu.append(tas.v)
        return actualise(tas.supprimer(), en_feu, en_pirate)
    elif tas.v.pirate: # Si l'avion est piraté, on l'ajoute à la liste et on le retire du tas
        en_pirate.append(tas.v)
        return actualise(tas.supprimer(), en_feu, en_pirate)
    tas.g = actualise(tas.g, en_feu, en_pirate)
    tas.d = actualise(tas.d, en_feu, en_pirate)
    return tas 


def redefini_avion_prioritaire(tas):
    """
    Cette fonction actualise le tas et récupère les avions en feu ou piratés,
    afin de les rajoute aux tas selon les nouveaux ordre de prioritées
    """
    assert type (tas) == Tas
    est_en_feu = []
    est_pirate = []
    tas = actualise(tas, est_en_feu, est_pirate)
    for avion in est_pirate:
        tas = tas.ajouter(avion)
    for avion in est_en_feu:
        tas = tas.ajouter(avion)
    assert type (tas) == Tas
    return tas  

def applique_probas(tas, feu_prob=0.05, pirate_prob=0.05):
    """
    Cette fonction permet de calculer pour chaque avion présent dans le tas si il va s'enflammer ou si il va etre pirate.
    De plus elle verifie que si il est pirate alors il ait un temps de pirate associe avant qu'il soit detourne
    Si lorsqu'elle parcours le tas une nouvelle fois , ce temps est ecoule , alors l'avion est supprime du tas.
    Elle retourne le tas aisni modifié.
    """
    if isinstance(tas, Empty_tas) or tas is None:
        return tas  # Retourne le tas inchangé si c'est un tas vide ou None
    if rnt(1, 100) < feu_prob * 100:
        tas.v.feu = True
        print("Un avion a prit feu")
    elif rnt(1, 100) < pirate_prob * 100:
        tas.v.pirate = True
        print("Un avion a été piraté")
        tas.v.temps_pirate = rnt(1,3)
    if tas.v.autonomie != 0 :
        tas.v.autonomie -=1
    if tas.v.pirate and tas.v.temps_pirate == 0 :
        tas.g = applique_probas(tas.g, feu_prob, pirate_prob)
        tas.d = applique_probas(tas.d, feu_prob, pirate_prob)
        tas = tas.g.fusion(tas.d)
    elif tas.v.pirate and tas.v.temps_pirate != 0 :
        tas.v.temps_pirate -= 1
        tas.g = applique_probas(tas.g, feu_prob, pirate_prob)# Appel récursif sur les sous-arbres gauche et droit
        tas.d = applique_probas(tas.d, feu_prob, pirate_prob)
    else : 
        tas.g = applique_probas(tas.g, feu_prob, pirate_prob)# Appel récursif sur les sous-arbres gauche et droit
        tas.d = applique_probas(tas.d, feu_prob, pirate_prob)
    return tas

def texte_clipboard(avion):
    """
    Fonction prennant en entre un objet avion et le transformant en str avec les statuts qui lui sont propres..
    """
    assert type(avion) == Avion
    result = '-- ' + avion.indicatif + ' '
    result += 'à une autonomie de ' + str(avion.autonomie) + 'h '
    if avion.feu == True:
        result += ' actuellement en feu !'

        if avion.pirate == True:
            result += ' Et il se fait détourner'
    elif avion.pirate == True:
        result += 'mais il y a un pirate à bord'
    return result


def animation_hijack(avion,aeroport_image,largeur,hauteur,fenetre):
    """
    Permet d'afficher une animation d'un avion hijacke.Pour l'instant est un prototype mais marchera a la prochaine mise a jour.
    """
    clock = pygame.time.Clock()
    for i in range(22):
        fenetre.blit(aeroport_image,(largeur//2,0))
        fenetre.blit(avion,(largeur-(i*largeur//50),hauteur//0.5))
        pygame.display.flip()
        clock.tick(22)
    pygame.time.wait(500)

def animation_atterrissage(avion,aeroport_image,largeur,hauteur,fenetre):
    """
    Permet d'afficher une animation d'un avion atterrissant et une musique d'avion atterissant(a320 pour etre précis), de temps a autre.
    """
    clock = pygame.time.Clock()
    if rnt(1,100)<15:
        aeroport.music = MusicPlayer(["musique_atterisage.mp3"])
        for i in range(22):
            fenetre.blit(aeroport_image,(largeur//2,0))
            fenetre.blit(avion,(largeur-(i*largeur//50),hauteur//2))
            pygame.display.flip()
            clock.tick(22)
        aeroport.music = MusicPlayer(["musique_attente.mp3"])
        pygame.time.wait(500)
    else :
        for i in range(22):
            fenetre.blit(aeroport_image,(largeur//2,0))
            fenetre.blit(avion,(largeur-(i*largeur//50),hauteur//2))
            pygame.display.flip()
            clock.tick(22)
        pygame.time.wait(500)

def print_tas(tas):
    """
    Permet d'afficher un element de la classe tas pour l'affichage dans le clipboard.
    """
    if tas.taille() == 0 :
        return ""
    else :
        res = tas.v.str_clipboard()
        return res + print_tas(tas.g.fusion(tas.d))

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

class Menu:
    def __init__(self, fenetre, options, image_de_fond):
        """
        Prend en entrée un Menu, une fenetre de pygame, les options qui s'affichent sur l'écran et l'image de fond
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet de définir les attributs d'un menu
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """
        self.fenetre = fenetre
        self.options = options
        self.choisi = 0
        self.police = pygame.font.Font(None, 50)
        self.fond = pygame.image.load(image_de_fond).convert_alpha()
        self.fleche = pygame.image.load("fleche.png").convert_alpha()
        self.music = MusicPlayer(["musique_attente.mp3"])

    def dessiner(self):
        """
        Prend en entrée un Menu
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet de dessiner les options d'un Menu sur l'image de fond
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """
        image = pygame.transform.scale(self.fond, (700, 700))
        self.fenetre.blit(image, (0, 0))
        for i, option in enumerate(self.options):
            couleur = BLANC if i == self.choisi else NOIR
            texte = self.police.render(option, True, couleur)
            rect = texte.get_rect(center=(700 // 2, 700 // 2 + i * 60))
            self.fenetre.blit(texte, rect)
            

    def gerer_event(self, event):
        """
        Prend en entrée un Menu et un évènement
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet de connaître l'option choisi
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Renvoie l'indice de l'option choisi
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN:
                self.choisi = (self.choisi + 1) % len(self.options)
            elif event.key == pygame.K_UP:
                self.choisi = (self.choisi - 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.choisi
            elif event.key == pygame.K_t:
                a = StickFigureWindow()
            return None
#---------------------------------------------------------------------------------------------------------------------------

class Aeroport :
    """
    Cette fonction nous permet de créer l'instance aéroport qui sauvegarde le tas d'arrive , le nombre de hangar.
    Ainsi que le temps d'attente avant de rentrer dans un hangar.
    """
    def __init__(self,tas_arrive,place_disponible = 3,temps_attente_dan_un_hangar = 4):
        self.t = tas_arrive
        self.place = place_disponible
        self.t = self.liste_en_tas()
        self.hangar = [0 for i in range  (place_disponible)]
        self.temps_attente_dan_un_hangar = temps_attente_dan_un_hangar
        self.music = MusicPlayer(["musique_attente.mp3"])
        #self.tour()
        
    
    def tour (self):
        while self.t.taille() != 0 :#pour l'instant les fonctions annexes ne marche pas mais je vais bientot les regler
            self.t = applique_probas(self.t)
            self.t = redefini_avion_prioritaire(self.t)
            indice = self.trouve_hangar()
            if indice == "pas de place":
                print(indice)
            else :
                avion_atterissant = self.t.minimum()
                self.t = self.t.supprimer()
                hangar_temporaire = self.hangar
                hangar_temporaire[indice] = [avion_atterissant,0]
                self.hangar = hangar_temporaire
            self.parcour_hangar()
            print (self.t.taille())
        print ("la partie est finie")

    def tourunique(self):
        """
        Cette fonction lance le declement d'un tour , on verifie dans un premier temps que la taille du tas d'avion est non nul
        Puis on redéfinis les avions prioritaire. 
        Puis il verifie que il y a de la place dans un des hangar, pour pouvoir stocke l'avion.
        Enfin si toutes ses cpnditions sont remplis il enleve le 1er avions du tas , fusionne son enfant gauche avec son fils droit
        Dans un dernier temps il effectue un tour pour que les hangar se vident progressivement
        ---------------------------------------------------------------------------------------------------------------------------

        Puisque aéroport est une classe , tout ceci est une méthode ne renvoyant rien et ne prenant que l'aeroport comme input.
        """
        if self.t.taille == 0:
            print("Il n'y a pas d'avion qui veut aterrir")
        else:
            self.t = redefini_avion_prioritaire(self.t)
            self.t = applique_probas(self.t)
            indice = self.trouve_hangar()
            if indice == "pas de place":
                print(indice)
            else :
                avion_atterissant = self.t.minimum()
                self.t = self.t.supprimer()
                hangar_temporaire = self.hangar
                hangar_temporaire[indice] = [avion_atterissant,0]
                self.hangar = hangar_temporaire
            self.parcour_hangar()
            print (self.t.taille())

    def parcour_hangar (self):#
        """
        Cette fonction parcourt les hangar a la fin d'un tour,
        elle vérifie si un avion est présent dans cet hangar,
        Si c'est le cas , elle vérifie si l'avion est en feu,
        si c'est le cas elle le fait attendre un tour en plus,
        Puis elle ajoute 1 à la valeur d'attente de chaque avion ,
        si cette valeur est égale au nombre de temps définie par l'utilisateur,
        alors l'avion est supprimé du hangar et part vers d'autres cieux.
        -----------------------------------------------------------------------------------

        Puisque aeroport est une classe ,
        tout ceci est une methode ne renvoyant rien et ne prent que l'aeroport comme input.
        """
        for i in range (len(self.hangar)):
            if type(self.hangar[i]) == list :
                if type(self.hangar[i][0]) == Avion:
                    if self.hangar[i][0].feu:
                        if self.hangar[i][1] == self.temps_attente_dan_un_hangar + 1:
                            self.hangar[i] = 0
                        else :
                            self.hangar[i][1] +=1
                    else : 
                        if self.hangar[i][1] == self.temps_attente_dan_un_hangar:
                            self.hangar[i] = 0
                        else :
                            self.hangar[i][1] +=1
                        
    def liste_en_tas(self):#
        """
        Cette fonction transforme la liste d'avion donné en un tas.
        La liste d'avion est stocke dans l'attribut self.t d'un aeroport,
        on ajoute toute la liste a un tas vide que l'on construit petit bout par petit bout.
        Finalement on renvoit ce tas temporaire afin qu'il puisse etre stocke dans l'attribut t de l'aéroport 
        """
        tas_temporaire = Empty_tas()
        for i in range(len(self.t)):
            tas_temporaire = tas_temporaire.ajouter(self.t[i])
        return tas_temporaire 



    def trouve_hangar(self):#
        """
        cette fonction parcour une liste contenur dans l'attribut hangar de la classe avion,
        si dans un endroit de la liste il trouve un 0 , indiquant que pas d'avion est stocke a cet emplacement ,
        il renvoit l'indice i,
        sinon il renvoit un message d'erreur , ne stoppant pas le deroulement du programme
        """
        for i in range (len(self.hangar)):
            if self.hangar[i] == 0:
                return i
        return "pas de place"
    
    def __str__(self):
        """
        Cette fonction permet de print un aeroport et d'ainsi avoir des informations sur tous ses attributs.
        """
        return 'Tas: ' + str(self.t) + ' Hangar: ' + str(self.hangar) + ' Temps attente dans hangar: ' + str(self.temps_attente_dan_un_hangar)

#---------------------------------------------------------------------------------------------------------------------------
class choisir:
    def __init__(self):
        """
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet de définir les attributs des choix sur le menu
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """
        pygame.init()
        self.fenetre = pygame.display.set_mode((700, 700))
        pygame.display.set_caption('Menu')
        self.clock = pygame.time.Clock()
        self.etat = 'menu_principal'
        self.menu_principal = Menu(self.fenetre, ["Liste d'avion aléatoire"],'image_de_fond.jpg')
        self.music = MusicPlayer(["musique_attente.mp3"])
        
    def choix_du_mode(self):
        """
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        Permet de lancer le menu avec les différents choix possibles
        ----------------------------------------------------------------------------------------------------------------------------------------------------
        """
        choix = None
        while choix == None:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if self.etat == 'menu_principal':
                    choix = self.menu_principal.gerer_event(event)
                    if choix is not None:
                        #Nous pensions faire une extension où l'algorithme pourrait lire un fichier texte, mais nous avons ecrit aucun fichier txt.
                        """
                            if choix == 0:
                            fichier = input ("veuillez rentrer le nom de la liste d'avion: ")
                            with open(fichier, 'r') as f:
                                tas =[]
                                lignes = f.readlines()
                                for i in range(len(lignes)):
                                    a = Avion(lignes[i][0],lignes[i][1],lignes[i][2],lignes[i][3])
                                    tas.append(a)
                                b = Aeroport(tas)
                        """ 
                        if choix == 0:
                            tas = creer_avions_aleatoires(10)
                            a = Aeroport(tas)
            if self.etat == 'menu_principal':
                self.menu_principal.dessiner()
            pygame.display.flip()
            self.clock.tick(30)
        pygame.quit()
        return tas,a

    def partie(self,tas,aeroport):
        """
        Permet de lancer une partie  , de l'afficher , de lancer un tour temps que la taille du tas n'est pas egale a 0
        De plus, permet d'ajouter de nouveaux avions a ce tas du au traffic aerien assez susceptible
        """
        pygame.init()
        self.music = MusicPlayer(["musique_attente.mp3"])
        clock = pygame.time.Clock()
        font = pygame.font.SysFont(None, 24)
        font2 =  pygame.font.SysFont(None, 54)
        tas = pivot(tas)
        fenetre = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        hauteur = fenetre.get_height()
        largeur = fenetre.get_width()

        aeroport_image = pygame.image.load("Imageaeroport.png").convert()
        avion_image = pygame.image.load("imageavion.png").convert_alpha()
        clipboard = pygame.image.load("clipboard.png").convert_alpha()
        image_de_fond =  pygame.image.load('image_de_fond.jpg').convert_alpha()
        image_de_fond = pygame.transform.scale(image_de_fond,(largeur,hauteur))
        aeroport_image = pygame.transform.scale(aeroport_image,(largeur//2,hauteur))
        avion_image = pygame.transform.scale(avion_image,(largeur//6,hauteur // 6))
        clipboard = pygame.transform.scale(clipboard,(largeur//2, hauteur ))

        continuer = 1
        temps_ecouler = 0
        reserve = creer_avions_aleatoires(8)
        while continuer:
            print('temps:',temps_ecouler)
            print('tas: ', aeroport.t)
            keyb= pygame.key.get_pressed()
            for event in pygame.event.get():
                pass
            if keyb[K_ESCAPE]:
                continuer = 0
            if temps_ecouler != 0:
                aeroport.tourunique()
                if len(reserve)>=1:
                    aeroport.t = aeroport.t.ajouter(reserve.pop())
            

            
            fenetre.blit(aeroport_image,(largeur//2,0))
            fenetre.blit(clipboard,(0,hauteur - clipboard.get_height()))
            increment_hauteur_texte = hauteur *(1/3)
            texte = print_tas(aeroport.t)
            texte = texte.split('_')[1:]
            cmpt = 0
            for txt in texte:
                if cmpt == 10:
                    break
                transformer_en_font = font.render(txt,True,(0,0,0))
                fenetre.blit(transformer_en_font,(largeur//8,increment_hauteur_texte))
                increment_hauteur_texte += hauteur//20
                cmpt += 1
            if aeroport.t.taille() != 0:
                animation_atterrissage(avion_image,aeroport_image,largeur,hauteur,fenetre)
            pygame.display.flip()
            temps_ecouler += 1 #Permet de garder compte du nbre de tour
            clock.tick(1)
            if aeroport.t.taille() == 0:
                boucle_inf = 1
                attendre = 15 #Attente pour qu'en ne cliquant qu'une seule fois sur la fleche il n'y est pas plusieurs actions
                i_pos_curseur = 0
                while boucle_inf: #Boucle infini pour faire apparaitre l'écran de redémarage jusqu'à ce que le joueur face un choix
                    keyb = pygame.key.get_pressed()
                    for event in pygame.event.get():
                        pass
                    if keyb[K_RETURN]:
                        boucle_inf = 0
                    if keyb[K_UP]:
                        if attendre > 15:
                            i_pos_curseur -=1 #Grace au modulo on restera dans une range de 0 à 2 malgré les -1 et +1
                            attendre = 0
                    if keyb[K_DOWN]:
                        if attendre > 15:
                            i_pos_curseur +=1
                            attendre = 0
                    fenetre.blit(image_de_fond,(0,0))
                    if i_pos_curseur%2 == 0:
                        fenetre.blit(font2.render('Recommencer?',True,(255,255,255)),(largeur/3,hauteur // 3)) #Affiche en blanc ou en noir suivant notre séléction
                        fenetre.blit(font2.render('Quitter',True,(0,0,0)),(largeur//3, 2 * hauteur // 3))
                    else:
                        fenetre.blit(font2.render('Recommencer?',True,(0,0,0)),(largeur/3,hauteur // 3))
                        fenetre.blit(font2.render('Quitter',True,(255,255,255)),(largeur//3,2 * hauteur // 3))
                    fenetre.blit(font2.render('Votre journée de travaille est terminée!',True,(0,0,0)),(largeur //3,  hauteur // 5))
                    pygame.display.flip()
                    attendre += 1
                    self.clock.tick(60)
                    
                if i_pos_curseur%2 == 0:
                    nouvelle_reserve = creer_avions_aleatoires(30)
                    aeroport.t = liste_en_tas(nouvelle_reserve)
                    reserve = creer_avions_aleatoires(10)
                    fenetre.fill((0,0,0))
                else :
                    continuer  = False
        pygame.quit()
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

jeu = choisir()
tas,aeroport = jeu.choix_du_mode()
jeu.partie(tas,aeroport)
pygame.quit()
