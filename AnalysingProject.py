from email.mime import base
from unittest.mock import Base


class cppClass:
    def __init__(self):
        self.className = None
        self.Baseclasses = [] #Stores Parents cppClass Objects for derived class
        self.purevirtualfunctions = []
        self.virtualfunctions = []
        self.normalfunctions = []
        self.overridenfunctions = []
    def getoverridenfunctions(self):
        for baseclass in self.Baseclasses:
            for pure in baseclass.purevirtualfunctions:
                if pure in self.virtualfunctions:
                    print(pure)
                    self.overridenfunctions.append(pure)
    def totalMethods (self):
        TotalMethods = []
        TotalMethods += self.purevirtualfunctions
        TotalMethods += self.virtualfunctions
        TotalMethods += self.normalfunctions
        return TotalMethods
    def is_interface (self):
        return self.normalfunctions == 0 and self.virtualfunctions == 0 and self.purevirtualfunctions != 0
    def is_abstract (self):
        return self.normalfunctions != 0 or self.virtualfunctions != 0 and self.purevirtualfunctions != 0
    def is_derivedclass(self):
        return len(self.Baseclasses) != 0
    def classMethods(self):
        return self.normalfunctions, self.virtualfunctions, self.purevirtualfunctions

# modelling Each inheritance 
class InheritanceData:
    def __init__(self):
        self.derivedclassName = None
        self.ParentClassNames = []
        self.derivedAdditionalfunctions = []
        self.Addedpurevirtualfunctions = []
        self.Addedvirtualfunctions = []
        self.Addednormalfunctions = []
        self.overridenfunctions = []
        self.typeofinheritance = None
        self.inherited_pure_virtual = []
        self.inherited_virtual = []
        self.inherited_normal = []
        self.inherited_overriden = []
        self.TypeOfClass = None
    def determineinheritanceType(self):
        if len(self.inherited_virtual) == 0 and len(self.inherited_normal) == 0 and len(self.inherited_overriden) == 0 and len(self.inherited_pure_virtual):
            self.typeofinheritance = "Interface inheritance"
        else: self.typeofinheritance = "Implementation inheritance"
        
class ProjectData:
    def __init__(self):
        self.cppClasses = {} #stores classes information in the project
        self.cppClassesNew = {} #stores project classes inheritance information 
        self.ProjectInheritanceData = [] #Store each inheritance information Data
    def getinheritancedata(self, className):
        for inheritancedata in self.ProjectInheritanceData:
            if inheritancedata.derivedclassName == className:
                return inheritancedata
    def insertclass(self, _class):
        self.cppClasses[_class.className] = _class
    def getcppClass(self, classname):
        return self.cppClasses[classname] 
    def is_interfaceinheritance(self, baseclasstypes):
       if len(baseclasstypes) == 0:
         return
       return (len(set(baseclasstypes)) == 1 and baseclasstypes[0] == 1)
    def computeInheritanceData(self):
        for _class in self.cppClasses:
            if self.cppClasses[_class].is_derivedclass():
                inheritancedata = InheritanceData()
                inheritancedata.Addedpurevirtualfunctions = self.cppClasses[_class].purevirtualfunctions
                inheritancedata.Addedvirtualfunctions = self.cppClasses[_class].purevirtualfunctions
                inheritancedata.Addednormalfunctions = self.cppClasses[_class].normalfunctions
                self.cppClasses[_class].getoverridenfunctions()
                inheritancedata.overridenfunctions += self.cppClasses[_class].overridenfunctions
                inheritancedata.derivedclassName = _class
                inherited_pure_virtual = []
                inherited_virtual = []
                inherited_normal = []
                inherited_overriden = []
                baseresults = []
                for Baseclass in self.cppClasses[_class].Baseclasses:
                    if self.getinheritancedata(Baseclass.className) != None:
                        print(Baseclass.className)
                        inherited_pure_virtual += self.getinheritancedata(Baseclass.className).inherited_pure_virtual
                        inherited_virtual += self.getinheritancedata(Baseclass.className).inherited_virtual
                        inherited_normal += self.getinheritancedata(Baseclass.className).inherited_normal
                        inherited_overriden += self.getinheritancedata(Baseclass.className).inherited_overriden
                        inherited_pure_virtual += Baseclass.purevirtualfunctions
                        inherited_virtual += Baseclass.virtualfunctions
                        inherited_normal += Baseclass.normalfunctions
                        inherited_overriden += Baseclass.overridenfunctions
                    else:
                        inherited_pure_virtual += Baseclass.purevirtualfunctions
                        inherited_virtual += Baseclass.virtualfunctions
                        inherited_normal += Baseclass.normalfunctions
                        inherited_overriden += Baseclass.overridenfunctions
                inheritancedata.inherited_pure_virtual = inherited_pure_virtual
                inheritancedata.inherited_virtual = inherited_virtual
                inheritancedata.inherited_normal = inherited_normal
                inheritancedata.inherited_overriden = inherited_overriden
                inheritancedata.determineinheritanceType()
                self.ProjectInheritanceData.append(inheritancedata)
        self.PrintResults()
        return self.ProjectInheritanceData
    
    #Re-arranging inheritance in form of Superclass and its subclasses to get Hierachy DEPTHS
    def organizeHierachy(self):
        for _class in self.cppClasses:
            for baseclass in self.cppClasses[_class].Baseclasses:
                if baseclass.className in self.cppClassesNew:
                   self.cppClassesNew[baseclass.className].Baseclasses.append(self.cppClasses[_class])
                else:
                   self.cppClassesNew[baseclass.className] = self.cppClasses[baseclass.className]
                   self.cppClassesNew[baseclass.className].Baseclasses = []
                   self.cppClassesNew[baseclass.className].Baseclasses.append(self.cppClasses[_class])
        return self.traverse_all_Hierachy()
    
    # Traverse The Hierachies and get all present classes Depths
    def traverse_all_Hierachy(self):
        traversedNodes = []
        hierachiesLevels = []
        for _class in self.cppClassesNew:
            level = {}
            if not _class in traversedNodes:
              traversedNodes += self.breadth_first_trasversal(_class, level)
              hierachiesLevels.append(level)
              #print(traversedNodes)
        return hierachiesLevels
    #Do Breadth first traversal on each inheritance hierachy 
    def breadth_first_trasversal(self, current_node, level):
        visit_complete = []
        visit_complete.append(current_node)
        queue = []
        queue.append(current_node)
        level[current_node] = 0
        while queue:
            s = queue.pop(0)
            #print(s)
            if s in self.cppClassesNew:
                for neighbour in self.cppClassesNew[s].Baseclasses:
                    if neighbour.className not in visit_complete:
                        level[neighbour.className] = level[s] + 1
                        visit_complete.append(neighbour.className)
                        queue.append(neighbour.className)
        return visit_complete  
    
    def PrintResults (self):
        for INDEX, inheritance in enumerate(self.ProjectInheritanceData):
            print("")
            print("inheritance number: ", INDEX + 1)
            print("Type of inheritance: ", inheritance.typeofinheritance)
            print("     Derived Class Data")
            print("         Additional Child Methods: ", inheritance.derivedAdditionalfunctions)
            print("         Overriden Functions: ", inheritance.overridenfunctions)
            print("         Inherited Virtual Functions: ", inheritance.inherited_virtual)
            print("         Inherited Pure Virtual Functions: ", inheritance.inherited_pure_virtual)
            print("         Inherited Normal Functions: ", inheritance.inherited_normal)
            print("         Inherited Overriden Functions: ", inheritance.inherited_overriden)