import threading

import tkinter as tk
from tkinter import ttk
from tkinter import *

import os
import Data_Extraction_Process_Refractored

#analyse source File 
def SourceFile(controller, Entry1):
    global obj
    res = Data_Extraction_Process_Refractored.parseTranslationUnit(Entry1.get())
    controller.show_frame(PageOne)
    obj = res
    return obj

#initialise Tkinter pages
class SourceFileAnalyzer(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.iconbitmap(self, default=None)
        tk.Tk.wm_title(self, "Source File Inheritance Analyzer")
        #set screen dimensions
        self.geometry('400x200')

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

        button2 = ttk.Button(self, text="Analyse File",
                             command=lambda:(threading.Thread(target=SourceFile,args=(controller, Entry1)).start()))
        button2.place(relx=0.74, rely=0.8, height=32, width=98)
        
        Label1 = tk.Label(self)
        Label1.place(relx=0.05, rely=0.044)
    
        Label1.configure(text='''SourceFile Path:''')
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
        
        Label1 = tk.Label(self)
        Label1.place(relx=0.3, rely=0.1)

        Label1.configure(text='''Implementation Inheritance(s): ''' + str(obj.ImplementationInheritance))
        
if __name__ == "__main__":
  app = SourceFileAnalyzer()
  app.mainloop()
  