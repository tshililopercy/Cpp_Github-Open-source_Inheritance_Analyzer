class cppClass:
    def __init__(self):
        self.className = None
        self.Baseclasses = [] #Stores Parents cppClass Objects for derived class
        self.publicMethods = {"purevirtualfunctions": [],"virtualfunctions": [], "normalfunctions": []}
        self.protectedMethods = {"purevirtualfunctions": [],"virtualfunctions": [], "normalfunctions": []}
        self.privateMethods = {"purevirtualfunctions": [],"virtualfunctions": [], "normalfunctions": []} # pure virtual functions[], virtual functions[], normal functions[]
        self.overridenfunctions = []
    def getoverridenfunctions(self):
        for baseclass in self.Baseclasses:
            for pure in baseclass.publicMethods["purevirtualfunctions"]:
                if pure in self.publicMethods["virtualfunctions"]:
                    self.overridenfunctions.append(pure)
    def is_interface (self):
        return (self.publicMethods["normalfunctions"] == 0 and self.publicMethods["virtualfunctions"]== 0 and 
                self.privateMethods["normalfunctions"] == 0 and self.privateMethods["virtualfunctions"]== 0 and
                self.protectedMethods["normalfunctions"] == 0 and self.protectedMethods["virtualfunctions"]== 0 
                and self.publicMethods["purevirtualfunctions"] != 0 or self.privateMethods["purevirtualfunctions"] != 0 or self.publicMethods["purevirtualfunctions"] != 0)
    def is_abstract (self):
        return not self.is_interface() and not self.is_Concrete()
    def is_Concrete(self):
        return (self.publicMethods["normalfunctions"] != 0 or self.publicMethods["virtualfunctions"]!= 0 or 
                self.privateMethods["normalfunctions"] != 0 or self.privateMethods["virtualfunctions"]== 0 or
                self.protectedMethods["normalfunctions"] != 0 or self.protectedMethods["virtualfunctions"] != 0
                and self.publicMethods["purevirtualfunctions"] == 0 and self.privateMethods["purevirtualfunctions"] == 0 and self.publicMethods["purevirtualfunctions"] == 0)
    def is_derivedclass(self):
        return len(self.Baseclasses) != 0

