from pickle import TRUE
from pydoc import classname
import unittest
import os.path

from AnalysingProject import ProjectData
import Data_Extraction_Process_Refractored

def getPath(file_path):
    cwd = os.getcwd() # get current working directory
    path = os.path.join(cwd, file_path) # path of the file being tested    
    return path 

#------------------------Getting Classes Level Data in a File--------------------------------------------------#
def ExtractedClassesData(file_path):
    source_path = getPath(file_path)
    project = ProjectData()
    Data_Extraction_Process_Refractored.parseTranslationUnit(source_path, project)
    return project.cppClasses
#------------------------For Computing Inheritance Data for every inheritance in a hierachy---------------------#
def InheritancesData(file_path):
    source_path = getPath(file_path)
    project = ProjectData()
    Data_Extraction_Process_Refractored.parseTranslationUnit(source_path, project)
    inheritanceData = project.computeInheritanceData()
    return inheritanceData
#---------------------For computing The Inheritance Hierachy---------------------------#
def getinheritanceHierachies(file_path):
    source_path = getPath(file_path)
    project = ProjectData()
    Data_Extraction_Process_Refractored.parseTranslationUnit(source_path, project)
    inheritancehierachies = project.organizeHierachy()
    return inheritancehierachies

class Extraction_test(unittest.TestCase):
    cppClasses = ExtractedClassesData('__mytests_\\class_object.cpp\\class_data.cpp') 
    className = 'A'
    PublicDerivedclassName = 'B' 
    PrivateDerivedclassName = 'C'
    ProtectedDerivedclassName = 'G'
    PublicPublicDerivedclassName = 'D'
    PrivatePriavteDerivedclassName = 'E'
    PrivatePublicDerivedclassName = 'F'
    def test_single_class_Methods_are_extracted_correctly(self):
        Publicmethods = {'purevirtualfunctions': ['void publicpuremethodA ()'],
                         'virtualfunctions': ['void publicvirtualmethodA (int)'], 
                         'normalfunctions': ['void privatenormalmethodA ()']}
        PrivateMethods = {'purevirtualfunctions': ['void privatepuremethodA ()'],
                          'virtualfunctions': ['void privatevirtualmethodA ()'],
                          'normalfunctions': ['void privatenormalmethodA ()']}
        ProtectedMethods = {'purevirtualfunctions': ['void protectedpuremethodA ()'],
                            'virtualfunctions': ['void protectedvirtualmethodA ()'],
                            'normalfunctions': ['void protectednormalmethodA ()']}
        #Methods Extration Tests
        self.assertDictEqual(self.cppClasses[self.className].publicMethods, Publicmethods)
        self.assertDictEqual(self.cppClasses[self.className].privateMethods, PrivateMethods)
        self.assertDictEqual(self.cppClasses[self.className].protectedMethods, ProtectedMethods)
    def test_single_class_does_not_have_baseclasses(self):
        self.assertEqual(self.cppClasses[self.className].Baseclasses, [])
    # def test_single_class_with_only_pure_virtual_functions_is_interface_class(self):
    # def test_single_class_with_pure_virtual_functions_and_virtual_functions_and_normal_function_is_Abstract_class(self):
    # def test_single_class_without_pure_virtual_functions_is_Concrete_class(self):
    # #-------------------------------Single Inheritance Extraction Tests-----------------------#
    # #-------------------------------PUBLIC INHERITANCE----------------------------------------------------#
    # def test_Single_Public_inheriting_class_Methods_are_extracted_correctly(self):
        
        Publicmethods = {'purevirtualfunctions': ['void publicpuremethodB ()'],
                         'virtualfunctions': ['void publicvirtualmethodB (int)'], 
                         'normalfunctions': ['void privatenormalmethodB ()']}
        PrivateMethods = {'purevirtualfunctions': ['void privatepuremethodB ()'],
                          'virtualfunctions': ['void privatevirtualmethodB ()'],
                          'normalfunctions': ['void privatenormalmethodB ()']}
        ProtectedMethods = {'purevirtualfunctions': ['void protectedpuremethodB ()'],
                            'virtualfunctions': ['void protectedvirtualmethodB ()'],
                            'normalfunctions': ['void protectednormalmethodB ()']}
        #Methods Extration Tests
        self.assertDictEqual(self.cppClasses[self.PublicDerivedclassName].publicMethods, Publicmethods)
        self.assertDictEqual(self.cppClasses[self.PublicDerivedclassName].privateMethods, PrivateMethods)
        self.assertDictEqual(self.cppClasses[self.PublicDerivedclassName].protectedMethods, ProtectedMethods)
    def test_Public_derived_class__have_Single_baseclasse(self):
        self.assertEqual(len(self.cppClasses[self.PublicDerivedclassName].Baseclasses), 1)
        self.assertEqual(self.cppClasses[self.PublicDerivedclassName].Baseclasses[0]['BaseClassInfo'].className, 'A')
    def test_the_derived_class_is_inheriting_publicly(self):
        self.assertEqual(self.cppClasses[self.PublicDerivedclassName].Baseclasses[0]['inheritancetype'], 'PUBLIC')
    #----------------------------Private Single Inheritance----------------------------#
    def test_Single_Private_inheriting_class_Methods_are_extracted_correctly(self):
        
        Publicmethods = {'purevirtualfunctions': ['void publicpuremethodB ()'],
                         'virtualfunctions': ['void publicvirtualmethodB (int)'], 
                         'normalfunctions': ['void privatenormalmethodB ()']}
        PrivateMethods = {'purevirtualfunctions': ['void privatepuremethodB ()'],
                          'virtualfunctions': ['void privatevirtualmethodB ()'],
                          'normalfunctions': ['void privatenormalmethodB ()']}
        ProtectedMethods = {'purevirtualfunctions': ['void protectedpuremethodB ()'],
                            'virtualfunctions': ['void protectedvirtualmethodB ()'],
                            'normalfunctions': ['void protectednormalmethodB ()']}
        #Methods Extration Tests
        self.assertDictEqual(self.cppClasses[self.PrivateDerivedclassName].publicMethods, Publicmethods)
        self.assertDictEqual(self.cppClasses[self.PrivateDerivedclassName].privateMethods, PrivateMethods)
        self.assertDictEqual(self.cppClasses[self.PrivateDerivedclassName].protectedMethods, ProtectedMethods)
    def test_Private_derived_class__have_Single_baseclasse(self):
        self.assertEqual(len(self.cppClasses[self.PrivateDerivedclassName].Baseclasses), 1)
        self.assertEqual(self.cppClasses[self.PrivateDerivedclassName].Baseclasses[0]['BaseClassInfo'].className, 'A')
    def test_the_derived_class_is_inheriting_privately(self):
        self.assertEqual(self.cppClasses[self.PrivateDerivedclassName].Baseclasses[0]['inheritancetype'], 'PRIVATE')
        
    #-------------------------------Protected Single inheritance Extraction Tests-----------------------#
    def test_Single_Protected_inheriting_class_Methods_are_extracted_correctly(self):
        Publicmethods = {'purevirtualfunctions': ['void publicpuremethodB ()'],
                         'virtualfunctions': ['void publicvirtualmethodB (int)'], 
                         'normalfunctions': ['void privatenormalmethodB ()']}
        PrivateMethods = {'purevirtualfunctions': ['void privatepuremethodB ()'],
                          'virtualfunctions': ['void privatevirtualmethodB ()'],
                          'normalfunctions': ['void privatenormalmethodB ()']}
        ProtectedMethods = {'purevirtualfunctions': ['void protectedpuremethodB ()'],
                            'virtualfunctions': ['void protectedvirtualmethodB ()'],
                            'normalfunctions': ['void protectednormalmethodB ()']}
        #Methods Extration Tests
        self.assertDictEqual(self.cppClasses[self.PrivateDerivedclassName].publicMethods, Publicmethods)
        self.assertDictEqual(self.cppClasses[self.PrivateDerivedclassName].privateMethods, PrivateMethods)
        self.assertDictEqual(self.cppClasses[self.PrivateDerivedclassName].protectedMethods, ProtectedMethods)
    def test_Protected_derived_class__have_Correct_Single_baseclasse(self):
        self.assertEqual(len(self.cppClasses[self.ProtectedDerivedclassName].Baseclasses), 1)
        self.assertEqual(self.cppClasses[self.ProtectedDerivedclassName].Baseclasses[0]['BaseClassInfo'].className, 'A')
    def test_the_type_of_inheritance_is_protected(self):
        self.assertEqual(self.cppClasses[self.ProtectedDerivedclassName].Baseclasses[0]['inheritancetype'], 'PROTECTED')
    
    #-------------------------------Public Multiple Inheritance Extraction Tests-----------------------#
    def test_Public_Multiple_inheriting_class_Methods_are_extracted_correctly(self):
        
        Publicmethods = {'purevirtualfunctions': ['void publicpuremethodB ()'],
                         'virtualfunctions': ['void publicvirtualmethodB (int)'], 
                         'normalfunctions': ['void privatenormalmethodB ()']}
        PrivateMethods = {'purevirtualfunctions': ['void privatepuremethodB ()'],
                          'virtualfunctions': ['void privatevirtualmethodB ()'],
                          'normalfunctions': ['void privatenormalmethodB ()']}
        ProtectedMethods = {'purevirtualfunctions': ['void protectedpuremethodB ()'],
                            'virtualfunctions': ['void protectedvirtualmethodB ()'],
                            'normalfunctions': ['void protectednormalmethodB ()']}
        #Methods Extration Tests
        self.assertDictEqual(self.cppClasses[self.PublicPublicDerivedclassName].publicMethods, Publicmethods)
        self.assertDictEqual(self.cppClasses[self.PublicPublicDerivedclassName].privateMethods, PrivateMethods)
        self.assertDictEqual(self.cppClasses[self.PublicPublicDerivedclassName].protectedMethods, ProtectedMethods)
    def test_derived_Multiple_Public_class__has_Two_baseclasses(self):
        self.assertEqual(len(self.cppClasses[self.PublicPublicDerivedclassName].Baseclasses), 2)
        self.assertEqual(self.cppClasses[self.PublicPublicDerivedclassName].Baseclasses[0]['BaseClassInfo'].className, 'C')
        self.assertEqual(self.cppClasses[self.PublicPublicDerivedclassName].Baseclasses[1]['BaseClassInfo'].className, 'B')
    def test_the_derived_class_is_inheriting_from_Both_BaseClasses_publicly(self):
        self.assertEqual(self.cppClasses[self.PublicPublicDerivedclassName].Baseclasses[0]['inheritancetype'], 'PUBLIC')
        self.assertEqual(self.cppClasses[self.PublicPublicDerivedclassName].Baseclasses[1]['inheritancetype'], 'PUBLIC')
    #-------------------------------Private Multiple Inheritance Extraction Tests-----------------------#
    def test_Private_Multiple_inheriting_class_Methods_are_extracted_correctly(self):

        Publicmethods = {'purevirtualfunctions': ['void publicpuremethodB ()'],
                         'virtualfunctions': ['void publicvirtualmethodB (int)'], 
                         'normalfunctions': ['void privatenormalmethodB ()']}
        PrivateMethods = {'purevirtualfunctions': ['void privatepuremethodB ()'],
                          'virtualfunctions': ['void privatevirtualmethodB ()'],
                          'normalfunctions': ['void privatenormalmethodB ()']}
        ProtectedMethods = {'purevirtualfunctions': ['void protectedpuremethodB ()'],
                            'virtualfunctions': ['void protectedvirtualmethodB ()'],
                            'normalfunctions': ['void protectednormalmethodB ()']}
        #Methods Extration Tests
        self.assertDictEqual(self.cppClasses[self.PrivatePriavteDerivedclassName].publicMethods, Publicmethods)
        self.assertDictEqual(self.cppClasses[self.PrivatePriavteDerivedclassName].privateMethods, PrivateMethods)
        self.assertDictEqual(self.cppClasses[self.PrivatePriavteDerivedclassName].protectedMethods, ProtectedMethods)
    def test_Multiple_Private_derived_class__has_Two_baseclasses(self):
        self.assertEqual(len(self.cppClasses[self.PrivatePriavteDerivedclassName].Baseclasses), 2)
        self.assertEqual(self.cppClasses[self.PrivatePriavteDerivedclassName].Baseclasses[0]['BaseClassInfo'].className, 'B')
        self.assertEqual(self.cppClasses[self.PrivatePriavteDerivedclassName].Baseclasses[1]['BaseClassInfo'].className, 'A')
    def test_the_derived_class_is_inheriting_from_Both_BaseClasses_privately(self):
        self.assertEqual(self.cppClasses[self.PrivatePriavteDerivedclassName].Baseclasses[0]['inheritancetype'], 'PRIVATE')
        self.assertEqual(self.cppClasses[self.PrivatePriavteDerivedclassName].Baseclasses[1]['inheritancetype'], 'PRIVATE')
    #-------------------------------Private Public Multiple Inheritance Extraction Tests-----------------------#
    def test_Public_And_Private_inheriting_class_Methods_are_extracted_correctly(self):
        
        Publicmethods = {'purevirtualfunctions': ['void publicpuremethodB ()'],
                         'virtualfunctions': ['void publicvirtualmethodB (int)'], 
                         'normalfunctions': ['void privatenormalmethodB ()']}
        PrivateMethods = {'purevirtualfunctions': ['void privatepuremethodB ()'],
                          'virtualfunctions': ['void privatevirtualmethodB ()'],
                          'normalfunctions': ['void privatenormalmethodB ()']}
        ProtectedMethods = {'purevirtualfunctions': ['void protectedpuremethodB ()'],
                            'virtualfunctions': ['void protectedvirtualmethodB ()'],
                            'normalfunctions': ['void protectednormalmethodB ()']}
        #Methods Extration Tests
        self.assertDictEqual(self.cppClasses[self.PrivatePublicDerivedclassName].publicMethods, Publicmethods)
        self.assertDictEqual(self.cppClasses[self.PrivatePublicDerivedclassName].privateMethods, PrivateMethods)
        self.assertDictEqual(self.cppClasses[self.PrivatePublicDerivedclassName].protectedMethods, ProtectedMethods)
    def test_Public_And_Private_derived_class__has_Two_baseclasses(self):
        self.assertEqual(len(self.cppClasses[self.PrivatePublicDerivedclassName].Baseclasses), 2)
        self.assertEqual(self.cppClasses[self.PrivatePublicDerivedclassName].Baseclasses[0]['BaseClassInfo'].className, 'C')
        self.assertEqual(self.cppClasses[self.PrivatePublicDerivedclassName].Baseclasses[1]['BaseClassInfo'].className, 'D')
    def test_the_derived_class_is_inheriting_from_Both_BaseClasses_privately_And_Publicly(self):
        self.assertEqual(self.cppClasses[self.PrivatePublicDerivedclassName].Baseclasses[0]['inheritancetype'], 'PRIVATE')
        self.assertEqual(self.cppClasses[self.PrivatePublicDerivedclassName].Baseclasses[1]['inheritancetype'], 'PUBLIC') 
               
