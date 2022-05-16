import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk
import os


class Voiture():
    def __init__(self, other, x, y):
        self.ville = other
        self.x = x
        self.y = y
        self.draw()
    
    def load(self, angle):
        self.image = ImageTk.PhotoImage(Image.open("Images/Voiture/voiture_1.png").rotate(angle, expand=True))
        return self.image

    def draw(self):
        x = self.x * 19 // 1900
        y = self.y * 10 // 1000
        _id = self.ville.map[y][x]
        if _id == None:
            return
        elif _id in [1, 2]:
            self.im = self.ville.canvas.create_image(self.x, y * 100 + 59, image=self.load(-90))
        elif _id in [3, 4]:
            self.im = self.ville.canvas.create_image(x * 100 + 59, self.y, image=self.load(0))
         


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
        self.order_route = []
        self.order_voiture = []

        self.map = [[None] * 19 for _ in range(10)]

        self.root.mainloop()

    def charger_image(self):
        self.image = {}
        self.image["route"] = {i: ImageTk.PhotoImage(Image.open(
            f"Images/Route/route_{i}.png")) for i in range(1, 5)}
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
            1: ImageTk.PhotoImage(Image.open(f"Images/Voiture/voiture_1.png"))
        }
        self.image_id = [
            None,
            *self.image["route"].values(),
            *self.image["tournant"].values(),
            *self.image["rp"][1].values(),
            *self.image["rp"][2_1].values(),
            *self.image["rp"][2_2].values(),
            *self.image["rp"][3].values(),
            *self.image["rp"][4].values()
        ]

    def placer(self, img, _id):
        """"""
        self.canvas.bind("<Motion>", lambda e,
                         img=img: self.image_motion(e, img, _id))
        self.canvas.bind("<Button-1>", lambda e: self.setVar("stop", True))

    def image_motion(self, event, img, _id):
        x, y = event.x, event.y
        self.canvas.delete("motion")
        self.canvas.create_image(x, y, image=img, tag="motion")
        if self.stop:
            self.canvas.unbind("<Motion>")
            self.canvas.unbind("<Button-1>")
            self.canvas.delete("motion")
            self.stop = False
            if _id != -1:
                # Placement de la route
                x1 = ((19 * x) // 1900) * 100 + 50
                y1 = ((10 * y) // 1000) * 100 + 50
                self.map[y1 // 100][x1 // 100] = _id
                self.order_route.append(self.canvas.create_image(x1, y1, image=img))
            else:
                # Place une voiture si il y a un route
                if self.map[y // 100][x // 100] != None:
                    self.order_voiture.append(Voiture(self, x, y))
            self.canvas.update()
            return

    def creer_menu(self):
        self.menu_bar = tk.Menu(self.root, tearoff=0)

        self.menu_Fichier = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_Fichier.add_command(label="Charger", command=self.charger)
        self.menu_Fichier.add_command(
            label="Enregistrer", command=self.enregistrer)

        self.menu_Création = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_Création.add_command(
            label="Undo", command=lambda: self.canvas.delete(self.order_route.pop()))

        # menu_voiture
        self.menu_Voiture = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_Création.add_cascade(label="Voiture", menu=self.menu_Voiture)
        self.menu_Voiture.add_command(
            image=self.image['voiture'][1], command=lambda: self.placer(self.image['voiture'][1], -1))
        # menu route
        self.menu_Route = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_Création.add_cascade(label="Route", menu=self.menu_Route)
        for i in range(1, 5):
            self.menu_Route.add_command(
                image=self.image['route'][i], command=lambda i=i: self.placer(self.image['route'][i], i))

        # menu tournant
        self.menu_Tourant = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_Création.add_cascade(label="Tourant", menu=self.menu_Tourant)
        for i in range(1, 5):
            self.menu_Tourant.add_command(
                image=self.image['tournant'][i], command=lambda i=i: self.placer(self.image['tournant'][i], i + 4))

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
                image=self.image['rp'][1][i], command=lambda i=i: self.placer(self.image['rp'][1][i], i + 8))

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
                image=self.image['rp'][2_1][i], command=lambda i=i: self.placer(self.image['rp'][2_1][i], i + 12))

        # menu rond-point 2-2
        self.menu_RP2_2 = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_RP2.add_cascade(
            label="Rond-point type 2", menu=self.menu_RP2_2)
        for i in range(1, 3):
            self.menu_RP2_2.add_command(
                image=self.image['rp'][2_2][i], command=lambda i=i: self.placer(self.image['rp'][2_2][i], i + 16))

        # menu rond-point 3
        self.menu_RP3 = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_Rond_point.add_cascade(
            label="Rond-point 3", menu=self.menu_RP3)
        for i in range(1, 5):
            self.menu_RP3.add_command(
                image=self.image['rp'][3][i], command=lambda i=i: self.placer(self.image['rp'][3][i], i + 18))

        # menu rond-point 4
        self.menu_RP4 = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_Rond_point.add_cascade(
            label="Rond-point 4", menu=self.menu_RP4)
        self.menu_RP4.add_command(
            image=self.image['rp'][4][1], command=lambda i=i: self.placer(self.image['rp'][4][1], 23))

        self.menu_Aide = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_Aide.add_command(label="Aide", command=lambda: os.system(
            "start https://github.com/uvsq22005188/traffic_car"))
        self.menu_Aide.add_command(label="Quitter", command=self.root.destroy)

        self.menu_bar.add_cascade(label="Fichier", menu=self.menu_Fichier)
        self.menu_bar.add_cascade(label="Création", menu=self.menu_Création)
        self.menu_bar.add_cascade(label="Aide", menu=self.menu_Aide)
        self.root.config(menu=self.menu_bar)

    def creer_canvas(self):
        self.canvas = tk.Canvas(self.root, width=1900,
                                height=1000, highlightthickness=0, bg='white')
        self.canvas.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.canvas.focus_set()

    def wait(self, ms):
        var = tk.IntVar()
        self.root.after(ms, lambda: var.set(1))
        self.root.wait_variable(var)

    def setVar(self, var, value):
        setattr(self, var, value)

    def creer_voiture(self, i):
        pass

    def charger(self):
        filename = askopenfilename(title="Ouvrir une map", filetypes=[
            ("Map", "*.map")], defaultextension=[("Map", ".map")])

        with open(filename, "r") as f:
            self.map = eval(f.readline())
            for y, liste in enumerate(self.map):
                for x, elem in enumerate(liste):
                    if elem != None:
                        self.canvas.create_image(
                            x * 100 + 50, y * 100 + 50, image=self.image_id[elem])

    def enregistrer(self):
        filename = asksaveasfilename(title="Enregistrer la map", filetypes=[
                                     ("Map", "*.map")], defaultextension=[("Map", ".map")])
        with open(filename, "w") as f:
            f.write(str(self.map).replace(" ", ""))


ville = Ville()