# modelling Each inheritance 
class InheritanceData:
    def __init__(self):
        self.derivedclassName = None
        self.Parents = []
        self.PublicMethods = {"Addedpurevirtualfunctions": [],"Addedvirtualfunctions":[],"Addednormalfunctions":[], "inherited_pure_virtual": [], "inherited_virtual":[], "inherited_normal": []}
        self.ProtectedMethods = {"Addedpurevirtualfunctions": [],"Addedvirtualfunctions":[],"Addednormalfunctions":[], "inherited_pure_virtual": [], "inherited_virtual":[], "inherited_normal": []}
        self.PrivateMethods = {"Addedpurevirtualfunctions": [],"Addedvirtualfunctions":[],"Addednormalfunctions":[], "inherited_pure_virtual": [], "inherited_virtual":[], "inherited_normal": []}
        self.overridenfunctions = []
        self.typeofinheritance = None
        self.inherited_overriden = []
        self.TypeOfClass = None
        #Data For Inheritance Analysis
        self.PublicInterface = [] # Public methods of a class
        self.Novelmethods = [] #added public normal, added virtual functions
    def compute_public_interface(self):
        self.PublicInterface += self.PublicMethods['Addedvirtualfunctions']
        self.PublicInterface += self.PublicMethods["Addednormalfunctions"]
        self.PublicInterface += self.PublicMethods["inherited_virtual"]
        self.PublicInterface += self.PublicMethods["inherited_normal"]
    def compute_Added_Methods(self):
        self.Novelmethods += self.PublicMethods["Addednormalfunctions"]
        self.Novelmethods += self.PublicMethods['Addedvirtualfunctions']
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
            elif inherited_virtual in (self.ProtectedMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                #print(self.overridenfunctions)
                self.ProtectedMethods["Addedvirtualfunctions"].remove(inherited_virtual)
        #In Private section
        for inherited_virtual in self.PrivateMethods["inherited_pure_virtual"]:
            if inherited_virtual in (self.PrivateMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                # print(self.overridenfunctions)
                self.PrivateMethods["Addedvirtualfunctions"].remove(inherited_virtual)
            elif inherited_virtual in (self.PublicMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                #print(self.overridenfunctions)
                self.PublicMethods["Addedvirtualfunctions"].remove(inherited_virtual)
            elif inherited_virtual in (self.ProtectedMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                #print(self.overridenfunctions)
                self.ProtectedMethods["Addedvirtualfunctions"].remove(inherited_virtual)
        #In Protected Section
        for inherited_virtual in self.ProtectedMethods["inherited_pure_virtual"]:
            if inherited_virtual in (self.ProtectedMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                #print(self.overridenfunctions)
                self.ProtectedMethods["Addedvirtualfunctions"].remove(inherited_virtual)
            elif inherited_virtual in (self.PrivateMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                #print(self.overridenfunctions)
                self.PrivateMethods["Addedvirtualfunctions"].remove(inherited_virtual)
            elif inherited_virtual in (self.PublicMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                #print(self.overridenfunctions)
                self.PublicMethods["Addedvirtualfunctions"].remove(inherited_virtual) 
        #-------------Overriden virtual functions-------------#
        #In public Section
        for inherited_virtual in self.PublicMethods["inherited_virtual"]:
            if inherited_virtual in (self.PublicMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                self.PublicMethods["Addedvirtualfunctions"].remove(inherited_virtual)
            elif inherited_virtual in (self.PrivateMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                self.PrivateMethods["Addedvirtualfunctions"].remove(inherited_virtual)
            elif inherited_virtual in (self.ProtectedMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                self.ProtectedMethods["Addedvirtualfunctions"].remove(inherited_virtual)
        #In Private Section
        for inherited_virtual in self.PrivateMethods["inherited_virtual"]:
            if inherited_virtual in (self.PrivateMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                self.PrivateMethods["Addedvirtualfunctions"].remove(inherited_virtual)
            elif inherited_virtual in (self.PublicMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                self.PublicMethods["Addedvirtualfunctions"].remove(inherited_virtual)
            elif inherited_virtual in (self.ProtectedMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                self.ProtectedMethods["Addedvirtualfunctions"].remove(inherited_virtual)
        #In Protected Section 
        for inherited_virtual in self.ProtectedMethods["inherited_virtual"]:
            if inherited_virtual in (self.PublicMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                self.PublicMethods["Addedvirtualfunctions"].remove(inherited_virtual)
            elif inherited_virtual in (self.PrivateMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                self.PrivateMethods["Addedvirtualfunctions"].remove(inherited_virtual)
            elif inherited_virtual in (self.PublicMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                self.PublicMethods["Addedvirtualfunctions"].remove(inherited_virtual)
    #Determine inheritance type
    def determineinheritanceType(self):
        if (len(self.PublicMethods["inherited_virtual"]) == 0 and len(self.PrivateMethods["inherited_virtual"]) == 0 and len(self.ProtectedMethods["inherited_virtual"]) == 0
        and len(self.PrivateMethods["inherited_normal"]) == 0 and len(self.inherited_overriden) == 0 and len(self.PublicMethods["inherited_normal"]) == 0 and len(self.ProtectedMethods["inherited_normal"]) == 0 
        and (self.PublicMethods["inherited_pure_virtual"] != 0 or self.PrivateMethods["inherited_pure_virtual"] != 0 or self.PrivateMethods["inherited_pure_virtual"])):
            self.typeofinheritance = "Interface Inheritance"
        else: self.typeofinheritance = "Implementation Inheritance"

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
    def PureVirtualPresentInProtected(self):
        for pure_virtual in self.ProtectedMethods["inherited_pure_virtual"]:
            if not pure_virtual in self.overridenfunctions and not pure_virtual in self.inherited_overriden:
                return True
        return False
    def identifyClassType(self):
        #The OR should Be In The Same Place
        if (len(self.PublicMethods["inherited_virtual"]) == 0 and len(self.PublicMethods["inherited_normal"]) == 0 and len(self.inherited_overriden) == 0 and (len(self.PublicMethods["inherited_pure_virtual"]) != 0 or len(self.PublicMethods["Addedpurevirtualfunctions"]) != 0) and len(self.PublicMethods["Addedvirtualfunctions"]) == 0 and len(self.PublicMethods["Addednormalfunctions"]) == 0 and 
        len(self.overridenfunctions) == 0 and len(self.PrivateMethods["inherited_virtual"]) == 0 and len(self.PrivateMethods["inherited_normal"]) == 0 and len(self.inherited_overriden) == 0 and (len(self.PrivateMethods["inherited_pure_virtual"]) != 0 or len(self.PrivateMethods["Addedpurevirtualfunctions"]) != 0)and len(self.PrivateMethods["Addedvirtualfunctions"]) == 0 and len(self.PrivateMethods["Addednormalfunctions"]) == 0
        and len(self.ProtectedMethods["inherited_virtual"]) == 0 and len(self.ProtectedMethods["inherited_normal"]) == 0 and (len(self.ProtectedMethods["inherited_pure_virtual"]) !=0 or len(self.ProtectedMethods["Addedpurevirtualfunctions"])) and len(self.ProtectedMethods["Addedvirtualfunctions"]) == 0 and len(self.ProtectedMethods["Addednormalfunctions"]) == 0):
            self.TypeOfClass = "Interface Class"
        elif len(self.PublicMethods["Addedpurevirtualfunctions"]) == 0 and len(self.ProtectedMethods["Addedpurevirtualfunctions"]) == 0 and len(self.PrivateMethods["Addedpurevirtualfunctions"]) == 0 and self.PureVirtualPresentInPublic() == False and self.PureVirtualPresentInPrivate() == False and self.PureVirtualPresentInProtected() == False:
            self.TypeOfClass = "Concrete Class"
        else:
            self.TypeOfClass = "Abstract Class"
                
class ProjectData:
    def __init__(self):
        self.cppClasses = {} #stores classes information in the project
        self.Declarations = []
        self.cppClassesNew = {} #stores project classes inheritance information 
        self.ProjectInheritanceData = [] #Store each inheritance information Data
    def getinheritancedata(self, className):
        for inheritancedata in self.ProjectInheritanceData:
            if inheritancedata.derivedclassName == className:
                return inheritancedata
    def getcppClass(self, classname):
        if classname in self.cppClasses:
            return self.cppClasses[classname]
        else:
            return {}
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
                
                inheritancedata.ProtectedMethods["Addedpurevirtualfunctions"] = self.cppClasses[_class].protectedMethods["purevirtualfunctions"]
                inheritancedata.ProtectedMethods["Addedvirtualfunctions"] = self.cppClasses[_class].protectedMethods["virtualfunctions"]
                inheritancedata.ProtectedMethods["Addednormalfunctions"] = self.cppClasses[_class].protectedMethods["normalfunctions"]
                inheritancedata.derivedclassName = _class
                inherited_overriden = []
                for Baseclass in self.cppClasses[_class].Baseclasses:

                    if Baseclass['inheritancetype'] == 'PUBLIC':
                        if self.getinheritancedata(Baseclass['BaseClassInfo'].className) != None:
                            inheritancedata.Parents.append(Baseclass['BaseClassInfo'].className)
                            inheritancedata.PublicMethods["inherited_pure_virtual"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).PublicMethods["inherited_pure_virtual"]
                            inheritancedata.PublicMethods["inherited_virtual"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).PublicMethods["inherited_virtual"]
                            inheritancedata.PublicMethods["inherited_normal"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).PublicMethods["inherited_normal"]
                            #For Protected Methods
                            inheritancedata.ProtectedMethods["inherited_pure_virtual"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).ProtectedMethods["inherited_pure_virtual"]
                            inheritancedata.ProtectedMethods["inherited_virtual"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).ProtectedMethods["inherited_virtual"]
                            inheritancedata.ProtectedMethods["inherited_normal"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).ProtectedMethods["inherited_normal"]
                            # computing For Private Method
                            inheritancedata.PrivateMethods["inherited_pure_virtual"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).PrivateMethods["inherited_pure_virtual"]
                            inheritancedata.PrivateMethods["inherited_virtual"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).PrivateMethods["inherited_virtual"]
                            #inheritancedata.PrivateMethods["inherited_normal"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).PrivateMethods["inherited_normal"]
                            inherited_overriden += self.getinheritancedata(Baseclass['BaseClassInfo'].className).inherited_overriden
                            inherited_overriden += self.getinheritancedata(Baseclass['BaseClassInfo'].className).overridenfunctions
                            inheritancedata.PublicMethods["inherited_pure_virtual"] += Baseclass['BaseClassInfo'].publicMethods["purevirtualfunctions"]
                            inheritancedata.PublicMethods["inherited_virtual"] += Baseclass['BaseClassInfo'].publicMethods["virtualfunctions"]
                            inheritancedata.PublicMethods["inherited_normal"] += Baseclass['BaseClassInfo'].publicMethods["normalfunctions"]
                            # computing For Private
                            inheritancedata.PrivateMethods["inherited_pure_virtual"] += Baseclass['BaseClassInfo'].privateMethods["purevirtualfunctions"]
                            inheritancedata.PrivateMethods["inherited_virtual"] += Baseclass['BaseClassInfo'].privateMethods["virtualfunctions"]
                            #inheritancedata.PrivateMethods["inherited_normal"] += Baseclass.privateMethods["normalfunctions"]
                            inheritancedata.ProtectedMethods["inherited_pure_virtual"] += Baseclass['BaseClassInfo'].protectedMethods["purevirtualfunctions"]
                            inheritancedata.ProtectedMethods["inherited_virtual"] += Baseclass['BaseClassInfo'].protectedMethods["virtualfunctions"]
                            inheritancedata.ProtectedMethods["inherited_normal"] += Baseclass['BaseClassInfo'].protectedMethods["normalfunctions"]
                        else:
                            inheritancedata.Parents.append(Baseclass['BaseClassInfo'].className)
                            inheritancedata.PublicMethods["inherited_pure_virtual"] += Baseclass['BaseClassInfo'].publicMethods["purevirtualfunctions"]
                            inheritancedata.PublicMethods["inherited_virtual"] += Baseclass['BaseClassInfo'].publicMethods["virtualfunctions"]
                            inheritancedata.PublicMethods["inherited_normal"] += Baseclass['BaseClassInfo'].publicMethods["normalfunctions"]
                            #Compute for Private
                            inheritancedata.PrivateMethods["inherited_pure_virtual"] += Baseclass['BaseClassInfo'].privateMethods["purevirtualfunctions"]
                            inheritancedata.PrivateMethods["inherited_virtual"] += Baseclass['BaseClassInfo'].privateMethods["virtualfunctions"]
                            #inheritancedata.PrivateMethods["inherited_normal"] += Baseclass.privateMethods["normalfunctions"]
                            inheritancedata.ProtectedMethods["inherited_pure_virtual"] += Baseclass['BaseClassInfo'].protectedMethods["purevirtualfunctions"]
                            inheritancedata.ProtectedMethods["inherited_virtual"] += Baseclass['BaseClassInfo'].protectedMethods["virtualfunctions"]
                            inheritancedata.ProtectedMethods["inherited_normal"] += Baseclass['BaseClassInfo'].protectedMethods["normalfunctions"]
                    #-------------------------For Private inheritance----------------------------#
                    elif Baseclass['inheritancetype'] == 'PRIVATE':
                        if self.getinheritancedata(Baseclass['BaseClassInfo'].className) != None:
                            inheritancedata.Parents.append(Baseclass['BaseClassInfo'].className)
                            inheritancedata.PrivateMethods["inherited_pure_virtual"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).PublicMethods["inherited_pure_virtual"]
                            inheritancedata.PrivateMethods["inherited_virtual"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).PublicMethods["inherited_virtual"]
                            inheritancedata.PrivateMethods["inherited_normal"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).PublicMethods["inherited_normal"]
                            #For Protected Methods
                            inheritancedata.PrivateMethods["inherited_pure_virtual"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).protectedMethods["inherited_pure_virtual"]
                            inheritancedata.PrivateMethods["inherited_virtual"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).protectedMethods["inherited_virtual"]
                            inheritancedata.PrivateMethods["inherited_normal"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).protectedMethods["inherited_virtual"]
                            # computing For Private Method
                            inheritancedata.PrivateMethods["inherited_pure_virtual"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).PrivateMethods["inherited_pure_virtual"]
                            inheritancedata.PrivateMethods["inherited_virtual"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).PrivateMethods["inherited_virtual"]
                            #inheritancedata.PrivateMethods["inherited_normal"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).PrivateMethods["inherited_normal"]
                            inherited_overriden += self.getinheritancedata(Baseclass['BaseClassInfo'].className).inherited_overriden
                            inherited_overriden += self.getinheritancedata(Baseclass['BaseClassInfo'].className).overridenfunctions
                            inheritancedata.PrivateMethods["inherited_pure_virtual"] += Baseclass['BaseClassInfo'].publicMethods["purevirtualfunctions"]
                            inheritancedata.PrivateMethods["inherited_virtual"] += Baseclass['BaseClassInfo'].publicMethods["virtualfunctions"]
                            inheritancedata.PrivateMethods["inherited_normal"] += Baseclass['BaseClassInfo'].publicMethods["normalfunctions"]
                            # computing For Private section
                            inheritancedata.PrivateMethods["inherited_pure_virtual"] += Baseclass['BaseClassInfo'].privateMethods["purevirtualfunctions"]
                            inheritancedata.PrivateMethods["inherited_virtual"] += Baseclass['BaseClassInfo'].privateMethods["virtualfunctions"]
                            #inheritancedata.PrivateMethods["inherited_normal"] += Baseclass['BaseClassInfo'].privateMethods["normalfunctions"]
                            #For Protected Methods
                            inheritancedata.PrivateMethods["inherited_pure_virtual"] += Baseclass['BaseClassInfo'].protectedMethods["purevirtualfunctions"]
                            inheritancedata.PrivateMethods["inherited_virtual"] += Baseclass['BaseClassInfo'].protectedMethods["virtualfunctions"]
                            inheritancedata.PrivateMethods["inherited_normal"] += Baseclass['BaseClassInfo'].protectedMethods["normalfunctions"]
                        else:
                            inheritancedata.Parents.append(Baseclass['BaseClassInfo'].className)
                            inheritancedata.PrivateMethods["inherited_pure_virtual"] += Baseclass['BaseClassInfo'].publicMethods["purevirtualfunctions"]
                            inheritancedata.PrivateMethods["inherited_virtual"] += Baseclass['BaseClassInfo'].publicMethods["virtualfunctions"]
                            inheritancedata.PrivateMethods["inherited_normal"] += Baseclass['BaseClassInfo'].publicMethods["normalfunctions"]
                            #Compute for Private
                            inheritancedata.PrivateMethods["inherited_pure_virtual"] += Baseclass['BaseClassInfo'].privateMethods["purevirtualfunctions"]
                            inheritancedata.PrivateMethods["inherited_virtual"] += Baseclass['BaseClassInfo'].privateMethods["virtualfunctions"]
                            #inheritancedata.PrivateMethods["inherited_normal"] += Baseclass['BaseClassInfo'].privateMethods["normalfunctions"]
                            #For Protected Methods
                            inheritancedata.PrivateMethods["inherited_pure_virtual"] += Baseclass['BaseClassInfo'].protectedMethods["purevirtualfunctions"]
                            inheritancedata.PrivateMethods["inherited_virtual"] += Baseclass['BaseClassInfo'].protectedMethods["virtualfunctions"]
                            inheritancedata.PrivateMethods["inherited_normal"] += Baseclass['BaseClassInfo'].protectedMethods["normalfunctions"]
                            
                    elif Baseclass['inheritancetype'] == 'PROTECTED':
                        if self.getinheritancedata(Baseclass['BaseClassInfo'].className) != None:
                            inheritancedata.Parents.append(Baseclass['BaseClassInfo'].className)
                            inheritancedata.ProtectedMethods["inherited_pure_virtual"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).PublicMethods["inherited_pure_virtual"]
                            inheritancedata.ProtectedMethods["inherited_virtual"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).PublicMethods["inherited_virtual"]
                            inheritancedata.ProtectedMethods["inherited_normal"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).PublicMethods["inherited_normal"]
                            # computing For Private Method
                            inheritancedata.PrivateMethods["inherited_pure_virtual"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).PrivateMethods["inherited_pure_virtual"]
                            inheritancedata.PrivateMethods["inherited_virtual"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).PrivateMethods["inherited_virtual"]
                            #inheritancedata.PrivateMethods["inherited_normal"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).PrivateMethods["inherited_normal"]
                            #Compute For Protected
                            inheritancedata.ProtectedMethods["inherited_pure_virtual"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).ProtectedMethods["inherited_pure_virtual"]
                            inheritancedata.ProtectedMethods["inherited_virtual"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).ProtectedMethods["inherited_virtual"]
                            inheritancedata.ProtectedMethods["inherited_normal"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).ProtectedMethods["inherited_normal"]
                            inherited_overriden += self.getinheritancedata(Baseclass['BaseClassInfo'].className).inherited_overriden
                            inherited_overriden += self.getinheritancedata(Baseclass['BaseClassInfo'].className).overridenfunctions
                            inheritancedata.ProtectedMethods["inherited_pure_virtual"] += Baseclass['BaseClassInfo'].publicMethods["purevirtualfunctions"]
                            inheritancedata.ProtectedMethods["inherited_virtual"] += Baseclass['BaseClassInfo'].publicMethods["virtualfunctions"]
                            inheritancedata.ProtectedMethods["inherited_normal"] += Baseclass['BaseClassInfo'].publicMethods["normalfunctions"]
                            # computing For Private
                            inheritancedata.PrivateMethods["inherited_pure_virtual"] += Baseclass['BaseClassInfo'].privateMethods["purevirtualfunctions"]
                            inheritancedata.PrivateMethods["inherited_virtual"] += Baseclass['BaseClassInfo'].privateMethods["virtualfunctions"]
                            #inheritancedata.PrivateMethods["inherited_normal"] += Baseclass.privateMethods["normalfunctions"]
                            
                            inheritancedata.ProtectedMethods["inherited_pure_virtual"] += Baseclass['BaseClassInfo'].protectedMethods["purevirtualfunctions"]
                            inheritancedata.ProtectedMethods["inherited_virtual"] += Baseclass['BaseClassInfo'].protectedMethods["virtualfunctions"]
                            inheritancedata.ProtectedMethods["inherited_normal"] += Baseclass['BaseClassInfo'].protectedMethods["normalfunctions"]
                        else:
                            inheritancedata.Parents.append(Baseclass['BaseClassInfo'].className)
                            inheritancedata.ProtectedMethods["inherited_pure_virtual"] += Baseclass['BaseClassInfo'].publicMethods["purevirtualfunctions"]
                            inheritancedata.ProtectedMethods["inherited_virtual"] += Baseclass['BaseClassInfo'].publicMethods["virtualfunctions"]
                            inheritancedata.ProtectedMethods["inherited_normal"] += Baseclass['BaseClassInfo'].publicMethods["normalfunctions"]
                            #Compute for Private
                            inheritancedata.PrivateMethods["inherited_pure_virtual"] += Baseclass['BaseClassInfo'].privateMethods["purevirtualfunctions"]
                            inheritancedata.PrivateMethods["inherited_virtual"] += Baseclass['BaseClassInfo'].privateMethods["virtualfunctions"]
                            #inheritancedata.PrivateMethods["inherited_normal"] += Baseclass.privateMethods["normalfunctions"]
                            inheritancedata.ProtectedMethods["inherited_pure_virtual"] += Baseclass['BaseClassInfo'].protectedMethods["purevirtualfunctions"]
                            inheritancedata.ProtectedMethods["inherited_virtual"] += Baseclass['BaseClassInfo'].protectedMethods["virtualfunctions"]
                            inheritancedata.ProtectedMethods["inherited_normal"] += Baseclass['BaseClassInfo'].protectedMethods["normalfunctions"]
                inheritancedata.inherited_overriden = inherited_overriden
                inheritancedata.determineinheritanceType()
                inheritancedata.identifyoverridenfunctions()
                inheritancedata.identifyClassType()
                inheritancedata.compute_public_interface()
                inheritancedata.compute_Added_Methods()
                self.ProjectInheritanceData.append(inheritancedata)
        #self.PrintResults()
        return self.ProjectInheritanceData
    
    #Re-arranging inheritance in form of Superclass and its subclasses to get Hierachy DEPTHS
    def organizeHierachy(self):
        for _class in self.cppClasses:
            for baseclass in self.cppClasses[_class].Baseclasses:
                if baseclass['BaseClassInfo'].className in self.cppClassesNew:
                   Parent = {}
                   Parent['BaseClassInfo'] = self.cppClasses[_class]
                   Parent['inheritancetype'] = baseclass['inheritancetype']
                   self.cppClassesNew[baseclass['BaseClassInfo'].className].Baseclasses.append(Parent)
                else:
                   self.cppClassesNew[baseclass['BaseClassInfo'].className] = self.cppClasses[baseclass['BaseClassInfo'].className]
                   self.cppClassesNew[baseclass['BaseClassInfo'].className].Baseclasses = []
                   Parent = {}
                   Parent['BaseClassInfo'] = self.cppClasses[_class]
                   Parent['inheritancetype'] = baseclass['inheritancetype']
                   self.cppClassesNew[baseclass['BaseClassInfo'].className].Baseclasses.append(Parent)
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
                    if neighbour['BaseClassInfo'].className not in visit_complete:
                        level[neighbour['BaseClassInfo'].className] = level[s] + 1
                        visit_complete.append(neighbour['BaseClassInfo'].className)
                        queue.append(neighbour['BaseClassInfo'].className)
        return visit_complete  
    
    def PrintResults (self):
        for INDEX, inheritance in enumerate(self.ProjectInheritanceData):
            print("")
            print("inheritance number: ", INDEX + 1)
            print("Type of inheritance: ", inheritance.typeofinheritance)
            print("Type of class: ",inheritance.TypeOfClass)
            print("     Derived Class Data")
            print("         Overriden Functions: ", inheritance.overridenfunctions)
            print("         Inherited Virtual Functions: ", inheritance.PublicMethods["inherited_virtual"], "\n                                      ", inheritance.PrivateMethods["inherited_virtual"], "\n                                      ", inheritance.ProtectedMethods["inherited_virtual"])
            print("         Inherited Pure Virtual Functions: ", inheritance.PublicMethods["inherited_pure_virtual"], "\n                                           ", inheritance.PrivateMethods["inherited_pure_virtual"],"\n                                           ", inheritance.ProtectedMethods["inherited_pure_virtual"])
            print("         Inherited Normal Functions: ", inheritance.PublicMethods["inherited_normal"], "\n                                      ", inheritance.PrivateMethods["inherited_normal"], "\n                                      ", inheritance.ProtectedMethods["inherited_normal"])
            print("         Inherited Overriden Functions: ", inheritance.inherited_overriden)
            print("         Added Pure Virtual Functions: ", inheritance.PublicMethods["Addedpurevirtualfunctions"], "\n                                           ", inheritance.PrivateMethods["Addedpurevirtualfunctions"], "\n                                           ", inheritance.ProtectedMethods["Addedpurevirtualfunctions"])
            print("         Added Virtual Functions: ", inheritance.PublicMethods["Addedvirtualfunctions"], "\n                                           ", inheritance.PrivateMethods["Addedvirtualfunctions"], "\n                                           ", inheritance.ProtectedMethods["Addedvirtualfunctions"])
            print("         Added Normal Functions: ", inheritance.PublicMethods["Addednormalfunctions"], "\n                                           ", inheritance.PrivateMethods["Addednormalfunctions"], "\n                                           ", inheritance.ProtectedMethods["Addednormalfunctions"])