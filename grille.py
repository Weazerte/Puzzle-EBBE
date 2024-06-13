from elements import *
from random import *
from personnage import *
from mouvement import *
import time


def creer_grille():
    grille = []
    n = 0
    for i in range(Grille.TAILLE):
        for j in range(Grille.TAILLE):
            grille.append(randint(0, 3))
            n += 1
            if n == 4:
                n = 0
    return grille


class Interface(object):
    WIDTH = 1000
    HEIGHT = 800
    IMG_BACKGROUND = pygame.image.load('img/wood_background.jpg')
    IMG_BACKGROUND = pygame.transform.scale(IMG_BACKGROUND, (1000,800))

    def __init__(self, grille):
        self.grille = grille
        self.grille.tests_debut()
        pygame.init()
        self.height = Interface.HEIGHT
        self.width = Interface.WIDTH
        pygame.display.set_caption("Puzzle EBBE")
        self.screen = pygame.display.set_mode((self.width, self.height))

    def run(self):
        running = True
        memoire = None
        mon_tour = True
        while running:
            self.paint(mon_tour)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if mon_tour:  # Entre dans le tour du joueur
                    if not self.grille.joueur.etat == "Etourdit":
                        self.grille.joueur.etat = 'neutre'
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            selected = self.grille.handleMouse(
                                pygame.mouse.get_pos())
                            if not memoire:  # Si rien n'est sélectionné
                                memoire = selected
                                # self.grille.paintSelected(
                                # self.screen, pygame.mouse.get_pos())
                            else:  # Si une case est déjà sélectionnée
                                if memoire == selected:  # Permet d'annuler une sélection
                                    memoire = None
                                else:  # Lance l'action
                                    if self.grille.adjacent(selected, memoire):
                                        self.grille.switch(selected, memoire)
                                        if not self.grille.adversaire.etat == "Protégé":  # lance attaque si adversaire non protégé
                                            self.grille.joueur.etat = "neutre"
                                            self.grille.lancer_action(self.screen, self.grille.contentByCoord(
                                                pygame.mouse.get_pos()), self.grille.joueur, self.grille.adversaire, mon_tour)
                                        elif (self.grille.contentByCoord(
                                                pygame.mouse.get_pos()).getNom() == "F") or (self.grille.contentByCoord(
                                                pygame.mouse.get_pos()).getNom() == "T"):  # Tentative d'attaque alors que adversaire protégé
                                            print(
                                                "Coup annulé, l'ennemi était protégé")
                                        else:
                                            self.grille.joueur.etat = "neutre"
                                            self.grille.lancer_action(self.screen, self.grille.contentByCoord(
                                                pygame.mouse.get_pos()), self.grille.joueur, self.grille.adversaire, mon_tour)

                                        memoire = None
                                        mon_tour = False
                                    else:  # Annule le coup car non adjacent
                                        memoire = None
                    else:  # Annule car joueur étourdit
                        mon_tour = False
                        print('Vous êtes étourdit, vous passez votre tour')
                        self.grille.joueur.etat = "neutre"
                else:  # Entre dans le tour du bot
                    self.grille.tests_comb(self.screen, mon_tour)
                    self.paint(mon_tour)
                    time.sleep(2)
                    self.grille.adversaire.comportement(self.screen, mon_tour, self.grille)
                    mon_tour = True
                    print(
                        '--------------------------------------------------------------')
        pygame.quit()

    def paint(self, mon_tour):
        self.grille.paint(self.screen, mon_tour)
        pygame.display.flip()

    def affichage_tour(self):
        pass


surfaceW = 1000 #Dimension de la fenêtre / Largeur
surfaceH = 800 #Dimension de la fenêtre / Longueur
 
class Menu :
    """ Création et gestion des boutons d'un menu """
    def __init__(self, application, *groupes) :
        self.couleurs = dict(
            normal=(0, 0, 0),
            survol=(50, 50, 50),
        )
        font = pygame.font.SysFont('Helvetica', 24, bold=True)
        # noms des menus et commandes associées
        items = (
            ('JOUER', application.jeu),
            ('QUITTER', application.quitter)
        )
        x = 500
        y = 280
        self._boutons = []
        for texte, cmd in items :
            mb = MenuBouton(texte,self.couleurs['normal'],font,x,y,200,50,cmd)
            self._boutons.append(mb)
            y += 120
            for groupe in groupes :
                groupe.add(mb)
 
    def update(self, events) :
        clicGauche, *_ = pygame.mouse.get_pressed()
        posPointeur = pygame.mouse.get_pos()
        for bouton in self._boutons :
            # Si le pointeur souris est au-dessus d'un bouton
            if bouton.rect.collidepoint(*posPointeur) :
                # Changement du curseur par un quelconque
                pygame.mouse.set_cursor(*pygame.cursors.tri_left)
                # Changement de la couleur du bouton
                bouton.dessiner(self.couleurs['survol'])
                # Si le clic gauche a été pressé
                if clicGauche :
                    # Appel de la fonction du bouton
                    bouton.executerCommande()
                break
            else :
                # Le pointeur n'est pas au-dessus du bouton
                bouton.dessiner(self.couleurs['normal'])
        else :
            # Le pointeur n'est pas au-dessus d'un des boutons
            # initialisation au pointeur par défaut
            pygame.mouse.set_cursor(*pygame.cursors.arrow)
 
    def detruire(self) :
        pygame.mouse.set_cursor(*pygame.cursors.arrow) # initialisation du pointeur
 
 
 
