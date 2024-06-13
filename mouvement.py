from personnage import*
from elements import*


class Mouvement():
    def __init__(self, elem, lanceur, receveur):
        self.elem = elem
        self.lanceur = lanceur
        self.receveur = receveur

    def toDo(self):
        if self.elem.getNom() == 'F':
            self.attaque()
            print(self.lanceur.getNom(), "lance une attaque FEU sur",
                  self.receveur.getNom(), ". Il a désormais", self.receveur.hp, "hp")
        elif self.elem.getNom() == 'T':
            self.attaque()

            print(self.lanceur.getNom(), "lance une attaque TERRE sur",
                  self.receveur.getNom(), ". Il a désormais", self.receveur.hp, "hp")
            if randint(0, 1) < 1:
                self.etourdit()
                print("L'adversaire à été étourdit")
        elif self.elem.getNom() == 'E':
            self.soin()
            print(self.lanceur.getNom(),
                  "lance un  soin EAU. Il a désormais", self.lanceur.hp, "hp")
        else:
            self.protection()
            print(self.lanceur.getNom(), "lance une attaque AIR . Il est protégé")

    def attaque(self):
        if self.receveur.hp > self.elem.getDammage():
            self.receveur.hp -= self.elem.getDammage()
        else:
            self.receveur.hp = 0

    def soin(self):
        if self.lanceur.hp < 185:
            self.lanceur.hp += self.elem.getSoin()
        else:
            self.lanceur.hp = 200

    def protection(self):
        self.lanceur.etat = "Protégé"

    def etourdit(self):
        self.receveur.etat = "Etourdit"
