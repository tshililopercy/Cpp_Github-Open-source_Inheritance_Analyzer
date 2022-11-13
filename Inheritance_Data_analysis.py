import json
from collections import Counter
#-------------------------------------------Analysis for All Inheritances Instances------------------------------#
class DataAnalysis:
    def __init__(self):       
#----------------------------------------This is for ALL inheritances available----------------------#
        #Total number of pure interface inheritance
        self.interfaceinheritance = 0
        #Total number of implementation inheritance (either concrete or abstract or any mixture of interface)
        self.implementationinheritance = 0
        #number of abstract only inheritance
        self.abstractOnly = []
        #number of concrete only inheritance
        self.concreteOnly = []
        #number of concrete, abstract, and interface commbined
        self.concrete_Abstract_interface = []
        #concrete and interface inheritance
        self.concrete_Interface = []
        #abstract and interface inheritance
        self.abstract_Interface = []
        #Concrete and Abstract inheritance
        self.concrete_Abstract = []
        #The SuperClass combination to deduce the above
        self.implementationinheritanceCombinations = []
        #interface combination 
        self.interfacecombination = []
        #The size of Concrete Super Classes
        self.PublicInterfaceOfConcreteSuperClasses = []
        self.AbstractClassesInterface = [] #Pure virtual functions/ virtual functions
        #Abstract classes per interface ratio
        self.AbstractClasses_per_interface_ratio = []
        #Abstract classes interface percentage
        self._abstract_interface_percentage = []
        self.DerivedAbstractClassesInterface = []
        self.InterfaceClassesInterface = []
        self.DerivedInterfaceClassesInterface = []
        #Concrete classes Are either root or children
        self.ConcreteClassesInterface = []
        self.DerivedConcreteClassesInterface = []
#----------------------------Interface Inheritance----------------------------------------------------------#
        #Derived Concrete classes that don't add Novel methods.
        self.InterfaceDerivedConcreteClassesNovelMethods = []
        #Derived Concrete classes Overriden Methods.
        self.InterfaceDerivedConcreteClassesOverridenMethods = []
#----------------------------Implementation Inheritance from Abstract Classes--------------------------------#
        #Derived Concrete classes that don't add Novel methods.
        self.AbstractDerivedConcreteClassesNovelMethods = []
        #Overriden Virtual(normal methods)
        self.AbstractDerivedConcreteClassesOverridenVirtualMethods = []
        #Derived concrete classes Inherited Methods
        self.AbstractDerivedConcreteClassesInheritedMethods = []
#----------------------------Implementation Inheritance from Concrete Classes--------------------------------#
        #Derived Concrete classes that don't add Novel methods.
        self.DerivedConcreteClassesNovelMethods = []
        #Derived Concrete classes Overriden Methods.
        self.DerivedConcreteClassesOverridenMethods = []
        #Derived concrete classes Inherited Methods
        self.DerivedConcreteClassesInheritedMethods = []
#------------------------------------------------------------------------------------------------------------#
        #Number_of_children_per_interface_class
        #Total number of Abstract classes
        self.abstract_classes = 0
        #Total number of Concrete Classes
        self.concrete_classes = 0
        #Total number of Interface Classes
        self.interface_classes = 0
        #Concrete Superclass
        self.concreteSuperclass = 0
        #Used Abstract Classes
        self.Used_Abstract_Classes = 0
        #Used Interface Classes
        self.Used_Interface_Classes = 0
        #Used Concrete Classes
        self.Used_concrete_Classes = 0
        self.number_of_children_per_interface_class = []
        #NUmber_of_children_per_abstract_class
        self.number_of_children_per_abstract_class = []
        #Number_of_children_per_concrete_super_class
        self.number_of_children_per_Concrete_SuperClass = []
#---------------------------For Derived Classes From Interface classes-------------------------#
        self.InterfacederivedConcrete_Classes_ratio_overriden = []
        self.InterfacederivedConcrete_Classes_ratio_NovelMethods = []
