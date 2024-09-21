import tkinter as tk

root = tk.Tk()

canvas = tk.Canvas(root, width=300, height=300)
canvas.pack()


def hello():
    label = tk.Label(root, text="Hello World!", fg="blue", font=("Arial", 18, "bold"))
    canvas.create_window(150, 200, window=label)


button = tk.Button(text="Click Me", command=hello, bg="brown", fg="white")
canvas.create_window(150, 150, window=button)

root.mainloop()