#--------------------------------------------Single Class Properties----------------------------------------------#
#Type of class Tests
class single_class_properties_Tests(unittest.TestCase):
    cppClasses = ExtractedClassesData('__mytests_\\class_object.cpp\\Single_class_properties.cpp') 
    def test_class_with_only_pure_virtual_functions_is_interface_class(self):
        self.assertEqual(len(self.cppClasses['A'].Baseclasses), 0)
        self.assertEqual(self.cppClasses['A'].is_interface(), True)
        self.assertNotEqual(self.cppClasses['A'].is_abstract(),True)
        #self.assertNotEqual(self.cppClasses['A'].is_Concrete(),True)
#     def test_class_with_only_normal_functions_is_concrete_class(self):
#         self.assertEqual(len(self.cppClasses['B'].Baseclasses), 0)
#         self.assertNotEqual(self.cppClasses['B'].is_interface(), True)
#         self.assertNotEqual(self.cppClasses['B'].is_abstract(),True)
#         self.assertEqual(self.cppClasses['B'].is_Concrete(),True)
#     def test_class_with_normal_functions_is_concrete_class(self):
#         self.assertEqual(len(self.cppClasses['B'].Baseclasses), 0)
#         self.assertNotEqual(self.cppClasses['B'].is_interface(), True)
#         self.assertNotEqual(self.cppClasses['B'].is_abstract(),True)
#         self.assertEqual(self.cppClasses['B'].is_Concrete(),True)
        
    #---------------------------------------Single Inheritance Data-----------------------------------------------------------#
