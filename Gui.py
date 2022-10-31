from cgitb import enable
from shutil import rmtree
import tkinter as tk
import threading
import os

from StoreData import *
from tkinter import *
from tkinter import ttk

import Data_Extraction_Process_Refractored
import GitHub_Search_And_Clone
import Data_Compute

class Clone_And_Analyse:
    def __init__(self):
        self.ClonedRepos = []    
    def CloneOpenSourceRepositories(self,my_tree, button):
        cloner = GitHub_Search_And_Clone.Cloner()
        repos_info = cloner.get_repos_info()
        for item in my_tree.get_children():
                my_tree.delete(item)
        for repo in repos_info:
            # clear text
            # print clone status
            for item in my_tree.get_children():
                my_tree.delete(item)
            clonedRepo = []
            before_current = True
            for repo2 in repos_info:
                if (repo["name"] == repo2["name"]):
                    clonedRepo.append({'name': repo2["name"], 'status': 'Cloning...'})
                    before_current = False
                elif before_current:
                    clonedRepo.append({'name': repo2["name"], 'status': 'Clone Complete'})
                else:
                    clonedRepo.append({'name': repo2["name"], 'status': 'Waiting...'})
                self.ClonedRepos = clonedRepo
            for i, print_ in enumerate(clonedRepo):
                print(i)
                my_tree.insert(parent='', index='end',iid=i, text="", values=(print_["name"],print_["status"]), tags=('oddrow'))
            if repo["name"] != "tensorflow":
                cloner.cloneARepo(repo)
        button['state'] = "active"

    def AnalyseRepositories(self,my_tree):
        extractor = Data_Extraction_Process_Refractored.Extractor()
        #Deleting Data Available in HierachiesData.json, for new analysis
        open('HierachiesData.json', 'w').close()
        ClonedRepoNames = os.listdir('../Repository')
        for name in ClonedRepoNames:
            for item in my_tree.get_children():
                my_tree.delete(item)
            ClonedRepos = []
            before_current = True
            for name_2 in ClonedRepoNames:
                if (name == name_2):
                    ClonedRepos.append({'name': name_2, 'status': 'Analysing....'})
                    before_current = False
                elif before_current:
                    ClonedRepos.append({'name': name_2, 'status': 'Done Analysing'})
                else:
                    ClonedRepos.append({'name': name_2, 'status': 'Waiting...'})
            for i, print_ in enumerate(ClonedRepos):
                print(i)
                my_tree.insert(parent='', index='end',iid=i, text="", values=(print_["name"],print_["status"]))
            projectdatastorage = ProjectDataStorage(extractor.AnalyseRepository(name))
            projectdatastorage.ComputeHieracyData()
            
        # projectdatavisualize = Data_Compute.ProjectDataVisualize()
        # projectdatavisualize.PrintingHierachyData()


class GraphicalUserInterface:
    def __init__(self):
        _clone_and_analyze = Clone_And_Analyse()
        projectdatavisualize = Data_Compute.ProjectDataVisualize()
        self.root = tk.Tk()
        self.root.title("GitHub Open Source Inheritance Analyzer")
        screen_width = str(self.root.winfo_screenwidth()//2)
        screen_height = str(self.root.winfo_screenheight()//2)
        resolution =screen_width +'x'+screen_height
        self.root.geometry(resolution)
        self.root.resizable(False, False)
        style = ttk.Style()
        
        style.theme_use("default")
        #Configure our treeview colors
        
        style.configure("Treeview",
                        Background="silver",
                        foreground="black",
                        rowheight=25,
                        fieldbackground="silver"
                        )
        #Change selected color
        style.map('Treeview', 
                  background=[('selected', 'darkgrey')])
        style.configure("Treeview.Heading", font=("Comic Sans MS", 12,'bold'))
        tree_frame = Frame(self.root)
        tree_frame.place(relx=0.4)
        
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT,fill=Y)
        
        my_tree = ttk.Treeview(tree_frame, height = 14, yscrollcommand=tree_scroll.set)
        
        my_tree.pack()
        
        my_tree.tag_configure('rowsdisplay', background="grey", font=("Comic Sans MS", 11,))
        
        tree_scroll.config(command=my_tree.yview)
            
        self.Analyzebutton = tk.Button(self.root, text="Analyze Repositories", font=('Arial', 8, 'bold'), command=lambda:(threading.Thread(target=_clone_and_analyze.AnalyseRepositories,args=(my_tree,)).start()))
        self.Analyzebutton.place(relx=0.1, rely=0.6, height=45, width = 125)
        self.clonebutton = tk.Button(self.root, text="Clone Repositories", font=('Arial', 8, 'bold'), command=lambda:(threading.Thread(target=_clone_and_analyze.CloneOpenSourceRepositories,args=(my_tree,self.Analyzebutton,)).start()))
        self.clonebutton.place(relx=0.1, rely=0.3, height=45, width = 125)
        self.resultsbutton = tk.Button(self.root, text="Show results", font=('Arial', 8, 'bold'), command=lambda:(threading.Thread(target=projectdatavisualize.PrintingHierachyData()).start()))
        self.resultsbutton.place(relx=0.1, rely=0.8, height=35, width = 105)
        
        # Define Columns
        my_tree['columns'] = ("Repository Name", "Status")
        
        #Formate Columns
        my_tree.column("#0", width=0, stretch=NO)
        my_tree.column("Repository Name", anchor=W, width=240)
        my_tree.column("Status", anchor=W, width=150)
        
        my_tree.heading("#0", text="", anchor=W)
        my_tree.heading("Repository Name", text="Repository Name", anchor= W)
        my_tree.heading("Status", text="Status", anchor= W)
        
        self.root.mainloop()
        
GraphicalUserInterface()