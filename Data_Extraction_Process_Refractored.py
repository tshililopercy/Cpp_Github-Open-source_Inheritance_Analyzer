import clang.cindex
import os
import fnmatch
from AnalysingProject import *
from git import rmtree
from StoreData import *

idx = clang.cindex.Index.create()

class Extractor:
    def __init__(self):
        self.RepoNames = []
    def getRepoNames(self):
        return self.RepoNames
    def ExtractDeclarations(self,cursor, project):
        project.Declarations.append(cursor.type.spelling)
    #print(project.Declarations)

    def extractClassData(self, cursor, classinfo, project):
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
                return
        project.cppClasses[classinfo.className] = classinfo
        
    def extractClass(self, cursor, project):
        
        # The full name of class is stored
        classinfo = cppClass()
        classinfo.className = cursor.type.spelling
        print(cursor.type.spelling)
        for children in cursor.get_children():
            #Extracting Class Members (Data and methods declaration)
            self.extractClassData(children, classinfo, project)
    
    def traverse_AST(self,cursor, project): # Transerving The Abstract Tree
        #get cursors that represents classes
        if cursor.kind.is_declaration():
            if (cursor.kind != clang.cindex.CursorKind.CLASS_DECL and cursor.kind != clang.cindex.CursorKind.CXX_ACCESS_SPEC_DECL 
                and cursor.kind != clang.cindex.CursorKind.CXX_METHOD):
               self.ExtractDeclarations(cursor, project)
        if cursor.kind == clang.cindex.CursorKind.CLASS_DECL:
            self.extractClass(cursor, project)
        for child in cursor.get_children():
            self.traverse_AST(child, project)
            
    # Searches The repository and return cpp files path
    def FindRepoFiles(self, RepoName, cppExtensions):
       cppFiles = []
       #Reading Project in Repository Folder
       dir = ( "../Repository", RepoName)
       Repositories = os.path.join(dir[0], dir[1])
       for root, dirs, files in os.walk(Repositories):
            for extension in cppExtensions:
                for filename in fnmatch.filter(files, extension):
                     cppFiles.append(os.path.join(root, filename))
       return cppFiles
    
    def parseTranslationUnit(self, file_path, project):  
        print(file_path)
        tu = idx.parse(path = file_path, args=['-x', 'c++'],  
                    unsaved_files=None,  options=0)
        self.traverse_AST(tu.cursor, project)
    
    def AnalyseRepository(self, RepoName):
        project = ProjectData()
        cppExtensions = ['*.hpp', '*.hxx', '*.h']
        RepositoryFiles = self.FindRepoFiles(RepoName,cppExtensions)
        self.RepoNames.append({'name': RepoName, 'Status': 'Analysing'})
        for file_path in RepositoryFiles:
            self.parseTranslationUnit(file_path, project)
        self.RepoNames.append({'name': RepoName, 'Status': 'Done Analysing'})
        #Deleting Repo After Finishing with Analysis
        dir = ( "../Repository", RepoName)
        RepoToDelete = os.path.join(dir[0], dir[1])
        #rmtree(RepoToDelete)
        #shutil.rmtree("../Repository")
        #File Must be deleted After Extraction to save Memory
        #Return Inheritance data 
        return project.computeInheritanceData(), project.organizeHierachy(), project.Declarations
        #rmtree("../Repository")
    #analyseAllRepositories()