class Single_Methods_Inheritance_Tests(unittest.TestCase):
    inheritanceData = InheritancesData('__mytests_\\Single_inheritance\\Single_Inheritance.cpp')
    #---------------------------------------------Public Inheritance------------------------------------#
    def test_baseclass_public_and_protected_methods_are_inherited_to_the_public_and_protected_respectively_and_private_normal_are_not(self):
        Publicmethods = {'Addedpurevirtualfunctions': ['void derivedpublicpuremethod ()'],
                         'Addedvirtualfunctions': ['void derivedpublicvirtualmethod ()'], 
                         'Addednormalfunctions': ['void derivedpublicnormalmethod ()'], 
                         'inherited_pure_virtual': ['void basepublicpuremethod ()'],
                         'inherited_virtual': ['void basepublicvirtualmethod ()'],
                         'inherited_normal': ['void basepublicnormalmethod ()']}
        PrivateMethods = {'Addedpurevirtualfunctions': ['void derivedprivatepuremethod ()'],
                          'Addedvirtualfunctions': ['void derivedprivatevirtualmethod ()'],
                          'Addednormalfunctions': ['void derivedprivatenormalmethod ()'],
                          'inherited_pure_virtual': ['void baseprivatepuremethod ()'],
                          'inherited_virtual': ['void baseprivatevirtualmethod ()'],
                          'inherited_normal': []}
        ProtectedMethods = {'Addedpurevirtualfunctions': ['void derivedprotectedpuremethod ()'],
                            'Addedvirtualfunctions': ['void derivedprotectedvirtualmethod ()'],
                            'Addednormalfunctions': ['void derivedprotectednormalmethod ()'],
                            'inherited_pure_virtual': ['void baseprotectedpuremethod ()'],
                            'inherited_virtual': ['void baseprotectedvirtualmethod ()'],
                            'inherited_normal': ['void baseprotectednormalmethod ()']}
        self.assertDictEqual(self.inheritanceData[0].PublicMethods, Publicmethods)
        self.assertDictEqual(self.inheritanceData[0].PrivateMethods, PrivateMethods)
        self.assertDictEqual(self.inheritanceData[0].ProtectedMethods, ProtectedMethods)