class MenuBouton(pygame.sprite.Sprite) :
    """ Création d'un simple bouton rectangulaire """
    def __init__(self, texte, couleur, font, x, y, largeur, hauteur, commande) :
        super().__init__()
        self._commande = commande
 
        self.image = pygame.Surface((largeur, hauteur))
 
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
 
        self.texte = font.render(texte, True, (200, 200, 200))
        self.rectTexte = self.texte.get_rect()
        self.rectTexte.center = (largeur/2, hauteur/2)
 
        self.dessiner(couleur)
 
    def dessiner(self, couleur) :
        self.image.fill(couleur)
        self.image.blit(self.texte, self.rectTexte)
 
    def executerCommande(self) :
        # Appel de la commande du bouton
        self._commande()
 

class Application :
    """ Classe maîtresse gérant les différentes interfaces du jeu """
    def __init__(self) :
        pygame.init()
        pygame.display.set_caption("puzzle EBBE")
 
        self.fond = pygame.image.load('img/auberge.jpg') 
        
        self.fenetre = pygame.display.set_mode((surfaceW,surfaceH))
        # Groupe de sprites utilisé pour l'affichage
        self.groupeGlobal = pygame.sprite.Group()
        self.statut = True
 
    def _initialiser(self) :
        try:
            self.ecran.detruire()
            # Suppression de tous les sprites du groupe
            self.groupeGlobal.empty()
        except AttributeError:
            pass
 
    def menu(self) :
        # Affichage du menu
        self._initialiser()
        self.ecran = Menu(self, self.groupeGlobal)
 
    def jeu(self) :
        # Affichage du jeu
        Interface(Grille(creer_grille(), Joueur(), Adversaire())).run()
 
    def quitter(self) :
        self.statut = False
 
    def update(self) :
        events = pygame.event.get()
 
        for event in events :
            if event.type == pygame.QUIT :
                self.quitter()
                return
 
        self.fenetre.blit(self.fond,(0,0))
        self.ecran.update(events)
        self.groupeGlobal.update()
        self.groupeGlobal.draw(self.fenetre)
        pygame.display.update()


