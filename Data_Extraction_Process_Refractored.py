import clang.cindex
import os
import fnmatch
from AnalysingProject import *
from git import rmtree
from StoreData import *
from Data_Compute import *

idx = clang.cindex.Index.create()

#Extract Method (including paramters) and variable declarations
def ExtractDeclarations(cursor, project):
    project.Declarations.append(cursor.type.spelling)
    #print(project.Declarations)

def extractClassData(cursor, classinfo, project):
    if cursor.kind == clang.cindex.CursorKind.CXX_BASE_SPECIFIER:
        for baseClass in cursor.get_children():
            if baseClass.kind == clang.cindex.CursorKind.TYPE_REF:
               Parent = {}
               if project.getcppClass(baseClass.type.spelling) == {}:
                   return
               else:
                   Parent['BaseClassInfo'] = project.getcppClass(baseClass.type.spelling)
               if cursor.access_specifier == clang.cindex.AccessSpecifier.PUBLIC:
                   Parent['inheritancetype'] = 'PUBLIC'
               elif cursor.access_specifier == clang.cindex.AccessSpecifier.PRIVATE:
                   Parent['inheritancetype'] = 'PRIVATE'
               elif cursor.access_specifier == clang.cindex.AccessSpecifier.PROTECTED:
                   Parent['inheritancetype'] = 'PROTECTED'
               classinfo.Baseclasses.append(Parent)
    elif cursor.kind == clang.cindex.CursorKind.CXX_METHOD:
        try:
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
                    classinfo.protectedMethods["purevirtualfunctions"].append(returnType + ' ' + cursor.spelling + ' ' + argumentTypes)
                elif cursor.is_virtual_method():
                    classinfo.protectedMethods["virtualfunctions"].append(returnType + ' ' + cursor.spelling + ' ' + argumentTypes)
                else:
                    classinfo.protectedMethods["normalfunctions"].append(returnType + ' ' + cursor.spelling + ' ' + argumentTypes)
        except:
            print("Invalid CXX_METHOD declaration! " + str(cursor.type.spelling))
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
    if cursor.kind.is_declaration():
        if (cursor.kind != clang.cindex.CursorKind.CLASS_DECL and cursor.kind != clang.cindex.CursorKind.CXX_ACCESS_SPEC_DECL 
            and cursor.kind != clang.cindex.CursorKind.CXX_METHOD):
           ExtractDeclarations(cursor, project)
    if cursor.kind == clang.cindex.CursorKind.CLASS_DECL:
        extractClass(cursor, project)
    for child in cursor.get_children():
        traverse_AST(child, project)
        
# Searches The repository and return cpp files path
def FindRepoFiles(RepoName, cppExtensions):
   cppFiles = []
   #Reading Project in Repository Folder
   dir = ( "../Repository", RepoName)
   Repositories = os.path.join(dir[0], dir[1])
   for root, dirs, files in os.walk(Repositories):
        for extension in cppExtensions:
            for filename in fnmatch.filter(files, extension):
                 cppFiles.append(os.path.join(root, filename))
   return cppFiles

def parseTranslationUnit(file_path, project): 
    # print(file_path) 
    tu = idx.parse(path = file_path, args=['-x', 'c++'],  
                unsaved_files=None,  options=0)
    traverse_AST(tu.cursor, project)

def AnalyseRepository(RepoName):
    project = ProjectData()
    cppExtensions = ['*.hpp', '*.hxx', '*.h']
    RepositoryFiles = FindRepoFiles(RepoName,cppExtensions)
    # print(RepositoryFiles)
    for file_path in RepositoryFiles:
        parseTranslationUnit(file_path, project)
    #Deleting Repo Folder after extracting inheritance Data
    #rmtree('../Repository')
    #shutil.rmtree("../Repository")
    #File Must be deleted After Extraction to save Memory
    #Return Inheritance data 
    return project.computeInheritanceData(), project.organizeHierachy(), project.Declarations

def analyseAllRepositories():
    #Deleting Data Available in HierachiesData.json, for new analysis
    open('HierachiesData.json', 'w').close()
    for name in os.listdir('../Repository'):
        projectdatastorage = ProjectDataStorage (AnalyseRepository(name))
        projectdatastorage.ComputeHieracyData()
    projectdatavisualize = ProjectDataVisualize()
    projectdatavisualize.PrintingHierachyData()

analyseAllRepositories()
