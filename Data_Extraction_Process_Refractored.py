import clang.cindex
import os
import fnmatch
from AnalysingProject import *
from StoreData import *
clang.cindex.Config.set_library_file("C:\\msys64\\mingw64\\bin\\libclang.dll")
import ccsyspath

idx = clang.cindex.Index.create()

# args    = '-x c++ --std=c++17'.split()
# syspath = ccsyspath.system_include_paths('clang++')
# incargs = [ b'-I' + inc for inc in syspath ]
# args    = args + incargs

class Extractor:
    def __init__(self):
        self.RepoNames = []
    def getRepoNames(self):
        return self.RepoNames
    def ExtractDeclarations(self,cursor, project):
        project.Declarations.append(cursor.type.spelling)
        
    def BaseClassData(self, cursor, baseclassname, project):
        Parent = {}
        Parent['BaseClassInfo'] = project.getcppClass(baseclassname)
        if cursor.access_specifier == clang.cindex.AccessSpecifier.PUBLIC:
            Parent['inheritancetype'] = 'PUBLIC'
        elif cursor.access_specifier == clang.cindex.AccessSpecifier.PRIVATE:
            Parent['inheritancetype'] = 'PRIVATE'
        elif cursor.access_specifier == clang.cindex.AccessSpecifier.PROTECTED:
            Parent['inheritancetype'] = 'PROTECTED'
        return Parent
    
    def MethodsData(self, cursor, classinfo):
        returnType, argumentTypes = cursor.type.spelling.split(' ', 1)
                #Extract class Public Methods Signatures
        if cursor.access_specifier == clang.cindex.AccessSpecifier.PUBLIC:
            #Extract information
            if cursor.is_pure_virtual_method():
                classinfo.publicMethods["purevirtualfunctions"].append(returnType + ' ' + cursor.spelling + ' ' + argumentTypes)
            elif cursor.is_virtual_method():
                classinfo.publicMethods["virtualfunctions"].append(returnType + ' ' + cursor.spelling + ' ' + argumentTypes)
            else:
                classinfo.publicMethods["normalfunctions"].append(returnType + ' ' + cursor.spelling + ' ' + argumentTypes)
        #Extract class Private Methods Signatures
        elif cursor.access_specifier == clang.cindex.AccessSpecifier.PRIVATE:
            if cursor.is_pure_virtual_method():
                classinfo.privateMethods["purevirtualfunctions"].append(returnType + ' ' + cursor.spelling + ' ' + argumentTypes)
            elif cursor.is_virtual_method():
                classinfo.privateMethods["virtualfunctions"].append(returnType + ' ' + cursor.spelling + ' ' + argumentTypes)
            else:
                classinfo.privateMethods["normalfunctions"].append(returnType + ' ' + cursor.spelling + ' ' + argumentTypes)
        #Extract class Protected Methods Signatures
        elif cursor.access_specifier == clang.cindex.AccessSpecifier.PROTECTED:
            if cursor.is_pure_virtual_method():
                classinfo.protectedMethods["purevirtualfunctions"].append(returnType + ' ' + cursor.spelling + ' ' + argumentTypes)
            elif cursor.is_virtual_method():
                classinfo.protectedMethods["virtualfunctions"].append(returnType + ' ' + cursor.spelling + ' ' + argumentTypes)
            else:
                classinfo.protectedMethods["normalfunctions"].append(returnType + ' ' + cursor.spelling + ' ' + argumentTypes)

    def extractClassData(self, cursor, classinfo, project):
        if cursor.kind == clang.cindex.CursorKind.CXX_BASE_SPECIFIER:
            for baseClass in cursor.get_children():
                if baseClass.kind == clang.cindex.CursorKind.TYPE_REF:
                    if project.getcppClass(baseClass.type.spelling) == {}:
                        return
                    else:
                        classinfo.Baseclasses.append(self.BaseClassData(cursor, baseClass.type.spelling, project))
                elif baseClass.kind == clang.cindex.CursorKind.TEMPLATE_REF:
                    if project.getcppClass(baseClass.spelling) == {}:
                        return
                    else:
                        classinfo.Baseclasses.append(self.BaseClassData(cursor, baseClass.spelling, project))
        elif cursor.kind == clang.cindex.CursorKind.CXX_METHOD:
            try:
                self.MethodsData(cursor, classinfo)
            except:
                print("Invalid CXX_METHOD declaration! " + str(cursor.type.spelling))
                return
        elif cursor.kind == clang.cindex.CursorKind.FUNCTION_TEMPLATE:
            #Extract class Public Methods Signatures
            self.MethodsData(cursor, classinfo)
        project.cppClasses[classinfo.className] = classinfo
        
    def extractClass(self, cursor, project):  
        #The full name of class is stored
        classinfo = cppClass()
        if cursor.kind == clang.cindex.CursorKind.CLASS_TEMPLATE:
            classinfo.className = cursor.spelling
            print(classinfo.className)
        else:
            classinfo.className = cursor.type.spelling
            print(classinfo.className)
        
        for children in cursor.get_children():
            #Extracting Class Members (methods declaration of classes)
            self.extractClassData(children, classinfo, project)
    
    def traverse_AST(self,cursor, project): #Transerving The Abstract Tree Using Recursion
        if cursor.kind.is_declaration():
            if (cursor.kind != clang.cindex.CursorKind.CLASS_DECL and cursor.kind != clang.cindex.CursorKind.CXX_ACCESS_SPEC_DECL 
                and cursor.kind != clang.cindex.CursorKind.CXX_METHOD):
               #Extract All Other Declarations
               self.ExtractDeclarations(cursor, project)
        if (cursor.kind == clang.cindex.CursorKind.CLASS_DECL
			or cursor.kind == clang.cindex.CursorKind.STRUCT_DECL
			or cursor.kind == clang.cindex.CursorKind.CLASS_TEMPLATE):
            self.extractClass(cursor, project)
            
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
        tu = idx.parse(path = file_path, args=['-x','c++'],  
                    unsaved_files=None,  options=0)
        for node in tu.cursor.walk_preorder():
            if node.location.file is None:
                continue
            if node.location.file.name != file_path:
                continue
            if node.kind.is_declaration():
                self.traverse_AST(node, project)
    
    def AnalyseRepository(self, RepoName):
        project = ProjectData()
        cppExtensions = ['*.hpp', '*.hxx', '*.h']
        RepositoryFiles = self.FindRepoFiles(RepoName,cppExtensions)
        self.RepoNames.append({'name': RepoName, 'Status': 'Analysing'})
        for file_path in RepositoryFiles:
            self.parseTranslationUnit(file_path, project)
        print(project.cppClasses)
        self.RepoNames.append({'name': RepoName, 'Status': 'Done Analysing'})
        #Deleting Repo After Finishing with Analysis
        dir = ( "../Repository", RepoName)
        RepoToDelete = os.path.join(dir[0], dir[1])
        return project.computeInheritanceData(), project.organizeHierachy(), project.Declarations
    #analyseAllRepositories()
