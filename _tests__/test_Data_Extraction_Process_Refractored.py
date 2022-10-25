import unittest
import os.path

from AnalysingProject import ProjectData
import Data_Extraction_Process_Refractored

def getPath(file_path):
    cwd = os.getcwd() # get current working directory
    path = os.path.join(cwd, file_path) # path of the file being tested
    
    return path 

def obtainInheritanceData(file_path):
    source_path = getPath(file_path)
    # print(source_path)
    project = ProjectData()
    Data_Extraction_Process_Refractored.parseTranslationUnit(source_path, project)
    inheritanceData = project.computeInheritanceData()
    # print(inheritanceData)
    return inheritanceData

#-----------------------------------------------------------------------------------------------------------------------
#--------------------------------------------------IMPLEMENTATION IMHERITANCE-----------------------------------------
#---------------------------------------------BASE CLASS TESTS -------------------------------------------

class baseclass_test(unittest.TestCase):  
    def test_number_of_base_classes_is_1(self):
        inheritanceData = obtainInheritanceData('_tests__\main.cpp')
        baseClassData = inheritanceData[0].ParentClassNames
        # print(inheritanceData)
        self.assertEqual(len(baseClassData), 1)

    def test_base_class_has_no_pure_virtual_functions(self):
        inheritanceData = obtainInheritanceData('_tests__\main.cpp')
        baseClassData_pvf = inheritanceData[0].inherited_pure_virtual
        # print(baseClassData["purevirtualfunctions"])
        self.assertEqual(baseClassData_pvf,0)

    def test_base_class_has_one_virtual_functions(self):
        inheritanceData = obtainInheritanceData('_tests__\main.cpp')
        baseClassData_vf = inheritanceData[0].inherited_virtual
        # print(baseClassData["purevirtualfunctions"])
        self.assertNotEqual( baseClassData_vf,0)
        self.assertEqual( baseClassData_vf,1)

    def test_base_class_has_normal_functions(self):
        inheritanceData = obtainInheritanceData('_tests__\main.cpp')
        baseClassData_nf = inheritanceData[0].inherited_normal
        # print(baseClassData["purevirtualfunctions"])
        self.assertNotEqual(baseClassData_nf,0)
        self.assertEqual(baseClassData_nf,2)
    

#--------------------------------------------------- CHILD CLASS TESTS ----------------------------
# Testing individual files
class implementation_inheritance_test(unittest.TestCase):
    def test_only_one_type_of_inheritance_occurs(self):
        InheritanceData = obtainInheritanceData('_tests__\main.cpp')
        self.assertEqual(len(InheritanceData), 1)

    def test_if_implementation_inheritance(self):
        inheritanceData1 = obtainInheritanceData('_tests__\main.cpp')
        inheritanceType = inheritanceData1[0].typeofinheritance
        self.assertEqual(inheritanceType, 'Implementation Inheritance')

    def test_if_no_interface_inheritance(self):
        inheritanceData = obtainInheritanceData('_tests__\main.cpp')
        inheritanceType = inheritanceData[0].typeofinheritance
        self.assertNotEqual(inheritanceType, 'Interface Inheritance')

#----------------------------------- METHODS TESTS - IN CHILD CLASS ----------------------------------
class methods_type_test(unittest.TestCase):
    def test_number_of_additional_function_is_1(self):
        inheritanceData = obtainInheritanceData('_tests__\main.cpp')
        additionalFnc = inheritanceData[0].derivedAdditionalfunctions
        self.assertEqual(additionalFnc,1)

    def test_number_of_overriden_functions_is_0(self):
        inheritanceData = obtainInheritanceData('_tests__\main.cpp')
        additionalFnc = inheritanceData[0].overridenfunctions
        self.assertEqual(additionalFnc,0)


#-----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------INTERFACE IMHERITANCE-----------------------------------------
#---------------------------------------------BASE CLASS TESTS -------------------------------------------