#---------------------------For Derived Classes From Abstract Classes--------------------------#
        self.AbstractderivedConcrete_Classes_ratio_inherited = []
        self.AbstractderivedConcrete_Classes_ratio_overriden = []
        self.AbstractderivedConcrete_Classes_ratio_NovelMethods = []
#---------------------------For Derived Classes From Concrete Classes--------------------------#
        #Ratios For Derived Concrete classes
        self.derivedConcrete_Classes_ratio_inherited = []
        self.derivedConcrete_Classes_ratio_overriden = []
        self.derivedConcrete_Classes_ratio_NovelMethods = []
#------------------------------------------------------------------------------------------------#
        #Number of classes Per Ratio
        self.number_of_Concrete_Classes_per_ratio_inherited = []
        self.number_of_Concrete_Classes_per_ratio_overriden = []
        self.number_of_Concrete_Classes_per_ratio_NovelMethods = []
        #Public interface Ratio Percentage
        self._inherited_methods_percentages = []
        self._overriden_methods_percentages = []
        self._novel_methods_percentages = []
        #Derived Concrete Classes Public Interface
        self.DerivedClasses_Public_interface = []

#------------------------------------Per Depth Information----------------------------------------#
        self.DepthsData = {}
        #How many interface inheritance 
        #How many implementation inheritance
        #Interface
        
        #STORE RETRIEVED INHERITANCE DATA.
        self.HierarchiesData = {}
        

    def read_Data_From_Json(self):
        with open('HierachiesData.json', 'r') as openfile:
            # Reading data from the storage json file 
            self.HierarchiesData = json.load(openfile)

    def number_of_inheritances(self):
        for project in self.HierarchiesData:
            concreteClassesNames = []
            concreteSuperClassName = []
            AbstractClassesNames = []
            InterfaceClassesNAmes = []
            number_of_children_per_interface_class = []
            #NUmber_of_children_per_abstract_class
            number_of_children_per_abstract_class = []
            #Number_of_children_per_concrete_super_class
            number_of_children_per_Concrete_SuperClass = []
            Used_Abstract_Classes = []
            Used_Interface_Classes = []
            for hierarchy in self.HierarchiesData[project]["Hierarchies"]:
                for index, depth in enumerate(self.HierarchiesData[project]["Hierarchies"][hierarchy]):
                    for inheritances in depth:
                       for inheritance in  depth[inheritances]:
                            #-----------------Implementation inheritance information-------------------#
                           if inheritance["typeofinheritance"] == "Implementation inheritance":
                               eachdepthcombination = []
                               #The number of implementation inheritance
                               self.implementationinheritance += 1
                               if inheritance["TypeOfClass"] == "Concrete Class":
                                   if inheritance["ClassName"] not in concreteClassesNames:
                                        concreteClassesNames.append(inheritance["ClassName"])
                               #--------------------------Parent Classes Data-------------------------#
                               for superclass in inheritance["SubClasses"]:
                                  pure_virtual_functions = []
                                  Abstract_public_interface = []
                                  eachdepthcombination.append(superclass["TypeOfClass"])
                                  _superclass_keys = superclass.keys()
                                  
                                  if "SuperClassName" in  _superclass_keys:
                                    if superclass["TypeOfClass"] == "Abstract Class":
                                       number_of_children_per_abstract_class.append(superclass["SuperClassName"])
                                       if superclass["SuperClassName"] not in AbstractClassesNames:
                                         pure_virtual_functions += superclass["public interface"]["Addedpurevirtualfunctions"]
                                         pure_virtual_functions += superclass["public interface"]["inherited_pure_virtual"]
                                         Abstract_public_interface += pure_virtual_functions
                                         Abstract_public_interface += superclass["public interface"]["Addednormalfunctions"]
                                         Abstract_public_interface += superclass["public interface"]["inherited_normal"]
                                         Abstract_public_interface += superclass["public interface"]["Addedvirtualfunctions"]
                                         Abstract_public_interface += superclass["public interface"]["inherited_virtual"]
                                         self.AbstractClassesInterface.append(round((len(pure_virtual_functions)/len(Abstract_public_interface))*100)) 
                                         AbstractClassesNames.append(superclass["SuperClassName"])
                                    elif superclass["TypeOfClass"] == "Concrete Class":
                                        number_of_children_per_Concrete_SuperClass.append(superclass["SuperClassName"])
                                        if superclass["SuperClassName"] not in concreteSuperClassName:
                                            concreteSuperClassName.append(superclass["SuperClassName"])
                                        if superclass["SuperClassName"] not in concreteClassesNames:
                                            concreteClassesNames.append(superclass["SuperClassName"])
                                    elif superclass["TypeOfClass"] == "Interface Class":
                                        number_of_children_per_interface_class.append(superclass["SuperClassName"])
                                        if superclass["SuperClassName"] not in InterfaceClassesNAmes:
                                           pure_virtual_functions += superclass["public interface"]["Addedpurevirtualfunctions"]
                                           pure_virtual_functions += superclass["public interface"]["inherited_pure_virtual"]
                                           self.InterfaceClassesInterface.append(len(pure_virtual_functions))
                                           InterfaceClassesNAmes.append(superclass["SuperClassName"])
                                    #Public interface for concrete Classes  
                                  else:
                                    if superclass["TypeOfClass"] == "Abstract Class":
                                       number_of_children_per_abstract_class.append(superclass["rootname"])
                                       if superclass["rootname"] not in AbstractClassesNames:
                                          pure_virtual_functions = superclass["PublicInterface"]["purevirtualfunctions"]
                                          Abstract_public_interface += pure_virtual_functions
                                          Abstract_public_interface += superclass["PublicInterface"]["virtualfunctions"]
                                          Abstract_public_interface += superclass["PublicInterface"]["normalfunctions"]
                                          self.AbstractClassesInterface.append(round((len(pure_virtual_functions)/len(Abstract_public_interface))*100))
                                          AbstractClassesNames.append(superclass["rootname"])
                                    elif superclass["TypeOfClass"] == "Concrete Class":
                                        if superclass["rootname"] not in concreteSuperClassName:
                                            concreteSuperClassName.append(superclass["rootname"])
                                        number_of_children_per_Concrete_SuperClass.append(superclass["rootname"])
                                        if superclass["rootname"] not in concreteClassesNames:
                                            publicInterface = superclass["PublicInterface"]["normalfunctions"]
                                            self.ConcreteClassesInterface.append(len(publicInterface))
                                            concreteClassesNames.append(superclass["rootname"])
                                    elif superclass["TypeOfClass"] == "Interface Class":
                                        number_of_children_per_interface_class.append(superclass["rootname"])
                                        if superclass["rootname"] not in InterfaceClassesNAmes:
                                            self.InterfaceClassesInterface.append(len(superclass["PublicInterface"]["purevirtualfunctions"]))
                                            InterfaceClassesNAmes.append(superclass["rootname"])
                                            
                               if inheritance["TypeOfClass"] == "Concrete Class":
                                    if len(set(eachdepthcombination)) == 1 and "Concrete Class" in eachdepthcombination:
                                        self.DerivedConcreteClassesNovelMethods.append(inheritance["Added Methods"])
                                        self.DerivedConcreteClassesOverridenMethods.append(inheritance["Overriden Methods"])
                                        #Verified formula
                                        self.DerivedConcreteClassesInheritedMethods.append(inheritance["Public Interface"]-inheritance["Added Methods"]-inheritance["Overriden Methods"])
                                    elif len(set(eachdepthcombination)) == 1 and "Abstract Class" in eachdepthcombination:
                                        self.AbstractDerivedConcreteClassesNovelMethods.append(inheritance["Added Methods"])
                                        self.AbstractDerivedConcreteClassesOverridenVirtualMethods.append(inheritance["Overriden Methods"])
                                        self.AbstractDerivedConcreteClassesInheritedMethods.append(inheritance["Public Interface"]-inheritance["Added Methods"]) 
                               self.implementationinheritanceCombinations.append(eachdepthcombination)
                           #----------------------------------Interface inheritance Information----------------#
                           elif inheritance["typeofinheritance"] == "Interface inheritance":
                               if inheritance["TypeOfClass"] == "Concrete Class":
                                    self.InterfaceDerivedConcreteClassesNovelMethods.append(inheritance["Added Methods"])
                                    self.InterfaceDerivedConcreteClassesOverridenMethods.append(inheritance["Overriden Methods"])
                                    if inheritance["ClassName"] not in concreteClassesNames:
                                        concreteClassesNames.append(inheritance["ClassName"])
                               #number of interface inheritance
                               self.interfaceinheritance += 1
                               for superclass in inheritance["SubClasses"]:
                                  pure_virtual_functions = []
                                  self.interfacecombination.append(superclass["TypeOfClass"])
                                  _superclass_keys = superclass.keys()
                                  if "SuperClassName" in  _superclass_keys :
                                    number_of_children_per_interface_class.append(superclass["SuperClassName"])
                                    if superclass["SuperClassName"] not in InterfaceClassesNAmes:
                                       pure_virtual_functions += superclass["public interface"]["Addedpurevirtualfunctions"]
                                       pure_virtual_functions += superclass["public interface"]["inherited_pure_virtual"]
                                       self.InterfaceClassesInterface.append(len(pure_virtual_functions))
                                       InterfaceClassesNAmes.append(superclass["SuperClassName"])
                                  else:
                                    number_of_children_per_interface_class.append(superclass["rootname"])
                                    if superclass["rootname"] not in InterfaceClassesNAmes:
                                       self.InterfaceClassesInterface.append(len(superclass["PublicInterface"]["purevirtualfunctions"]))
                                       InterfaceClassesNAmes.append(superclass["rootname"])
                            # The public interface of the SuperClasses
            for _classUsed in self.HierarchiesData[project]["ClassesUsed"]:
                for abstractclass in AbstractClassesNames:
                        splittedabstractclass = abstractclass.split("::")
                        name = splittedabstractclass[-1]
                        if _classUsed == name:
                             Used_Abstract_Classes.append(_classUsed)
                for interfaceclass in InterfaceClassesNAmes:
                        splittedinterfaceclass = interfaceclass.split("::")
                        name = splittedinterfaceclass[-1]
                        if _classUsed == name:
                            Used_Interface_Classes.append(_classUsed)
            for interface_class in InterfaceClassesNAmes:
                counts = Counter(number_of_children_per_interface_class)
                self.number_of_children_per_interface_class.append(counts[interface_class])

            for abstract_class in AbstractClassesNames:
                counts = Counter(number_of_children_per_abstract_class)
                self.number_of_children_per_abstract_class.append(counts[abstract_class])
            
            for concrete_class in concreteSuperClassName:
                #print(concrete_class)
                counts = Counter(number_of_children_per_Concrete_SuperClass)
                self.number_of_children_per_Concrete_SuperClass.append(counts[concrete_class])
            #print("Concrete Classes Names: ", concreteClassesNames)
            self.abstract_classes += len(AbstractClassesNames)
            self.concrete_classes += len(concreteClassesNames)
            self.interface_classes += len(InterfaceClassesNAmes)
            #Used Abstract Classes & Interface
            self.Used_Abstract_Classes += len(Used_Abstract_Classes)
            self.Used_Interface_Classes += len(Used_Interface_Classes)
            #Number Of Concrete Super Class
            self.concreteSuperclass += len(concreteSuperClassName)
    def implementation_instances(self):
        for instance in self.implementationinheritanceCombinations:
            instanceSet = set(instance)
            #print(instance)
            if set(["Abstract Class","Interface Class","Concrete Class"]).issubset(instanceSet):
                self.concrete_Abstract_interface.append(instance)
            elif set(["Abstract Class","Interface Class"]).issubset(instanceSet):
                self.abstract_Interface.append(instance)
            elif set(["Abstract Class", "Concrete Class"]).issubset(instanceSet):
                self.concrete_Abstract.append(instance)
            elif set(["Concrete Class", "Interface Class"]).issubset(instanceSet):
                self.concrete_Interface.append(instance)
            elif set(["Concrete Class"]).issubset(instanceSet):
                self.concreteOnly.append(instance)
            elif set(["Abstract Class"]).issubset(instanceSet):
                #print(instance)
                self.abstractOnly.append(instance)
                
    def abstract_classes_public_interface_distribution(self):
        for percentage in range(0,101):
            counts_abstract_interface = Counter(self.AbstractClassesInterface)
            if counts_abstract_interface[percentage] != 0:
                self.AbstractClasses_per_interface_ratio.append(counts_abstract_interface[percentage])
                self._abstract_interface_percentage.append(percentage)
                
    def subclasses_percentage_distribution(self):
        #----------------------------------------For Derived Concrete Classes From Concrete-------------------------------------#
        for concrete_class_number in range(0,len(self.DerivedConcreteClassesInheritedMethods)):
            total_interface = self.DerivedConcreteClassesInheritedMethods[concrete_class_number] + self.DerivedConcreteClassesNovelMethods[concrete_class_number] + self.DerivedConcreteClassesOverridenMethods[concrete_class_number]
            self.DerivedClasses_Public_interface.append(total_interface)
            inheriting_data_class = False
            if total_interface != 0:
                ratio_inherited = self.DerivedConcreteClassesInheritedMethods[concrete_class_number]/total_interface
                if ratio_inherited != 0:
                    self.derivedConcrete_Classes_ratio_inherited.append(round(ratio_inherited*100))
                    inheriting_data_class = True
                if inheriting_data_class:
                    ratio_overriden = self.DerivedConcreteClassesOverridenMethods[concrete_class_number]/total_interface
                    self.derivedConcrete_Classes_ratio_overriden.append(round(ratio_overriden*100))
                    
                    ratio_NovelMethods = self.DerivedConcreteClassesNovelMethods[concrete_class_number]/total_interface
                    self.derivedConcrete_Classes_ratio_NovelMethods.append(round(ratio_NovelMethods*100))
        #-----------------------------------------For Derived Concrete Classes From Abstract-----------------------------------# 
        for concrete_class_number in range(0,len(self.AbstractDerivedConcreteClassesInheritedMethods)):
            total_interface = self.AbstractDerivedConcreteClassesInheritedMethods[concrete_class_number] + self.AbstractDerivedConcreteClassesNovelMethods[concrete_class_number] + self.AbstractDerivedConcreteClassesOverridenVirtualMethods[concrete_class_number]
            #self.AbstractDerivedClasses_Public_interface.append(total_interface)
            if total_interface != 0:
                ratio_inherited = self.AbstractDerivedConcreteClassesInheritedMethods[concrete_class_number]/total_interface
                self.AbstractderivedConcrete_Classes_ratio_inherited.append(round(ratio_inherited*100))
                
                ratio_overriden = self.AbstractDerivedConcreteClassesOverridenVirtualMethods[concrete_class_number]/total_interface
                self.AbstractderivedConcrete_Classes_ratio_overriden.append(round(ratio_overriden*100))
                
                ratio_NovelMethods = self.AbstractDerivedConcreteClassesNovelMethods[concrete_class_number]/total_interface
                self.AbstractderivedConcrete_Classes_ratio_NovelMethods.append(round(ratio_NovelMethods*100))
                
        for concrete_class_number in range(0,len(self.InterfaceDerivedConcreteClassesNovelMethods)):
            total_interface = self.InterfaceDerivedConcreteClassesNovelMethods[concrete_class_number] + self.InterfaceDerivedConcreteClassesOverridenMethods[concrete_class_number]
            if total_interface != 0:
                
                ratio_overriden = self.InterfaceDerivedConcreteClassesOverridenMethods[concrete_class_number]/total_interface
                self.InterfacederivedConcrete_Classes_ratio_overriden.append(round(ratio_overriden*100))
                
                ratio_NovelMethods = self.InterfaceDerivedConcreteClassesNovelMethods[concrete_class_number]/total_interface
                self.InterfacederivedConcrete_Classes_ratio_NovelMethods.append(round(ratio_NovelMethods*100))
                
        for percentage in range(0,101):
            counts_inherited_ratio = Counter(self.derivedConcrete_Classes_ratio_inherited)
            if counts_inherited_ratio[percentage] != 0:
                self.number_of_Concrete_Classes_per_ratio_inherited.append(counts_inherited_ratio[percentage])
                self._inherited_methods_percentages.append(percentage)
            
            counts_overriden_ratio = Counter(self.derivedConcrete_Classes_ratio_overriden)
            if counts_overriden_ratio[percentage] != 0:
                self.number_of_Concrete_Classes_per_ratio_overriden.append(counts_overriden_ratio[percentage])
                self._overriden_methods_percentages.append(percentage)
                
            counts_novel_ratio = Counter(self.derivedConcrete_Classes_ratio_NovelMethods)
            if counts_novel_ratio[percentage] != 0:
                self.number_of_Concrete_Classes_per_ratio_NovelMethods.append(counts_novel_ratio[percentage]) 
                self._novel_methods_percentages.append(percentage)
                
    def Subclasses_Concrete_classes_Interface(self):
        counts_Derivedconcrete_classes_interface = Counter(self.DerivedClasses_Public_interface)
        NOC_counts = []
        Exact_Number = []
        for number in range(0,max(self.DerivedClasses_Public_interface)+1):
            if counts_Derivedconcrete_classes_interface[number] != 0:
                NOC_counts.append(counts_Derivedconcrete_classes_interface[number])
                Exact_Number.append(number)
        return NOC_counts, Exact_Number
        
    def interface_classes_interface(self):
        counts_interface_classes_interface = Counter(self.InterfaceClassesInterface)
        NOC_counts = []
        Exact_Number = []
        for number in range(0,max(self.InterfaceClassesInterface)+1):
            if counts_interface_classes_interface[number] != 0:
                NOC_counts.append(counts_interface_classes_interface[number])
                Exact_Number.append(number)
        return NOC_counts, Exact_Number

    def NOC_per_AbstractClasses(self):
        counts_abstract_classes = Counter(self.number_of_children_per_abstract_class)
        NOC_counts = []
        Exact_Number = []
        for number in range(0,max(self.number_of_children_per_abstract_class)+1):
            if counts_abstract_classes[number] != 0:
                NOC_counts.append(counts_abstract_classes[number])
                Exact_Number.append(number)
        return NOC_counts, Exact_Number
    
    def NOC_per_InterfaceClasses(self):
        counts_interface_classes = Counter(self.number_of_children_per_interface_class)
        NOC_counts = []
        Exact_Number = []
        for number in range(0,max(self.number_of_children_per_abstract_class)+1):
            if counts_interface_classes[number] != 0:
                NOC_counts.append(counts_interface_classes[number])
                Exact_Number.append(number)
        return NOC_counts, Exact_Number
    
    def NOC_per_ConcreteClasses(self):
        counts_concrete_classes = Counter(self.number_of_children_per_Concrete_SuperClass)
        NOC_counts = []
        Exact_Number = []
        for number in range(0,max(self.number_of_children_per_abstract_class)+1):
            if counts_concrete_classes[number] != 0:
                NOC_counts.append(counts_concrete_classes[number])
                Exact_Number.append(number)
        return NOC_counts, Exact_Number  
      

    def startAnalysis(self):
        self.read_Data_From_Json()
        self.number_of_inheritances()
        self.implementation_instances()
        self.subclasses_percentage_distribution()
        self.abstract_classes_public_interface_distribution()