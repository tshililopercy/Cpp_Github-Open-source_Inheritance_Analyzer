import tkinter as tk
import threading
from tkinter.font import ROMAN

import Data_Extraction_Process_Refractored
import GitHub_Search_And_Clone

def CloneOpenSourceRepositories():
    GitHub_Search_And_Clone.SearchForOpenSourceProjects()

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
        
        self.clonebutton = tk.Button(self.root, text="Clone Repositories", font=('Arial', 8), command=lambda:(threading.Thread(target=CloneOpenSourceRepositories,args=()).start()))
        self.clonebutton.place(relx=0.1, rely=0.25, height=45)
        
        self.Analyzebutton = tk.Button(self.root, text="Analyze Repositories", font=('Arial', 8), command=lambda:(threading.Thread(target=AnalyseRepositories,args=()).start()))
        self.Analyzebutton.place(relx=0.1, rely=0.5, height=45)
        self.root.mainloop()
        
UserInterface()