class Grille(object):
    TAILLE = 8
    CELLULE = 66
    OFFSETX = (Interface.WIDTH / 2) - ((TAILLE*CELLULE) / 2)
    OFFSETY = (Interface.HEIGHT / 2) - ((TAILLE*CELLULE) / 2)

    def __init__(self, details, joueur, adversaire):
        self.cells = []
        self.joueur = joueur
        self.adversaire = adversaire
        for detail in details:  # Passe de la grille de chiffres à une grille d'élements
            self.cells.append(constructeurElement(detail))

    def handleMouse(self, pos):
        grille_xmax = self.OFFSETX + self.TAILLE * \
            self.CELLULE  # Valeur max en x de la grille
        grille_ymax = self.OFFSETY + self.TAILLE * \
            self.CELLULE  # Valeur max en y de la grille
        # Test si le clic est à l'intérieur de la grille
        if self.OFFSETX < pos[0] and pos[0] < grille_xmax and self.OFFSETY < pos[1] and pos[1] < grille_ymax:
            valeur_j = int((pos[0] - self.OFFSETX) / self.CELLULE)
            valeur_i = int((pos[1] - self.OFFSETY) / self.CELLULE)
            # Renvoie le couple de coordonnées de la case dans la grille (0 <= i/j <= 8)
            return (valeur_i, valeur_j)
        return (-1, -1)

    # Renvoie l'élément présent dans la grille aux coord de la souris au moment du clic (utilise handleMouse)
    def contentByCoord(self, pos):
        if Grille.handleMouse(self, pos) == (-1, -1):
            pass
        else:
            cellule_visee = Grille.handleMouse(self, pos)
            indexGrille = cellule_visee[0]*8 + cellule_visee[1]
            element = self.cells[indexGrille]
            return element

    def lancer_action(self, screen, element, lanceur, receveur, mon_tour):
        Mouvement(element, lanceur, receveur).toDo()
        self.paint(screen, mon_tour)

    def paint(self, screen, mon_tour):
        
        screen.blit(Interface.IMG_BACKGROUND,(0,0))
        color = (0,0,0)
        pygame.draw.rect(screen, color, pygame.Rect(self.OFFSETX-8, self.OFFSETY-8, self.TAILLE*(self.CELLULE+1)+8, self.TAILLE*(self.CELLULE+1)+8))
        for i in range(self.TAILLE):
            for j in range(self.TAILLE):
                # paint de la cellule (i, j)
                self.cells[i * self.TAILLE + j].paint(
                    screen, self.OFFSETX + j * self.CELLULE, self.OFFSETY + i * self.CELLULE)
        self.joueur.paint(screen, mon_tour)
        self.adversaire.paint(screen, mon_tour)

    # def paintSelected(self, screen, memoire):
    #     cellule_visee = Grille.handleMouse(self, memoire)
    #     indexGrille = cellule_visee[0]*8 + cellule_visee[1]
    #     self.cells[indexGrille].paintSelected(
    #         screen, self.OFFSETX + cellule_visee[0] * self.CELLULE, self.OFFSETY + cellule_visee[1] * self.CELLULE)

    def adjacent(self, pos_1, pos_2):
        if pos_1 == (-1, -1) or pos_2 == (-1, -1):
            return False
        i = pos_1[0]  # /!\ VOIR SI ON PEUT CHANGER /!\
        j = pos_1[1]
        k = pos_2[0]
        l = pos_2[1]
        if abs((i-k)) == 1 and abs((j-l)) == 0:
            return True
        elif abs((j-l)) == 1 and abs((i-k)) == 0:
            return True
        else:
            return False

    def switch(self, pos_1, pos_2):  # Switch deux cellules
        indexGrille_1 = pos_1[0]*8 + pos_1[1]
        indexGrille_2 = pos_2[0]*8 + pos_2[1]
        transit = self.cells[indexGrille_1]
        self.cells[indexGrille_1] = self.cells[indexGrille_2]
        self.cells[indexGrille_2] = transit

    def horizontal(self, type):
        for i in range(Grille.TAILLE):
            for j in range(Grille.TAILLE - 2):
                n = 0
                while j + n < Grille.TAILLE and self.cells[i * Grille.TAILLE + j + n].getNom() == type.getNom():
                    n += 1
                if n >= 3:
                    return (i, j, n, type)
        return (0, 0, 0)

    def vertical(self, type):
        for j in range(Grille.TAILLE):
            for i in range(Grille.TAILLE - 2):
                n = 0
                while i + n < Grille.TAILLE and self.cells[(i + n) * Grille.TAILLE + j].getNom() == type.getNom():
                    n += 1
                if n >= 3:
                    return (i, j, n, type)
        return (0, 0, 0)

    # remplace les series d'élément verticales par des nouveaux éléments aléatoires
    def remplacer_vertical(self, i, j, n):
        for nb in range(n):
            self.cells[(i+nb)*Grille.TAILLE + j] = constructeurElement(randint(0, 3))

    # remplace les series d'élément horizontales par des nouveaux éléments aléatoires
    def remplacer_horizontal(self, i, j, n):
        for nb in range(j, n+j):
            self.cells[i * Grille.TAILLE + nb] = constructeurElement(randint(0, 3))

    def tests_debut(self):  # test début et rend la grille triée sans combinaisons
        for elmt in range(4):
            element = constructeurElement(elmt)
            result1 = self.horizontal(element)
            result2 = self.vertical(element)
            while result1[2] != 0 or result2[2] != 0:
                if result1[2] != 0:
                    self.remplacer_horizontal(
                        result1[0], result1[1], result1[2])
                    self.tests_debut()
                if result2[2] != 0:
                    self.remplacer_vertical(result2[0], result2[1], result2[2])
                    self.tests_debut()
                result1 = self.horizontal(element)
                result2 = self.vertical(element)

    def tests_comb(self, screen, mon_tour):
        for elmt in range(4):
            element = constructeurElement(elmt)
            result1 = self.horizontal(element)
            result2 = self.vertical(element)
            while result1[2] != 0 or result2[2] != 0:
                if result1[2] != 0:
                    self.remplacer_horizontal(result1[0], result1[1], result1[2])
                    self.paint(screen, mon_tour)
                    pygame.display.flip()
                    time.sleep(0.5)
                    self.tests_comb(screen, mon_tour)
                if result2[2] != 0:
                    self.remplacer_vertical(result2[0], result2[1], result2[2])
                    self.paint(screen, mon_tour)
                    pygame.display.flip()
                    time.sleep(0.5)
                    self.tests_comb(screen, mon_tour)
                result1 = self.horizontal(element)
                result2 = self.vertical(element)


"""Interface(Grille(creer_grille(), Joueur(), Adversaire())).run()"""
app = Application()
app.menu()
 
clock = pygame.time.Clock()
 
while app.statut :
    app.update()
    clock.tick(30)
 
pygame.quit()