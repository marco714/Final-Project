from PIL import Image, ImageTk
from tkinter import *
from tkinter import ttk
class createTable:

    HEIGHT = 900
    WIDTH = 800
    def __init__(self, tk, graph_result):
        self.tk = tk
        self.graph_result = graph_result
        self.past_total_death_country()
    
    def past_total_death_country(self):
        graph_result = self.graph_result
        top = self.tk()

        canvas = Canvas(top, height=self.HEIGHT, width=self.WIDTH)
        canvas.pack()

        backgroundImage = PhotoImage(file='landscape.png')
        backgroundLabel = Label(top, image=backgroundImage)
        backgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)

        frame1 = Frame(top, bg='#80c1ff', bd=5)
        frame1.place(relx = 0.5, rely= 0.0, relwidth=0.75, relheight=0.50, anchor='n')

        label1 = Label(frame1, text="Last Updated Data", font=('bold',14))
        label1.pack()
        tv = ttk.Treeview(frame1, columns=(1,2,3), show="headings", height="5", selectmode='browse')
        tv.pack(pady=50)
        tv.heading(1, text="Country")
        tv.heading(2, text="Total_Cases")
        tv.heading(3, text="Total_Deaths")

        for row in graph_result['Past-Country-Result']:
            tv.insert('', 'end', values=(row['Name'], row['Total_Cases'], row['Total_Deaths']))
        
        tv1 = ttk.Treeview(frame1, columns=(1,2), show="headings", height="5", selectmode="browse")
        tv1.pack()

        tv1.heading(1, text="Name")
        tv1.heading(2, text="Total_Value")

        for row in graph_result['Past-Total-Result']:
            tv1.insert('', 'end', values=(row[0], row[1]))

        frame2 = Frame(top, bg='#80c1ff', bd=5)
        frame2.place(relx = 0.5, rely= 0.5, relwidth=0.75, relheight=0.50, anchor='n')

        label2 = Label(frame2, text="Latest Updated Data", font=('bold',14))
        label2.pack()

        tv3 = ttk.Treeview(frame2, columns=(1,2,3), show="headings", height="5", selectmode='browse')
        tv3.pack(pady=50)
        tv3.heading(1, text="Country")
        tv3.heading(2, text="Total_Cases")
        tv3.heading(3, text="Total_Deaths")

        for row in graph_result['Present-Country-Result']:
            tv3.insert('', 'end', values=(row['Name'], row['Total_Cases'], row['Total_Deaths']))

        tv4 = ttk.Treeview(frame2, columns=(1,2), show="headings", height="5", selectmode="browse")
        tv4.pack()

        tv4.heading(1, text="Name")
        tv4.heading(2, text="Total_Value")

        for row in graph_result['Present-Total-Result']:
            tv4.insert('', 'end', values=(row[0], row[1]))