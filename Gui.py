import threading

import tkinter as tk
from tkinter import ttk
from tkinter import *

import os

import Data_Extraction_Process_Refractored
import GitHub_Search_And_Clone

def cloneRepo (Entry1):
    clone_url = Entry1.get()
    print(clone_url)
    GitHub_Search_And_Clone.Clone(clone_url)

#analyse source File 
def Repository(controller):
    global obj
    res = Data_Extraction_Process_Refractored.AnalyseRepository()
    controller.show_frame(PageOne)
    obj = res
    return obj

#initialise Tkinter pages
class SourceFileAnalyzer(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default=None)
        tk.Tk.wm_title(self, "GitHub Open source Inheritance Analyzer")
        #set screen dimensions
        self.geometry('700x500')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand = True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        #create page frames
        for F in (StartPage,PageOne):

            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        button2 = ttk.Button(self, text="Analyse Repo",
                             command=lambda:Repository(controller))
        button2.place(relx=0.74, rely=0.8, height=32, width=98)
        
        button1 = ttk.Button(self, text="Clone Repo",
                             command=lambda:cloneRepo(Entry1))
        button1.place(relx=0.01, rely=0.8, height=32, width=98)
        
        Label1 = tk.Label(self)
        Label1.place(relx=0.05, rely=0.044)
    
        Label1.configure(text='''Repo Clone URL:''')
        Entry1 = tk.Entry(self)
        Entry1.place(relx=0.3, rely=0.044,height=26, relwidth=0.65)
        
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        self.frame = tk.Frame.__init__(self, parent)
        
        button1 = ttk.Button(self, text="Show Results",
                            command=lambda: (self.plot()))

        button3 = ttk.Button(self, text="Back to Home",
                            command=lambda:controller.show_frame(StartPage))
        
        button1.place(relx=0, rely=0.1)
        button3.place(relx=0, rely=0.25)
        
    def plot(self):
        text = ""
        Label1 = tk.Label(self)
        Label1.place(relx=0.2, rely=0)
        for INDEX, inheritance in enumerate(obj):
            text +='''\n'''+ '''\n'''+ "INHERITANCE NUMBER: " + str(INDEX + 1) + '''\n'''+ "Type of inheritance: " + str(inheritance.typeofinheritance)+ '''\n''' + "DERIVED CLASS DATA" + '''\n'''+ "         Additional Child Methods: " + str(inheritance.derivedAdditionalfunctions) + "         Overriden Functions: " + str(inheritance.overridenfunctions)
            for index, base in enumerate(inheritance.BaseClassesData):
                if len(inheritance.BaseClassesData) == 1:
                    text +='''\n'''"PARENT DATA" + '''\n'''
                else:
                   text+=" Parent Number" + str(index + 1) + "Data"+'''\n'''
                text +="     Pure Virtual Functions: " + str(base["purevirtualfunctions"])+'''\n'''
                text +="     Virtual Functions: " + str(base["virtualfunctions"])+'''\n'''
                text +="     Normal Functions: " + str(base["normalfunctions"])
        #print(text)
        Label1.configure(text=str(text))
if __name__ == "__main__":
  app = SourceFileAnalyzer()
  app.mainloop()
  