#     #-----------------------------------------------Private Inheritance------------------------------------------#
    def test_public_and_protected_methods_are_become_private_methods_of_the_derived_class_and_private_normal_methods_not_inherited(self):
        PublicMethods = {'Addedpurevirtualfunctions': ['void derivedpublicpuremethod ()'],
                         'Addedvirtualfunctions': ['void derivedpublicvirtualmethod ()'],
                         'Addednormalfunctions': ['void derivedpublicnormalmethod ()'],
                         'inherited_pure_virtual': [],
                         'inherited_virtual': [],
                         'inherited_normal': []}
        PrivateMethods = {'Addedpurevirtualfunctions': ['void derivedprivatepuremethod ()'],
                          'Addedvirtualfunctions': ['void derivedprivatevirtualmethod ()'],
                          'Addednormalfunctions': ['void derivedprivatenormalmethod ()']
                          , 'inherited_pure_virtual': ['void basepublicpuremethod ()', 'void baseprivatepuremethod ()', 'void baseprotectedpuremethod ()'],
                          'inherited_virtual': ['void basepublicvirtualmethod ()', 'void baseprivatevirtualmethod ()', 'void baseprotectedvirtualmethod ()'],
                          'inherited_normal': ['void basepublicnormalmethod ()', 'void baseprotectednormalmethod ()']} 
        ProtectedMethods = {'Addedpurevirtualfunctions': ['void derivedprotectedpuremethod ()'],
                            'Addedvirtualfunctions': ['void derivedprotectedvirtualmethod ()'],
                            'Addednormalfunctions': ['void derivedprotectednormalmethod ()'],
                            'inherited_pure_virtual': [], 
                            'inherited_virtual': [], 
                            'inherited_normal': []}
        self.assertDictEqual(self.inheritanceData[1].PublicMethods, PublicMethods)
        self.assertDictEqual(self.inheritanceData[1].PrivateMethods, PrivateMethods)
        self.assertDictEqual(self.inheritanceData[1].ProtectedMethods, ProtectedMethods)
