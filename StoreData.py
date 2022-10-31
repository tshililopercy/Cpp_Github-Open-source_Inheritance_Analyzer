import json
import os
        
class ProjectDataStorage:
    def __init__(self, ProjectInheritanceData_HierachyLevels_And_Declarations):
        self.ProjectData, self.HierachiesLevels, self.Declarations = ProjectInheritanceData_HierachyLevels_And_Declarations
        self.ProjectHierachies = {}
        self.ProjectHierarchiesData = {}
        self.HierarchiesData = {}
        self.ClassesUsedInCode = []
        
    def ComputeHieracyData(self):
        for HierachyID, hierachylevels in enumerate(self.HierachiesLevels):
            HierarchyDepthsInformation = []
            Hierarchy_Max_Depth = max(hierachylevels.values())
            
            for depth in range(0,Hierarchy_Max_Depth + 1, 1):
                InheritancesData = []
                max_keys = [key for key, value in hierachylevels.items() if value == depth]
                if depth >=1:
                    DepthData = {}
                    for inheritance in self.ProjectData:
                        if inheritance.derivedclassName in max_keys:
                            InheritanceInfo = {}
                            InheritanceInfo["Depth"] = depth
                            InheritanceInfo["ClassName"] = inheritance.derivedclassName
                            InheritanceInfo["TypeOfClass"] = inheritance.TypeOfClass
                            InheritanceInfo["SubClasses"] = inheritance.Parents
                            InheritanceInfo["typeofinheritance"] = inheritance.typeofinheritance
                            InheritanceInfo["Public Interface"] = len(inheritance.PublicInterface)
                            InheritanceInfo["Added Methods"] = len(inheritance.Novelmethods)
                            InheritanceInfo["Overriden Methods"] = len(inheritance.overridenfunctions)
                            InheritancesData.append(InheritanceInfo)
                            
                    DepthData["Depth Number " + str(depth)] = InheritancesData
                    HierarchyDepthsInformation.append(DepthData)   
            self.HierarchiesData["Hierarchy " + str(HierachyID + 1)] = HierarchyDepthsInformation
            self.ClassesUsedInCode += self.DetermineClassesUsedInCode(hierachylevels)
        self.ProjectHierarchiesData["Hierarchies"] = self.HierarchiesData
        self.ProjectHierarchiesData["ClassesUsed"] = self.ClassesUsedInCode
        if os.path.getsize("HierachiesData.json") == 0: 
            #-------------------------Store First Project Hierarchies Data And Declaration--------------------#
            self.StoreHierachiesData(self.ProjectHierarchiesData)
        else:
            #-------------------------Store From Second Project Hierarchies Data And Declaration-------------------#
            self.write_json(self.ProjectHierarchiesData)
            
    def StoreHierachiesData(self,ProjectHierachiesData):
        ProjectDataObject = {}
        ProjectDataObject["Project " + '1'] = ProjectHierachiesData
        with open("HierachiesData.json", "w") as outfile:
            json.dump(ProjectDataObject, outfile, indent=4)

    def write_json(self, ProjectHierachiesData):
        print(len(ProjectHierachiesData))
        with open('HierachiesData.json','r+') as file:
          #First we load existing data into a dict.
            file_data = json.load(file)
        # Join new_data with file_data inside emp_details
            ProjectID = len(file_data) + 1
            ProjectObject = {}
            ProjectObject["Project " + str(ProjectID)] = ProjectHierachiesData
            file_data.update(ProjectObject)
        # convert back to json.
        with open('HierachiesData.json', 'w') as json_file:
            json.dump(file_data, json_file, indent=4)
    #Determines Hierarchy Members Used As Types In Client Code  
    def DetermineClassesUsedInCode(self, hierarchyLevels):
        usedClasses = []
        hierarchyClasses = hierarchyLevels.keys()
        for classname in hierarchyClasses:
            for declaration in self.Declarations:
                if classname in declaration:
                    if classname not in usedClasses:
                        usedClasses.append(classname)   
        return usedClasses