class interf_baseclass_test(unittest.TestCase):  
    def test_number_of_interf_base_classes_is_1(self):
        inheritanceData = obtainInheritanceData('_tests__\interf_inheritance.cpp')
        baseClassData = inheritanceData[0].ParentClassNames
        # print(baseClassData)
        self.assertEqual(len(baseClassData), 1)

    def test_inter_base_class_has_no_pure_virtual_functions(self):
        inheritanceData = obtainInheritanceData('_tests__\interf_inheritance.cpp')
        baseClassData_pvf = inheritanceData[0].inherited_pure_virtual
        # print(baseClassData["purevirtualfunctions"])
        self.assertEqual(baseClassData_pvf,2)

    def test_base_class_has_one_virtual_functions(self):
        inheritanceData = obtainInheritanceData('_tests__\interf_inheritance.cpp')
        baseClassData_vf = inheritanceData[0].inherited_virtual
        # print(baseClassData["virtualfunctions"])
        # self.assertNotEqual(baseClassData["virtualfunctions"],0)
        self.assertEqual(baseClassData_vf,0)

    def test_base_class_has_normal_functions(self):
        inheritanceData = obtainInheritanceData('_tests__\interf_inheritance.cpp')
        baseClassData_nf = inheritanceData[0].inherited_normal
        # print(baseClassData["purevirtualfunctions"])
        # self.assertNotEqual(baseClassData["normalfunctions"],0)
        self.assertEqual(baseClassData_nf,0)

#---------------------------------------------CHILD CLASS TESTS -------------------------------------------
# Testing individual files
class interface_inheritance_test(unittest.TestCase):
    def test_only_one_type_of_inheritance_occurs_(self):
        InheritanceData = obtainInheritanceData('_tests__\interf_inheritance.cpp')
        self.assertEqual(len(InheritanceData), 1)

    def test_if_no_implementation_inheritance(self):
        inheritanceData1 = obtainInheritanceData('_tests__\interf_inheritance.cpp')
        inheritanceType = inheritanceData1[0].typeofinheritance
        self.assertNotEqual(inheritanceType, 'Implementation Inheritance')

    def test_if_interface_inheritance(self):
        inheritanceData = obtainInheritanceData('_tests__\interf_inheritance.cpp')
        inheritanceType = inheritanceData[0].typeofinheritance
        self.assertEqual(inheritanceType, 'Interface Inheritance')

#----------------------------------- METHODS TESTS - IN CHILD CLASS ----------------------------------
class methods_type_test(unittest.TestCase):
    def test_number_of_additional_function_is_1_(self):
        inheritanceData = obtainInheritanceData('_tests__\interf_inheritance.cpp')
        additionalFnc = inheritanceData[0].derivedAdditionalfunctions
        self.assertEqual(additionalFnc,2)

    def test_number_of_overriden_functions_is_0_(self):
        inheritanceData = obtainInheritanceData('_tests__\interf_inheritance.cpp')
        additionalFnc = inheritanceData[0].overridenfunctions
        self.assertEqual(additionalFnc,0)


# -----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------HYBRID INHERITANCE -----------------------------------------
#---------------------------------------------BASE CLASS TESTS -------------------------------------------

class hybrid_baseclass_test(unittest.TestCase):  
    def test_number_of_base_classes_is_1_for_inh1(self):
        inheritanceData = obtainInheritanceData('_tests__\hybrid_inheritance.cpp')
        baseClassData = inheritanceData[0].ParentClassNames
        self.assertEqual(len(baseClassData), 1)

    def test_number_of_base_classes_is_1_for_inh2(self):
        inheritanceData = obtainInheritanceData('_tests__\hybrid_inheritance.cpp')
        baseClassData = inheritanceData[1].ParentClassNames
        self.assertEqual(len(baseClassData), 1)

    def test_number_of_base_classes_is_1_for_inh3(self):
        inheritanceData = obtainInheritanceData('_tests__\hybrid_inheritance.cpp')
        baseClassData = inheritanceData[2].ParentClassNames
        self.assertEqual(len(baseClassData), 1)

    def test_number_of_base_classes_is_1_for_inh4(self):
        inheritanceData = obtainInheritanceData('_tests__\hybrid_inheritance.cpp')
        baseClassData = inheritanceData[3].ParentClassNames
        # print(baseClassData)
        self.assertEqual(len(baseClassData), 1)

    def test_inh2_and_inh3_have_same_base_class(self):
        inheritanceData = obtainInheritanceData('_tests__\hybrid_inheritance.cpp')
        baseClassData1 = inheritanceData[1].ParentClassNames
        baseClassData2 = inheritanceData[2].ParentClassNames
        self.assertEqual(baseClassData1, baseClassData2)

    def test_inh1_and_inh2_dont_have_same_base_class(self):
        inheritanceData = obtainInheritanceData('_tests__\hybrid_inheritance.cpp')
        baseClassData1 = inheritanceData[0].ParentClassNames
        baseClassData2 = inheritanceData[1].ParentClassNames
        self.assertNotEqual(baseClassData1, baseClassData2)

