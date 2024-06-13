from random import *
import os
import sys
import pygame


def constructeurElement(type, selected = False):  # Prend un entier en argument et renvoie un élément + Par défaut selected est en False jusqu'au passage en True
    if type == 0:
        cell = Feu()
    if type == 1:
        cell = Eau()
    if type == 2:
        cell = Air()
    if type == 3:
        cell = Terre()
    cell.selected = selected
    return cell


class Element(object):
    IMG_FOLDER = "img"

    def __init__(self, effet, mouvement):
        self.selected = False
        self.effet = effet
        self.mouvement = mouvement

    def switchSelected(self):
        self.selected = not self.selected

    def paint(self, screen, x, y):
        if self.selected:
            screen.blit(self.getSelectedImage(), (x, y))
        else:
            screen.blit(self.getImage(), (x, y))

    def paintSelected(self, screen, x, y):
        screen.blit(self.getSelectedImage(), (x, y))

    def getNom(self):
        return "j'ai pas de nom"

    def toString(self):
        return "je suis l'élément {} d'effet {} et de mouvement {}".format(self.getNom(), self.effet, self.mouvement)


class Feu(Element):
    PATH_IMG_ELT = os.path.join(Element.IMG_FOLDER, "feu.png")
    PATH_IMG_SLCT_ELT = os.path.join(Element.IMG_FOLDER, "selected_feu.png")

    def __init__(self):
        super().__init__("Brûle", "Attaque")

    def getNom(self):
        return "F"

    def getImage(self):
        return pygame.image.load(Feu.PATH_IMG_ELT)

    def getSelectedImage(self):
        return pygame.image.load(Feu.PATH_IMG_SLCT_ELT)

    def getDammage(self):
        return 20


class Air(Element):
    PATH_IMG_ELT = os.path.join(Element.IMG_FOLDER, "air.png")
    PATH_IMG_SLCT_ELT = os.path.join(Element.IMG_FOLDER, "selected_air.png")

    def __init__(self):
        super().__init__("Protège", "Protège")

    def getNom(self):
        return "A"

    def getImage(self):
        return pygame.image.load(Air.PATH_IMG_ELT)

    def getSelectedImage(self):
        return pygame.image.load(Air.PATH_IMG_SLCT_ELT)


class Eau(Element):
    PATH_IMG_ELT = os.path.join(Element.IMG_FOLDER, "eau.png")
    PATH_IMG_SLCT_ELT = os.path.join(Element.IMG_FOLDER, "selected_eau.png")

    def __init__(self):
        super().__init__("Soigne", "Soigne")

    def getNom(self):
        return "E"

    def getImage(self):
        return pygame.image.load(Eau.PATH_IMG_ELT)

    def getSelectedImage(self):
        return pygame.image.load(Eau.PATH_IMG_SLCT_ELT)

    def getSoin(self):
        return 15


class Terre(Element):
    PATH_IMG_ELT = os.path.join(Element.IMG_FOLDER, "terre.png")
    PATH_IMG_SLCT_ELT = os.path.join(Element.IMG_FOLDER, "selected_terre.png")

    def __init__(self):
        super().__init__("Etourdit", "Attaque")

    def getNom(self):
        return "T"

    def getImage(self):
        return pygame.image.load(Terre.PATH_IMG_ELT)

    def getSelectedImage(self):
        return pygame.image.load(Terre.PATH_IMG_SLCT_ELT)

    def getDammage(self):
        return 10
