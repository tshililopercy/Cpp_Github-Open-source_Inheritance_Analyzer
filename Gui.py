import tkinter as tk
import threading
import os
from StoreData import *

import Data_Extraction_Process_Refractored
import GitHub_Search_And_Clone

class Clone_And_Analyse:
    def __init__(self):
        self.ClonedRepos = []
    def CloneOpenSourceRepositories(self,lbox):
        cloner = GitHub_Search_And_Clone.Cloner()
        repos_info = cloner.get_repos_info()
        lbox.delete(0, tk.END)
        for repo in repos_info:
            # clear text
            # print clone status
            lbox.delete(0, tk.END)
            clonedRepo = []
            before_current = True
            for repo2 in repos_info:
                if (repo["name"] == repo2["name"]):
                    clonedRepo.append({'name': repo2["name"], 'status': 'Cloning...'})
                    before_current = False
                elif before_current:
                    clonedRepo.append({'name': repo2["name"], 'status': 'Clone Complete..'})
                else:
                    clonedRepo.append({'name': repo2["name"], 'status': 'Waiting...'})
                self.ClonedRepos = clonedRepo
            for i, print_ in enumerate(clonedRepo):
                print(print_)
                lbox.insert(tk.END, f"{print_['name']}              {print_['status']}")
            if repo["name"] != "tensorflow":
                cloner.cloneARepo(repo)
    
    #Analyse Repositories
    def AnalyseRepositories(self,lbox):
        extractor = Data_Extraction_Process_Refractored.Extractor()
            #Deleting Data Available in HierachiesData.json, for new analysis
        open('HierachiesData.json', 'w').close()
        for name in os.listdir('../Repository'):
            lbox.delete(0, tk.END)
            for index, clonerepo in enumerate(self.ClonedRepos):
                if clonerepo["name"] == name:
                    self.ClonedRepos[index]['status'] = "Analysing" 
            for i, print_ in enumerate(self.ClonedRepos):
                lbox.insert(tk.END, f"{print_['name']}              {print_['status']}")
            print("analysing", name)
            projectdatastorage = ProjectDataStorage(extractor.AnalyseRepository(name))
            projectdatastorage.ComputeHieracyData()
            for index, clonerepo in enumerate(self.ClonedRepos):
                if clonerepo["name"] == name:
                    self.ClonedRepos[index]['status'] = "Done Analysing"
            lbox.delete(0, tk.END)
            for i, print_ in enumerate(self.ClonedRepos):
                lbox.insert(tk.END, f"{print_['name']}              {print_['status']}")

class UserInterface:
    def __init__(self):
        _clone_and_analyze = Clone_And_Analyse()
        self.root = tk.Tk()
        self.root.title("GitHub Open Source Inheritance Analyzer")
        screen_width = str(self.root.winfo_screenwidth()//2)
        screen_height = str(self.root.winfo_screenheight()//2)
        resolution =screen_width +'x'+screen_height
        self.root.geometry(resolution)
        
        
        self.Label1 = tk.Label(self.root)
        self.Label1.place(relx=0.4, rely=0, height=31)
        self.Label1.configure(text="Repository Name")
        
        self.Label2 = tk.Label(self.root)
        self.Label2.place(relx=0.76, rely=0, height=31)
        self.Label2.configure(text="Status")
        Font_tuple = ("Comic Sans MS", 10, "bold")
        Font_tuple2 = ("Arial", 10)
  
        self.Label1.configure(font = Font_tuple)
        self.Label2.configure(font= Font_tuple)
        
        self.lbox = tk.Listbox(self.root)
        self.lbox.place(relx=0.4, rely=0.07, relheight=0.858, relwidth=0.55)
        
        self.lbox.configure(font= Font_tuple2)
        
        self.scrollbar = tk.Scrollbar(self.root)
        self.scrollbar.pack(side = tk.RIGHT, fill = tk.BOTH)
        
        self.lbox.config(yscrollcommand = self.scrollbar.set)
  
        self.scrollbar.config(command = self.lbox.yview)

        self.clonebutton = tk.Button(self.root, text="Clone Repositories", font=('Arial', 8, 'bold'), command=lambda:(threading.Thread(target=_clone_and_analyze.CloneOpenSourceRepositories,args=(self.lbox,)).start()))
        self.clonebutton.place(relx=0.1, rely=0.3, height=45, width = 125)
        
        self.Analyzebutton = tk.Button(self.root, text="Analyze Repositories", font=('Arial', 8, 'bold'), command=lambda:(threading.Thread(target=_clone_and_analyze.AnalyseRepositories,args=(self.lbox,)).start()))
        self.Analyzebutton.place(relx=0.1, rely=0.6, height=45, width = 125)
        self.root.mainloop()
        
UserInterface()