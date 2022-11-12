from Inheritance_Data_analysis import *
from matplotlib import pyplot as plt
import numpy as np

data_analysis = DataAnalysis()

data_analysis.startAnalysis()
#-----------------------------------This is For implementation inheritance (From Concrete SuperClasses)----------------------------------------#
# plt.figure(1)
# print("Overriden", data_analysis.derivedConcrete_Classes_ratio_overriden)
# plt.hist(data_analysis.derivedConcrete_Classes_ratio_overriden)
# plt.xlabel("Percentage of Overriden")
# plt.title("Concrete Subclasses Public interface Overriden Methods")
# plt.ylabel("Number Of Derived Concrete Subclasses")
# # Displaying the graph
# plt.show()
# plt.figure(2)
# print("Added Methods", data_analysis.derivedConcrete_Classes_ratio_NovelMethods)
# plt.hist(data_analysis.derivedConcrete_Classes_ratio_NovelMethods)
# plt.xlabel("Percentage of Novel Methods")
# plt.title("Concrete Subclasses Public interface Novel Methods")
# plt.ylabel("Number Of Derived Concrete Subclasses")
# # Displaying the graph
# plt.show()
# plt.figure(3)
# print("Inherited and Used", data_analysis.derivedConcrete_Classes_ratio_inherited)
# plt.hist(data_analysis.derivedConcrete_Classes_ratio_inherited)
# plt.xlabel("Percentage of Inherited Unoverriden")
# plt.title("Concrete Subclasses Public interface Unoverriden Methods")
# plt.ylabel("Number Of Derived Concrete Subclasses")
# # Displaying the graph
# plt.show()

# # #------------------------------------For inheriting from completly Abstract classes--------------------------------#
# # plt.figure(4)
# # plt.hist(data_analysis.AbstractderivedConcrete_Classes_ratio_NovelMethods)
# # plt.xlabel("Percentage of Novel Methods")
# # plt.title("Concrete Subclasses Public interface Novel methods")
# # plt.ylabel("Number Of Derived Concrete Subclasses")
# # # Displaying the graph

# # plt.show()
# # plt.figure(5)
# # plt.hist(data_analysis.AbstractderivedConcrete_Classes_ratio_inherited)
# # plt.xlabel("Percentage of Inherited Unoverriden")
# # plt.title("Concrete Subclasses Overriden Methods")
# # plt.ylabel("Number Of Derived Concrete Subclasses")
# # # Displaying the graph
# # plt.show()

# # #-----------------------------------For pure interface inheritance----------------------------------------------#

# # plt.figure(6)
# # print(data_analysis.InterfaceClassesInterface)
# # print("Number of interface classes: ", data_analysis.interface_classes)
# # plt.hist(data_analysis.InterfaceClassesInterface)
# # plt.xlabel("Interface classes Public Interface")
# # plt.ylabel("Number Of Interface Classes")
# # # Displaying the graph
# # plt.show()

# #-----Analysis For Pure Implementation inheritance(Concrete SUBCLASS, Concrete SUPERCLASS)---------------------------------#
# #--------------Whiskers Plots-------------------------------------------------------------------------------------#
# import matplotlib.pyplot as plt
# import numpy as np
 
 
# # Creating dataset
# np.random.seed(10)
# data_1 = data_analysis.derivedConcrete_Classes_ratio_overriden
# data_2 = data_analysis.derivedConcrete_Classes_ratio_inherited
# data_3 = data_analysis.derivedConcrete_Classes_ratio_NovelMethods

# import pandas as pd
 
# # creating pandas dataframe
# df_cars = pd.DataFrame({'Overriden': data_1,
#      'Inherited': data_2,
#      'Novel': data_3,
#      })

# writer = pd.ExcelWriter('Tshililo_Inheritance_Usage.xlsx')

# # write dataframe to excel
 
# df_cars.to_excel(writer)
 
# # save the excel
# writer.save()
 
# fig = plt.figure(figsize =(10, 7))
 
# # Creating plot
# DataList = [data_1,data_2,data_3]
# plt.title("Overriden, Inherited and Used, Novel Methods")
# plt.boxplot(DataList)
# # show plot
# plt.show()
# # #-------------------------------------------------Standard Deviation----------------------------------------------#
# import statistics
# Overriden_Methods = data_analysis.derivedConcrete_Classes_ratio_overriden
# standard_deviation = statistics.stdev(Overriden_Methods)
# print("Overriden Standard Deviation: ", standard_deviation)

# Inherited_And_Used_Methods = data_analysis.derivedConcrete_Classes_ratio_inherited
# standard_deviation = statistics.stdev(Inherited_And_Used_Methods)
# print("Inherited And USED Standard Deviation: ", standard_deviation)

