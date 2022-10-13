
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
            max_Depth = max(hierachylevels.values())
            max_size = len(hierachylevels)
            
            for depth in range(0,max_Depth + 1, 1):
                InheritancesData = []
                max_keys = [key for key, value in hierachylevels.items() if value == depth]
                if depth >=1:
                    DepthData = {}
                    for inheritance in self.ProjectData:
                        if inheritance.derivedclassName in max_keys:
                            InheritanceInfo = {}
                            DepthData["Depth Number"] = depth
                            InheritanceInfo["ClassName"] = inheritance.derivedclassName
                            InheritanceInfo["SubClasses"] = inheritance.ParentClassNames
                            InheritanceInfo["typeofinheritance"] = inheritance.typeofinheritance
                            InheritanceInfo["inherited_pure_virtual"] = inheritance.inherited_pure_virtual
                            InheritanceInfo["inherited_virtual"] = inheritance.inherited_virtual
                            InheritanceInfo["inherited_normal"] = inheritance.inherited_normal
                            InheritanceInfo["Additionalfunctions"] = inheritance.derivedAdditionalfunctions
                            InheritanceInfo["overridenfunctions"] = inheritance.overridenfunctions
                            
                            InheritancesData.append(InheritanceInfo)
                    
                    
                    DepthData["Inheritances"] = InheritancesData
                    hieracydata.DepthsInformation.append(DepthData)     
                hieracydata.depth = max_Depth
                hieracydata.size = max_size
            self.HierachiesData.append(hieracydata)
        self.PrintingHierachyData()
            
    def PrintingHierachyData(self):
        for hierachydata in self.HierachiesData:
            print(hierachydata.DepthsInformation)