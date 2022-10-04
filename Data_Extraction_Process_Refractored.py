import clang.cindex
import os
import fnmatch
import GitHub_Search_And_Clone


idx = clang.cindex.Index.create()

def chkList(lst):
    if len(lst) == 0:
        return
    return (len(set(lst)) == 1 and lst[0] == 1)

def classProcessing(classCursors): # processing Class methods data memebers
    Class_and_Methods_type = {}
    for class_cursor in classCursors:
      methods_type = []
      for child in class_cursor.get_children():
       if child.kind == clang.cindex.CursorKind.CXX_METHOD:
          methods_type.append(child.is_pure_virtual_method()) 
      Class_and_Methods_type[class_cursor.type.spelling] = methods_type
    print(Class_and_Methods_type)
    return identify_class_type (Class_and_Methods_type)

def identify_class_type(Class_and_Methods_type): # Identify if a class is interface or Abstract
    for x in Class_and_Methods_type:
      if chkList(Class_and_Methods_type[x]) == True:
        Class_and_Methods_type[x] = "" # If all the class member fuctions are pure virtual 
      elif chkList(Class_and_Methods_type[x]) == False: Class_and_Methods_type[x] = "Abstract Class" #It is represent abstract and concrete class
    return Class_and_Methods_type
    

def checkinginheritance(lst):
    if len(lst) == 0:
        return
    return (len(set(lst)) == 1 and lst[0] == "")

def type_of_class (className, classTypes):
 return  classTypes[className]

def inheritedBaseClassTypes(class_And_BaseClass, classTypes):
  for availabale_class_Name_and_Base_Classes in class_And_BaseClass:
      Me = []
      for baseclass in class_And_BaseClass[availabale_class_Name_and_Base_Classes]:
        for ClassName_and_Methods_type in classTypes:
           if baseclass == ClassName_and_Methods_type:
              Me.append(type_of_class(ClassName_and_Methods_type, classTypes))
      class_And_BaseClass[availabale_class_Name_and_Base_Classes] = Me
  return class_And_BaseClass

def identify_inheritance_type(class_And_BaseClass, classTypes):
   #Types Of Inheritance
 class_And_BaseClassType = inheritedBaseClassTypes(class_And_BaseClass, classTypes)
 class_And_InheritanceType = {}
 for x in class_And_BaseClassType:
    if checkinginheritance(class_And_BaseClassType[x]) == True:
        class_And_InheritanceType[x] = "Interface Inheritance"
    elif checkinginheritance(class_And_BaseClassType[x]) == False: class_And_InheritanceType[x] = "Implementation Inheritance"
 return class_And_InheritanceType

def InheritanceProcessing(Classcursors, classTypes):
  class_And_BaseClass = {}
  for class_cursor in Classcursors:
    Base_Classes = []
    for child in class_cursor.get_children():
      if child.kind == clang.cindex.CursorKind.CXX_BASE_SPECIFIER:
          for baseClass in child.get_children():
            if baseClass.kind == clang.cindex.CursorKind.TYPE_REF:
                Base_Classes.append(baseClass.type.spelling)
            elif baseClass.kind == clang.cindex.CursorKind.TEMPLATE_REF:
                Base_Classes.append(baseClass.spelling)
    class_And_BaseClass[class_cursor.type.spelling] = Base_Classes
  print(class_And_BaseClass)
  return identify_inheritance_type(class_And_BaseClass, classTypes)
def traverse_AST(cursor,ClassNodes): # Transerving The Abstract Tree

    for child in cursor.get_children():
        traverse_AST(child, ClassNodes)
    if (cursor.kind == clang.cindex.CursorKind.CLASS_DECL or cursor.kind == clang.cindex.CursorKind.STRUCT_DECL or cursor.kind == clang.cindex.CursorKind.CLASS_TEMPLATE):
       # Check if we have a class, struct or template declaration.
       # Store all nodes pointing to the declarations in the ClassNode list
       ClassNodes.append(cursor) 
    print ('Found %s [line=%s, col=%s]' % (cursor.displayname, cursor.location.line, cursor.location.column), cursor.kind)

def parseTranslationUnit(file_path):
    tu = idx.parse(path = file_path, args=None,  
                unsaved_files=None,  options=0)
    sourceFileInheritanceObject = SourceFileInheritanceResults ()
    ClassNodes = []
    traverse_AST(tu.cursor, ClassNodes)
    ClassTypes = classProcessing(ClassNodes)
    class_And_InheritanceTypes = InheritanceProcessing(ClassNodes, ClassTypes)
    print(class_And_InheritanceTypes)
    for class_And_InheritanceType in class_And_InheritanceTypes:
        if class_And_InheritanceTypes[class_And_InheritanceType] == "Implementation Inheritance":
            sourceFileInheritanceObject.ImplementationInheritance += 1
        elif class_And_InheritanceTypes[class_And_InheritanceType] == "Interface Inheritance":
            sourceFileInheritanceObject.InterfaceInheritance += 1

    print("Number of implementation inheritance: ", sourceFileInheritanceObject.ImplementationInheritance)
    print("Number of interface inheritance: ", sourceFileInheritanceObject.InterfaceInheritance)
    return sourceFileInheritanceObject

# Searches The repository and return cpp files path
def FindRepoFiles(cppExtensions):
   cppFiles = []
   for root, dirs, files in os.walk('Repository'):
        for extension in cppExtensions:
            for filename in fnmatch.filter(files, extension):
                 cppFiles.append(os.path.join(root, filename))
   return cppFiles
def AnalyseRepository():
     cppExtensions = ['*.cpp', '*.cxx', '*.c', '*.cc']
     
class SourceFileInheritanceResults:
    def __init__(self):
        self.ImplementationInheritance = 0
        self.InterfaceInheritance = 0
cppExtensions = ['*.cpp', '*.cxx', '*.c', '*.cc']
print(FindRepoFiles(cppExtensions))