# Novel_Methods = data_analysis.derivedConcrete_Classes_ratio_NovelMethods
# standard_deviation = statistics.stdev(Novel_Methods)
# print("Novel Methods Standard Deviation: ", standard_deviation)

# #------------------------------------------------THE MEAN---------------------------------------------------------#
# import statistics
 
# # list of positive integer numbers
# Data_List = [data_1,data_2,data_3]
 
# overriden_mean = statistics.mean(data_1)
# Inherited_And_Used_mean = statistics.mean(data_2)
# Novel_mean = statistics.mean(data_3)
 
# # Printing the mean
# print("Overriden Mean :", overriden_mean)
# print("Inherited And Used Mean :", Inherited_And_Used_mean)
# print("Novel Mean: ", Novel_mean)

# #-------------------------------------------------Correlation of them---------------------------------------------#
# # # collect data
# import pandas as pd
# data = {
#     'Novel': data_analysis.derivedConcrete_Classes_ratio_NovelMethods,
#     'Inherited': data_analysis.derivedConcrete_Classes_ratio_inherited,
#     'Overriden': data_analysis.derivedConcrete_Classes_ratio_overriden
# }
 
# # form dataframe
# dataframe = pd.DataFrame(data, columns=['Novel', 'Inherited', 'Overriden'])
# print("Dataframe is : ")
# print(dataframe)
 
# # form correlation matrix
# matrix = dataframe.corr()
# print("Correlation matrix is : ")
# print(matrix)

# #-------------------------------------------For Interface Inheritance (Concrete SUBCLASS)---------------------------------------------#
# plt.figure(1)
# print("Overriden",data_analysis.InterfacederivedConcrete_Classes_ratio_overriden)
# plt.hist(data_analysis.InterfacederivedConcrete_Classes_ratio_overriden)
# plt.xlabel("Percentage of Overriden")
# plt.title("Concrete Subclasses Public interface Overriden Methods")
# plt.ylabel("Number Of Derived Concrete Subclasses")
# # Displaying the graph
# plt.show()
# #----------------------------------------------Novel Methods Distribution-----------------------------------------#
# plt.figure(2)
# print("Overriden",data_analysis.InterfacederivedConcrete_Classes_ratio_NovelMethods)
# plt.hist(data_analysis.InterfacederivedConcrete_Classes_ratio_NovelMethods)
# plt.xlabel("Percentage Added Methods")
# plt.title("Concrete Subclasses Public interface Added Methods")
# plt.ylabel("Number Of Derived Concrete Subclasses")
# # Displaying the graph
# plt.show()

# #------------------------------------------------Interface Analysis------------------------------------------------#
# #--------------Whiskers Plots-------------------------------------------------------------------------------------#
# import matplotlib.pyplot as plt
# import numpy as np
 
 
# # Creating dataset
# np.random.seed(10)
# data_1 = data_analysis.InterfacederivedConcrete_Classes_ratio_overriden
# data_2 = data_analysis.InterfacederivedConcrete_Classes_ratio_NovelMethods
 
# fig = plt.figure(figsize =(10, 7))
 
# # Creating plot
# DataList = [data_1,data_2]
# plt.title("Overriden, Novel Methods")
# plt.boxplot(DataList)
# # show plot
# plt.show()
# # #-------------------------------------------------Standard Deviation----------------------------------------------#
# import statistics
# Overriden_Methods = data_analysis.InterfacederivedConcrete_Classes_ratio_overriden
# standard_deviation = statistics.stdev(Overriden_Methods)
# print("Overriden Standard Deviation: ", standard_deviation)

# Novel_Methods = data_analysis.InterfacederivedConcrete_Classes_ratio_NovelMethods
# standard_deviation = statistics.stdev(Novel_Methods)
# print("Novel Methods Standard Deviation: ", standard_deviation)

# #------------------------------------------------THE MEAN---------------------------------------------------------#
# import statistics
 
# # list of positive integer numbers
 
# overriden_mean = statistics.mean(data_1)
# Novel_mean = statistics.mean(data_2)
 
# # Printing the mean
# print("Overriden Mean :", overriden_mean)
# print("Novel Mean: ", Novel_mean)

# #-------------------------------------------------Correlation of them---------------------------------------------#
# # # collect data
# import pandas as pd
# data = {
#     'Novel': data_analysis.InterfacederivedConcrete_Classes_ratio_NovelMethods,
#     'Overriden': data_analysis.InterfacederivedConcrete_Classes_ratio_overriden
# }
 
# # form dataframe
# dataframe = pd.DataFrame(data, columns=['Novel', 'Overriden'])
# print("Dataframe is : ")
# print(dataframe)
 
# # form correlation matrix
# matrix = dataframe.corr()
# print("Correlation matrix is : ")
# print(matrix)

