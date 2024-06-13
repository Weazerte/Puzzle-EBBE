import pygame
from elements import *


class Personnage(object):
    def __init__(self, hp, etat):
        self.hp = hp
        self.etat = etat

    def getNom(self):
        return "j'ai pas de nom"

    def toString(self):
        return " je suis le personnage {} j'ai {} hp et d'état {}".format(self.getNom(), self.hp, self.etat)

    def paint(self, screen, mon_tour):
        font = pygame.font.SysFont(None, 24)
        img = font.render('HP = {}'.format(self.getHP()),
                          True, self.couleurAffichage())
        img2 = font.render('État = {}'.format(self.etat),
                           True, self.couleurAffichage())
        screen.blit(img, self.coordonneesAffichage())
        screen.blit(img2, tuple(
            map(lambda i, j: i + j, self.coordonneesAffichage(), (0, 20))))

        font = pygame.font.SysFont(None, 40)
        self.update_health_bar_joueur(screen)

       # Affiche lavatar de l'adversaire et son cadre
        pygame.draw.rect(screen, (20,0,0), ((810,90),(170,170)))
        img_adversaire = pygame.image.load("img/adversaire_un.png").convert_alpha()
        img_adversaire = pygame.transform.scale(img_adversaire, (150,150))
        screen.blit(img_adversaire, (820,100))

        # Affiche l'avatar du joueur et son cadre
        pygame.draw.rect(screen, (0,0,20), ((30,90),(170,170)))
        img_joueur = pygame.image.load("img/joueur_un.png").convert_alpha()
        img_joueur = pygame.transform.scale(img_joueur, (150,150))
        screen.blit(img_joueur, (40,100))


        Le_Tour = font.render("C'est au tour de :", True,(255,255,255))
        screen.blit(Le_Tour, (380, 20))
        if mon_tour:  # Alternation de l'affichage du tour
            affiche_tour = font.render("{}".format(
                'Joueur'), True, Joueur().couleurAffichage())
            coord_affichage = (450,60)
        else:
            affiche_tour = font.render("{}".format(
                'Adversaire'), True, Adversaire().couleurAffichage())
            coord_affichage = (420,60)
        screen.blit(affiche_tour, coord_affichage)

    def zerohp(self):
        if(self.grille.joueur.hp <= 0):
            print("Vous avez perdu !")
            pygame.quit()
        elif(self.grille.adversaire.hp <=0 ):
            print("Vous avez gagnez !")
            pygame.quit() 
        else:
            pass


    def update_health_bar_joueur(self, screen):

        #definir couleur arriere plan barre de vie
        back_bar_color = (169, 169, 169)
        arround_bar_color = (0,0,0)
        #definir la position, largeur et epaisseur
        bar_position = pygame.Rect(self.coordonneesAffichageBar(), (self.hp, 20))

        #definir la position de l'arriere plan de la barre de vie
        back_bar_position = pygame.Rect(self.coordonneesAffichageBar(), (200, 20))

        arround_bar_position = pygame.Rect(self.coordoneesAffichageArroundBar(), (210,30))

        #dessiner la barre de vie
        pygame.draw.rect(screen, arround_bar_color, arround_bar_position)
        pygame.draw.rect(screen, back_bar_color, back_bar_position)
        pygame.draw.rect(screen, self.couleurAffichage(), bar_position)



class Joueur(Personnage):
    def __init__(self):
        super().__init__(200, "neutre")

    def getNom(self):
        return "joueur"

    def getHP(self):
        return self.hp

    def coordonneesAffichage(self):
        return (20, 50)

    def coordonneesAffichageBar(self):
        return(20,20)

    def coordoneesAffichageArroundBar(self):
        return(15,15)

    def couleurAffichage(self):
        return (0, 50, 255)


class Adversaire(Personnage):
    def __init__(self):
        super().__init__(200, "neutre")

    def getNom(self):
        return "adversaire"

    def getHP(self):
        return self.hp

    def coordonneesAffichage(self):
        return (780, 50)

    def coordonneesAffichageBar(self):
        return(780,20)

    def coordoneesAffichageArroundBar(self):
        return(775,15)


    def couleurAffichage(self):
        return (255, 0, 0)

    def comportement(self, screen, mon_tour, grille):
        if not self.etat == "Etourdit":
            self.etat = "neutre"
            if grille.joueur.etat == "Protégé": #Si le joueur est protégé, l'adversaire lancera une protection ou un soin
                print('protégé')
                if self.hp > 185: # Si l'adversaire à plus de 185hp, il ne se soignera pas.
                    grille.lancer_action(screen, constructeurElement(2), grille.adversaire, grille.joueur, mon_tour)
                else :
                    grille.lancer_action(screen, constructeurElement(
                                    randint(1,2)), grille.adversaire, grille.joueur, mon_tour)
                    return None
            elif grille.joueur.hp <=20: #Lance le coup de grâce avec feu
                print('coup grace feu')
                grille.lancer_action(screen, constructeurElement(
                                    0), grille.adversaire, grille.joueur, mon_tour)
            elif grille.joueur.hp <=10: #Lance le coup de grâce
                print('coup grace')
                liste = [0,3]
                grille.lancer_action(screen, constructeurElement(
                                    liste[randint(0,1)]), grille.adversaire, grille.joueur, mon_tour)
            elif self.hp <= 20: #L'adversaire se soigne ou se protège si il est vulnérable
                print('adversaire vulnérable')
                grille.lancer_action(screen, constructeurElement(
                                    randint(1,2)), grille.adversaire, grille.joueur, mon_tour)
            elif self.hp >= 185: # Si l'adversaire à plus de 185hp, il ne se soignera pas.
                liste = [0,2,3]
                grille.lancer_action(screen, constructeurElement(
                                    liste[randint(0,2)]), grille.adversaire, grille.joueur, mon_tour)
            else:
                print('autre')
                grille.lancer_action(screen, constructeurElement(
                                    randint(0, 3)), grille.adversaire, grille.joueur, mon_tour)
        else:
            print("L'adversaire est étourdi, il passe son tour")
            self.etat = "neutre"
