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
        self.additional_methods = []
        self.depth_per_method_add= []
        self.overriden_methods = []
        self.methodNovelty = []
        
        
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
            self.public_interface = []
            self.public_interface_metrics = []
            self.methods_metrics = []
            
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
                            InheritanceInfo["Overriden Methods"] = inheritance.overridenfunctions
                            
                            InheritancesData.append(InheritanceInfo)
                            # print(InheritanceInfo["Public Interface"], len(InheritanceInfo["Public Interface"]))
                            self.public_interface.append(len(InheritanceInfo["Public Interface"]))
                            self.depth_per_method_add.append(DepthData["Depth Number"])
                            self.additional_methods.append(InheritanceInfo["Added Methods"])
                            self.overriden_methods.append(InheritanceInfo["Overriden Methods"])

                            # print(self.additional_methods, '\n')
                            self.overriden_methods.append(InheritanceInfo["Overriden Methods"])

                    DepthData["Inheritances"] = InheritancesData
                    hieracydata.DepthsInformation.append(DepthData)
                    # print(hieracydata.DepthsInformation[index]['Inheritances'])
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
        for index in range(0, max(DIT_Max), 1): # seach each depth
            # print(hierachydata.DepthsInformation[index]['Inheritances'], '\n', 'HHHHHH')
            width = len(hierachydata.DepthsInformation[index]['Inheritances'])
            widths.append(width)
        return widths

    def grouped_methods_per_depth(self, depth_count, methods_iter, max_depths, methods_type):   
        # methods_type=[]
        for depth_val in range(1, max(max_depths)+1, 1):
            count = 0
            if depth_val == 1:
                i=depth_val-1
                i_max = depth_count[depth_val-1]+i
            else:
                i=i_max
                i_max += depth_count[depth_val-1]
            for index in range(i,i_max, 1):
                count += methods_iter[i]
                i+=1
            methods_type.append(count)
        return methods_type

    def methods_per_depth(self, max_depths):
        added_meth = [] 
        depth_count = []
        novel_methods = []

        overriden_meth = [] 
        overriden_methods = []
        methods_type = []

        # Number of added methods per depth for all hierachies
        for index in range(0, len(self.additional_methods), 1):
            num_of_add_methods_ = len(self.additional_methods[index])
            added_meth.append(num_of_add_methods_)
        print(added_meth)

        # Number of added methods per depth for all hierachies
        for index in range(0, len(self.overriden_methods), 1):
            num_of_overriden_methods_ = len(self.overriden_methods[index])
            overriden_meth.append(num_of_overriden_methods_)
        # print(overriden_meth)

        # number of counted methods in each depth
        for depth_val in range(1, max(max_depths)+1, 1):
            count=0
            for depth_ in self.depth_per_method_add:
                if depth_val == depth_:
                    count += 1
            depth_count.append(count)
        # print(depth_count)


        #Group added functions by depth
        novel_methods =  self.grouped_methods_per_depth(depth_count, added_meth, max_depths, methods_type)
        # overriden_methods = self.grouped_methods_per_depth(depth_count, overriden_meth, max_depths, methods_type)
        return novel_methods #, overriden_methods

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

    def hierachy_count_per_public_interface(self):
        max_public_interface = max(self.public_interface)
        min_public_interface = min(self.public_interface) 
        total_hierachies = [] 
        public_interface_sequence = []

        for p_i_val in range(min_public_interface, max_public_interface+1, 1):
            count=0
            public_interface_sequence.append(p_i_val)
            for p_i_ in self.public_interface:
                if p_i_val == p_i_:
                    count += 1
            total_hierachies.append(count)    
        return public_interface_sequence, total_hierachies

    
    def PrintingHierachyData(self):
        index = 0
        # DIT_Max - Depth of Inheritance Tree Maximum
        DIT_Max = [] # Stores all hierachy maximums
        depth_data = {}
        # BIT_Max - Breadth of Inheritance Tree Maximum
        BIT_Max = [] # Stores number of children maximums (NOC)
        width_data = {}
        # public_interface = []
        public_interface_data = {}
        methods_data = {}

        for hierachydata in self.HierachiesData:
            DIT_Max.append(hierachydata.depth)
            # # print(DIT_Max)
            # print(hierachydata.DepthsInformation[index])
            widths = self.widths_metrics(DIT_Max, hierachydata)
            BIT_Max.append(max(widths))
            # public_interface.append(hierachydata.DepthsInformation[index])

        width_, num_of_hierachy_per_width = self.hierachy_count_per_width(BIT_Max)
        depth_ , num_of_hierachy_per_depth = self.hierachy_count_per_depth(DIT_Max)
        public_interface_, num_of_hierachy_per_public_interface = self.hierachy_count_per_public_interface()
        novel_functions = self.methods_per_depth(DIT_Max) #, overriden_functions

        depth_data['Depth '] = depth_
        depth_data['Number of hierachies per depth'] = num_of_hierachy_per_depth
        self.depth_metrics.append(depth_data)

        width_data['Width'] = width_
        width_data['Number of hierachies per width'] = num_of_hierachy_per_width
        self.width_metrics.append(width_data)

        public_interface_data['Public interface'] = public_interface_
        public_interface_data['Number of hierachies per public_interface'] = num_of_hierachy_per_public_interface
        self.public_interface_metrics.append(public_interface_data)
        
        methods_data['Novel methods'] = novel_functions
        # methods_data['Overriden methods'] = overriden_functions
        self.methods_metrics.append(methods_data)

        self.StoreDataInFile()

    def StoreDataInFile(self):
        # Serializing json
        results_ = {}
        results_['Depth Metrics'] = self.depth_metrics
        results_['Width Metrics'] = self.width_metrics
        results_['Public Interface Metrics'] = self.public_interface_metrics
        results_['Methods Metrics'] = self.methods_metrics
        json_object = json.dumps(results_, indent=2)
        
        # Writing to sample.json
        with open("results.json", "w") as outfile:
            outfile.write(json_object)