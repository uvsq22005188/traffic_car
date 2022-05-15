import tkinter as tk


def main():
    global root
    root = tk.Tk()
    root.title("Traffic Car")
    root.geometry("800x600")
    root.iconbitmap("Images/icon.ico")
    root.bind("<Escape>", lambda e: root.destroy())
    root.bind("<Button-1>", ville)
    root.mainloop()


def ville(_):
    canvas = tk.Canvas(root, highlightthickness=0)
    canvas.pack(fill=tk.BOTH, expand=True)
    canvas.focus_set()
    x1, y1 = (54, 84)
    x2, y2 = (800, 400)
    canvas.create_line(x1, y1, x2, y2)
    a = (y2 - y1) / (x2 - x1)
    a2 = -1 / a
    b = y1 - a * x1
    print(a, b)
    voiture = canvas.create_rectangle(x1 - 10, y1 + 10, x1 + 10, y1 + 30, fill="red")
    canvas.move(voiture, -25, -25*a2)
    while True:
        n = 0.1
        canvas.move(voiture, n, n*a)
        wait(10)


def wait(ms):
    root.update()
    root.after(ms)


main()