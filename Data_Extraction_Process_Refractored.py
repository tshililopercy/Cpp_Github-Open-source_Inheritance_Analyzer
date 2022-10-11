import clang.cindex
import os
import fnmatch
from AnalysingProject import *

idx = clang.cindex.Index.create()

def extractClassData(cursor, classinfo, project):
    if cursor.kind == clang.cindex.CursorKind.CXX_BASE_SPECIFIER:
        for baseClass in cursor.get_children():
            if baseClass.kind == clang.cindex.CursorKind.TYPE_REF:
               Parent = {}
               inheritanceType = cursor.access_specifier
               Parent[baseClass.type.spelling] = inheritanceType
               classinfo.Baseclasses.append(project.getcppClass(baseClass.type.spelling))
    elif cursor.kind == clang.cindex.CursorKind.CXX_METHOD:
            overridePresent = False
            for child in cursor.get_children():
                if child.kind == clang.cindex.CursorKind.CXX_OVERRIDE_ATTR:
                      classinfo.overridenfunctions += 1
                      overridePresent = True
            if overridePresent == False:
             if cursor.is_pure_virtual_method():
                     classinfo.purevirtualfunctions += 1
             elif cursor.is_virtual_method():
                     classinfo.virtualfunctions += 1
             else:
                     classinfo.normalfunctions += 1
    project.cppClasses[classinfo.className] = classinfo

def extractClass(cursor, project):
    
    # The full name of class is stored
    classinfo = cppClass()
    classinfo.className = cursor.type.spelling 
    
    for children in cursor.get_children():
        #Extracting Class Members (Data and methods declaration)
        extractClassData(children, classinfo, project)

def traverse_AST(cursor, project): # Transerving The Abstract Tree
    #get cursors that represents classes 
    if cursor.kind == clang.cindex.CursorKind.CLASS_DECL:
        extractClass(cursor, project)
    for child in cursor.get_children():
        traverse_AST(child, project)
        
# Searches The repository and return cpp files path
def FindRepoFiles(cppExtensions):
   cppFiles = []
   #Reading Project in Repository Folder
   for root, dirs, files in os.walk('../Repository'):
        for extension in cppExtensions:
            for filename in fnmatch.filter(files, extension):
                 cppFiles.append(os.path.join(root, filename))
   return cppFiles

def parseTranslationUnit(file_path, project):  
    tu = idx.parse(path = file_path, args=None,  
                unsaved_files=None,  options=0)
    traverse_AST(tu.cursor, project)

def AnalyseRepository():
    project = ProjectData()
    cppExtensions = ['*.cpp', '*.cxx', '*.c', '*.cc']
    RepositoryFiles = FindRepoFiles(cppExtensions)
    for file_path in RepositoryFiles:
        parseTranslationUnit("main.cpp", project)
    #shutil.rmtree("../Repository")
    #File Must be deleted After Extraction to save Memory
    #Return Inheritance data 
    return project.computeInheritanceData()