import json
import os

class HierachyData:
    def __init__(self):
        self.DepthsInformation = [] # Dictionary for each depth {depth Number:,inheritances[]}

class ProjectDataStorage:
    def __init__(self, ProjectInheritanceData_HierachyLevels_And_Declarations):
        self.ProjectData, self.HierachiesLevels, Declarations = ProjectInheritanceData_HierachyLevels_And_Declarations
        print(Declarations)
        print(self.HierachiesLevels)
        self.HierachiesData = []
        
    def ComputeHieracyData(self):
        for HierachyID, hierachylevels in enumerate(self.HierachiesLevels):
            hieracydata = HierachyData()
            #Getting Hierarchy maximum Depth 
            Hierarchy_Max_Depth = max(hierachylevels.values())
            #Number of Hierarchy members (Hierarchy Size)
            Hierachy_Size = len(hierachylevels)
            #count all number of methods in each hierachy Level
            self.depth_metrics = []
            self.width_metrics = []
            self.public_interface_metrics = []
            self.additional_methods_metrics = []
            self.overriden_methods_metrics = []

            self.methods_vs_depth_metrics = []
            self.methods_vs_class_metrics = []
            self.methods_vs_hierarchy_metrics = []
            
            for depth in range(0,Hierarchy_Max_Depth + 1, 1):
                InheritancesData = []
                max_keys = [key for key, value in hierachylevels.items() if value == depth]
                if depth >=1:
                    DepthData = {}
                    for inheritance in self.ProjectData:
                        if inheritance.derivedclassName in max_keys:
                            InheritanceInfo = {}
                            DepthData["Depth Number"] = depth
                            InheritanceInfo["ClassName"] = inheritance.derivedclassName
                            InheritanceInfo["TypeOfClass"] = inheritance.TypeOfClass
                            InheritanceInfo["SubClasses"] = inheritance.Parents
                            InheritanceInfo["typeofinheritance"] = inheritance.typeofinheritance
                            InheritanceInfo["Public Interface"] = len(inheritance.PublicInterface)
                            InheritanceInfo["Added Methods"] = len(inheritance.Novelmethods)
                            InheritanceInfo["Overriden Methods"] = len(inheritance.overridenfunctions)
                            InheritancesData.append(InheritanceInfo)

                    DepthData["Inheritances"] = InheritancesData
                    hieracydata.DepthsInformation.append(DepthData)
            if os.path.getsize("HierachiesData.json") == 0: 
                #-------------------------Store First Hierachy--------------------#
                self.StoreHierachiesData(hieracydata.DepthsInformation)
            else:
                #-------------------------Store Second Hierachy-------------------#
                self.write_json(hieracydata.DepthsInformation)

    def StoreHierachiesData(self,hierachy):
        print(len(hierachy))
        Object = {}
        Object['1'] = hierachy
        with open("HierachiesData.json", "w") as outfile:
            json.dump(Object, outfile, indent=4)

    def write_json(self, hierachydata):
        print(len(hierachydata))
        with open('HierachiesData.json','r+') as file:
          #First we load existing data into a dict.
            file_data = json.load(file)
        # Join new_data with file_data inside emp_details
            HierachyID = len(file_data) + 1
            HierachyObject = {}
            HierachyObject[HierachyID] = hierachydata
            file_data.update(HierachyObject)
        # convert back to json.
        with open('HierachiesData.json', 'w') as json_file:
            json.dump(file_data, json_file, indent=4)
