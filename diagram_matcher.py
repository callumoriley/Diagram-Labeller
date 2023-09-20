import tkinter as tk
from PIL import Image, ImageTk

img = None

MARGIN = 100 # can be this many pixels away from the correct position in any direction
HORIZONTAL_PADDING = 300
VERTICAL_PADDING = 100
IMAGE_FILE_NAME = "image.png"
FILE_NAME = "points.csv"
SPACING_BETWEEN_LABELS = 50

# CHANGE TO BE A LABEL THAT'S MOVING INSTEAD OF AN IMAGE
class Match:
    # coords, dimensions, and home_coords are all tuples of (x, y) coordinates
    def __init__(self, coords, home_coords, label_text, root):
        global img
        
        self.correct_coords = coords
        self.home_coords = home_coords
        self.x = home_coords[0]
        self.y = home_coords[1]
        self.in_correct_spot = False
        self.label_text = label_text
        self.root = root

        self.label = tk.Label(self.root, text=label_text, relief="raised")
        self.label.pack()

        self.move_label(self.x, self.y)

    def check_match(self):
        if self.distance_from(self.correct_coords[0], self.correct_coords[1]) < MARGIN:
            self.move_label(self.correct_coords[0], self.correct_coords[1])
            self.in_correct_spot = True
        else:
            self.move_label(self.home_coords[0], self.home_coords[1])

    def distance_from(self, x, y):
        return ((self.x - x)**2+(self.y - y)**2)**0.5

    def move_label(self, x, y):
        if not self.in_correct_spot:
            self.label.place(x=x, y=y) # just SPEWING errors
            
            self.x = x
            self.y = y
        
class DiagramMatcher:
    def __init__(self, root):
        global img
        
        self.root = root
        self.root.title("Diagram Label Matching")

        self.im = Image.open(IMAGE_FILE_NAME)
        width, height = self.im.size
        root.geometry(f"{width+HORIZONTAL_PADDING}x{height+VERTICAL_PADDING}")
        
        self.canvas = tk.Canvas(root)
        self.canvas.pack(fill=tk.BOTH, expand=True)

        img = ImageTk.PhotoImage(self.im)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)

        self.canvas.bind("<Button-1>", self.on_button_press)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_button_release)


        with open(FILE_NAME, "r") as f:
            lines = f.readlines()
            points_str = [line[:-1].split(",") for line in lines]
            points = [[int(i) for i in line[:-1]] for line in points_str]
            label_texts = [line[-1] for line in points_str]

        self.matches = []
        label_number = 1
        
        for match_coords in points:
            self.matches.append(Match((match_coords[0], match_coords[1]),
                                      (width+HORIZONTAL_PADDING/2, label_number*SPACING_BETWEEN_LABELS),
                                      label_texts[label_number - 1],
                                      self.root))
            label_number += 1

    def on_button_press(self, event):
        self.drag_index = self.matches.index(sorted(self.matches, key=lambda match: match.distance_from(event.x, event.y))[0])

    def on_mouse_drag(self, event):
        self.matches[self.drag_index].move_label(event.x, event.y)

    def on_button_release(self, event):
        self.matches[self.drag_index].check_match()
        self.drag_index = len(self.matches)

if __name__ == "__main__":
    root = tk.Tk()
    app = DiagramMatcher(root)
    root.mainloop()
