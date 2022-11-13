from Inheritance_Data_analysis import *
from matplotlib import pyplot as plt
import numpy as np
import statistics
import numpy as np
import pandas as pd

class DataAnalysisVisualizer:
    def __init__(self):
        self.data_analysis = DataAnalysis()
        self.data_analysis.startAnalysis()
    def _ConcreteSuperClassesPlot(self):
        #-----------------------------------This is For implementation inheritance (From Concrete SuperClasses)----------------------------------------#
        plt.figure(1)
        print("Overriden", self.data_analysis.derivedConcrete_Classes_ratio_overriden)
        plt.hist(self.data_analysis.derivedConcrete_Classes_ratio_overriden)
        plt.xlabel("Overriden methods percentage ratios")
        plt.title("Histogram for concrete subclasses Overriden methods percentage ratios")
        plt.ylabel("Number Of Derived Concrete Subclasses")
        # Displaying the graph
        plt.show()
        plt.figure(2)
        print("Added Methods", self.data_analysis.derivedConcrete_Classes_ratio_NovelMethods)
        plt.hist(self.data_analysis.derivedConcrete_Classes_ratio_NovelMethods)
        plt.xlabel("Novel methods percentage ratios")
        plt.title("Histogram for concrete subclasses Novel methods percentage ratios")
        plt.ylabel("Number Of Derived Concrete Subclasses")
        # Displaying the graph
        plt.show()
        plt.figure(3)
        print("Inherited and Used", self.data_analysis.derivedConcrete_Classes_ratio_inherited)
        plt.hist(self.data_analysis.derivedConcrete_Classes_ratio_inherited)
        plt.xlabel("Inherited and used methods percentage")
        plt.title("Histogram for concrete subclasses inherited and used methods percentage ratios")
        plt.ylabel("Number Of Derived Concrete Subclasses")
        # Displaying the graph
        plt.show()
        print("\n")

    def _ConcreteSuperClassStatisticAnalysis(self):
        
        print("-----Analysis For Pure Implementation inheritance(Concrete SUBCLASS, Concrete SUPERCLASS)---------------------------------")
        #--------------Whiskers Plots-------------------------------------------------------------------------------------#
        #Taking Overriden methods, inherited and used methods
        data_1 = self.data_analysis.derivedConcrete_Classes_ratio_overriden
        data_2 = self.data_analysis.derivedConcrete_Classes_ratio_inherited
        data_3 = self.data_analysis.derivedConcrete_Classes_ratio_NovelMethods
         
        fig = plt.figure(figsize =(10, 7))
         
        # Creating plot
        DataList = [data_1,data_2,data_3]
        plt.title("Overriden, Inherited and Used, Novel Methods")
        plt.ylabel("Public interface percentage Ratio")
        plt.boxplot(DataList)
        # show plot
        plt.show()
        # #-------------------------------------------------Standard Deviation----------------------------------------------#
        import statistics
        Overriden_Methods = self.data_analysis.derivedConcrete_Classes_ratio_overriden
        standard_deviation = statistics.stdev(Overriden_Methods)
        print("Overriden percentage ratio Standard Deviation: ", standard_deviation)
        
        Inherited_And_Used_Methods = self.data_analysis.derivedConcrete_Classes_ratio_inherited
        standard_deviation = statistics.stdev(Inherited_And_Used_Methods)
        print("Inherited and used Standard Deviation: ", standard_deviation)
        
        Novel_Methods = self.data_analysis.derivedConcrete_Classes_ratio_NovelMethods
        standard_deviation = statistics.stdev(Novel_Methods)
        print("Novel Methods Standard Deviation: ", standard_deviation)
        
        #------------------------------------------------THE MEAN---------------------------------------------------------#
        overriden_mean = statistics.mean(data_1)
        Inherited_And_Used_mean = statistics.mean(data_2)
        Novel_mean = statistics.mean(data_3)
         
        # Printing the mean
        print()
        print("Overriden percentage ratio mean :", overriden_mean)
        print("Inherited and used percentage ratio mean :", Inherited_And_Used_mean)
        print("Novel percentage ratio mean: ", Novel_mean)
        
        #-------------------------------------------------Correlation of them---------------------------------------------#
        # # collect data
        import pandas as pd
        data = {
            'Novel percentage ratio': self.data_analysis.derivedConcrete_Classes_ratio_NovelMethods,
            'Inherited and used percentage ratio': self.data_analysis.derivedConcrete_Classes_ratio_inherited,
            'Overriden percentage ratio': self.data_analysis.derivedConcrete_Classes_ratio_overriden
        }
        # form dataframe
        dataframe = pd.DataFrame(data, columns=['Novel percentage ratio', 'Inherited and used percentage ratio', 'Overriden percentage ratio'])
        print()
        print("Dataframe is : ")
        print(dataframe)
         
        # form correlation matrix
        matrix = dataframe.corr()
        print("Correlation matrix is : ")
        print(matrix, "\n")
    
    def _Interface_Analysis_Plots(self):
        # # #-----------------------------------For pure interface inheritance----------------------------------------------#
        plt.figure(6)
        plt.hist(self.data_analysis.InterfaceClassesInterface)
        plt.xlabel("Interface classes pure virtual methods")
        plt.ylabel("Number of interface classes")
        plt.show()
        
        # #-------------------------------------------For Interface Inheritance (Concrete SUBCLASS)---------------------------------------------#
        plt.figure(1)
        plt.hist(self.data_analysis.InterfacederivedConcrete_Classes_ratio_overriden)
        plt.xlabel("Overriden methods percentage ratio")
        plt.title("Concrete subclasses overriden methods percentage ratio")
        plt.ylabel("Number of concrete subclasses")
        # Displaying the graph
        plt.show()
        #----------------------------------------------Novel Methods Distribution-----------------------------------------#
        plt.figure(2)
        plt.hist(self.data_analysis.InterfacederivedConcrete_Classes_ratio_NovelMethods)
        plt.xlabel("Novel methods percentage ratio")
        plt.title("Histogram for subclasses novel methods percentage ratios")
        plt.ylabel("Number of concrete subclasses")
        # Displaying the graph
        plt.show()
        #------------------------------------------------Interface Analysis------------------------------------------------#
        #--------------Whiskers Plots-------------------------------------------------------------------------------------#
        # Creating dataset
        data_1 = self.data_analysis.InterfacederivedConcrete_Classes_ratio_overriden
        data_2 = self.data_analysis.InterfacederivedConcrete_Classes_ratio_NovelMethods
         
        # Creating plot
        DataList = [data_1,data_2]
        plt.title("Box and Whisker Plot for Concrete subclass Overriden methods percentage ratio and Concrete subclass Novel Methods percentage ratio")
        plt.boxplot(DataList)
        # show plot
        plt.show()
        print("---------------------------------------Interface inheritance(Concrete Subclass) Analaysis-----------------------------------------")
        # #-------------------------------------------------Standard Deviation----------------------------------------------#
        import statistics
        Overriden_Methods = self.data_analysis.InterfacederivedConcrete_Classes_ratio_overriden
        standard_deviation = statistics.stdev(Overriden_Methods)
        print("Overriden methods percentage ratio Standard Deviation: ", standard_deviation)
        
        Novel_Methods = self.data_analysis.InterfacederivedConcrete_Classes_ratio_NovelMethods
        standard_deviation = statistics.stdev(Novel_Methods)
        print("Novel Methods percentage ratio Standard Deviation: ", standard_deviation)
        
        #------------------------------------------------THE MEAN---------------------------------------------------------#
         
        overriden_mean = statistics.mean(data_1)
        Novel_mean = statistics.mean(data_2)
         
        # Printing the mean
        print("Overriden methods percentage ratio Mean: ", overriden_mean)
        print("Novel methods percentage ratio Mean: ", Novel_mean)
        
        #-------------------------------------------------Correlation of them---------------------------------------------#
        data = {
            'Novel methods percentage ratio': self.data_analysis.InterfacederivedConcrete_Classes_ratio_NovelMethods,
            'Overriden methods percentage ratio': self.data_analysis.InterfacederivedConcrete_Classes_ratio_overriden
        }
         
        # form dataframe
        dataframe = pd.DataFrame(data, columns=['Novel methods percentage ratio', 'Overriden methods percentage ratio'])
        print("Dataframe is : ")
        print(dataframe)
         
        # form correlation matrix
        matrix = dataframe.corr()
        print("Correlation matrix is : ")
        print(matrix, "\n")
        
    def _Interface_Number_of_children_Analysis(self):
         
        data_1 = self.data_analysis.InterfaceClassesInterface
        data_2 = self.data_analysis.number_of_children_per_interface_class
        plt.figure(1)
        plt.scatter(data_1, data_2, c ="green")
        plt.xlabel("Number of Interface pure virtual functions")
        plt.ylabel("Number of inheriting classes")
        plt.title("Interface class interface and number of children")
        plt.show
        
        plt.figure(2)
        # Creating plot
        DataList = [data_1,data_2]
        plt.title("Interface classes interfaces, Interface classes number of children")
        plt.boxplot(DataList)
        # show plot
        plt.show()
        # #-------------------------------------------------Standard Deviation----------------------------------------------#
        Interface_interface = self.data_analysis.InterfaceClassesInterface
        standard_deviation = statistics.stdev(Interface_interface)
        print("Interface classes interface Standard Deviation: ", standard_deviation)
        
        Number_Of_Children = self.data_analysis.number_of_children_per_interface_class
        standard_deviation = statistics.stdev(Number_Of_Children)
        print("Interface classes number of children Standard Deviation: ", standard_deviation)
        
        #------------------------------------------------THE MEAN---------------------------------------------------------#
         
        # list of positive integer numbers
         
        interface_interface_mean = statistics.mean(data_1)
        Interface_NOC_mean = statistics.mean(data_2)
         
        # Printing the mean
        print("Interface classes interface mean :", interface_interface_mean)
        print("Interface classes number of children mean: ", Interface_NOC_mean)
        
        #-------------------------------------------------Correlation of them---------------------------------------------#
        data = {
            'Interface classes interface': self.data_analysis.InterfaceClassesInterface,
            'Interface classes number of children': self.data_analysis.number_of_children_per_interface_class
        }
         
        # form dataframe
        dataframe = pd.DataFrame(data, columns=['Interface classes interface', 'Interface classes number of children'])
        print("Dataframe is : ")
        print(dataframe)
         
        # form correlation matrix
        matrix = dataframe.corr()
        print("Correlation matrix is : ")
        print(matrix, "\n")

    def _Presence_Abstract_Classes_Analysis(self):
        
        print("-------------------------------Abstract Class (SuperClass) Analysis------------------------------------")
        plt.show()
        plt.figure(1)
        print("Abstract classes percentage pure virtual methods", self.data_analysis.AbstractClassesInterface)
        plt.hist(self.data_analysis.AbstractClassesInterface)
        plt.xlabel("Percentage of Pure virtual function")
        plt.title("Histogram for Abstract classes pure virtual methods percentage ratios")
        plt.ylabel("Number of Abstract Classes")
        # Displaying the graph
        plt.show()
        Abstract_interface = self.data_analysis.AbstractClassesInterface
        standard_deviation = statistics.stdev(Abstract_interface)
        print("Abstract pure virual percentage ratio Standard Deviation: ", standard_deviation)
        
        Number_Of_Children = self.data_analysis.number_of_children_per_abstract_class
        standard_deviation = statistics.stdev(Number_Of_Children)
        print("Abstract class Number of children Standard Deviation: ", standard_deviation)
        
        #------------------------------------------------THE MEAN---------------------------------------------------------#
    
        data_1 = self.data_analysis.AbstractClassesInterface
        data_2 = self.data_analysis.number_of_children_per_abstract_class
         
        # Creating plot
        DataList = [data_1,data_2]
        plt.title("Abstract classes percentage pure virtual methods, Abstract classes number of children")
        plt.boxplot(DataList)
        # show plot
        plt.show()
        # #-------------------------------------------------Standard Deviation----------------------------------------------#
         
        # list of positive integer numbers
        Abstract_interface_mean = statistics.mean(data_1)
        Abstract_NOC_mean = statistics.mean(data_2)
         
        # Printing the mean
        print("Abstract percentage pure virtual ratio Mean :", Abstract_interface_mean)
        print("Abstract Number of children Mean: ", Abstract_NOC_mean)
        
        #-------------------------------------------------Correlation of them---------------------------------------------#

        data = {
            'Abstract percentage pure virtual ratio': self.data_analysis.AbstractClassesInterface,
            'Abstract Number of children': self.data_analysis.number_of_children_per_abstract_class
        }
         
        dataframe = pd.DataFrame(data, columns=['Abstract percentage pure virtual ratio', 'Abstract Number of children'])
        print("Dataframe is : ")
        print(dataframe)
         
        # form correlation matrix
        matrix = dataframe.corr()
        print("Correlation matrix is : ")
        print(matrix, "\n")
    
    def generalized_Results(self):
        print("--------------------------Genaral Results About Inheritnace----------------------------")
        
        print("-----------------------Inheritance instances STATS---------------------")
        print("Number of implementation inheritance: ", self.data_analysis.implementationinheritance)
        print("Number of interface inheritance: ", self.data_analysis.interfaceinheritance)
        print("Number of Abstract classes: ", self.data_analysis.abstract_classes)
        print("Number of Concrete classes: ", self.data_analysis.concrete_classes)
        print("Number of Interface classes: ", self.data_analysis.interface_classes)
        # plt.figure(6)
        Label = ["Implementation inheritance", "Interface Inheritance"]
        data = [self.data_analysis.implementationinheritance, self.data_analysis.interfaceinheritance]
        plt.pie(data, labels = Label,autopct='%1.1f%%')
        # show plot
        plt.show()
        
        # #Breakdown of implementation inheritance
        plt.figure(8)
        Label = ["Abstract only", "Abstract And Interface", "Concrete Only", "Concrete And Abstract", "Concrete And Interface"]
        data = [len(self.data_analysis.abstractOnly), len(self.data_analysis.abstract_Interface), len(self.data_analysis.concreteOnly), len(self.data_analysis.concrete_Abstract), len(self.data_analysis.concrete_Interface)]
        plt.title('Implementation Inheritance breakdown')
        plt.pie(data, labels = Label, autopct='%1.1f%%')
        plt.show()
        
        # plt.figure(7)
        labels = ['Abstract Classes', 'Concrete Classes', 'Interface Classes']
        data = [self.data_analysis.abstract_classes,self.data_analysis.concrete_classes, self.data_analysis.interface_classes]
        plt.title('Distribution of classes types in inheritance instances')
        plt.pie(data, labels=labels, autopct='%1.1f%%') 
        plt.show()
        
        plt.figure(4)
        Label = ["Unused INTERFACE CLASSES", "USED INTERFACE CLASSES"]
        data = [self.data_analysis.interface_classes-self.data_analysis.Used_Interface_Classes, self.data_analysis.Used_Interface_Classes]
        plt.pie(data, labels = Label, autopct='%1.1f%%')
        # show plot
        plt.show()
        
        plt.figure(5)
        Label = ["Unused ABSTRACT CLASSES", "USED ABSTRACT CLASSES"]
        data = [self.data_analysis.abstract_classes-self.data_analysis.Used_Abstract_Classes, self.data_analysis.Used_Abstract_Classes]
        plt.pie(data, labels = Label, autopct='%1.1f%%')
        # show plot
        plt.show()
          
    def perform_Analysis(self):
        self.generalized_Results()
        self._ConcreteSuperClassesPlot()
        self._ConcreteSuperClassStatisticAnalysis()
        self._Interface_Analysis_Plots()
        self._Interface_Number_of_children_Analysis()
        self._Presence_Abstract_Classes_Analysis()


if __name__ == '__main__':
    _visualizer = DataAnalysisVisualizer()
    _visualizer.perform_Analysis()