#     #-----------------------------------------------Protected Inheritance-----------------------------------------#
    def test_public_and_protected_methods_both_become_derived_class_protected_methods_and_base_class_private_normal_not_inherited(self):
        PublicMethods = {'Addedpurevirtualfunctions': ['void derivedpublicpuremethod ()'],
                         'Addedvirtualfunctions': ['void derivedpublicvirtualmethod ()'],
                         'Addednormalfunctions': ['void derivedpublicnormalmethod ()'],
                         'inherited_pure_virtual': [],
                         'inherited_virtual': [],
                         'inherited_normal': []}
        ProtectedMethods = {'Addedpurevirtualfunctions': ['void derivedprotectedpuremethod ()'],
                            'Addedvirtualfunctions': ['void derivedprotectedvirtualmethod ()'],
                            'Addednormalfunctions': ['void derivedprotectednormalmethod ()'],
                            'inherited_pure_virtual': ['void basepublicpuremethod ()', 'void baseprotectedpuremethod ()'],
                            'inherited_virtual': ['void basepublicvirtualmethod ()', 'void baseprotectedvirtualmethod ()'],
                            'inherited_normal': ['void basepublicnormalmethod ()', 'void baseprotectednormalmethod ()']}
        PrivateMethods  = {'Addedpurevirtualfunctions': ['void derivedprivatepuremethod ()'],
                           'Addedvirtualfunctions': ['void derivedprivatevirtualmethod ()'],
                           'Addednormalfunctions': ['void derivedprivatenormalmethod ()'],
                           'inherited_pure_virtual': ['void baseprivatepuremethod ()'],
                           'inherited_virtual': ['void baseprivatevirtualmethod ()'],
                           'inherited_normal': []}
        self.assertDictEqual(self.inheritanceData[2].PublicMethods, PublicMethods)
        self.assertDictEqual(self.inheritanceData[2].PrivateMethods, PrivateMethods)
        self.assertDictEqual(self.inheritanceData[2].ProtectedMethods, ProtectedMethods)

class Single_Interface_Inheritace_Tests(unittest.TestCase):
    inheritanceData = InheritancesData('__mytests_\\Single_inheritance\\Single_interface_inheritance.cpp')
#--------------------------------------------THE BASE CLASS IS INTERFACE CLASS--------------------------------------------------#
    def test_if_derived_class_inherit_publicly_from_interface_class_is_interface_inheritance(self):
        #--------------------------------Public Inheritance-------------------------------------#
        self.assertEqual(self.inheritanceData[0].Parents[0].className, 'A')
        self.assertEqual(self.inheritanceData[0].derivedclassName, 'B')
        self.assertEqual(self.inheritanceData[0].Parents[0].is_interface(), True)
        self.assertEqual(self.inheritanceData[0].typeofinheritance, 'Interface Inheritance')
        #-------------------------------Private Inheritance-------------------------------------#
    def test_if_derived_class_inherit_privately_from_interface_class_is_interface_inheritance(self):
        #--------------------------------Private Inheritance-------------------------------------#
        self.assertEqual(self.inheritanceData[1].Parents[0].className, 'A')
        self.assertEqual(self.inheritanceData[1].derivedclassName, 'C')
        self.assertEqual(self.inheritanceData[1].Parents[0].is_interface(), True)
        self.assertEqual(self.inheritanceData[1].typeofinheritance, 'Interface Inheritance')
    def test_if_derived_class_inherit_protectedly_from_interface_class_is_interface_inheritance(self):
        #--------------------------------Protected Inheritance-------------------------------------#
        self.assertEqual(self.inheritanceData[2].Parents[0].className, 'A')
        self.assertEqual(self.inheritanceData[2].derivedclassName, 'D')
        self.assertEqual(self.inheritanceData[2].Parents[0].is_interface(), True)
        self.assertEqual(self.inheritanceData[2].typeofinheritance, 'Interface Inheritance')
        
class Single_Abstract_Inheritace_Tests(unittest.TestCase):
    inheritanceData = InheritancesData('__mytests_\\Single_inheritance\\Single_Abstract_inheritance.cpp')
