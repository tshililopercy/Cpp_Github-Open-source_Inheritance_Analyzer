import os
import re
import html
import clang.cindex

class cppClass:
    def __init__(self, cursor : clang.cindex.Cursor):

        self.filename = os.path.abspath(cursor.location.file.name).strip()
        
        self.relname = ""

        self.line = cursor.location.line
        
        
        self.location_file_name = self.filename
        
        self.location_file =  cursor.location.file
        
        self.className = None

        if cursor.kind == clang.cindex.CursorKind.CLASS_TEMPLATE:
            self.className = cursor.spelling
            #print(self.className)
        else:
            self.className = cursor.type.spelling
            #print(self.className)
    
        self.Baseclasses = []
        self.publicMethods = {"purevirtualfunctions": [],"virtualfunctions": [], "normalfunctions": []}
        self.protectedMethods = {"purevirtualfunctions": [],"virtualfunctions": [], "normalfunctions": []}
        self.privateMethods = {"purevirtualfunctions": [],"virtualfunctions": [], "normalfunctions": []} # pure virtual functions[], virtual functions[], normal functions[]
        self.typeofclass = None
        self.overridenfunctions = []
        self.declarations = []

    def addParentByFQN(self, fullyQualifiedClassName):
            
        self.Baseclasses.append(fullyQualifiedClassName)
        
    def getLocation(self) -> str:

        return str(f"{self.filename}:{self.line}\n")
		
    def isUnamed(self) -> bool:
        ret = "(unnamed struct" in self.className
        return ret
        
    def isAnonymous(self) -> bool:
        ret = "(anonymous struct" in self.className
        return ret
        #Stores the class Parents classes
    def BaseClassData(self, cursor, baseclassname):
        Parent = {}
        #print(baseclassname)
        Parent['BaseClassName'] = baseclassname
        if cursor.access_specifier == clang.cindex.AccessSpecifier.PUBLIC:
            Parent['inheritancetype'] = 'PUBLIC'
        elif cursor.access_specifier == clang.cindex.AccessSpecifier.PRIVATE:
            Parent['inheritancetype'] = 'PRIVATE'
        elif cursor.access_specifier == clang.cindex.AccessSpecifier.PROTECTED:
            Parent['inheritancetype'] = 'PROTECTED'
        return Parent
    def _getting_types_from_class_field(self, cursor):
        types = list()
        classfields = list(cursor.get_children())
        if len(classfields) == 0:
           types.append(cursor.type.spelling)
        else:
            types.append(cursor.type.spelling)
            for field in classfields:
                if field.kind == clang.cindex.CursorKind.TEMPLATE_REF:
                    types.append(field.spelling)
                elif field.kind == clang.cindex.CursorKind.TYPE_REF:
                    types.append(field.type.spelling)
        return types
        

        


    def _processClassMemberDeclaration(self, cursor):
        if cursor.kind == clang.cindex.CursorKind.CXX_BASE_SPECIFIER:
            for baseClass in cursor.get_children():
                if baseClass.kind == clang.cindex.CursorKind.TYPE_REF:
                    self.Baseclasses.append(self.BaseClassData(cursor,baseClass.type.spelling))
                elif baseClass.kind == clang.cindex.CursorKind.TEMPLATE_REF:
                    self.Baseclasses.append(self.BaseClassData(cursor,baseClass.spelling))
        elif cursor.kind == clang.cindex.CursorKind.CXX_METHOD:
            try:
                self.MethodsData(cursor)
            except:
                print("Invalid CXX_METHOD declaration! " + str(cursor.type.spelling))
                return
        elif cursor.kind == clang.cindex.CursorKind.FUNCTION_TEMPLATE:
            #Extract class Public Methods Signatures
            self.MethodsData(cursor)
        elif cursor.kind == clang.cindex.CursorKind.FIELD_DECL:
            self.declarations += self._getting_types_from_class_field(cursor)

    def MethodsData(self, cursor):
        returnType, argumentTypes = cursor.type.spelling.split(' ', 1)
        #Extract types from methods
        self.declarations.append(returnType)
        self.declarations.append(argumentTypes)
        print(self.declarations)
        if cursor.access_specifier == clang.cindex.AccessSpecifier.PUBLIC:
            #Extract information
            if cursor.is_pure_virtual_method():
                self.publicMethods["purevirtualfunctions"].append(cursor.spelling + ' ' + argumentTypes)
            elif cursor.is_virtual_method():
                self.publicMethods["virtualfunctions"].append(cursor.spelling + ' ' + argumentTypes)
            else:
                self.publicMethods["normalfunctions"].append(cursor.spelling + ' ' + argumentTypes)
        #Extract class Private Methods Signatures
        elif cursor.access_specifier == clang.cindex.AccessSpecifier.PRIVATE:
            if cursor.is_pure_virtual_method():
                self.privateMethods["purevirtualfunctions"].append(cursor.spelling + ' ' + argumentTypes)
            elif cursor.is_virtual_method():
                self.privateMethods["virtualfunctions"].append(cursor.spelling + ' ' + argumentTypes)
            else:
                self.privateMethods["normalfunctions"].append(cursor.spelling + ' ' + argumentTypes)
        #Extract class Protected Methods Signatures
        elif cursor.access_specifier == clang.cindex.AccessSpecifier.PROTECTED:
            if cursor.is_pure_virtual_method():
                self.protectedMethods["purevirtualfunctions"].append(cursor.spelling + ' ' + argumentTypes)
            elif cursor.is_virtual_method():
                self.protectedMethods["virtualfunctions"].append(cursor.spelling + ' ' + argumentTypes)
            else:
                self.protectedMethods["normalfunctions"].append(cursor.spelling + ' ' + argumentTypes)

    def Process(self,cursor):
        for c in cursor.get_children():
            self._processClassMemberDeclaration(c)


    def getoverridenfunctions(self):
        for baseclass in self.Baseclasses:
            for pure in baseclass.publicMethods["purevirtualfunctions"]:
                if pure in self.publicMethods["virtualfunctions"]:
                    self.overridenfunctions.append(pure)
    #Return True if class is interface class
    def is_interface (self):
        return ((len(self.publicMethods["normalfunctions"]) == 0 and len(self.publicMethods["virtualfunctions"])== 0 and 
                len(self.privateMethods["normalfunctions"]) == 0 and len(self.privateMethods["virtualfunctions"])== 0 and
                len(self.protectedMethods["normalfunctions"]) == 0 and len(self.protectedMethods["virtualfunctions"]) == 0) 
                and (len(self.publicMethods["purevirtualfunctions"]) != 0 or len(self.privateMethods["purevirtualfunctions"]) != 0 or len(self.publicMethods["purevirtualfunctions"]) != 0))
    #Returns True if class is Abstract Clas
    def is_abstract (self):
        return not self.is_interface() and not self.is_Concrete()
    #Returns True if class is Concrete Class
    def is_Concrete(self):
        return ((len(self.publicMethods["normalfunctions"]) != 0 or len(self.publicMethods["virtualfunctions"])!= 0 or 
                len(self.privateMethods["normalfunctions"]) != 0 or len(self.privateMethods["virtualfunctions"]) == 0 or
                len(self.protectedMethods["normalfunctions"]) != 0 or len(self.protectedMethods["virtualfunctions"]) != 0)
                and (len(self.publicMethods["purevirtualfunctions"]) == 0 and len(self.privateMethods["purevirtualfunctions"]) == 0 and len(self.publicMethods["purevirtualfunctions"]) == 0))
    #Returns the type Of Class (Concrete, Abstract or Interface)
    def getClassType(self):
        if self.is_interface():
            self.typeofclass = "Interface Class"
        elif self.is_abstract():
            self.typeofclass = "Abstract Class"
        elif self.is_Concrete():
            self.typeofclass = "Concrete Class"
        return self.typeofclass
    #Returns true if class is subclass
    def is_derivedclass(self):
        return len(self.Baseclasses) != 0

