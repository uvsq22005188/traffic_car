import tkinter as tk
import os


class Voiture():
    def __init__(self, x, y, couleur):
        pass


class Route():
    def __init__(self, id, x1, y1, x2, y2):
        self.id = id
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2


class Ville():
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes("-fullscreen", True)
        self.root.iconbitmap("Images/icon.ico")

        self.creer_menu()
        self.creer_canvas()

        self.route = []
        self.voiture = []

        self.root.mainloop()

    def creer_menu(self):
        self.menu_bar = tk.Menu(self.root, tearoff=0)

        self.menu_Fichier = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_Fichier.add_command(label="Charger", command=self.charger)
        self.menu_Fichier.add_command(label="Enregistrer", command=self.enregistrer)

        self.menu_Création = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_Création.add_command(label="Nouvelle route", command=self.creer_route)
        self.menu_Création.add_command(label="Nouvelle voiture", command=self.creer_voiture)

        self.menu_Aide = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_Aide.add_command(label="Aide", command=lambda: os.system("start https://github.com/uvsq22005188/traffic_car"))
        self.menu_Aide.add_command(label="Quitter", command=self.root.destroy)

        self.menu_bar.add_cascade(label="Fichier", menu=self.menu_Fichier)
        self.menu_bar.add_cascade(label="Création", menu=self.menu_Création)
        self.menu_bar.add_cascade(label="Aide", menu=self.menu_Aide)
        self.root.config(menu=self.menu_bar)

    def creer_canvas(self):
        self.canvas = tk.Canvas(self.root, highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.focus_set()

    def creer_route(self):
        self.coords = []
        self.stop = False
        self.croisement = False
        self.canvas.bind("<Button-1>", lambda e: self.coords.append((e.x, e.y)))
        self.canvas.bind("<Escape>", lambda _: self.setVar("stop", True))
        self.canvas.config(cursor="crosshair")
        while len(self.coords) < 2:
            if self.stop:
                self.coords = []
                self.canvas.unbind("<Button-1>")
                self.canvas.unbind("<Escape>")
                self.canvas.config(cursor="arrow")
                return
            self.wait(100)

        x1, y1, x2, y2 = (e for liste in self.coords for e in liste)

        for route in self.route:
            if abs(route.x1 - x1) < 25 and abs(route.y1 - y1) < 25:
                x1, y1 = route.x1, route.y1
                self.croisement = True
            if abs(route.x2 - x1) < 25 and abs(route.y2 - y1) < 25:
                x1, y1 = route.x2, route.y2
                self.croisement = True
            if abs(route.x1 - x2) < 25 and abs(route.y1 - y2) < 25:
                x2, y2 = route.x1, route.y1
                self.croisement = True
            if abs(route.x2 - x2) < 25 and abs(route.y2 - y2) < 25:
                x2, y2 = route.x2, route.y2
                self.croisement = True

            if (x1, y1) == (x2, y2) or (x1, y1, x2, y2) == (route.x1, route.y1, route.x2, route.y2):
                self.coords = []
                self.canvas.unbind("<Button-1>")
                self.canvas.unbind("<Escape>")
                self.canvas.config(cursor="arrow")
                return

        if self.croisement:
            id = self.canvas.create_line(x1, y1, x2, y2, width=1)
            # self.canvas.create_line(x1, y1, x2, y2, width=40, fill="white")
            # self.canvas.create_line(x1, y1, x2, y2, width=10, fill="black", dash=(20, 5))
            pass
        else:
            id = self.canvas.create_line(x1, y1, x2, y2, width=1)
            # self.canvas.create_line(x1, y1, x2, y2, width=40, fill="white")
            # self.canvas.create_line(x1, y1, x2, y2, width=10, fill="black", dash=(20, 5))
        self.route.append(Route(id, x1, y1, x2, y2))
        self.canvas.config(cursor="arrow")
        self.stop = False
        self.canvas.unbind("<Button-1>")
        self.canvas.unbind("<Escape>")

    def wait(self, ms):
        var = tk.IntVar()
        self.root.after(ms, lambda: var.set(1))
        self.root.wait_variable(var)

    def setVar(self, var, value):
        setattr(self, var, value)

    def creer_voiture(self):
        self.coords = []
        self.stop = False
        self.canvas.bind("<Button-1>", lambda e: self.coords.append((e.x, e.y)))
        self.canvas.bind("<Escape>", lambda _: self.setVar("stop", True))
        self.canvas.config(cursor="crosshair")
        while len(self.coords) < 1:
            if self.stop:
                self.coords = []
                self.canvas.unbind("<Button-1>")
                self.canvas.unbind("<Escape>")
                self.canvas.config(cursor="arrow")
                return
            self.wait(100)

        x, y = self.coords[0]
        l1 = self.canvas.find_overlapping(x - 25, y - 25, x + 25, y + 25)
        if l1 != []:

            self.voiture.append(Voiture(x, y))

    def charger(self):
        pass

    def enregistrer(self):
        pass


ville = Ville()