#--------------------------------------------THE BASE CLASS IS ABSTRACT CLASS--------------------------------------------------#
    def test_if_derived_class_inherit_publicly_from_Abstract_class_is_interface_inheritance(self):
        #--------------------------------Public Inheritance-------------------------------------#
        self.assertEqual(self.inheritanceData[0].Parents[0].className, 'A')
        self.assertEqual(self.inheritanceData[0].derivedclassName, 'B')
        self.assertEqual(self.inheritanceData[0].Parents[0].is_interface(), True)
        self.assertEqual(self.inheritanceData[0].typeofinheritance, 'Implementation Inheritance')
        #-------------------------------Private Inheritance-------------------------------------#
    def test_if_derived_class_inherit_privately_from_Abstract_class_is_interface_inheritance(self):
        #--------------------------------Private Inheritance-------------------------------------#
        self.assertEqual(self.inheritanceData[1].Parents[0].className, 'A')
        self.assertEqual(self.inheritanceData[1].derivedclassName, 'C')
        self.assertEqual(self.inheritanceData[1].Parents[0].is_interface(), True)
        self.assertEqual(self.inheritanceData[1].typeofinheritance, 'Implementation Inheritance')
    def test_if_derived_class_inherit_protectedly_from_Abstract_class_is_interface_inheritance(self):
        #--------------------------------Protected Inheritance-------------------------------------#
        self.assertEqual(self.inheritanceData[2].Parents[0].className, 'A')
        self.assertEqual(self.inheritanceData[2].derivedclassName, 'D')
        self.assertEqual(self.inheritanceData[2].Parents[0].is_interface(), True)
        self.assertEqual(self.inheritanceData[2].typeofinheritance, 'Implementation Inheritance')
        
class Single_Concrete_Inheritace_Tests(unittest.TestCase):
    inheritanceData = InheritancesData('__mytests_\\Single_inheritance\\Single_Concrete_inheritance.cpp')
#--------------------------------------------THE BASE CLASS IS CONCRETE CLASS--------------------------------------------------#
    def test_if_derived_class_inherit_publicly_from_Concrete_class_is_interface_inheritance(self):
        #--------------------------------Public Inheritance-------------------------------------#
        self.assertEqual(self.inheritanceData[0].Parents[0].className, 'A')
        self.assertEqual(self.inheritanceData[0].derivedclassName, 'B')
        self.assertEqual(self.inheritanceData[0].Parents[0].is_Concrete(), True)
        self.assertEqual(self.inheritanceData[0].typeofinheritance, 'Implementation Inheritance')
        #-------------------------------Private Inheritance-------------------------------------#
    def test_if_derived_class_inherit_privately_from_Concrete_class_is_interface_inheritance(self):
        #--------------------------------Private Inheritance-------------------------------------#
        self.assertEqual(self.inheritanceData[1].Parents[0].className, 'A')
        self.assertEqual(self.inheritanceData[1].derivedclassName, 'C')
        self.assertEqual(self.inheritanceData[1].Parents[0].is_Concrete(), True)
        self.assertEqual(self.inheritanceData[1].typeofinheritance, 'Implementation Inheritance')
    def test_if_derived_class_inherit_protectedly_from_Concrete_class_is_interface_inheritance(self):
        #--------------------------------Protected Inheritance-------------------------------------#
        self.assertEqual(self.inheritanceData[2].Parents[0].className, 'A')
        self.assertEqual(self.inheritanceData[2].derivedclassName, 'D')
        self.assertEqual(self.inheritanceData[2].Parents[0].is_Concrete(), True)
        self.assertEqual(self.inheritanceData[2].typeofinheritance, 'Implementation Inheritance')
#Same For Public, Private AND PROTECTED
#--------------Virtual functions can be overriden from everywhere irrespective of access specifiers--------------------------#
class Single_Inheritace_Pure_Virtual_Override_Tests(unittest.TestCase):
    inheritanceData = InheritancesData('__mytests_\\Single_inheritance\\Derived_class_type\\Single_Overriding.cpp')
    def test_the_derived_class_functions_with_same_signature_as_the_pure_virtual_overrides_them(self):
        
        OverridenFunction = ['void publicpuremethodA1 (int)', 'void privatepuremethodA2 (int, int)', 'void protectedpuremethodA1 ()']
        self.assertEqual(self.inheritanceData[0].derivedclassName, 'B')
        self.assertEqual(self.inheritanceData[0].Parents[0].className, 'A')
        self.assertEqual(self.inheritanceData[0].overridenfunctions, OverridenFunction )
    def test_the_derived_class_functions_with_different_signature_as_the_pure_virtual_doesnot_overrides_them(self):
        OverridenFunction = []
        self.assertEqual(self.inheritanceData[1].derivedclassName, 'C')
        self.assertEqual(self.inheritanceData[1].Parents[0].className, 'A')
        self.assertEqual(self.inheritanceData[1].overridenfunctions, OverridenFunction )
