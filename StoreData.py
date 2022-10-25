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
            self.public_interface_metrics = []
            self.additional_methods_metrics = []
            self.overriden_methods_metrics = []
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

                    DepthData["Inheritances"] = InheritancesData
                    hieracydata.DepthsInformation.append(DepthData)
                    # print(hieracydata.DepthsInformation[index]['Inheritances'])
                hieracydata.depth = Hierarchy_Max_Depth
                hieracydata.size = Hierachy_Size
            self.HierachiesData.append(hieracydata)

        self.PrintingHierachyData()

    #--------------- depth metrics----------------
    def HierachyCountPerDepth(self, max_depths):
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
            
#---------------------width metrics---------------------------
    def WidthMetrics(self, DIT_Max, hierachydata):
        '''Finds number of children per hierachy'''
        widths = []
        for hierachyinfo in hierachydata.DepthsInformation:
            width = len(hierachyinfo['Inheritances'])
            widths.append(width)
        return widths

    def HierachyCountPerWidth(self, widths):
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

    # --------------------------public interface metrics----------------
    def PublicInterfaceMetrics(self, hierachydata):
        '''Returns public interfaces per hierachy'''
        public_interfaces = []
        for hierachyinfo in hierachydata.DepthsInformation:
            for inheritances in hierachyinfo['Inheritances']:
                public_interface = len(inheritances['Public Interface'])
                public_interfaces.append(public_interface)
        return public_interfaces

    def HierachyCountPerPublicInterface(self, total_public_interfaces):
        '''Compute the occurrence of hierachies for public interfaces found'''
        max_public_interface = max(total_public_interfaces)
        min_public_interface = min(total_public_interfaces) 
        total_hierachies = [] 
        public_interface_sequence = []

        for p_i_val in range(min_public_interface, max_public_interface+1, 1):
            count=0 # reset count for each hierachy
            public_interface_sequence.append(p_i_val)
            for p_i_ in total_public_interfaces:
                if p_i_val == p_i_:
                    count += 1
            total_hierachies.append(count)   
        return public_interface_sequence, total_hierachies

    #-------------------------methods metrics----------------------
    #------------------------------additional------------------
    def AdditionalMethodsMetrics(self, hierachydata):
        '''Returns additional methods for all hierachies'''
        # Names of added methods per depth for all hierachies
        additional_methods_names = []
        # Number of added methods per depth for all hierachies
        additional_methods_occurrence = []
        # keep track which added method belongs to which depth
        depth_per_method = []
        for hierachyinfo in hierachydata.DepthsInformation:
            for inheritances in hierachyinfo['Inheritances']:
                depth_ = hierachyinfo['Depth Number']
                depth_per_method.append(depth_)
                additional_method = inheritances['Added Methods']
                additional_methods_names.append(additional_method)
                occurrence = len(additional_method)
                additional_methods_occurrence.append(occurrence)
        print(additional_methods_occurrence, depth_per_method)
        return additional_methods_names, additional_methods_occurrence, depth_per_method

    #------------------------------overrriden------------------
    def OverridenMethodsMetrics(self, hierachydata):
        '''Returns public interfaces for all hierachies'''
        # Names of overriden methods per depth for all hierachies 
        overriden_methods = []
        # Number of overriden methods per depth for all hierachies
        overriden_methods_occurrence = []
        # keep track which pverriden method belongs to which depth
        depth_per_method = [] 
        for hierachyinfo in hierachydata.DepthsInformation:
            for inheritances in hierachyinfo['Inheritances']:
                depth_ = hierachyinfo['Depth Number']
                depth_per_method.append(depth_)
                overriden_method = inheritances['Overriden Methods']
                overriden_methods.append(overriden_method)
                occurrence = len(overriden_method)
                overriden_methods_occurrence.append(occurrence)
        print(overriden_methods_occurrence, depth_per_method)
        return overriden_methods, overriden_methods_occurrence, depth_per_method

    def groupedMethodsPerDepth(self, depth_count, methods_iter, max_depths):   
        methods_type=[]
        # print(methods_iter)
        for depth_val in range(1, max(max_depths)+1, 1):
            count = 0
            if depth_val == 1:
                i=depth_val-1
                i_max = depth_count[depth_val-1]+i
            else:
                i=i_max
                i_max += depth_count[depth_val-1]
            for index in range(i,i_max, 1):
                count += methods_iter[index]
                i+=1
            methods_type.append(count)
        return methods_type

    def MethodsPerDepth(self, max_depths, additional_methods_occurrence, overriden_methods_occurrence, depth_per_method):
        depth_count = []

        # number of counted methods in each depth
        for depth_val in range(1, max(max_depths)+1, 1):
            count=0
            for depth_ in depth_per_method:
                if depth_val == depth_:
                    count += 1
            depth_count.append(count)

        #Group added functions by depth
        novel_methods =  self.groupedMethodsPerDepth(depth_count, additional_methods_occurrence, max_depths)
        print(novel_methods)
        overriden_methods = self.groupedMethodsPerDepth(depth_count, overriden_methods_occurrence, max_depths)
        print(overriden_methods)
        return novel_methods, overriden_methods
    
    def PrintingHierachyData(self):
        # DIT_Max - Depth of Inheritance Tree Maximum
        DIT_Max = [] # Stores depths per tree maximums
        depth_data = {}
        # BIT_Max - Breadth of Inheritance Tree Maximum
        BIT_Max = [] # Stores number of children maximums (NOC)
        width_data = {}
        total_public_interfaces = []
        public_interface_data = {}
        methods_data = {}

        for hierachydata in self.HierachiesData:
            DIT_Max.append(hierachydata.depth)
            widths = self.WidthMetrics(DIT_Max, hierachydata)
            BIT_Max.append(max(widths))
            total_public_interfaces = self.PublicInterfaceMetrics(hierachydata)
            added_methods, additional_methods_occurrence,  depth_per_method = self.AdditionalMethodsMetrics(hierachydata)
            overriden_methods, overriden_methods_occurrence,  depth_per_method = self.OverridenMethodsMetrics(hierachydata)

        width_, num_of_hierachy_per_width = self.HierachyCountPerWidth(BIT_Max)
        depth_ , num_of_hierachy_per_depth = self.HierachyCountPerDepth(DIT_Max)
        public_interface_, num_of_hierachy_per_public_interface = self.HierachyCountPerPublicInterface(total_public_interfaces)
        added_functions, overriden_functions = self.MethodsPerDepth(DIT_Max, additional_methods_occurrence, overriden_methods_occurrence, depth_per_method) #, overriden_functions

        depth_data['Depth '] = depth_
        depth_data['Number of hierachies per depth'] = num_of_hierachy_per_depth
        self.depth_metrics.append(depth_data)

        width_data['Width'] = width_
        width_data['Number of hierachies per width'] = num_of_hierachy_per_width
        self.width_metrics.append(width_data)

        public_interface_data['Public interface'] = public_interface_
        public_interface_data['Number of hierachies per public_interface'] = num_of_hierachy_per_public_interface
        self.public_interface_metrics.append(public_interface_data)
        
        methods_data['Novel methods'] = added_functions
        methods_data['Overriden methods'] = overriden_functions
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