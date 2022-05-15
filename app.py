import tkinter as tk
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
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
        self.root.configure(bg='darkgrey')
        self.root.attributes("-fullscreen", True)
        self.root.iconbitmap("Images/icon.ico")

        self.charger_image()
        self.creer_menu()
        self.creer_canvas()

        self.route = []
        self.voiture = []
        self.stop = False
        self.order = []

        self.root.mainloop()

    def charger_image(self):
        self.image = {}
        self.image["route"] = {
            i: ImageTk.PhotoImage(Image.open(f"Images/Route/route_{i}.png")) for i in range(1, 5)
        }
        self.image["tournant"] = {
            i: ImageTk.PhotoImage(Image.open(f"Images/Tournant/tournant_{i}.png")) for i in range(1, 5)
        }
        self.image["rp"] = {
            1: {i: ImageTk.PhotoImage(Image.open(f"Images/Rond_point/1/rp_{i}.png")) for i in range(1, 5)},
            2_1: {i: ImageTk.PhotoImage(Image.open(f"Images/Rond_point/2_1/rp_{i}.png")) for i in range(1, 5)},
            2_2: {i: ImageTk.PhotoImage(Image.open(f"Images/Rond_point/2_2/rp_{i}.png")) for i in range(1, 3)},
            3: {i: ImageTk.PhotoImage(Image.open(f"Images/Rond_point/3/rp_{i}.png")) for i in range(1, 5)},
            4: {1: ImageTk.PhotoImage(Image.open(f"Images/Rond_point/4/rp_1.png"))}
        }
        self.image["voiture"] = {
            i: ImageTk.PhotoImage(Image.open(f"Images/Voiture/voiture_{i}.png")) for i in range(1, 5)
        }

    def placer_route(self, img):
        """"""
        self.canvas.bind("<Motion>", lambda e,
                         img=img: self.image_motion(e, img))
        self.canvas.bind("<Button-1>", lambda e: self.setVar("stop", True))

    def image_motion(self, event, img):
        x, y = event.x, event.y
        self.canvas.delete("motion")
        self.canvas.create_image(x, y, image=img, tag="motion")
        if self.stop:
            self.canvas.unbind("<Motion>")
            self.canvas.unbind("<Button-1>")
            self.canvas.delete("motion")
            self.stop = False
            # Placement de la route
            x1 = ((19 * x) // 1900) * 100 + 50
            y1 = ((10 * y) // 1000) * 100 + 50
            self.order.append(self.canvas.create_image(x1, y1, image=img))
            self.canvas.update()
            return

    def creer_menu(self):
        self.menu_bar = tk.Menu(self.root, tearoff=0)

        self.menu_Fichier = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_Fichier.add_command(label="Charger", command=self.charger)
        self.menu_Fichier.add_command(
            label="Enregistrer", command=self.enregistrer)

        self.menu_Création = tk.Menu(self.menu_bar, tearoff=0)
        # self.menu_Création.add_command(label="Nouvelle route", command=self.creer_route)
        self.menu_Création.add_command(
            label="Nouvelle voiture", command=self.creer_voiture)
        self.menu_Création.add_command(
            label="Undo", command=lambda: self.canvas.delete(self.order.pop()))

        # menu_voiture
        self.menu_Voiture = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_Création.add_cascade(label="Voiture", menu=self.menu_Voiture)
        for i in range(1, 5):
            self.menu_Voiture.add_command(
                image=self.image['voiture'][i], command=lambda i=i: self.creer_voiture(i))
        # menu route
        self.menu_Route = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_Création.add_cascade(label="Route", menu=self.menu_Route)
        for i in range(1, 5):
            self.menu_Route.add_command(
                image=self.image['route'][i], command=lambda i=i: self.placer_route(self.image['route'][i]))

        # menu tournant
        self.menu_Tourant = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_Création.add_cascade(label="Tourant", menu=self.menu_Tourant)
        for i in range(1, 5):
            self.menu_Tourant.add_command(
                image=self.image['tournant'][i], command=lambda i=i: self.placer_route(self.image['tournant'][i]))

        # menu rond-point
        self.menu_Rond_point = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_Création.add_cascade(
            label="Rond-point", menu=self.menu_Rond_point)

        # menu rond-point 1
        self.menu_RP1 = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_Rond_point.add_cascade(
            label="Rond-point 1", menu=self.menu_RP1)
        for i in range(1, 5):
            self.menu_RP1.add_command(
                image=self.image['rp'][1][i], command=lambda i=i: self.placer_route(self.image['rp'][1][i]))

        # menu rond-point 2-1
        self.menu_RP2 = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_Rond_point.add_cascade(
            label="Rond-point 2", menu=self.menu_RP2)

        # menu rond-point 2-1
        self.menu_RP2_1 = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_RP2.add_cascade(
            label="Rond-point type 1", menu=self.menu_RP2_1)
        for i in range(1, 5):
            self.menu_RP2_1.add_command(
                image=self.image['rp'][2_1][i], command=lambda i=i: self.placer_route(self.image['rp'][2_1][i]))

        # menu rond-point 2-2
        self.menu_RP2_2 = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_RP2.add_cascade(
            label="Rond-point type 2", menu=self.menu_RP2_2)
        for i in range(1, 3):
            self.menu_RP2_2.add_command(
                image=self.image['rp'][2_2][i], command=lambda i=i: self.placer_route(self.image['rp'][2_2][i]))

        # menu rond-point 3
        self.menu_RP3 = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_Rond_point.add_cascade(
            label="Rond-point 3", menu=self.menu_RP3)
        for i in range(1, 5):
            self.menu_RP3.add_command(
                image=self.image['rp'][3][i], command=lambda i=i: self.placer_route(self.image['rp'][3][i]))

        # menu rond-point 4
        self.menu_RP4 = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_Rond_point.add_cascade(
            label="Rond-point 4", menu=self.menu_RP4)
        self.menu_RP4.add_command(
            image=self.image['rp'][4][1], command=lambda i=i: self.placer_route(self.image['rp'][4][1]))

        self.menu_Aide = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_Aide.add_command(label="Aide", command=lambda: os.system(
            "start https://github.com/uvsq22005188/traffic_car"))
        self.menu_Aide.add_command(label="Quitter", command=self.root.destroy)

        self.menu_bar.add_cascade(label="Fichier", menu=self.menu_Fichier)
        self.menu_bar.add_cascade(label="Création", menu=self.menu_Création)
        self.menu_bar.add_cascade(label="Aide", menu=self.menu_Aide)
        self.root.config(menu=self.menu_bar)

    def creer_canvas(self):
        self.canvas = tk.Canvas(self.root, width=1900, height=1000, highlightthickness=0, bg='white')
        self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.canvas.focus_set()

    def creer_route(self):
        self.coords = []
        self.stop = False
        self.croisement = False
        self.canvas.bind(
            "<Button-1>", lambda e: self.coords.append((e.x, e.y)))
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

    def creer_voiture(self, i):
        self.coords = []
        self.stop = False
        self.canvas.bind(
            "<Button-1>", lambda e: self.coords.append((e.x, e.y)))
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
        filename = askopenfilename(title="Ouvrir une map", filetypes=[
                                   ("Fichier", "*.map")])

    def enregistrer(self):
        pass


ville = Ville()
