import clang.cindex
import os
import fnmatch
from AnalysingProject import *
from StoreData import *
import ccsyspath
import configparser
config = configparser.ConfigParser()

class Extractor:
    def __init__(self):

        self.RepoNames = []
        config.read("Setup.ini")
        self.clang_path = "//usr//bin//clang++"
        self.libclangpath = ""
        
        if os.sys.platform == "linux" or os.sys.platform == "linux2":
            self.libclangpath = "/usr/lib/x86_64-linux-gnu/libclang-14.so"
            self.clang_system_include_paths = [path.decode('utf-8') for path in ccsyspath.system_include_paths(self.clang_path)]
        elif os.sys.platform == "win32":
            self.libclangpath = "C:\\msys64\\mingw64\\bin\\libclang.dll"
            self.clang_system_include_paths = []
        #Set the libclang_path to create the Index Entry point
        clang.cindex.Config.set_library_file(self.libclangpath)
        self.index = clang.cindex.Index.create()

    def getRepoNames(self):
        return self.RepoNames
        
    def extractClass(self, cursor, RepositoryFiles, excludeNamespaces : list, excludeFilepaths : list, project):  
    
        classinfo = cppClass(cursor)
        
        #Exclude classes, structs that don't have defined names
        if classinfo.isUnamed() or classinfo.isAnonymous():
            return
        
        if classinfo.location_file is None:
            return
        #Excluding the standard c++ classes
        for ns in excludeNamespaces:
            if re.search(ns, classinfo.className) != None:
                return
        
        abspath = os.path.abspath(classinfo.filename)
        for xp in excludeFilepaths:
            if abspath.find(xp) != -1:
                return
        #Checking if the class has already been stored
        if project.hasClass(classinfo.className):
            return
        #Process The Class Information Data
        classinfo.Process(cursor)
        
        #Store extracted class, struct or template
        project.addClass(classinfo)

    #Resursively transversing The Abstract Teree
    def traverse_AST(self,cursor,RepositoryFiles, excludeNamespaces, excludeFilepaths, project):
        try:
            if (cursor.kind == clang.cindex.CursorKind.CLASS_DECL
			       or cursor.kind == clang.cindex.CursorKind.STRUCT_DECL
			       or cursor.kind == clang.cindex.CursorKind.CLASS_TEMPLATE):
               self.extractClass(cursor,RepositoryFiles, excludeNamespaces, excludeFilepaths, project)
            for child in cursor.get_children():
                self.traverse_AST(child,RepositoryFiles, excludeNamespaces, excludeFilepaths, project)
        except Exception:
            pass
            
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
    #Parse source files using LibClang API Python binding
    def parseTranslationUnit(self, file_path : str,RepositoryFiles, clangArgs : list, includeDirs : list, excludeNamespaces : list, excludeFilepaths : list, project):  
        includeDirs = includeDirs + self.clang_system_include_paths
        clangArgs += ['-I' + includeDir for includeDir in includeDirs]
        tu = self.index .parse(path = file_path, args=clangArgs,  
                    unsaved_files=None,  options=0)
        self.traverse_AST(tu.cursor,RepositoryFiles, excludeNamespaces, excludeFilepaths, project)
    #Analyse a Repository
    def AnalyseRepository(self, RepoName):
        project = ProjectData()
        cppExtensions = ['*.hpp', '*.hxx', '*.h']

        excludeNamespace = ["std"]
        excludeFilepath = ["\vs2022","\vs2019","\vs2017","\vs2012","\Windows Kits", "\msys64"]

        clangArgs=['-x','c++']
        clangstandard = "c++17"
        clangArgs += [ f"-std={clangstandard.strip()}" ]
        clangdefines = "_IS_WINDOWS,_MBCS"
        clangDefines = [ f"-D{s.strip()}" for s in clangdefines.split(',') ]
        include = "../include,../Repository"
        includeDirs = include.split(",")
        includeDirs = [ s.strip() for s in includeDirs ]

        clangArgs += clangDefines

        RepositoryFiles = self.FindRepoFiles(RepoName,cppExtensions)
        
        RepoFiles = []
        
        #for files in RepositoryFiles:
            #RepoFiles.append(files)
        self.RepoNames.append({'name': RepoName, 'Status': 'Analysing'})
        for file_path in RepositoryFiles:
            print(file_path)
            self.parseTranslationUnit(file_path, RepoFiles, clangArgs, includeDirs, excludeNamespace, excludeFilepath, project)
        project.computestheclasses()
        self.RepoNames.append({'name': RepoName, 'Status': 'Done Analysing'})
        return project.computeInheritanceData(), project.organizeHierachy(), project.getdeclarations()