import tkinter as tk

def on_label_press(event):
    # Record the starting position of the label and the mouse cursor
    global selected_label, start_x, start_y
    selected_label = event.widget
    start_x, start_y = event.x, event.y

def on_label_release(event):
    # Clear the selected_label when the mouse button is released
    global selected_label
    selected_label = None

def on_label_drag(event):
    if selected_label:
        # Calculate the new position of the label based on the mouse movement
        delta_x = event.x - start_x
        delta_y = event.y - start_y
        new_x = selected_label.winfo_x() + delta_x
        new_y = selected_label.winfo_y() + delta_y

        # Move the label to the new position
        selected_label.place(x=new_x, y=new_y)

# Create the main window
root = tk.Tk()
root.title("Drag and Drop Text")

# Create a Label widget for the text
label = tk.Label(root, text="Drag me!", bg="lightgray")
label.pack()

# Bind mouse events to the Label widget
label.bind("<ButtonPress-1>", on_label_press)
label.bind("<ButtonRelease-1>", on_label_release)
label.bind("<B1-Motion>", on_label_drag)

# Initialize the selected_label variable
selected_label = None

root.mainloop()