#-----------------------------Virtual functions can be overriden irrespective of access specifiers-------------------#
class Single_Inheritace_Virtual_funtion_Override_Tests(unittest.TestCase):
    inheritanceData = InheritancesData('__mytests_\\Single_inheritance\\Derived_class_type\\Single_Overriding.cpp')
    def test_the_derived_class_functions_with_same_signature_as_the_Base_virtual_overrides_them(self):
        OverridenFunction = ['void publicpuremethodA2 (int)', 'void publicvirtualmethodA2 ()', 'void privatepuremethodA2 (int, int)']
        self.assertEqual(self.inheritanceData[2].derivedclassName, 'B2')
        self.assertEqual(self.inheritanceData[2].Parents[0].className, 'A2')
        self.assertEqual(self.inheritanceData[2].overridenfunctions, OverridenFunction )
    def test_the_derived_class_functions_with_different_signature_as_the_Base_virtual_doesnot_overrides_them(self):
        OverridenFunction = []
        self.assertEqual(self.inheritanceData[3].derivedclassName, 'C2')
        self.assertEqual(self.inheritanceData[3].Parents[0].className, 'A2')
        self.assertEqual(self.inheritanceData[3].overridenfunctions, OverridenFunction )
class Single_Inheritance_Derived_class_Type_Tests(unittest.TestCase):
    inheritanceData = InheritancesData('__mytests_\\Single_inheritance\\Derived_class_type\\Single_derived_class_type.cpp')
    def test_derived_class_is_concrete_class_if_it_overrides_all_base_class_pure_virtual_functions(self):
        self.assertEqual(self.inheritanceData[0].TypeOfClass, 'Concrete Class')
    def test_derived_class_become_abstract_class_if_it_doesnot_override_all_base_class_pure_virtual_functions(self):
        self.assertEqual(self.inheritanceData[1].TypeOfClass, 'Abstract Class')
    def test_derived_class_is_interface_class_if_it_doesnot_override_base_class_add_pure_virtual_functions(self):
        self.assertEqual(self.inheritanceData[2].TypeOfClass, 'Interface Class')
    def test_derived_class_is_abstract_class_if_it_overrides_all_base_class_pure_virtual_functions_and_adda_pure_virtual_functions(self):
        self.assertEqual(self.inheritanceData[3].TypeOfClass, 'Abstract Class')
     #----------------------------------------Multiple inheritance------------------------------------------#
