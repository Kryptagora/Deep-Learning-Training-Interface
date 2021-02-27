import tkinter as tk
from tkinter import ttk
import re

from interface.draw_frame import DrawFrame
from interface.network_frame import NetworkFrame
from interface.console_frame import ConsoleFrame
from interface.animation_frame import AnimationFrame
from architecture.train_CNN import train
from utils.theme import theme
from utils.richtext import RichText


class DrawAndPredict(tk.Frame):
    def __init__(self, title):
        self.root = tk.Tk()
        self.root.title(title)
        self.bgcolor = self.root.cget('bg')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        self.style = ttk.Style()
        self.style.theme_create('improved', settings=theme())
        self.style.theme_use('improved')

        self.font_1 = ('Helvetica', 10, 'bold')
        self.font_2 = ('Helvetica', 10)

        self.padding = 30
        self.tabs = ttk.Notebook(self.root, padding=10)

        self.add_tabs()
        self.add_content()
        self.add_about()
        self.add_warnlabel()

        self.root.mainloop()


    def add_tabs(self):
        self.tool = ttk.Frame(self.tabs)
        self.tabs.add(self.tool, text=' Main ')

        self.about = ttk.Frame(self.tabs)
        self.tabs.add(self.about, text=' About ')

        self.tabs.grid(row=0, column=0)


    def add_content(self):
        '''Adds all content to the main tab'''
        network_frame = ttk.LabelFrame(self.tool, text="Network Settings", padding=self.padding, relief=tk.RIDGE)
        network_frame.grid(row=0, column=0, sticky=tk.E + tk.W + tk.N + tk.S)
        self.NetworkFrame = NetworkFrame(network_frame, train, self)

        console_frame = ttk.LabelFrame(self.tool, text="Training Information", padding=self.padding, relief=tk.RIDGE)
        console_frame.grid(row=0, column=1, sticky=tk.E + tk.W + tk.N + tk.S)
        self.ConsoleFrame = ConsoleFrame(console_frame)

        animation_frame = ttk.LabelFrame(self.tool, text="Loss Information", padding=0, relief=tk.RIDGE)
        animation_frame.grid(row=0, column=2, sticky=tk.E + tk.W + tk.N + tk.S)
        self.AnimationFrame = AnimationFrame(animation_frame, self.bgcolor)

        draw_frame = ttk.LabelFrame(self.tool, text="Draw and Predict", padding=self.padding, relief=tk.RIDGE)
        draw_frame.grid(row=0, column=3, sticky=tk.E + tk.W + tk.N + tk.S)
        self.DrawFrame = DrawFrame(draw_frame, self)


    def add_about(self):
        '''Adds content from readme.md to the about tab'''
        with open('README.md', 'r') as fh:
            about = fh.readlines()

        ab_text = RichText(self.about, wrap=tk.WORD)
        ab_text.pack(fill="both", expand=True)

        for line in about:
            line = re.sub(r'\:[^.]*\:', '', line)
            line = re.sub(r'\([^)]*\)', '', line)
            # header tags
            if line.startswith('###'):
                ab_text.insert("end", line[4:], "h3")
            elif line.startswith('##'):
                ab_text.insert("end", line[3:], "h2")
            elif line.startswith('#'):
                ab_text.insert("end", line[2:], "h1")

            #extract the url in parentheis and insert image
            elif line.startswith('!'):
                continue

            # draw bulletpoints
            elif line.startswith('-') or line.startswith('*'):
                ab_text.insert_bullet('end', line.split(' ', 1)[1])

            else:
                ab_text.insert("end", line)

        ab_text.configure(state='disabled')
        return True


    def add_warnlabel(self):
        self.warntext = tk.StringVar()
        self.warntext.set('[INFO] ')
        self.warnlabel = tk.Label(self.root, textvariable=self.warntext, font=(None, 10, 'bold'))
        self.warnlabel.grid(row=1, column=0, columnspan=3, sticky='w', padx=10, pady=(0,5))

    def set_warnlabel_normal(self):
        self.warnlabel.config(fg='black')
        self.warntext.set('[INFO] ')

    def set_warn(self, warntext:str=None):
        self.warnlabel.config(fg='red')
        self.warntext.set(f'[WARNING] {warntext}')
        self.root.after(5000, lambda: self.set_warnlabel_normal())

    def set_info(self, infotext:str=None):
        self.warnlabel.config(fg='black')
        self.warntext.set(f'[INFO] {infotext}')
        self.root.after(5000, lambda: self.set_warnlabel_normal())
