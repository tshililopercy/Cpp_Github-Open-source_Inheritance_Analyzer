class cppClass:
    def __init__(self):
        self.className = None
        self.Baseclasses = [] #Stores Parents cppClass Objects for derived class
        self.purevirtualfunctions = 0
        self.virtualfunctions = 0
        self.normalfunctions = 0 
        self.overridenfunctions = 0
    def totalMethods (self):
        TotalMethods = self.purevirtualfunctions + self.virtualfunctions + self.normalfunctions
        return TotalMethods
    def is_interface (self):
     return self.normalfunctions == 0 and self.virtualfunctions == 0 and self.purevirtualfunctions != 0
    def is_derivedclass(self):
        return len(self.Baseclasses) != 0
    def classMethods(self):
        return self.normalfunctions, self.virtualfunctions, self.purevirtualfunctions

# modelling Each inheritance 
class InheritanceData:
    def __init__(self):
        self.BaseClassesData = []
        self.derivedAdditionalfunctions = 0
        self.overridenfunctions = 0 
        self.typeofinheritance = None

class ProjectData:
    def __init__(self):
        self.cppClasses = {} #stores classes information in the project
        self.cppClassesNew = {} #stores project classes inheritance information 
        self.ProjectInheritanceData = [] #Store each inheritance information Data
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
                inheritancedata.derivedAdditionalfunctions = self.cppClasses[_class].totalMethods()
                inheritancedata.overridenfunctions = self.cppClasses[_class].overridenfunctions
                baseresults = []
                for Baseclass in self.cppClasses[_class].Baseclasses:
                    BaseData = {} # {purevirtualfunctions: ,virtualfunctions: ,normalfunctions}
                    baseresults.append(Baseclass.is_interface())
                    BaseData["purevirtualfunctions"] = Baseclass.purevirtualfunctions
                    BaseData["virtualfunctions"] = Baseclass.virtualfunctions
                    BaseData["normalfunctions"] = Baseclass.normalfunctions
                    inheritancedata.BaseClassesData.append(BaseData)
                if self.is_interfaceinheritance(baseresults):
                    inheritancedata.typeofinheritance = "Interface Inheritance"
                else:
                    inheritancedata.typeofinheritance = "Implementation Inheritance"
                self.ProjectInheritanceData.append(inheritancedata)
        self.organizeHierachy()
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
        
    
    def PrintResults (self):
        for INDEX, inheritance in enumerate(self.ProjectInheritanceData):
            print("")
            print("inheritance number: ", INDEX + 1)
            print("Type of inheritance: ", inheritance.typeofinheritance)
            print("     Derived Class Data")
            print("         Additional Child Methods: ", inheritance.derivedAdditionalfunctions)
            print("         Overriden Functions: ", inheritance.overridenfunctions)
            for index, base in enumerate(inheritance.BaseClassesData):
                if len(inheritance.BaseClassesData) == 1:
                   print(" Parent Data")
                else:
                   print(" Parent Number", index + 1, "Data") 
                print("     Pure Virtual Functions: ",base["purevirtualfunctions"])
                print("     Virtual Functions: ",base["virtualfunctions"])
                print("     Normal Functions: ",base["normalfunctions"])