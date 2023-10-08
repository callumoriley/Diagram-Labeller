import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk

IMAGE_FILE_NAME = filedialog.askopenfilename(
        title="Select image",
        filetypes=[("PNG files", "*.png")])
SAVE_FILE_NAME = IMAGE_FILE_NAME[:-3]+"csv"
IMAGE_SCALE_FACTOR = 1

img = None

class DiagramMatchCreator:
    def __init__(self, root):
        global img
        
        self.root = root
        self.root.title("Match Diagram Creator")

        self.im = Image.open(IMAGE_FILE_NAME)
        self.width, self.height = self.im.size
        self.im = self.im.resize((int(self.width*IMAGE_SCALE_FACTOR), int(self.height*IMAGE_SCALE_FACTOR)))
        root.geometry(f"{int(self.width*IMAGE_SCALE_FACTOR)}x{int(self.height*IMAGE_SCALE_FACTOR)}")

        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        img = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)

        self.canvas.bind("<Button-1>", self.add_item)

        self.root.bind('<Escape>', self.close_window)

        self.labels = []

    def add_item(self, event):
        label_name = simpledialog.askstring("Enter a string", "What do you want to label this point?")
        if label_name:
            self.labels.append((int(event.x/IMAGE_SCALE_FACTOR), int(event.y/IMAGE_SCALE_FACTOR), label_name))
            text_label = tk.Label(self.canvas, text=label_name)
            text_label.pack()
            text_label.place(relx=event.x/(self.width*IMAGE_SCALE_FACTOR), rely=event.y/(self.height*IMAGE_SCALE_FACTOR), anchor='se')

    def close_window(self, e):
        lines = [",".join([str(e) for e in line])+"\n" for line in self.labels]
        # maybe open a save file dialog window for this operation so that you can choose the file names without editing the code
        with open(SAVE_FILE_NAME, "w") as f:
            f.writelines(lines)

        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = DiagramMatchCreator(root)
    root.mainloop()
