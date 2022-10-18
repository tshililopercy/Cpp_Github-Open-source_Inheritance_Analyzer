from email.mime import base
from unittest.mock import Base


class cppClass:
    def __init__(self):
        self.className = None
        self.Baseclasses = [] #Stores Parents cppClass Objects for derived class
        self.publicMethods = {"purevirtualfunctions": [],"virtualfunctions": [], "normalfunctions": []}
        self.protectedMethods = {"purevirtualfunctions": [],"virtualfunctions": [], "normalfunctions": []}
        self.privateMethods = {"purevirtualfunctions": [],"virtualfunctions": [], "normalfunctions": []} # pure virtual functions[], virtual functions[], normal functions[]
        self.purevirtualfunctions = []
        self.virtualfunctions = []
        self.normalfunctions = []
        self.overridenfunctions = []
    def getoverridenfunctions(self):
        for baseclass in self.Baseclasses:
            for pure in baseclass.publicMethods["purevirtualfunctions"]:
                if pure in self.publicMethods["virtualfunctions"]:
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
        self.PublicMethods = {"Addedpurevirtualfunctions": [],"Addedvirtualfunctions":[],"Addednormalfunctions":[], "inherited_pure_virtual": [], "inherited_virtual":[], "inherited_normal": []}
        self.ProtectedMethods = {"Addedpurevirtualfunctions": [],"Addedvirtualfunctions":[],"Addednormalfunctions":[], "inherited_pure_virtual": [], "inherited_virtual":[], "inherited_normal": []}
        self.PrivateMethods = {"Addedpurevirtualfunctions": [],"Addedvirtualfunctions":[],"Addednormalfunctions":[], "inherited_pure_virtual": [], "inherited_virtual":[], "inherited_normal": []}
        self.overridenfunctions = []
        self.typeofinheritance = None
        self.inherited_overriden = []
        self.TypeOfClass = None
    def identifyoverridenfunctions(self):
        #-------------Overriden pure virtual functions-------------#
        #In Public Section
        for inherited_virtual in self.PublicMethods["inherited_pure_virtual"]:
            if inherited_virtual in (self.PublicMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                #print(self.overridenfunctions)
                self.PublicMethods["Addedvirtualfunctions"].remove(inherited_virtual)
            elif inherited_virtual in (self.PrivateMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                #print(self.overridenfunctions)
                self.PrivateMethods["Addedvirtualfunctions"].remove(inherited_virtual) 
        #In Private section
        for inherited_virtual in self.PrivateMethods["inherited_pure_virtual"]:
            if inherited_virtual in (self.PrivateMethods["Addedvirtualfunctions"] or self.PrivateMethods["Addednormalfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                print(self.overridenfunctions)
                self.PrivateMethods["Addedvirtualfunctions"].remove(inherited_virtual)
            elif inherited_virtual in (self.PublicMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                #print(self.overridenfunctions)
                self.PublicMethods["Addedvirtualfunctions"].remove(inherited_virtual)
        #-------------Overriden virtual functions-------------#
        #In public Section
        for inherited_virtual in self.PublicMethods["inherited_virtual"]:
            if inherited_virtual in (self.PublicMethods["Addedvirtualfunctions"] or self.PublicMethods["Addednormalfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                self.PublicMethods["Addedvirtualfunctions"].remove(inherited_virtual)
            elif inherited_virtual in (self.PrivateMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                self.PrivateMethods["Addedvirtualfunctions"].remove(inherited_virtual)    
        #In Private Section
        for inherited_virtual in self.PrivateMethods["inherited_virtual"]:
            if inherited_virtual in (self.PrivateMethods["Addedvirtualfunctions"] or self.PrivateMethods["Addednormalfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                self.PrivateMethods["Addedvirtualfunctions"].remove(inherited_virtual)
            elif inherited_virtual in (self.PublicMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                self.PublicMethods["Addedvirtualfunctions"].remove(inherited_virtual)
        
    #Determine inheritance type
    def determineinheritanceType(self):
        if len(self.PublicMethods["inherited_virtual"]) == 0 and len(self.PublicMethods["inherited_normal"]) == 0 and len(self.inherited_overriden) == 0 and len(self.PublicMethods["inherited_pure_virtual"]) and len(self.PrivateMethods["inherited_virtual"]) == 0 and len(self.PrivateMethods["inherited_normal"]) == 0 and len(self.PrivateMethods["inherited_pure_virtual"]) :
            self.typeofinheritance = "Interface inheritance"
        else: self.typeofinheritance = "Implementation inheritance"
    #Determine The Type of Class. (Abstract, interface or concrete class)
    #Abstract class: atleast one pure virtual function 
    #interface class: Strictly pure virtual functions
    #Conctrete class: Any instantiable class (no unoverriden pure virtual function)
    def PureVirtualPresentInPublic(self):
        for pure_virtual in self.PublicMethods["inherited_pure_virtual"]:
            if not pure_virtual in self.overridenfunctions and not pure_virtual in self.inherited_overriden:
                return True
        return False
    def PureVirtualPresentInPrivate(self):
        for pure_virtual in self.PrivateMethods["inherited_pure_virtual"]:
            if not pure_virtual in self.overridenfunctions and not pure_virtual in self.inherited_overriden:
                return True
        return False
    def identifyClassType(self):
        if len(self.PublicMethods["inherited_virtual"]) == 0 and len(self.PublicMethods["inherited_normal"]) == 0 and len(self.inherited_overriden) == 0 and (len(self.PublicMethods["inherited_pure_virtual"]) != 0 or len(self.PublicMethods["Addedpurevirtualfunctions"]) != 0)and len(self.PublicMethods["Addedvirtualfunctions"]) == 0 and len(self.PublicMethods["Addednormalfunctions"]) == 0 and len(self.overridenfunctions) == 0 and len(self.PrivateMethods["inherited_virtual"]) == 0 and len(self.PrivateMethods["inherited_normal"]) == 0 and len(self.inherited_overriden) == 0 and (len(self.PrivateMethods["inherited_pure_virtual"]) != 0 or len(self.PrivateMethods["Addedpurevirtualfunctions"]) != 0)and len(self.PrivateMethods["Addedvirtualfunctions"]) == 0 and len(self.PrivateMethods["Addednormalfunctions"]) == 0:
            self.TypeOfClass = "Interface Class"
        elif len(self.PublicMethods["Addedpurevirtualfunctions"]) == 0 and self.PureVirtualPresentInPublic() == False and self.PureVirtualPresentInPrivate() == False:
            self.TypeOfClass = "Concrete Class"
        else:
            self.TypeOfClass = "Abstract Class"
                
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
                inheritancedata.PublicMethods["Addedpurevirtualfunctions"] = self.cppClasses[_class].publicMethods["purevirtualfunctions"]
                inheritancedata.PublicMethods["Addedvirtualfunctions"] = self.cppClasses[_class].publicMethods["virtualfunctions"]
                inheritancedata.PublicMethods["Addednormalfunctions"] = self.cppClasses[_class].publicMethods["normalfunctions"]
                #Getting Private methods Data
                inheritancedata.PrivateMethods["Addedpurevirtualfunctions"] = self.cppClasses[_class].privateMethods["purevirtualfunctions"]
                inheritancedata.PrivateMethods["Addedvirtualfunctions"] = self.cppClasses[_class].privateMethods["virtualfunctions"]
                inheritancedata.PrivateMethods["Addednormalfunctions"] = self.cppClasses[_class].privateMethods["normalfunctions"]
                inheritancedata.derivedclassName = _class
                inherited_overriden = []
                for Baseclass in self.cppClasses[_class].Baseclasses:
                    if self.getinheritancedata(Baseclass.className) != None:
                        inheritancedata.PublicMethods["inherited_pure_virtual"] += self.getinheritancedata(Baseclass.className).PublicMethods["inherited_pure_virtual"]
                        inheritancedata.PublicMethods["inherited_virtual"] += self.getinheritancedata(Baseclass.className).PublicMethods["inherited_virtual"]
                        inheritancedata.PublicMethods["inherited_normal"] += self.getinheritancedata(Baseclass.className).PublicMethods["inherited_normal"]
                        # computing For Private Method
                        inheritancedata.PrivateMethods["inherited_pure_virtual"] += self.getinheritancedata(Baseclass.className).PrivateMethods["inherited_pure_virtual"]
                        inheritancedata.PrivateMethods["inherited_virtual"] += self.getinheritancedata(Baseclass.className).PrivateMethods["inherited_virtual"]
                        inheritancedata.PrivateMethods["inherited_normal"] += self.getinheritancedata(Baseclass.className).PrivateMethods["inherited_normal"]
                        inherited_overriden += self.getinheritancedata(Baseclass.className).inherited_overriden
                        inherited_overriden += self.getinheritancedata(Baseclass.className).overridenfunctions
                        inheritancedata.PublicMethods["inherited_pure_virtual"] += Baseclass.publicMethods["purevirtualfunctions"]
                        inheritancedata.PublicMethods["inherited_virtual"] += Baseclass.publicMethods["virtualfunctions"]
                        inheritancedata.PublicMethods["inherited_normal"] += Baseclass.publicMethods["normalfunctions"]
                        # computing For Private
                        inheritancedata.PrivateMethods["inherited_pure_virtual"] += Baseclass.privateMethods["purevirtualfunctions"]
                        inheritancedata.PrivateMethods["inherited_virtual"] += Baseclass.privateMethods["virtualfunctions"]
                        inheritancedata.PrivateMethods["inherited_normal"] += Baseclass.privateMethods["normalfunctions"]
                    else:
                        inheritancedata.PublicMethods["inherited_pure_virtual"] += Baseclass.publicMethods["purevirtualfunctions"]
                        inheritancedata.PublicMethods["inherited_virtual"] += Baseclass.publicMethods["virtualfunctions"]
                        inheritancedata.PublicMethods["inherited_normal"] += Baseclass.publicMethods["normalfunctions"]
                        #Compute for Private
                        inheritancedata.PrivateMethods["inherited_pure_virtual"] += Baseclass.privateMethods["purevirtualfunctions"]
                        inheritancedata.PrivateMethods["inherited_virtual"] += Baseclass.privateMethods["virtualfunctions"]
                        inheritancedata.PrivateMethods["inherited_normal"] += Baseclass.privateMethods["normalfunctions"]
                inheritancedata.inherited_overriden = inherited_overriden
                inheritancedata.determineinheritanceType()
                inheritancedata.identifyoverridenfunctions()
                inheritancedata.identifyClassType()
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
            print("Type of class: ",inheritance.TypeOfClass)
            print("     Derived Class Data")
            print("         Overriden Functions: ", inheritance.overridenfunctions)
            print("         Inherited Virtual Functions: ", inheritance.PublicMethods["inherited_virtual"])
            print("         Inherited Pure Virtual Functions: ", inheritance.PublicMethods["inherited_pure_virtual"], "\n                                           ", inheritance.PrivateMethods["inherited_pure_virtual"])
            print("         Inherited Normal Functions: ", inheritance.PublicMethods["inherited_normal"])
            print("         Inherited Overriden Functions: ", inheritance.inherited_overriden)
            print("         Added Pure Virtual Functions: ", inheritance.PublicMethods["Addedpurevirtualfunctions"])
            print("         Added Virtual Functions: ", inheritance.PublicMethods["Addedvirtualfunctions"])
            print("         Added Normal Functions: ", inheritance.PublicMethods["Addednormalfunctions"])