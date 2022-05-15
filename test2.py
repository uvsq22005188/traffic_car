import tkinter as tk

from click import style

root = tk.Tk()
root.title("Traffic Car")
root.geometry("1000x1000")
root.iconbitmap("Images/icon.ico")
root.bind("<Escape>", lambda e: root.destroy())
root.bind('<Button-1>', lambda e: print(e.x, e.y))

canvas = tk.Canvas(root, highlightthickness=0, bg="white")
canvas.pack(fill=tk.BOTH, expand=True)

# Route verticale haut gauche
coord = (50, 100, 50, 250)
route1 = canvas.create_line(*coord, fill="black", width=50)
route1 = canvas.create_line(*coord, fill="white", width=40)
route1 = canvas.create_line(*coord, fill="black", width=10, dash=(20, 5))

# Route horizontale haut gauche
coord = (100, 50, 250, 50)
route1 = canvas.create_line(*coord, fill="black", width=50)
route1 = canvas.create_line(*coord, fill="white", width=40)
route1 = canvas.create_line(*coord, fill="black", width=10, dash=(20, 5))

# Route tourante haut droite
n = 27
coord = (250 - n, 100 - n, 250 + n, 100 + n)
canvas.create_arc(*coord, start=0, extent=90, width=5, style=tk.ARC)
n = 73
coord = (250 - n, 100 - n, 250 + n, 100 + n)
canvas.create_arc(*coord, start=0, extent=90, width=5, style=tk.ARC)

# Route tourante bas droite
n = 27
coord = (250 - n, 100 - n, 250 + n, 100 + n)
canvas.create_arc(*coord, start=0, extent=90, width=5, style=tk.ARC)
n = 73
coord = (250 - n, 100 - n, 250 + n, 100 + n)
canvas.create_arc(*coord, start=0, extent=90, width=5, style=tk.ARC)

# Route verticale haut droite
# coord = (300, 100, 300, 250)
# route1 = canvas.create_line(*coord, fill="black", width=50)
# route1 = canvas.create_line(*coord, fill="white", width=40)
# route1 = canvas.create_line(*coord, fill="black", width=10, dash=(20, 5))

# Route horizontale bas gauche
coord = (100, 300, 250, 300)
# route1 = canvas.create_line(*coord, fill="black", width=50)
# route1 = canvas.create_line(*coord, fill="white", width=40)
# route1 = canvas.create_line(*coord, fill="black", width=10, dash=(20, 5))

# # Route verticale bas droite
# coord = (300, 350, 300, 500)
# route1 = canvas.create_line(*coord, fill="black", width=50)
# route1 = canvas.create_line(*coord, fill="white", width=40)
# route1 = canvas.create_line(*coord, fill="black", width=10, dash=(20, 5))

# Route horizontale bas droite
coord = (350, 300, 500, 300)
route1 = canvas.create_line(*coord, fill="black", width=50)
route1 = canvas.create_line(*coord, fill="white", width=40)
route1 = canvas.create_line(*coord, fill="black", width=10, dash=(20, 5))

# Centre rond point
n = 5
n2 = 20
coord = (250 - n, 250 - n, 350 + n, 350 + n)
coordCentre = (300 - n2, 300 - n2, 300 + n2, 300 + n2)

canvas.create_arc(*coord, start=22, extent=90, width=5, style=tk.ARC)
canvas.create_arc(*coord, start=112, extent=90, width=5, style=tk.ARC)
canvas.create_arc(*coord, start=202, extent=90, width=5, style=tk.ARC)
canvas.create_arc(*coord, start=292, extent=46, width=5, style=tk.ARC)

canvas.create_oval(*coordCentre, fill="black", width=5)


root.mainloop()