class InheritanceData:
    def __init__(self):
        self.derivedclassName = None
        self.Parents = []
        self.PublicMethods = {"Addedpurevirtualfunctions": [],"Addedvirtualfunctions":[],"Addednormalfunctions":[], "inherited_pure_virtual": [], "inherited_virtual":[], "inherited_normal": []}
        self.ProtectedMethods = {"Addedpurevirtualfunctions": [],"Addedvirtualfunctions":[],"Addednormalfunctions":[], "inherited_pure_virtual": [], "inherited_virtual":[], "inherited_normal": []}
        self.PrivateMethods = {"Addedpurevirtualfunctions": [],"Addedvirtualfunctions":[],"Addednormalfunctions":[], "inherited_pure_virtual": [], "inherited_virtual":[], "inherited_normal": []}
        self.inherited_pure_virtual = []
        self.inherited_virtual = []
        self.overridenfunctions = []
        self.typeofinheritance = None
        self.inherited_overriden = []
        self.TypeOfClass = None
        self.public_Pure_virtual_Methods = []
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
    def compute_public_pure_virtual_methods(self):
        self.public_Pure_virtual_Methods += self.PublicMethods['Addedpurevirtualfunctions']
        self.public_Pure_virtual_Methods += self.PublicMethods['inherited_pure_virtual'] 
    def ComputesOverridenMethods(self):
        self.identifyoverridenmethods(self.PublicMethods)
        self.identifyoverridenmethods(self.PrivateMethods)
        self.identifyoverridenmethods(self.ProtectedMethods)
    def identifyoverridenmethods(self, methods):
        #-------------Determing Overriden PURE Virtual methods-------------#
        #In Public Section
        for inherited_pure_virtual in methods["inherited_pure_virtual"]:
            if inherited_pure_virtual in (self.PublicMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_pure_virtual)
                self.PublicMethods["Addedvirtualfunctions"].remove(inherited_pure_virtual)
            elif inherited_pure_virtual in (self.PrivateMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_pure_virtual)
                self.PrivateMethods["Addedvirtualfunctions"].remove(inherited_pure_virtual) 
            elif inherited_pure_virtual in (self.ProtectedMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_pure_virtual)
                self.ProtectedMethods["Addedvirtualfunctions"].remove(inherited_pure_virtual)
            #Check presence in normal functions 
            if inherited_pure_virtual in (self.PublicMethods["Addednormalfunctions"]):
                self.overridenfunctions.append(inherited_pure_virtual)
                self.PublicMethods["Addednormalfunctions"].remove(inherited_pure_virtual)
            elif inherited_pure_virtual in (self.PrivateMethods["Addednormalfunctions"]):
                self.overridenfunctions.append(inherited_pure_virtual)
                self.PrivateMethods["Addednormalfunctions"].remove(inherited_pure_virtual) 
            elif inherited_pure_virtual in (self.ProtectedMethods["Addednormalfunctions"]):
                self.overridenfunctions.append(inherited_pure_virtual)
                self.ProtectedMethods["Addednormalfunctions"].remove(inherited_pure_virtual)
            #Get inherited Pure Virtual Methods
            self.inherited_pure_virtual.append(inherited_pure_virtual) 
        #-------------Determing Overriden Virtual methods-------------#
        #In public Section
        for inherited_virtual in methods["inherited_virtual"]:
            if inherited_virtual in (self.PublicMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                self.PublicMethods["Addedvirtualfunctions"].remove(inherited_virtual)
            elif inherited_virtual in (self.PrivateMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                self.PrivateMethods["Addedvirtualfunctions"].remove(inherited_virtual)
            elif inherited_virtual in (self.ProtectedMethods["Addedvirtualfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                self.ProtectedMethods["Addedvirtualfunctions"].remove(inherited_virtual)
            if inherited_virtual in (self.PublicMethods["Addednormalfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                self.PublicMethods["Addednormalfunctions"].remove(inherited_virtual)
            elif inherited_virtual in (self.PrivateMethods["Addednormalfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                self.PrivateMethods["Addednormalfunctions"].remove(inherited_virtual)
            elif inherited_virtual in (self.ProtectedMethods["Addednormalfunctions"]):
                self.overridenfunctions.append(inherited_virtual)
                self.ProtectedMethods["Addednormalfunctions"].remove(inherited_virtual)
            #Get inherited Virtual Methods
            self.inherited_virtual.append(inherited_virtual)
    
    def determineinheritanceType(self):
        typesOfparents = []
        for parent in self.Parents:
            typesOfparents.append(parent.type)

        # if (len(self.inherited_virtual) == 0 and len(self.PrivateMethods["inherited_normal"]) == 0 and len(self.inherited_overriden) == 0 and len(self.PublicMethods["inherited_normal"]) == 0 and len(self.ProtectedMethods["inherited_normal"]) == 0 
        # and len(self.inherited_pure_virtual) != 0):
        #     self.typeofinheritance = "Interface Inheritance"
        # elif: 
        # else: self.typeofinheritance = "Implementation Inheritance"
    #Checks if there is nonoverriden pure virtual function in public section
    # def PureVirtualPresentInPublic(self):
    #     for pure_virtual in self.PublicMethods["inherited_pure_virtual"]:
    #         if not pure_virtual in self.overridenfunctions and not pure_virtual in self.inherited_overriden:
    #             return True
    #     return False
    # #Checks if there is nonoverriden pure virtual function in private section
    # def PureVirtualPresentInPrivate(self):
    #     for pure_virtual in self.PrivateMethods["inherited_pure_virtual"]:
    #         if not pure_virtual in self.overridenfunctions and not pure_virtual in self.inherited_overriden:
    #             return True
    #     return False
    # #Checks if there is nonoverriden pure virtual function in protected section
    # def PureVirtualPresentInProtected(self):
    #     for pure_virtual in self.ProtectedMethods["inherited_pure_virtual"]:
    #         if not pure_virtual in self.overridenfunctions and not pure_virtual in self.inherited_overriden:
    #             return True
    #     return False
    def is_non_overriden_pure_method_present(self):
        OverridenMethods = self.overridenfunctions + self.inherited_overriden
        for pure_virtual in self.inherited_pure_virtual:
            if not pure_virtual in OverridenMethods:
                return True
        return False
    #Identifies the class Type
    def identifyClassType(self):
        #The OR should Be In The Same Place  
        if (len(self.PublicMethods["inherited_virtual"]) == 0 and len(self.PublicMethods["inherited_normal"]) == 0 and len(self.inherited_overriden) == 0 and (len(self.PublicMethods["inherited_pure_virtual"]) != 0 or len(self.PublicMethods["Addedpurevirtualfunctions"]) != 0) and len(self.PublicMethods["Addedvirtualfunctions"]) == 0 and len(self.PublicMethods["Addednormalfunctions"]) == 0 and 
        len(self.overridenfunctions) == 0 and len(self.PrivateMethods["inherited_virtual"]) == 0 and len(self.PrivateMethods["inherited_normal"]) == 0 and len(self.inherited_overriden) == 0 and (len(self.PrivateMethods["inherited_pure_virtual"]) != 0 or len(self.PrivateMethods["Addedpurevirtualfunctions"]) != 0)and len(self.PrivateMethods["Addedvirtualfunctions"]) == 0 and len(self.PrivateMethods["Addednormalfunctions"]) == 0
        and len(self.ProtectedMethods["inherited_virtual"]) == 0 and len(self.ProtectedMethods["inherited_normal"]) == 0 and (len(self.ProtectedMethods["inherited_pure_virtual"]) !=0 or len(self.ProtectedMethods["Addedpurevirtualfunctions"])) and len(self.ProtectedMethods["Addedvirtualfunctions"]) == 0 and len(self.ProtectedMethods["Addednormalfunctions"]) == 0):
            self.TypeOfClass = "Interface Class"
        elif len(self.PublicMethods["Addedpurevirtualfunctions"]) == 0 and len(self.ProtectedMethods["Addedpurevirtualfunctions"]) == 0 and len(self.PrivateMethods["Addedpurevirtualfunctions"]) == 0 and self.is_non_overriden_pure_method_present() == False:
            self.TypeOfClass = "Concrete Class"
        else:
            self.TypeOfClass = "Abstract Class"
                
class ProjectData:
    def __init__(self):
        #Stores Project Classes information
        self.cppClasses = {}
        
        #Stores All The Declaration present in a project
        self.Declarations = []
        #Stores Project Classes in Hierachy form (Parents and children)
        self.cppClassesNew = {}
        self.ProjectInheritanceData = [] #Store each inheritance information Data
    #Returns Inheritance Data Of A class
    def hasClass(self, aClass) -> bool:
        return self.cppClasses.get(aClass) is not None
    def addClass(self, aClass) -> None:
        self.cppClasses[aClass.className] = aClass
    def count(self) -> int:
        return len(self.cppClasses)
    def getinheritancedata(self, className):
        for inheritancedata in self.ProjectInheritanceData:
            if inheritancedata.derivedclassName == className:
                return inheritancedata
    #Returns class object
    def getcppClass(self, classname):
        if classname in self.cppClasses:
            return self.cppClasses[classname]
        else:
            return {}
    def getdeclarations(self):
        return self.Declarations
#---------------------------------------- Organize Classes and Their Children Objects (For preorder traversal)-----------------------#
    def computestheclasses(self):
        for _class in self.cppClasses:
            self.Declarations += self.cppClasses[_class].declarations
            if len(self.cppClasses[_class].Baseclasses) != 0:
                BaseClasses = []
                for base in self.cppClasses[_class].Baseclasses:
                    Parent = {}
                    inheritancetype = base["inheritancetype"]
                    baseObject = self.getcppClass(base["BaseClassName"])
                    if baseObject != {}:
                       #print(baseObject.className)
                       Parent['BaseClassInfo'] = baseObject
                       Parent['inheritancetype'] = inheritancetype
                       BaseClasses.append(Parent)
                #print(BaseClasses)
                self.cppClasses[_class].Baseclasses = BaseClasses
    def check_same_elements(self, baseclasstypes):
        return len(set(baseclasstypes)) == 1
    def determine_inheritance_type(self, baseclasstypes):
        if self.check_same_elements(baseclasstypes) and baseclasstypes[0] == "Interface Class":
            return "Interface inheritance"
        else: 
            return "Implementation inheritance"


    
    def computeInheritanceData(self):
        for _class in self.cppClasses:
            #print("Clases Available", _class)
            if self.cppClasses[_class].is_derivedclass():
                #print("classes inheriting", _class)
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
                typesofBaseclasses = []
                for Baseclass in self.cppClasses[_class].Baseclasses:
                    if Baseclass['inheritancetype'] == 'PUBLIC':
                        if self.getinheritancedata(Baseclass['BaseClassInfo'].className) != None:
                            BaseClassNameAndType = {}
                            BaseClassNameAndType["SuperClassName"] = Baseclass['BaseClassInfo'].className
                            baseClassInfo = self.getinheritancedata(Baseclass['BaseClassInfo'].className)
                            BaseClassNameAndType["public interface"] = baseClassInfo.PublicMethods
                            BaseClassNameAndType["TypeOfClass"] = baseClassInfo.TypeOfClass
                            inheritancedata.Parents.append(BaseClassNameAndType)
                            typesofBaseclasses.append(baseClassInfo.TypeOfClass)
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
                            
                            inherited_overriden += self.getinheritancedata(Baseclass['BaseClassInfo'].className).inherited_overriden
                            inherited_overriden += self.getinheritancedata(Baseclass['BaseClassInfo'].className).overridenfunctions
                            inheritancedata.PublicMethods["inherited_pure_virtual"] += Baseclass['BaseClassInfo'].publicMethods["purevirtualfunctions"]
                            inheritancedata.PublicMethods["inherited_virtual"] += Baseclass['BaseClassInfo'].publicMethods["virtualfunctions"]
                            inheritancedata.PublicMethods["inherited_normal"] += Baseclass['BaseClassInfo'].publicMethods["normalfunctions"]
                            # computing For Private
                            inheritancedata.PrivateMethods["inherited_pure_virtual"] += Baseclass['BaseClassInfo'].privateMethods["purevirtualfunctions"]
                            inheritancedata.PrivateMethods["inherited_virtual"] += Baseclass['BaseClassInfo'].privateMethods["virtualfunctions"]
                            
                            inheritancedata.ProtectedMethods["inherited_pure_virtual"] += Baseclass['BaseClassInfo'].protectedMethods["purevirtualfunctions"]
                            inheritancedata.ProtectedMethods["inherited_virtual"] += Baseclass['BaseClassInfo'].protectedMethods["virtualfunctions"]
                            inheritancedata.ProtectedMethods["inherited_normal"] += Baseclass['BaseClassInfo'].protectedMethods["normalfunctions"]
                        else:
                            RootObject = {}
                            RootObject["rootname"] = Baseclass['BaseClassInfo'].className
                            baseclassOject = self.getcppClass(Baseclass['BaseClassInfo'].className)
                            RootObject["PublicInterface"] = baseclassOject.publicMethods
                            RootObject["TypeOfClass"] = baseclassOject.getClassType()
                            inheritancedata.Parents.append(RootObject)
                            typesofBaseclasses.append(baseclassOject.getClassType())
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
                            BaseClassNameAndType["SuperClassName"] = Baseclass['BaseClassInfo'].className
                            baseClassInfo = self.getinheritancedata(Baseclass['BaseClassInfo'].className)
                            BaseClassNameAndType["TypeOfClass"] = baseClassInfo.TypeOfClass
                            BaseClassNameAndType["public interface"] = baseClassInfo.PublicMethods
                            inheritancedata.Parents.append(BaseClassNameAndType)
                            typesofBaseclasses.append(baseClassInfo.TypeOfClass)
                            inheritancedata.PrivateMethods["inherited_pure_virtual"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).PublicMethods["inherited_pure_virtual"]
                            inheritancedata.PrivateMethods["inherited_virtual"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).PublicMethods["inherited_virtual"]
                            inheritancedata.PrivateMethods["inherited_normal"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).PublicMethods["inherited_normal"]
                            #For Protected Methods
                            inheritancedata.PrivateMethods["inherited_pure_virtual"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).ProtectedMethods["inherited_pure_virtual"]
                            inheritancedata.PrivateMethods["inherited_virtual"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).ProtectedMethods["inherited_virtual"]
                            inheritancedata.PrivateMethods["inherited_normal"] += self.getinheritancedata(Baseclass['BaseClassInfo'].className).ProtectedMethods["inherited_virtual"]
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
                            RootObject = {}
                            RootObject["rootname"] = Baseclass['BaseClassInfo'].className
                            baseclassOject = self.getcppClass(Baseclass['BaseClassInfo'].className)
                            RootObject["PublicInterface"] = baseclassOject.publicMethods
                            RootObject["TypeOfClass"] = baseclassOject.getClassType()
                            inheritancedata.Parents.append(RootObject)
                            typesofBaseclasses.append(baseclassOject.getClassType())
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
                            BaseClassNameAndType = {}
                            BaseClassNameAndType["SuperClassName"] = Baseclass['BaseClassInfo'].className
                            baseClassInfo = self.getinheritancedata(Baseclass['BaseClassInfo'].className)
                            BaseClassNameAndType["TypeOfClass"] = baseClassInfo.TypeOfClass
                            BaseClassNameAndType["public interface"] = baseClassInfo.PublicMethods
                            inheritancedata.Parents.append(BaseClassNameAndType)
                            typesofBaseclasses.append(baseClassInfo.TypeOfClass)
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
                            RootObject = {}
                            RootObject["rootname"] = Baseclass['BaseClassInfo'].className
                            baseclassOject = self.getcppClass(Baseclass['BaseClassInfo'].className)
                            RootObject["PublicInterface"] = baseclassOject.publicMethods
                            RootObject["TypeOfClass"] = baseclassOject.getClassType()
                            inheritancedata.Parents.append(RootObject)
                            typesofBaseclasses.append(baseclassOject.getClassType())
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
                inheritancedata.typeofinheritance = self.determine_inheritance_type(typesofBaseclasses)
                inheritancedata.inherited_overriden = inherited_overriden
                inheritancedata.ComputesOverridenMethods()
                inheritancedata.identifyClassType()
                inheritancedata.compute_public_pure_virtual_methods()
                inheritancedata.compute_public_interface()
                inheritancedata.compute_Added_Methods()
                self.ProjectInheritanceData.append(inheritancedata)
        #self.PrintResults()
        #print("Number of inheritances",self.ProjectInheritanceData)
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