import json
class HierachyData:
    def __init__(self):
        self.depth = 0 # Maximum Hierachy level
        self.size = 0 # number of classes 
        self.DepthsInformation = [] # Dictionary for each depth {depth Number:,inheritances[]}

class ProjectDataStorage:
    def __init__(self, ProjectDataAndHierachyLevels):
        self.ProjectData, self.HierachiesLevels = ProjectDataAndHierachyLevels
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
                            InheritanceInfo["SubClasses"] = inheritance.ParentClassNames
                            InheritanceInfo["typeofinheritance"] = inheritance.typeofinheritance
                            InheritanceInfo["Public Interface"] = inheritance.PublicInterface
                            InheritanceInfo["Added Methods"] = inheritance.Novelmethods
                            InheritanceInfo["overridenfunctions"] = inheritance.overridenfunctions
                            
                            InheritancesData.append(InheritanceInfo)

                    DepthData["Inheritances"] = InheritancesData
                    hieracydata.DepthsInformation.append(DepthData)
                hieracydata.depth = Hierarchy_Max_Depth
                hieracydata.size = Hierachy_Size
            self.HierachiesData.append(hieracydata)

        self.PrintingHierachyData()
    
    def hierachy_count_per_depth(self, max_depths):
        total_hierachies = [] 
        depth_sequence = []
        
        for depth_val in range(1, max(max_depths)+1, 1):
            count=0
            depth_sequence.append(depth_val)
            for depth_ in max_depths:
                if depth_val == depth_:
                    count += 1
            total_hierachies.append(count)    

        return depth_sequence, total_hierachies
            
            
    def PrintingHierachyData(self):
        # DIT_Max - Depth of Inheritance Tree Maximum
        DIT_Max = [] # Stores all hierachy maximums
        depth_data = {}

        for hierachydata in self.HierachiesData:
            DIT_Max.append(hierachydata.depth)

        # print(DIT_Max)
        # print(hierachydata.DepthsInformation)
        depth_ , num_of_hierachy_per_depth = self.hierachy_count_per_depth(DIT_Max)
        depth_data['Depth '] = depth_
        depth_data['Number of Hierachies per depth'] = num_of_hierachy_per_depth
        self.depth_metrics.append(depth_data)
        
        self.StoreDataInFile()

    def StoreDataInFile(self):
        # Serializing json
        json_object = json.dumps(self.depth_metrics)
        
        # Writing to sample.json
        with open("results.json", "w") as outfile:
            outfile.write(json_object)