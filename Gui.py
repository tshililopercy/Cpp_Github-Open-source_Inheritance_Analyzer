import tkinter as tk
import threading
from tkinter.font import ROMAN

import Data_Extraction_Process_Refractored
import GitHub_Search_And_Clone

def CloneOpenSourceRepositories(lbox):
    #GitHub_Search_And_Clone.SearchForOpenSourceProjects()
    lbox.delete(0,tk.END)
    RepoNames = ['deve1', 'dev2', 'dev3']
    lbox.insert(tk.END,'Cloning....')

#Analyse Repositories
def AnalyseRepositories():
    Data_Extraction_Process_Refractored.analyseAllRepositories()

class UserInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("GitHub Open Source Inheritance Analyzer")
        screen_width = str(self.root.winfo_screenwidth()//2)
        screen_height = str(self.root.winfo_screenheight()//2)
        resolution =screen_width +'x'+screen_height
        self.root.geometry(resolution)
        
        self.Label1 = tk.Label(self.root)
        self.Label1.place(relx=0, rely=0, height=31, width=59)

        self.Label1.configure(text='''Username :''')
        self.lbox = tk.Listbox(self.root)
        self.lbox.place(relx=0.5, rely=0.05, relheight=0.858, relwidth=0.44)
        self.clonebutton = tk.Button(self.root, text="Clone Repositories", font=('Arial', 8), command=lambda: CloneOpenSourceRepositories(self.lbox))
        self.clonebutton.place(relx=0.1, rely=0.25, height=45)
        
        self.Analyzebutton = tk.Button(self.root, text="Analyze Repositories", font=('Arial', 8), command=lambda:(threading.Thread(target=AnalyseRepositories,args=()).start()))
        self.Analyzebutton.place(relx=0.1, rely=0.5, height=45)
        self.root.mainloop()
        
UserInterface()