#---------------------------------------------CHILD CLASS TESTS -------------------------------------------
class inheritance_test(unittest.TestCase):
    def test_4_types_of_inheritance_occurs_(self):
        inheritanceData = obtainInheritanceData('_tests__\hybrid_inheritance.cpp')
        self.assertEqual(len(inheritanceData), 4)

    def test_if_child_with_only_pure_funcs_inherits_parent_with_only_pure_funcs_is_interface_inheritance(self):
        inheritanceData = obtainInheritanceData('_tests__\hybrid_inheritance.cpp')
        inheritanceType = inheritanceData[0].typeofinheritance
        self.assertEqual(inheritanceType, 'Interface Inheritance')

    def test_if_child_with_only_pure_funcs_inherits_parent_without_pure_funcs_is_implementation_inheritance(self):
        inheritanceData = obtainInheritanceData('_tests__\hybrid_inheritance.cpp')
        inheritanceType = inheritanceData[1].typeofinheritance
        self.assertEqual(inheritanceType, 'Implementation Inheritance')

    def test_if_child_without_pure_funcs_inherits_parent_without_pure_funcs_is_implementation_inheritance(self):
        inheritanceData = obtainInheritanceData('_tests__\hybrid_inheritance.cpp')
        inheritanceType = inheritanceData[2].typeofinheritance
        self.assertEqual(inheritanceType, 'Implementation Inheritance')

    def test_if_child_with_pure_funcs_inherits_parent_mixed_funcs_is_implementation_inheritance(self):
        inheritanceData = obtainInheritanceData('_tests__\hybrid_inheritance.cpp')
        inheritanceType = inheritanceData[3].typeofinheritance
        self.assertEqual(inheritanceType, 'Implementation Inheritance')


# -----------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------MULTIPLE INHERITANCE -----------------------------------------
#---------------------------------------------BASE CLASS TESTS -------------------------------------------
class multiple_baseclass_test(unittest.TestCase):  
    # Total of 7 instances of inheritance
    def test_if_inheritance_of_2_base_classes_is_detected(self):
        inheritanceData = obtainInheritanceData('_tests__\multiple_inheritance.cpp')
        baseClassData = inheritanceData[1].ParentClassNames
        self.assertEqual(len(baseClassData), 2)

    def test_if_inheritance_of_more_than_2_base_classes_is_detected(self):
        inheritanceData = obtainInheritanceData('_tests__\multiple_inheritance.cpp')
        baseClassData = inheritanceData[2].ParentClassNames
        self.assertEqual(len(baseClassData), 3)

#---------------------------------------------CHILD CLASS TESTS -------------------------------------------
class multiple_inheritance_test(unittest.TestCase):
    def test_7_types_of_inheritance_occurs_(self):
        inheritanceData = obtainInheritanceData('_tests__\multiple_inheritance.cpp')
        self.assertEqual(len(inheritanceData), 7)

    def test_if_child_with_only_pure_funcs_inherits_2_parents_with_only_pure_and_mixed_is_implementation_inheritance(self):
        inheritanceData = obtainInheritanceData('_tests__\multiple_inheritance.cpp')
        inheritanceType = inheritanceData[1].typeofinheritance
        self.assertEqual(inheritanceType, 'Implementation Inheritance')

    def test_if_child_with_only_pure_funcs_inherits_3_non_pure_funcs_is_implementation_inheritance(self):
        inheritanceData = obtainInheritanceData('_tests__\multiple_inheritance.cpp')
        inheritanceType = inheritanceData[2].typeofinheritance
        self.assertEqual(inheritanceType, 'Implementation Inheritance')

    def test_if_child_without_pure_funcs_inherits_2_non_pure_funcs_is_implementation_inheritance(self):
        inheritanceData = obtainInheritanceData('_tests__\multiple_inheritance.cpp')
        inheritanceType = inheritanceData[3].typeofinheritance
        self.assertEqual(inheritanceType, 'Implementation Inheritance')

    def test_if_child_without_pure_funcs_inherits_an_interface_inherited_class_is_interface_inheritance(self):
        inheritanceData = obtainInheritanceData('_tests__\multiple_inheritance.cpp')
        inheritanceType = inheritanceData[4].typeofinheritance
        self.assertEqual(inheritanceType, 'Interface Inheritance')

    def test_if_child_with_pure_funcs_inherits_an_interface_inherited_class_is_implementation_inheritance(self):
        inheritanceData = obtainInheritanceData('_tests__\multiple_inheritance.cpp')
        inheritanceType = inheritanceData[6].typeofinheritance
        self.assertEqual(inheritanceType, 'Interface Inheritance')
        
#----------------Final Detection Algorithm Test-----------------------#


if __name__ == '__main__':
    unittest.main()