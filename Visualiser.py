from Inheritance_Data_analysis import *
from matplotlib import pyplot as plt
import numpy as np

data_analysis = DataAnalysis()

data_analysis.startAnalysis()
#-------------------------------------For Concrete Subclasses------------------------------------------------#
plt.figure(1)
plt.plot(data_analysis._inherited_methods_percentages,data_analysis.number_of_Concrete_Classes_per_ratio_inherited, 'bo', label = "Inherited Methods")
plt.plot(data_analysis._novel_methods_percentages,data_analysis.number_of_Concrete_Classes_per_ratio_NovelMethods,'go', label = "Novel Methods")
plt.plot(data_analysis._overriden_methods_percentages,data_analysis.number_of_Concrete_Classes_per_ratio_overriden,'r+', label = "Overriden Methods")
plt.xlabel('percentage of Methods')
plt.ylabel('Number of concrete subclasses')
plt.title('Public interface percentage')
plt.legend()
plt.show()
#---------------------------------------For Abstract Classes-------------------------------------------------#
plt.figure(2)
plt.plot(data_analysis._abstract_interface_percentage, data_analysis.AbstractClasses_per_interface_ratio, 'go', label = "Pure Virtual functions")
plt.xlabel('Pure virtual methods Percentage')
plt.ylabel('Number of Abstract Classes')
plt.title('Abstract Classes Interface')
plt.legend()
plt.show()

number_of_DerivedConcrete_classes, Concrete_interface = data_analysis.Subclasses_Concrete_classes_Interface()
number_of_interface_classes, interface_classes_interface = data_analysis.interface_classes_interface()
plt.figure(3)
plt.plot(Concrete_interface, number_of_DerivedConcrete_classes, 'go', label = "Derived Concrete Class")
plt.plot(interface_classes_interface, number_of_interface_classes, 'bo', label = "Interface Class")
plt.xlabel('Number of public interface')
plt.ylabel('Number of classes')
plt.title('Derived Concrete classes Interface')
plt.legend()
plt.show()

plt.figure(4)
Label = ["Unused INTERFACE CLASSES", "USED INTERFACE CLASSES"]
data = [data_analysis.interface_classes-data_analysis.Used_Interface_Classes, data_analysis.Used_Interface_Classes]
plt.pie(data, labels = Label, autopct='%1.1f%%')
# show plot
plt.show()

plt.figure(5)
Label = ["Unused ABSTRACT CLASSES", "USED ABSTRACT CLASSES"]
data = [data_analysis.abstract_classes-data_analysis.Used_Abstract_Classes, data_analysis.Used_Abstract_Classes]
plt.pie(data, labels = Label, autopct='%1.1f%%')
# show plot
plt.show()
plt.figure(6)
Label = ["Implementation inheritance", "Interface Inheritance"]
data = [data_analysis.implementationinheritance, data_analysis.interfaceinheritance]
plt.pie(data, labels = Label,autopct='%1.1f%%')
# show plot
plt.show()
plt.figure(7)
labels = ['Abstract Classes', 'Concrete Classes', 'Interface Classes']
data = [data_analysis.abstract_classes,data_analysis.concrete_classes, data_analysis.interface_classes]
plt.title('Class Types Distribution')
plt.pie(data, labels=labels, autopct='%1.1f%%') 
plt.show()     

#Breakdown of implementation inheritance
plt.figure(8)
Label = ["Abstract only", "Abstract And Interface", "Concrete Only", "Concrete And Abstract", "Concrete And Interface"]
data = [len(data_analysis.abstractOnly), len(data_analysis.abstract_Interface), len(data_analysis.concreteOnly), len(data_analysis.concrete_Abstract), len(data_analysis.concrete_Interface)]
plt.title('Implementation Inheritance breakdown')
plt.pie(data, labels = Label, autopct='%1.1f%%')
plt.show()

#----------------------------------------Number Of Chidren Per Subclass-------------------------------------------#
number_of_abstract_classes, Abstract_classes_NOC = data_analysis.NOC_per_AbstractClasses()
number_of_interface_classes, interface_classes_NOC = data_analysis.NOC_per_InterfaceClasses()
number_of_Concrete_classes, Concrete_classes_NOC = data_analysis.NOC_per_ConcreteClasses()

print(data_analysis.number_of_children_per_abstract_class)
plt.figure(9)
plt.plot(Abstract_classes_NOC,number_of_abstract_classes,  'bo', label = "Abstract Class")
plt.plot(interface_classes_NOC,number_of_interface_classes,  'go', label = "Interface Class")
plt.plot(Concrete_classes_NOC,number_of_Concrete_classes,  'r+', label = "Concrete Class")
plt.ylabel('Number of classes')
plt.xlabel('Number of Children')
plt.title('Number of Subclasses Per Superclass Types')
plt.legend()
plt.show()



    