# # #-------------------------------------For Concrete Subclasses------------------------------------------------#
# # plt.figure(1)
# # plt.plot(data_analysis._inherited_methods_percentages,data_analysis.number_of_Concrete_Classes_per_ratio_inherited, 'bo', label = "Inherited Methods")
# # plt.plot(data_analysis._novel_methods_percentages,data_analysis.number_of_Concrete_Classes_per_ratio_NovelMethods,'go', label = "Novel Methods")
# # plt.plot(data_analysis._overriden_methods_percentages,data_analysis.number_of_Concrete_Classes_per_ratio_overriden,'r+', label = "Overriden Methods")
# # plt.xlabel('percentage of Methods')
# # plt.ylabel('Number of concrete subclasses')
# # plt.title('Public interface percentage')
# # plt.legend()
# # plt.show()
# # #---------------------------------------For Abstract Classes-------------------------------------------------#
# # plt.figure(2)
# # plt.plot(data_analysis._abstract_interface_percentage, data_analysis.AbstractClasses_per_interface_ratio, 'go', label = "Pure Virtual functions")
# # plt.xlabel('Pure virtual methods Percentage')
# # plt.ylabel('Number of Abstract Classes')
# # plt.title('Abstract Classes Interface')
# # plt.legend()
# # plt.show()

# # number_of_DerivedConcrete_classes, Concrete_interface = data_analysis.Subclasses_Concrete_classes_Interface()
# # number_of_interface_classes, interface_classes_interface = data_analysis.interface_classes_interface()
# # plt.figure(3)
# # plt.plot(Concrete_interface, number_of_DerivedConcrete_classes, 'go', label = "Derived Concrete Class")
# # plt.plot(interface_classes_interface, number_of_interface_classes, 'bo', label = "Interface Class")
# # plt.xlabel('Number of public interface')
# # plt.ylabel('Number of classes')
# # plt.title('Derived Concrete classes Interface')
# # plt.legend()
# # plt.show()

# # plt.figure(4)
# # Label = ["Unused INTERFACE CLASSES", "USED INTERFACE CLASSES"]
# # data = [data_analysis.interface_classes-data_analysis.Used_Interface_Classes, data_analysis.Used_Interface_Classes]
# # plt.pie(data, labels = Label, autopct='%1.1f%%')
# # # show plot
# # plt.show()

# # plt.figure(5)
# # Label = ["Unused ABSTRACT CLASSES", "USED ABSTRACT CLASSES"]
# # data = [data_analysis.abstract_classes-data_analysis.Used_Abstract_Classes, data_analysis.Used_Abstract_Classes]
# # plt.pie(data, labels = Label, autopct='%1.1f%%')
# # # show plot
# # plt.show()
# # plt.figure(6)
# # Label = ["Implementation inheritance", "Interface Inheritance"]
# # data = [data_analysis.implementationinheritance, data_analysis.interfaceinheritance]
# # plt.pie(data, labels = Label,autopct='%1.1f%%')
# # # show plot
# # plt.show()
# # plt.figure(7)
# # labels = ['Abstract Classes', 'Concrete Classes', 'Interface Classes']
# # data = [data_analysis.abstract_classes,data_analysis.concrete_classes, data_analysis.interface_classes]
# # plt.title('Total classes')
# # plt.pie(data, labels=labels, autopct='%1.1f%%') 
# # plt.show()     

# # #Breakdown of implementation inheritance
# plt.figure(8)
# Label = ["Abstract only", "Abstract And Interface", "Concrete Only", "Concrete And Abstract", "Concrete And Interface"]
# data = [len(data_analysis.abstractOnly), len(data_analysis.abstract_Interface), len(data_analysis.concreteOnly), len(data_analysis.concrete_Abstract), len(data_analysis.concrete_Interface)]
# plt.title('Implementation Inheritance breakdown')
# plt.pie(data, labels = Label, autopct='%1.1f%%')
# plt.show()

# # #----------------------------------------Number Of Chidren Per Subclass-------------------------------------------#
# # number_of_abstract_classes, Abstract_classes_NOC = data_analysis.NOC_per_AbstractClasses()
# # number_of_interface_classes, interface_classes_NOC = data_analysis.NOC_per_InterfaceClasses()
# # number_of_Concrete_classes, Concrete_classes_NOC = data_analysis.NOC_per_ConcreteClasses()

# # print(data_analysis.number_of_children_per_abstract_class)
# # plt.figure(9)
# # plt.plot(Abstract_classes_NOC,number_of_abstract_classes,  'bo', label = "Abstract Class")
# # plt.plot(interface_classes_NOC,number_of_interface_classes,  'go', label = "Interface Class")
# # plt.plot(Concrete_classes_NOC,number_of_Concrete_classes,  'r+', label = "Concrete Class")
# # plt.ylabel('Number of classes')
# # plt.xlabel('Number of Children')
# # plt.title('Number of Subclasses Per Superclass Types')
# # plt.legend()
# # plt.show()