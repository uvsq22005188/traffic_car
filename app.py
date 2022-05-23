import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import Image, ImageTk
import os
import threading as th
import math

class Voiture():
    def __init__(self, other, x, y):
        self.ville = other
        self.x = x
        self.y = y
        self.a = 3
        self.b = 1 / self.a
        self.vitesse = 1
        self.f = lambda dx: (58**self.a - dx**self.a)**self.b
        self.g = lambda dx: (42**self.a - dx**self.a)**self.b 
        self.fp = lambda dx: math.atan(dx**(self.a-1) * (58**self.a - dx**self.a)**(self.b - 1))
        self.gp = lambda dx: math.atan(dx**(self.a-1) * (42**self.a - dx**self.a)**(self.b - 1))
        self.d = lambda x: round(math.degrees(x), 2)

        self.init()
        th.Thread(target=self.move, daemon=True).start()
    
    def init(self):
        x = int(self.x * 19 // 1900)
        y = int(self.y * 10 // 1000)
        self._id = self.ville.map[y][x]
        dx = self.x - (x * 100)
        dy = self.y - (y * 100)

        if self._id == 1:
            if dy > 50:
                self.angle = 0
                self.y = y * 100 + 58
            else:
                self.angle = 180
                self.y = y * 100 + 42
        elif self._id == 2:
            if dx > 50:
                self.angle = 90
                self.x = x * 100 + 58
            else:
                self.angle = 270
                self.x = x * 100 + 42
        self.direction = self.checkDirection()
    
    def checkDirection(self):
        if 45 > self.angle >= 0 or 360 >= self.angle >= 315:
            return "E"
        elif 135 > self.angle >= 45:
            return "N"
        elif 225 > self.angle >= 135:
            return "O"
        elif 315 > self.angle >= 225:
            return "S"

    def load(self, angle):
        self.image = ImageTk.PhotoImage(Image.open("Images/Voiture/voiture_1.png").rotate(angle, expand=True))
        return self.image

    def draw(self):
        self.im = self.ville.canvas.create_image(self.x, self.y, image=self.load(self.angle))
    
    def move(self):
        while True:
            x = int(self.x * 19 // 1900)
            y = int(self.y * 10 // 1000)
            self._id = self.ville.map[y][x]
            dx = math.trunc((self.x - (x * 100)) * 100) / 100
            dy = math.trunc((self.y - (y * 100)) * 100) / 100
            
            if self._id == 1:
                if self.direction == "E":
                    self.angle = 0
                    self.y = y * 100 + 58
                else:
                    self.angle = 180
                    self.y = y * 100 + 42
            
            elif self._id == 2:
                if self.direction == "N":
                    self.angle = 90
                    self.x = x * 100 + 58
                else:
                    self.angle = 270
                    self.x = x * 100 + 42

            elif self._id == 3:
                if self.direction in ("N", "O"):
                    self.angle = 180 - (self.d(self.fp(self.f(100 - dy))) if dy > 42 else 0)
                else:
                    self.angle = 0 - (self.d(self.gp(dx)) if dx < 42 else 90)

            elif self._id == 4:
                if self.direction in ("O", "S"):
                    self.angle = 180 + (self.d(self.fp(abs(dx - 100))) if dx > 42 else 90)
                else:
                    self.angle = 0 + (self.d(self.gp(self.g(100 - dy))) if dy > 58 else 0)

            elif self._id == 5:
                if self.direction in ("S", "E"):
                    self.angle = 360 - (self.d(self.fp(self.f(dy))) if 0 < dy < 58 else 90 if dy == 0 else 0)
                else:
                    self.angle = 180 - (self.d(self.gp(abs(dx - 100))) if dx > 58 else 90)

            elif self._id == 6:
                if self.direction in ("E", "N"):
                    self.angle = 0 + (self.d(self.fp(dx)) if dx < 58 else 90)
                else:
                    self.angle = 180 + (self.d(self.gp(self.g(dy))) if 0 < dy < 42 else 90 if dy == 0 else 0)
            self.direction = self.checkDirection()

            self.x += self.vitesse * round(math.cos(-self.angle * math.pi / 180), 2)
            self.y += self.vitesse * round(math.sin(-self.angle * math.pi / 180), 2)
            
            self.ville.info[0]['text'] = f"x: {self.x}"
            self.ville.info[1]['text'] = f"y: {self.y}"
            self.ville.info[2]['text'] = f"dy - 42: {dy - 42}"
            self.ville.info[3]['text'] = f"angle: {self.angle}"

            self.draw()
            self.ville.wait(50)
    
    def wait(self, ms):
        var = tk.IntVar()
        self.ville.root.after(ms, var.set(0))
        self.ville.root.wait_variable(var)
         


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

        self.map = [[0] * 19 for _ in range(10)]

        # debug
        self.info = [0] * 4
        self.info[0] = tk.Label(self.root, text="x: ", bg='darkgrey', fg='white', font=("Helvetica", 20))
        self.info[1] = tk.Label(self.root, text="y: ", bg='darkgrey', fg='white', font=("Helvetica", 20))
        self.info[2] = tk.Label(self.root, text="dy: ", bg='darkgrey', fg='white', font=("Helvetica", 20))
        self.info[3] = tk.Label(self.root, text="angle :", bg='darkgrey', fg='white', font=("Helvetica", 20))
        self.info[0].place(x=1700, y=50)
        self.info[1].place(x=1700, y=100)
        self.info[2].place(x=1700, y=150)
        self.info[3].place(x=1700, y=200)
        # Fin debug
        self.root.mainloop()

    def charger_image(self):
        self.image = {}
        self.image["route"] = {i: ImageTk.PhotoImage(Image.open(
            f"Images/Route/route_{i}.png")) for i in range(1, 3)}
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
                if self.map[y // 100][x // 100] is not None:
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
        for i in range(1, 3):
            self.menu_Route.add_command(
                image=self.image['route'][i], command=lambda i=i: self.placer(self.image['route'][i], i))

        # menu tournant
        self.menu_Tourant = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_Création.add_cascade(label="Tourant", menu=self.menu_Tourant)
        for i in range(1, 5):
            self.menu_Tourant.add_command(
                image=self.image['tournant'][i], command=lambda i=i: self.placer(self.image['tournant'][i], i + 2))

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
                image=self.image['rp'][1][i], command=lambda i=i: self.placer(self.image['rp'][1][i], i + 6))

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
                image=self.image['rp'][2_1][i], command=lambda i=i: self.placer(self.image['rp'][2_1][i], i + 10))

        # menu rond-point 2-2
        self.menu_RP2_2 = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_RP2.add_cascade(
            label="Rond-point type 2", menu=self.menu_RP2_2)
        for i in range(1, 3):
            self.menu_RP2_2.add_command(
                image=self.image['rp'][2_2][i], command=lambda i=i: self.placer(self.image['rp'][2_2][i], i + 14))

        # menu rond-point 3
        self.menu_RP3 = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_Rond_point.add_cascade(
            label="Rond-point 3", menu=self.menu_RP3)
        for i in range(1, 5):
            self.menu_RP3.add_command(
                image=self.image['rp'][3][i], command=lambda i=i: self.placer(self.image['rp'][3][i], i + 16))

        # menu rond-point 4
        self.menu_RP4 = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_Rond_point.add_cascade(
            label="Rond-point 4", menu=self.menu_RP4)
        self.menu_RP4.add_command(
            image=self.image['rp'][4][1], command=lambda i=i: self.placer(self.image['rp'][4][1], 21))

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
                    if elem != 0:
                        self.canvas.create_image(
                            x * 100 + 50, y * 100 + 50, image=self.image_id[elem])

    def enregistrer(self):
        filename = asksaveasfilename(title="Enregistrer la map", filetypes=[
                                     ("Map", "*.map")], defaultextension=[("Map", ".map")])
        with open(filename, "w") as f:
            f.write(str(self.map).replace(" ", ""))


ville = Ville()
