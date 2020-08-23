from data import (
    run_data
)
import tkinter as tk

# THIS IS MASTER Branch
def run_input(entry,another_window):
    tk = another_window
    user_input = entry
    result = run_data(user_input, tk.Toplevel)
    label['text'] = result

def run_Application():
    HEIGHT = 500
    WIDTH = 600
    global label

    root = tk.Tk()
    root.title("Coronavirus Desktop Application")
    root.resizable(False,False)

    canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
    canvas.pack()

    background = tk.PhotoImage(file='landscape.png')
    backgroundLabel = tk.Label(root, image=background)
    backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)

    toplabel = tk.Label(root, text="Desktop Application",font=20, relief="raised", bg="#80c1ff")
    toplabel.place(relx=0.4, rely=0.0)

    frame = tk.Frame(root, bg='#80c1ff', bd=5)
    frame.place(relx=0.5, rely=0.1, relwidth=0.75, relheight=0.1, anchor='n')

    entry = tk.Entry(frame, font=40,relief="sunken", justify= "center")
    entry.focus_force()
    entry.place(relwidth=0.65, relheight=1)

    button = tk.Button(frame, text="Get Data", font=40, relief="raised", cursor="heart" ,command=lambda :run_input(entry.get(), tk))
    button.place(relx=0.7, relheight=1, relwidth=0.3)

    lower_frame = tk.Frame(root, bg='#80c1ff', bd=10)
    lower_frame.place(relx = 0.5, rely=0.25, relwidth=0.75, relheight=0.6, anchor='n')

    label = tk.Label(lower_frame,font=20)
    label.place(relwidth=1, relheight=1)

    root.mainloop()

if __name__ == '__main__':
    run_Application()