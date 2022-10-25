import clang.cindex
import os
import fnmatch
from AnalysingProject import *
from git import rmtree
from StoreData import *

idx = clang.cindex.Index.create()

#Extract Method (including paramters) and variable declarations
def ExtractDeclarations(cursor, project):
    project.Declarations.append(cursor.type.spelling)
    print(project.Declarations)

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

def verbose(*args, **kwargs):
    '''filter predicate for show_ast: show all'''
    return True
def no_system_includes(cursor, level):
    '''filter predicate for show_ast: filter out verbose stuff from system include files'''
    return (level!= 1) or (cursor.location.file is not None and not cursor.location.file.name.startswith('/usr/include'))

# A function show(level, *args) would have been simpler but less fun
# and you'd need a separate parameter for the AST walkers if you want it to be exchangeable.
class Level(int):
    '''Represent currently visited level of a tree'''
    def show(self, *args):
        '''Print an indented line'''
        print ('\t'*self + ' '.join(map(str, args)))
    def __add__(self, inc):
        '''Increase level'''
        return Level(super(Level, self).__add__(inc))

def is_valid_type(t):
    '''Used to check if a cursor has a type'''
    return t.kind != clang.cindex.TypeKind.INVALID
    
def qualifiers(t):
    '''Set of qualifiers of a type'''
    q = set()
    if t.is_const_qualified(): q.add('const')
    if t.is_volatile_qualified(): q.add('volatile')
    if t.is_restrict_qualified(): q.add('restrict')
    return q

def show_type(t, level, title):
    '''Print type AST'''
    level.show(title, str(t.kind), ' '.join(qualifiers(t)))
    if is_valid_type(t.get_pointee()):
        show_type(t.get_pointee(), level+1, 'points to:')

def show_AST(cursor, filter_pred=verbose, level=Level()):
    '''Print cursor AST'''
    if filter_pred(cursor, level):
        level.show(cursor.kind, cursor.spelling, cursor.displayname, cursor.location)
        if is_valid_type(cursor.type):
            show_type(cursor.type, level+1, 'type:')
        for c in cursor.get_children():
            show_AST(c, filter_pred, level+1)

def parseTranslationUnit(file_path, project): 
    tu = idx.parse(path = file_path, args=['-x', 'c++'],  
                unsaved_files=None,  options=0)
    traverse_AST(tu.cursor, project)
    #show_AST(tu.cursor, no_system_includes)

def AnalyseRepository(RepoName):
    project = ProjectData()
    cppExtensions = ['*.hpp', '*.hxx', '*.h']
    #RepositoryFiles = FindRepoFiles(RepoName,cppExtensions)
    #for file_path in RepositoryFiles:
    parseTranslationUnit("test.cpp", project)
    #Deleting Repo Folder after extracting inheritance Data
    #rmtree('../Repository')
    #shutil.rmtree("../Repository")
    #File Must be deleted After Extraction to save Memory
    #Return Inheritance data 
    return project.computeInheritanceData(), project.organizeHierachy(), project.Declarations

def analyseAllRepositories():
    
    for name in os.listdir('../Repository'):
        projectdatastorage = ProjectDataStorage (AnalyseRepository(name), )
        projectdatastorage.ComputeHieracyData()
        
analyseAllRepositories()
