import matplotlib.pyplot as plt
import json

class ProjectDataVisualize:
    def __init__(self):
        self.HierarchiesData = []
        
    def read_json(self):
        with open('HierachiesData.json', 'r') as openfile:
            # Reading data from the storage json file 
            self.HierachiesData = json.load(openfile)
        # print(self.HierachiesData)
#----------------------------------Code To Go through every thing -------------------------#
        # for project in self.HierachiesData:
        #         for hierarachy in self.HierachiesData[project]['Hierarchies']:
        #             for index, depths in enumerate(self.HierachiesData[project]['Hierarchies'][hierarachy]):
        #                 for depth in depths:
        #                     print(len(depths[depth]))
        print(len(self.HierachiesData))

    #--------------- depth metrics----------------
    def DepthMetrics(self, hierachydata):
        '''Finds depths per hierachy'''
        depths = []
        depth = len(hierachydata)
        depths.append(depth)
        return depths
        
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
    def WidthMetrics(self, hierachydata):
        '''Finds number of children per hierachy'''
        widths = []
        for hierachyinfo in hierachydata:
            width = len(hierachyinfo['Inheritances'])
            widths.append(width)
        return widths

    def HierachyCountPerWidth(self, widths):
        total_hierachies = [] 
        width_sequence = []
        for width_val in range(0, max(widths)+1, 1):
            count=0
            width_sequence.append(width_val)
            for width_ in widths:
                if width_val == width_:
                    count += 1
            total_hierachies.append(count)    
        return width_sequence, total_hierachies

    # --------------------------public interface metrics----------------
    def PublicInterfaceMetrics(self, hierachydata):
        '''Returns public interfaces per class'''
        public_interfaces = []
        for hierachyinfo in hierachydata:
            for inheritances in hierachyinfo['Inheritances']:
                public_interface = inheritances['Public Interface']
                public_interfaces.append(public_interface)
        return public_interfaces

    def ClassesCountPerPublicInterface(self, total_public_interfaces):
        '''Compute the occurrence of classes for public interfaces found'''
        max_public_interface = max(total_public_interfaces)
        min_public_interface = min(total_public_interfaces) 
        total_classes = [] 
        public_interface_sequence = []

        for p_i_val in range(min_public_interface, max_public_interface+1, 1):
            count=0 # reset count for each class
            public_interface_sequence.append(p_i_val)
            for p_i_ in total_public_interfaces:
                if p_i_val == p_i_:
                    count += 1
            total_classes.append(count)   
        # print('PUBLIC INTERFACE', public_interface_sequence, total_classes)
        return public_interface_sequence, total_classes

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
        for hierachyinfo in hierachydata:
            for inheritances in hierachyinfo['Inheritances']:
                depth_ = len(hierachyinfo)
                depth_per_method.append(depth_)
                additional_method = inheritances['Added Methods']
                additional_methods_names.append(additional_method)
                additional_methods_occurrence.append(additional_method)
        return additional_methods_names, additional_methods_occurrence, depth_per_method

    #------------------------------overrriden------------------
    def OverridenMethodsMetrics(self, hierachydata):
        '''Returns overriden for all hierachies'''
        # Names of overriden methods per depth for all hierachies 
        overriden_methods = []
        # Number of overriden methods per depth for all hierachies
        overriden_methods_occurrence = []
        # keep track which pverriden method belongs to which depth
        depth_per_method = [] 
        for hierachyinfo in hierachydata:
            for inheritances in hierachyinfo['Inheritances']:
                depth_ = len(hierachyinfo)
                depth_per_method.append(depth_)
                overriden_method = inheritances['Overriden Methods']
                overriden_methods.append(overriden_method)
                overriden_methods_occurrence.append(overriden_method)
        return overriden_methods, overriden_methods_occurrence, depth_per_method

    def groupedMethodsPerDepth(self, depth_count, methods_iter, max_depths):   
        methods_type=[]
        depth_sequence = []
        methods_per_depth = {}
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
            depth_sequence.append(depth_val)
        methods_per_depth['depth'] = depth_sequence
        methods_per_depth['methods'] = methods_type
        return methods_per_depth

    def MethodsPerClass(self, methods_occurrence):
        total_classes = [] 
        method_sequence = []
        methods_per_classes_data = {}
        for method_val in range(0, max(methods_occurrence)+1, 1):
            count=0
            method_sequence.append(method_val)
            for method_ in methods_occurrence:
                if method_val == method_:
                    count += 1
            total_classes.append(count)   
        methods_per_classes_data['Method sequence'] = method_sequence
        methods_per_classes_data['Total Classes'] = total_classes

        return methods_per_classes_data

    def MethodsPerHierachy(self, methods_occurrence, ):
        total_hierachies = [] 
        method_sequence = []
        methods_per_hierachy_data = {}
        for method_val in range(0, max(methods_occurrence)+1, 1):
            count=0
            method_sequence.append(method_val)
            for method_ in methods_occurrence:
                if method_val == method_:
                    count += 1
            total_hierachies.append(count)   
        methods_per_hierachy_data['Method sequence'] = method_sequence
        methods_per_hierachy_data['Total Hierarchies'] = total_hierachies

        return methods_per_hierachy_data

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
        # print(novel_methods)
        overriden_methods = self.groupedMethodsPerDepth(depth_count, overriden_methods_occurrence, max_depths)
        # print(overriden_methods)
        return novel_methods, overriden_methods

   #-------------------------Class types metrics----------------------
    def ClassTypeMetrics(self, hierachydata):
        '''Returns Class types'''
        class_types = []
        abstract_class = []
        all_class_types = []
        count = 0
        for hierachyinfo in hierachydata:
            for inheritances in hierachyinfo['Inheritances']:
                class_type = inheritances['TypeOfClass']
                class_types.append(class_type)
                all_class_types.append(class_type)
                # print(class_type)
                if class_type == 'Abstract Class':
                    count += 1
                    abstract_class.append(count)
                else:
                    abstract_class.append(count)
                
                # include root hierachy memmbers
                for rootclassInfo in inheritances['SubClasses']:
                    # root classes have more infomation, i.e. name of rootclass, type of class and public interfaces
                    if len(rootclassInfo) > 2:
                        class_type_rootclass = rootclassInfo['TypeOfClass']
                        all_class_types.append(class_type_rootclass)
        return class_types, abstract_class, all_class_types

    def ClassTypesOccurrence(self, class_types, all_class_types):
        # for hierarchy members inside the hierarchy (i.e. from depth >1)
        class_type_data = []
        abstract = class_types.count('Abstract Class')
        concrete = class_types.count('Concrete Class')
        interface = class_types.count('Interface Class')

        # for all hierachy members including depth=0
        all_abstract = all_class_types.count('Abstract Class')
        all_concrete = all_class_types.count('Concrete Class')
        all_interface = all_class_types.count('Interface Class')

        all_class_types_data = [all_abstract, all_concrete, all_interface]
        class_type_data = [abstract, concrete, interface]
        return class_type_data, all_class_types_data

    #-------------------------Abstract Class metrics----------------------
    def HierachyCountPerAbstractClass(self, max_abstract_classes_per_hierarchy):
        total_hierachies = [] 
        abstract_class_sequence = []
        for abstract_class_val in range(0, max(max_abstract_classes_per_hierarchy)+1, 1):
            count=0
            abstract_class_sequence.append(abstract_class_val)
            for abstract_class_ in max_abstract_classes_per_hierarchy:
                if abstract_class_val == abstract_class_:
                    count += 1
            total_hierachies.append(count)    
        return abstract_class_sequence, total_hierachies

    def BreachOfDIP(self, hierachydata):
        dip_ = []
        Info = []
        # DIP = 0 (no DIP breach/ Abstract classes). DIP = 1 (direct breach of the DIP - abstract class inheriting from concrete class)
        for hierachyinfo in hierachydata:
            for inheritances in hierachyinfo['Inheritances']:
                class_type_childclass = inheritances['TypeOfClass']
                if class_type_childclass == 'Abstract Class':
                    childclass = inheritances['ClassName']
                    for parentclassInfo in inheritances['SubClasses']:
                        parentclassName = parentclassInfo['rootname']

                        class_type_parentclass = parentclassInfo['TypeOfClass']
                        Info.append(f'ClassName:{childclass} Type:{class_type_childclass}  ParentName:{parentclassName} Type:{class_type_parentclass}')
                        if class_type_parentclass == 'Concrete Class':
                            dip_.append(1)
                        else:
                            dip_.append(0)
                else:
                    Info.append(class_type_childclass)
                    dip_.append(0)     
        return dip_, Info
                    
    def HierarchyOutOfOrder(self, dip):
        total_hierachies = [] 
        dip_sequence = []
        for dip_val in range(0, max(dip)+1, 1):
            count=0
            dip_sequence.append(dip_val)
            for dip_ in dip:
                if dip_val == dip_:
                    count += 1
            total_hierachies.append(count)    
        return dip_sequence, total_hierachies

    def PrintingHierachyData(self):
        # Read hierarchy data for all repos
        self.read_json() 

        # DIT_Max - Depth of Inheritance Tree Maximum
        DIT_Max = [] # Stores depths per tree maximums

        # BIT_Max - Breadth of Inheritance Tree Maximum
        BIT_Max = [] # Stores number of children maximums (NOC)

        max_public_interfaces_per_class = []

        max_additional_methods_occurrence_per_hierarchy = []
        max_overriden_methods_occurrence_per_hierarchy = []

        novel_methods_class_occurrence_per_class = []
        overriden_methods_class_occurrence_per_class = []
        depth_per_method_data = []
        
        all_class_types_ = []
        class_types = []
        max_abstract_classes_per_hierarchy = []
        DIP_occurence_per_hierarchy = []
        dipS = []
        Info_ = []

        for hierachydata_index in self.HierachiesData:
            hierachydata = self.HierachiesData[hierachydata_index]
            # depth
            depths = self.DepthMetrics(hierachydata)
            DIT_Max.append(max(depths))
            # widths
            widths = self.WidthMetrics(hierachydata)
            BIT_Max.append(max(widths))
            # public interface
            total_public_interfaces = self.PublicInterfaceMetrics(hierachydata)
            max_public_interfaces_per_class += total_public_interfaces
            # novel methods
            added_methods, additional_methods_occurrence,  depth_per_method = self.AdditionalMethodsMetrics(hierachydata)
            novel_methods_class_occurrence_per_class += additional_methods_occurrence
            max_additional_methods_occurrence_per_hierarchy.append(max(additional_methods_occurrence))
            # # overriden methods
            overriden_methods, overriden_methods_occurrence,  depth_per_method = self.OverridenMethodsMetrics(hierachydata)
            overriden_methods_class_occurrence_per_class += overriden_methods_occurrence
            max_overriden_methods_occurrence_per_hierarchy.append(max(overriden_methods_occurrence))

            depth_per_method_data += depth_per_method
            # class types
            class_type, abstract_class, all_class_types = self.ClassTypeMetrics(hierachydata)
            class_types += class_type # for all hierarchies - types include abstract, concrete, and interface
            all_class_types_ += all_class_types
            max_abstract_classes_per_hierarchy.append(max(abstract_class)) #for all hierarchies -only abstract classes
            # store out of order occurrence
            dip_, Info = self.BreachOfDIP(hierachydata)
            # Info_ += Info
            # dipS += dip_
            DIP_occurence_per_hierarchy.append(max(dip_))
        
        # print(dipS, Info_)
        # # depth metrics
        depth_ , num_of_hierachy_per_depth = self.HierachyCountPerDepth(DIT_Max)
        plt.figure(1)
        self.plotData(depth_, num_of_hierachy_per_depth, "Depth", "Hierachies",  "Number of hierachies per depth")

        # # width metrics
        width_, num_of_hierachy_per_width = self.HierachyCountPerWidth(BIT_Max)
        plt.figure(2)
        self.plotData(width_, num_of_hierachy_per_width, "Width", "Hierachies",  "Number of hierachies per width")

        # public interface metrics
        public_interface_, num_of_classes_per_public_interface = self.ClassesCountPerPublicInterface(max_public_interfaces_per_class)
        plt.figure(3)
        self.plotData(public_interface_, num_of_classes_per_public_interface, "Public Interface", "Classes",  "Number of Classes per public_interface")

        # methods per depth
        added_functions, overriden_functions = self.MethodsPerDepth(DIT_Max, novel_methods_class_occurrence_per_class, overriden_methods_class_occurrence_per_class, depth_per_method_data) #, overriden_functions
        plt.figure(4)
        self.plotData( added_functions['depth'],added_functions['methods'], "Depth", "Novel method",  "Number of novel methods per depth")
        plt.figure(5)
        self.plotData( overriden_functions['depth'], overriden_functions['methods'], "Depth",  "Overriden method",  "Number of overriden methods per depth")

        # methods per hierarchy
        novel_methods_hierarchy_occurrence = self.MethodsPerHierachy(max_additional_methods_occurrence_per_hierarchy)
        overriden_methods_hierarchy_occurrence = self.MethodsPerHierachy(max_overriden_methods_occurrence_per_hierarchy)
        plt.figure(6)
        self.plotData( novel_methods_hierarchy_occurrence['Method sequence'], novel_methods_hierarchy_occurrence['Total Hierarchies'], "Methods", "Hierarchies",  "Novel Methods vs Hierarchies")
        plt.figure(7)
        self.plotData( overriden_methods_hierarchy_occurrence['Method sequence'], overriden_methods_hierarchy_occurrence['Total Hierarchies'], "Methods",  "Hierarchies",  "Overriden Methods vs Hierarchies") 
        
        # methods per class
        novel_methods_class_occurrence= self. MethodsPerClass(novel_methods_class_occurrence_per_class)
        overriden_methods_class_occurrence = self. MethodsPerClass(overriden_methods_class_occurrence_per_class)
        plt.figure(8)
        self.plotData( novel_methods_class_occurrence['Method sequence'], novel_methods_class_occurrence['Total Classes'], "Methods", "Classes",  "Novel Methods vs Classes")
        plt.figure(9)
        self.plotData( overriden_methods_class_occurrence['Method sequence'], overriden_methods_class_occurrence['Total Classes'], "Methods",  "Classes",  "Overriden Methods vs Classes")

        #class types 
        class_types_data, all_class_types_data = self.ClassTypesOccurrence(class_types, all_class_types_)
        labels = ['Abstract Classes', 'Conctrete Classes', 'Interface Classes']
        fig, plot10 = plt.subplots()
        plt.title('Class Types for all hierarchy members')
        plot10.pie(all_class_types_data, labels=labels, autopct='%1.1f%%')
        plot10.axis('equal')       
        
        fig, plot11 = plt.subplots()
        plt.title('Class Types for hierarchy members inside the hierarchies')
        plot11.pie(class_types_data, labels=labels, autopct='%1.1f%%')
        plot11.axis('equal')

        print(100 - (class_types_data[0]/all_class_types_data[0])*100, '% Of the abstract classes are hierarchy roots')

        #abstract classes
        abstract_classes_, num_of_hierachy_per_abstract_class = self.HierachyCountPerAbstractClass(max_abstract_classes_per_hierarchy)
        plt.figure(12)
        self.plotData( abstract_classes_, num_of_hierachy_per_abstract_class, "Abstract Classes",  "Hierarchies",  "Abstract Classes vs Hierachies")

        Out_of_Order_occurrence, num_of_hierarchy_out_of_order = self. HierarchyOutOfOrder(DIP_occurence_per_hierarchy)
        plt.figure(13)
        self.plotData( Out_of_Order_occurrence, num_of_hierarchy_out_of_order, "Out of Order (0 - no, 1 - yes)",  "Hierarchies",  "Hierarchies vs Out of Order")
        plt.show()
    
    def plotData(self, x_axis, y_axis, x_label, y_label, plot_title):
        '''This function plots y_axis vs x_axis'''
        x= x_axis
        y= y_axis
        plt.bar(x, y)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(plot_title)

# ProjectDataVisualize().PrintingHierachyData()