# class Multilevel_inheritance_Tests(unittest.TestCase):
#-------------------------------------------------------------------------
class Multiple_inheritance_Tests(unittest.TestCase):
    inheritanceData = InheritancesData('__mytests_\\Multiple_inheritance\\multiple_inheritance.cpp')
    def test_methods_are_inherited_correctly_for_public_and_public(self):
        PublicMethods = {'Addedpurevirtualfunctions': ['void derivedpublicpuremethod ()'],
                         'Addedvirtualfunctions': ['void derivedpublicvirtualmethod ()'],
                         'Addednormalfunctions': ['void derivedpublicnormalmethod ()'],
                         'inherited_pure_virtual': ['void basepublicpuremethodA ()', 'void basepublicpuremethodB ()'],
                         'inherited_virtual': ['void basepublicvirtualmethodA ()', 'void basepublicvirtualmethodB ()'],
                         'inherited_normal': ['void basepublicnormalmethodA ()', 'void basepublicnormalmethodB ()']}
        PrivateMethods = {'Addedpurevirtualfunctions': ['void derivedprivatepuremethod ()'],
                          'Addedvirtualfunctions': ['void derivedprivatevirtualmethod ()'],
                          'Addednormalfunctions': ['void derivedprivatenormalmethod ()'],
                          'inherited_pure_virtual': ['void baseprivatepuremethodA ()', 'void baseprivatepuremethodB ()'],
                          'inherited_virtual': ['void baseprivatevirtualmethodA ()', 'void baseprivatevirtualmethodB ()'],
                          'inherited_normal': []}
        ProtectedMethods = {'Addedpurevirtualfunctions': ['void derivedprotectedpuremethod ()'],
                            'Addedvirtualfunctions': ['void derivedprotectedvirtualmethod ()'],
                            'Addednormalfunctions': ['void derivedprotectednormalmethod ()'],
                            'inherited_pure_virtual': ['void baseprotectedpuremethodA ()', 'void baseprotectedpuremethodB ()'],
                            'inherited_virtual': ['void baseprotectedvirtualmethodA ()', 'void baseprotectedvirtualmethodB ()'],
                            'inherited_normal': ['void baseprotectednormalmethodA ()', 'void baseprotectednormalmethodB ()']}
        self.assertDictEqual(self.inheritanceData[0].PublicMethods, PublicMethods)
        self.assertDictEqual(self.inheritanceData[0].PrivateMethods, PrivateMethods)
        self.assertDictEqual(self.inheritanceData[0].ProtectedMethods, ProtectedMethods)
    def test_methods_are_inherited_are_inherited_correctly_for_public_and_private_multiple_inheritance(self):
        PublicMethods = {'Addedpurevirtualfunctions': ['void derivedpublicpuremethod ()'],
                         'Addedvirtualfunctions': ['void derivedpublicvirtualmethod ()'],
                         'Addednormalfunctions': ['void derivedpublicnormalmethod ()'],
                         'inherited_pure_virtual': ['void basepublicpuremethodA ()'],
                         'inherited_virtual': ['void basepublicvirtualmethodA ()'],
                         'inherited_normal': ['void basepublicnormalmethodA ()']}
        PrivateMethods = {'Addedpurevirtualfunctions': ['void derivedprivatepuremethod ()'],
                          'Addedvirtualfunctions': ['void derivedprivatevirtualmethod ()'],
                          'Addednormalfunctions': ['void derivedprivatenormalmethod ()'],
                          'inherited_pure_virtual': ['void baseprivatepuremethodA ()', 'void basepublicpuremethodB ()', 'void baseprivatepuremethodB ()', 'void baseprotectedpuremethodB ()'],
                          'inherited_virtual': ['void baseprivatevirtualmethodA ()', 'void basepublicvirtualmethodB ()', 'void baseprivatevirtualmethodB ()', 'void baseprotectedvirtualmethodB ()'],
                          'inherited_normal': ['void basepublicnormalmethodB ()', 'void baseprotectednormalmethodB ()']}
        ProtectedMethods = {'Addedpurevirtualfunctions': ['void derivedprotectedpuremethod ()'],
                            'Addedvirtualfunctions': ['void derivedprotectedvirtualmethod ()'],
                            'Addednormalfunctions': ['void derivedprotectednormalmethod ()'],
                            'inherited_pure_virtual': ['void baseprotectedpuremethodA ()'],
                            'inherited_virtual': ['void baseprotectedvirtualmethodA ()'],
                            'inherited_normal': ['void baseprotectednormalmethodA ()']}
        self.assertDictEqual(self.inheritanceData[1].PublicMethods, PublicMethods)
        self.assertDictEqual(self.inheritanceData[1].PrivateMethods, PrivateMethods)
        self.assertDictEqual(self.inheritanceData[1].ProtectedMethods, ProtectedMethods)
    def test_if_methods_are_combinely_inherited_correctly_for_public_and_protected_inheritance(self):
        PublicMethods = {'Addedpurevirtualfunctions': ['void derivedpublicpuremethod ()'],
                         'Addedvirtualfunctions': ['void derivedpublicvirtualmethod ()'],
                         'Addednormalfunctions': ['void derivedpublicnormalmethod ()'],
                         'inherited_pure_virtual': ['void basepublicpuremethodA ()'],
                         'inherited_virtual': ['void basepublicvirtualmethodA ()'],
                         'inherited_normal': ['void basepublicnormalmethodA ()']}
        PrivateMethods = {'Addedpurevirtualfunctions': ['void derivedprivatepuremethod ()'],
                          'Addedvirtualfunctions': ['void derivedprivatevirtualmethod ()'],
                          'Addednormalfunctions': ['void derivedprivatenormalmethod ()'],
                          'inherited_pure_virtual': ['void baseprivatepuremethodA ()', 'void baseprivatepuremethodB ()'],
                          'inherited_virtual': ['void baseprivatevirtualmethodA ()', 'void baseprivatevirtualmethodB ()'],
                          'inherited_normal': []}
        ProtectedMethods = {'Addedpurevirtualfunctions': ['void derivedprotectedpuremethod ()'],
                            'Addedvirtualfunctions': ['void derivedprotectedvirtualmethod ()'],
                            'Addednormalfunctions': ['void derivedprotectednormalmethod ()'],
                            'inherited_pure_virtual': ['void baseprotectedpuremethodA ()', 'void basepublicpuremethodB ()', 'void baseprotectedpuremethodB ()'],
                            'inherited_virtual': ['void baseprotectedvirtualmethodA ()', 'void basepublicvirtualmethodB ()', 'void baseprotectedvirtualmethodB ()'],
                            'inherited_normal': ['void baseprotectednormalmethodA ()', 'void basepublicnormalmethodB ()', 'void baseprotectednormalmethodB ()']}
        self.assertDictEqual(self.inheritanceData[2].PublicMethods, PublicMethods)
        self.assertDictEqual(self.inheritanceData[2].PrivateMethods, PrivateMethods)
        self.assertDictEqual(self.inheritanceData[2].ProtectedMethods, ProtectedMethods)
    #-----------------The Algorithm Uses Inherited Methods to evalaute(type of class, type of inheritance), therefore it will work for multiple inheritance-----------#
class Inheritance_Hierachy_Level_Tests(unittest.TestCase):
    def test_if_the_correct_hierarchy_level_are_computed_for_hierachy_with_single_root(self):
        inheritancehierachies = getinheritanceHierachies('__mytests_\\Inheritance_Hierachy\\inheritance_hierachy_Level.cpp')
        Hierarchy = {'G': 0, 'B': 1, 'E': 1, 'A': 2, 'D': 2, 'F': 2}
        self.assertDictEqual(inheritancehierachies[0],Hierarchy)
    
if __name__ == '__main__':
    unittest.main()