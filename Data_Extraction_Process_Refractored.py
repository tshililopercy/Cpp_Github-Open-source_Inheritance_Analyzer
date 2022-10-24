import clang.cindex
import os
import fnmatch
from AnalysingProject import *
from git import rmtree
from StoreData import *

idx = clang.cindex.Index.create()

def extractClassData(cursor, classinfo, project):
    if cursor.kind == clang.cindex.CursorKind.CXX_BASE_SPECIFIER:
        for baseClass in cursor.get_children():
            if baseClass.kind == clang.cindex.CursorKind.TYPE_REF:
               Parent = {}
               Parent['BaseClassInfo'] = project.getcppClass(baseClass.type.spelling)
               if cursor.access_specifier == clang.cindex.AccessSpecifier.PUBLIC:
                   Parent['inheritancetype'] = 'PUBLIC'
               elif cursor.access_specifier == clang.cindex.AccessSpecifier.PRIVATE:
                   Parent['inheritancetype'] = 'PRIVATE'
               classinfo.Baseclasses.append(Parent)
    elif cursor.kind == clang.cindex.CursorKind.CXX_METHOD:
        returnType, argumentTypes = cursor.type.spelling.split(' ', 1)
        if cursor.access_specifier == clang.cindex.AccessSpecifier.PUBLIC:
            if cursor.is_pure_virtual_method():
            #print(cursor.spelling)
                classinfo.publicMethods["purevirtualfunctions"].append(returnType + ' ' + cursor.spelling + ' ' + argumentTypes)
                #classinfo.purevirtualfunctions.append((returnType,cursor.spelling, argumentTypes))
            elif cursor.is_virtual_method():
                classinfo.publicMethods["virtualfunctions"].append(returnType + ' ' + cursor.spelling + ' ' + argumentTypes)
                #classinfo.virtualfunctions.append((returnType,cursor.spelling, argumentTypes))
            else:
                classinfo.publicMethods["normalfunctions"].append(returnType + ' ' + cursor.spelling + ' ' + argumentTypes)
                #classinfo.normalfunctions.append((returnType,cursor.spelling, argumentTypes))
        elif cursor.access_specifier == clang.cindex.AccessSpecifier.PRIVATE:
            if cursor.is_pure_virtual_method():
            #print(cursor.spelling)
                classinfo.privateMethods["purevirtualfunctions"].append(returnType + ' ' + cursor.spelling + ' ' + argumentTypes)
                #classinfo.purevirtualfunctions.append((returnType,cursor.spelling, argumentTypes))
            elif cursor.is_virtual_method():
                classinfo.privateMethods["virtualfunctions"].append(returnType + ' ' + cursor.spelling + ' ' + argumentTypes)
                #classinfo.virtualfunctions.append((returnType,cursor.spelling, argumentTypes))
            else:
                classinfo.privateMethods["normalfunctions"].append(returnType + ' ' + cursor.spelling + ' ' + argumentTypes)
                #classinfo.normalfunctions.append((returnType,cursor.spelling, argumentTypes))
        elif cursor.access_specifier == clang.cindex.AccessSpecifier.PROTECTED:
            if cursor.is_pure_virtual_method():
            #print(cursor.spelling)
                classinfo.purevirtualfunctions.append(returnType + ' ' + cursor.spelling + ' ' + argumentTypes)
            elif cursor.is_virtual_method():
                classinfo.virtualfunctions.append(returnType + ' ' + cursor.spelling + ' ' + argumentTypes)
            else:
                classinfo.normalfunctions.append(returnType + ' ' + cursor.spelling + ' ' + argumentTypes)
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
    tu = idx.parse(path = file_path, args=['-x', 'c++'],  
                unsaved_files=None,  options=0)
    traverse_AST(tu.cursor, project)
    #show_AST(tu.cursor, no_system_includes)

def AnalyseRepository():
    project = ProjectData()
    cppExtensions = ['*.hpp', '*.hxx', '*.h']
    RepositoryFiles = FindRepoFiles(cppExtensions)
    for file_path in RepositoryFiles:
        parseTranslationUnit(file_path, project)
    #Deleting Repo Folder after extracting inheritance Data
    #rmtree('../Repository')
    #shutil.rmtree("../Repository")
    #File Must be deleted After Extraction to save Memory
    #Return Inheritance data 
    return project.computeInheritanceData(), project.organizeHierachy()

projectdatastorage = ProjectDataStorage (AnalyseRepository())
projectdatastorage.ComputeHieracyData()