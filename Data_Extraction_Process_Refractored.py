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
    tu = idx.parse(path = file_path, args=None,  
                unsaved_files=None,  options=0)
    traverse_AST(tu.cursor, project)
    # show_AST(tu.cursor, no_system_includes)

def AnalyseRepository():
    project = ProjectData()
    cppExtensions = ['*.cpp', '*.cxx', '*.c', '*.cc']
    RepositoryFiles = FindRepoFiles(cppExtensions)
    for file_path in RepositoryFiles:
        parseTranslationUnit("mytestingMain.cpp", project)
    #Deleting Repo Folder after extracting inheritance Data
    #rmtree('../Repository')
    #shutil.rmtree("../Repository")
    #File Must be deleted After Extraction to save Memory
    #Return Inheritance data 
    return project.computeInheritanceData(), project.organizeHierachy()

projectdatastorage = ProjectDataStorage (AnalyseRepository())

projectdatastorage.ComputeHieracyData()