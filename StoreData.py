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
            self.width_metrics = []
            
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
                            # print(InheritanceInfo['ClassName'])

                    DepthData["Inheritances"] = InheritancesData
                    hieracydata.DepthsInformation.append(DepthData)
                    # print(Hierachy_Size)
                    # print(hieracydata.DepthsInformation[index]['Inheritances'])
                    # print(len(DepthData['Inheritances']))
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
            
    def widths_metrics(self, DIT_Max, hierachydata):
        widths = []
        width = 0
        for index in range(0, max(DIT_Max), 1):
            # print(hierachydata.DepthsInformation[index]['Inheritances'], '\n', 'HHHHHH')
            width = len(hierachydata.DepthsInformation[index]['Inheritances'])
            widths.append(width)
        return widths

    def hierachy_count_per_width(self, widths):
        total_hierachies = [] 
        width_sequence = []
        for width_val in range(1, max(widths)+1, 1):
            count=0
            width_sequence.append(width_val)
            for width_ in widths:
                if width_val == width_:
                    count += 1
            total_hierachies.append(count)    
        return width_sequence, total_hierachies

    def PrintingHierachyData(self):
        index = 0
        # DIT_Max - Depth of Inheritance Tree Maximum
        DIT_Max = [] # Stores all hierachy maximums
        depth_data = {}
        # BIT_Max - Breadth of Inheritance Tree Maximum
        BIT_Max = [] # Stores number of children maximums (NOC)
        width_data = {}
        
        for hierachydata in self.HierachiesData:
            DIT_Max.append(hierachydata.depth)
            # print(DIT_Max)
            print(hierachydata.DepthsInformation[index])
            widths = self.widths_metrics(DIT_Max, hierachydata)
            BIT_Max.append(max(widths))
        print(BIT_Max)

        width_, num_of_hierachy_per_width = self.hierachy_count_per_width(BIT_Max)
        depth_ , num_of_hierachy_per_depth = self.hierachy_count_per_depth(DIT_Max)

        depth_data['Depth '] = depth_
        depth_data['Number of Hierachies per depth'] = num_of_hierachy_per_depth
        self.depth_metrics.append(depth_data)

        width_data['Width'] = width_
        width_data['Number of Hierachies per width'] = num_of_hierachy_per_width
        self.width_metrics.append(width_data)
        
        self.StoreDataInFile()

    def StoreDataInFile(self):
        # Serializing json
        results_ = {}
        results_['Depth Metrics'] = self.depth_metrics
        results_['Width Metrics'] = self.width_metrics
        json_object = json.dumps(results_, indent=1)
        
        # Writing to sample.json
        with open("results.json", "w") as outfile:
            outfile.write(json_object)