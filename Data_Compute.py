import matplotlib.pyplot as plt
import json
import numpy as np

class ProjectDataVisualize:
    def __init__(self):
        self.HierarchiesData = []
        self.project_count = []
        self.count = 0
        self.types_ = []
        
    def read_json(self):
        with open('HierachiesData.json', 'r') as openfile:
            # Reading data from the storage json file 
            self.HierarchiesData = json.load(openfile)
            #self.CalculateData()
    # def CalculateData(self):
    #     for project in self.HierarchiesData:
    #         for hierarchy in self.HierarchiesData[project]["Hierarchies"]:
    #             for depth in self.HierarchiesData[project]["Hierarchies"][hierarchy]:
    #                 for inheritances in depth:
    #                    for inheritance in  depth[inheritances]:
    #                        print("ClassName: ", inheritance["ClassName"], "ClassType: ", inheritance["TypeOfClass"],"Public pure virtual: ", inheritance["public pure virtual functions"], "Public interface: ", inheritance["Public Interface"])
    #                        for ID, parent in enumerate(inheritance["SubClasses"]):
    #                            print("parent " + str(ID), inheritance["SubClasses"])
                           

    #--------------- depth metrics----------------
    def HierarchyCountPerDepth(self, max_depths):
        total_hierarchies = [] 
        depth_sequence = []
        for depth_val in range(1, max(max_depths)+1, 1):
            count=0
            depth_sequence.append(depth_val)
            for depth_ in max_depths:
                if depth_val == depth_:
                    count += 1
            total_hierarchies.append(count)    
        return depth_sequence, total_hierarchies
            
    #------------------width metrics---------------------------
    def WidthMetrics(self, hierarchydata):
        '''Finds number of children per hierarchy'''
        widths = []
        width = len(hierarchydata)
        widths.append(width)
        return widths

    def HierarchyCountPerWidth(self, widths):
        total_hierarchies = [] 
        width_sequence = []
        for width_val in range(0, max(widths)+1, 1):
            count=0
            width_sequence.append(width_val)
            for width_ in widths:
                if width_val == width_:
                    count += 1
            total_hierarchies.append(count)    
        return width_sequence, total_hierarchies

    # --------------------------public interface metrics----------------
    def PublicInterfaceMetrics(self, hierarchydata):
        '''Returns public interfaces per class'''
        public_interfaces = []
        for hierarchyinfo in hierarchydata:
            public_interfaces.append(hierarchyinfo['Public Interface'])
            
            # include root public interfaces
            root_public_interfaces = 0
            for rootclassInfo in hierarchyinfo['SubClasses']:
                # root classes have more infomation, i.e. name of rootclass, type of class and public interfaces
                if len(rootclassInfo) > 2:
                    root_public_interfaces += len((rootclassInfo['PublicInterface']['purevirtualfunctions']))
                    root_public_interfaces += len((rootclassInfo['PublicInterface']['virtualfunctions']))
                    root_public_interfaces += len((rootclassInfo['PublicInterface']['normalfunctions']))

                    public_interfaces.append(root_public_interfaces)
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
    def AdditionalMethodsMetrics(self, hierarchydata):
        '''Returns additional methods for all hierarchies'''
        # Names of added methods per depth for all hierarchies
        # additional_methods_names = []
        # Number of added methods per depth for all hierarchies
        additional_methods_occurrence = []
        # keep track which added method belongs to which depth
        depth_per_method = []
        for hierarchyinfo in hierarchydata:
            depth_ = hierarchyinfo['Depth']
            depth_per_method.append(depth_)
            additional_method = hierarchyinfo['Added Methods']
            # additional_methods_names.append(additional_method)
            additional_methods_occurrence.append(additional_method)
        return additional_methods_occurrence, depth_per_method

    #------------------------------overrriden------------------
    def OverridenMethodsMetrics(self, hierarchydata):
        '''Returns overriden for all hierarchies'''
        # Names of overriden methods per depth for all hierarchies 
        # overriden_methods = []
        # Number of overriden methods per depth for all hierarchies
        overriden_methods_occurrence = []
        # keep track which pverriden method belongs to which depth
        depth_per_method = [] 
        for hierarchyinfo in hierarchydata:
            # print(hierarchyinfo, '\n')
            depth_ = hierarchyinfo['Depth']
            depth_per_method.append(depth_)
            overriden_method = hierarchyinfo['Overriden Methods']
            overriden_methods_occurrence.append(overriden_method)
        return overriden_methods_occurrence, depth_per_method

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

    def MethodsPerHierarchy(self, methods_occurrence ):
        total_hierarchies = [] 
        method_sequence = []
        methods_per_hierarchy_data = {}
        for method_val in range(0, max(methods_occurrence)+1, 1):
            count=0
            method_sequence.append(method_val)
            for method_ in methods_occurrence:
                if method_val == method_:
                    count += 1
            total_hierarchies.append(count)   
        methods_per_hierarchy_data['Method sequence'] = method_sequence
        methods_per_hierarchy_data['Total Hierarchies'] = total_hierarchies

        return methods_per_hierarchy_data

    def MethodsPerDepth(self, max_depths, additional_methods_occurrence, overriden_methods_occurrence, depth_per_method_data):
        depth_count = []
        novel_methods = {}
        overriden_methods = {}
        novel_methods_count_ = []
        overriden_methods_count_ = []

        # number of counted methods in each depth
        for depth_val in range(1, max(max_depths)+1, 1):
            depths_indices = []
            novel = 0
            overriden = 0

            for depthss in range(len(depth_per_method_data)):
                if depth_per_method_data[depthss] == depth_val:
                    depths_indices.append(depthss)

            for depths_index in depths_indices:
                novel += additional_methods_occurrence[depths_index]
            
            for depths_index in depths_indices:
                overriden += overriden_methods_occurrence[depths_index]

            novel_methods_count_.append(novel)
            overriden_methods_count_.append(overriden)
            depth_count.append(depth_val)
        
        novel_methods['depth'] = depth_count
        novel_methods['methods'] = novel_methods_count_
        overriden_methods['depth'] = depth_count
        overriden_methods['methods'] = overriden_methods_count_

        return novel_methods, overriden_methods

    def MethodsPerDepthLargeHierarchies(self, hierarchydata, hierarchy_information):
        added_hierarchy_functions = []
        overriden_hierarchy_functions = []
        public_interface_hierarchy_functions = []
        pure_virtual_hierarchy_functions = []
        depth_per_hierarchy_methods = []

        if len(hierarchy_information) > 2:
            for index, depths in enumerate(hierarchy_information):
                added_methods_ = []
                overriden_methods_ = []
                public_interface_ = []
                pure_virtual_methods_ =[]
                depth_per_method = []

                for depth in depths:
                    for hierarchyinfo in depths[depth]:
                        depth_ = hierarchyinfo['Depth']
                        depth_per_method.append(depth_)
                        added_methods = hierarchyinfo['Added Methods']
                        overriden_methods = hierarchyinfo['Overriden Methods']
                        public_interface = hierarchyinfo['Public Interface']
                        pure_virtual_methods = hierarchyinfo['public pure virtual functions']
                        
                        root_public_interfaces = 0
                        for rootclassInfo in hierarchyinfo['SubClasses']:
                            # root classes have more infomation, i.e. name of rootclass, type of class and public interfaces
                            if len(rootclassInfo) > 2:
                                root_public_interfaces += len((rootclassInfo['PublicInterface']['purevirtualfunctions']))
                                root_public_interfaces += len((rootclassInfo['PublicInterface']['virtualfunctions']))
                                root_public_interfaces += len((rootclassInfo['PublicInterface']['normalfunctions']))
                                public_interface_.append(root_public_interfaces)
                                
                        added_methods_.append(added_methods)
                        overriden_methods_.append(overriden_methods)
                        public_interface_.append(public_interface )
                        pure_virtual_methods_.append(pure_virtual_methods)

                added_hierarchy_functions += added_methods_
                overriden_hierarchy_functions += overriden_methods_
                public_interface_hierarchy_functions += public_interface_
                pure_virtual_hierarchy_functions += pure_virtual_methods_
                depth_per_hierarchy_methods += depth_per_method
           
            novel_methods_count_ = []
            overriden_methods_count_ = []
            pure_virtual_methods_count_ = []
            public_interface_methods_count_ = []
            depth_count = []

            for depth_val in range(1, len(hierarchy_information)+1, 1):
                novel = 0
                overriden = 0
                pure_virtual = 0
                public_interface = 0
                depths_indices = [] 

                for depthss in range(len(depth_per_hierarchy_methods)):
                    if depth_per_hierarchy_methods[depthss] == depth_val:
                        depths_indices.append(depthss)

                for depths_index in depths_indices:
                    novel += added_hierarchy_functions[depths_index]

                for depths_index in depths_indices:
                    pure_virtual += pure_virtual_hierarchy_functions[depths_index]

                for depths_index in depths_indices:
                    public_interface += public_interface_hierarchy_functions[depths_index]
                
                for depths_index in depths_indices:
                    overriden += overriden_hierarchy_functions[depths_index]

                novel_methods_count_.append(novel)
                overriden_methods_count_.append(overriden)
                pure_virtual_methods_count_.append(pure_virtual)
                public_interface_methods_count_.append(public_interface)
                depth_count.append(depth_val)

            plt.figure(16)
            plt.plot(depth_count, novel_methods_count_, 'bo', label = f"Novel Methods")
            plt.plot(depth_count, overriden_methods_count_,'go', label = "Overriden methods")
            plt.plot(depth_count, public_interface_methods_count_, 'r+', label = "Public Interface methods")
            plt.plot(depth_count, pure_virtual_methods_count_, 'm^', label = "Added and inheritted pure virtual methods")
            plt.xlabel('Depth')
            plt.ylabel('Number of functions')
            plt.title(f'Number of functions in one hierarchy with depth = {len(hierarchy_information)}')
            plt.legend()
            plt.show()

    def PureVirtualMetrics(self, hierarchydata):
        '''Returns the number of added and inherited methods in all class of a project'''
        # Number of added methods per depth for all hierarchies
        public_pure_virtual_methods_occurrence = []
        # keep track which added method belongs to which depth
        for hierarchyinfo in hierarchydata:
            public_pure_virtual_method = hierarchyinfo['public pure virtual functions']
            public_pure_virtual_methods_occurrence.append(public_pure_virtual_method)
        return public_pure_virtual_methods_occurrence
   
   #-------------------------Class types metrics----------------------
    def ClassTypeMetrics(self, hierarchydata):
        '''Returns Class types'''
        class_types = []
        abstract_class_count = []
        all_class_types = []
        abstract_class = []
        concrete_class = []
        interface_class = []
        count = 0
        for hierarchyinfo in hierarchydata:
            class_type = hierarchyinfo['TypeOfClass']
            class_types.append(class_type)
            all_class_types.append(class_type)
            # print(class_type)
            if class_type == 'Abstract Class':
                count += 1
                abstract_class.append(hierarchyinfo['ClassName'])
                abstract_class_count.append(count)
            elif class_type == 'Concrete Class':
                concrete_class.append(hierarchyinfo['ClassName'])
                abstract_class_count.append(count)
            else:
                interface_class.append(hierarchyinfo['ClassName'])    
                abstract_class_count.append(count)
            
            # include root hierarchy memmbers
            for rootclassInfo in hierarchyinfo['SubClasses']:
                # root classes have more infomation, i.e. name of rootclass, type of class and public interfaces
                if len(rootclassInfo) > 2:
                    class_type_rootclass = rootclassInfo['TypeOfClass']
                    all_class_types.append(class_type_rootclass)

                    if class_type_rootclass == 'Abstract Class':
                        abstract_class.append(rootclassInfo['rootname'])
                    elif class_type_rootclass == 'Concrete Class':   
                        concrete_class.append(rootclassInfo['rootname'])
                    else:    
                        interface_class.append(rootclassInfo['rootname'])
        return class_types, abstract_class_count, all_class_types, abstract_class, concrete_class, interface_class

    def ClassTypesOccurrence(self, class_types, all_class_types):
        # for hierarchy members inside the hierarchy (i.e. from depth >1)
        class_type_data = []
        abstract = class_types.count('Abstract Class')
        concrete = class_types.count('Concrete Class')
        interface = class_types.count('Interface Class')

        # for all hierarchy members including depth=0
        all_abstract = all_class_types.count('Abstract Class')
        all_concrete = all_class_types.count('Concrete Class')
        all_interface = all_class_types.count('Interface Class')

        all_class_types_data = [all_abstract, all_concrete, all_interface]
        class_type_data = [abstract, concrete, interface]
        return class_type_data, all_class_types_data

    def CheckRoleModellingUse(self, abstract_classes, concrete_classes, interface_classes, classes_used_in_code):
        # print(abstract_classes, classes_used_in_code, '\n')
        #check if concrete class is used in code, if yes, re-use, If abc or interface is used in code, then role modelling
        self.count +=1
        count_reuse = 0
        count_ABC = 0
        count_Interface = 0
        count_neither = 0
        self.project_count.append(self.count)
        for c_class in concrete_classes:
            if classes_used_in_code.count(c_class) > 0:
                count_reuse += 1
                # print (c_class, "Reuse")
            else:
                # print(c_class, "NOPE NOPE")
                count_neither += 1 
        
        for abc_class in abstract_classes:
            if classes_used_in_code.count(abc_class) > 0:
                count_ABC += 1
                # print (abc_class, "ABC Role modelling")
            else:
                # print(abc_class, "NOPE NOPE")
                count_neither += 1 

        for interface in interface_classes:
            if classes_used_in_code.count(interface) > 0:
                count_Interface += 1
                # print (interface, "INTERFACE Role modelling") 
            else:
                # print(interface, "NOPE NOPE")
                count_neither += 1 

        total = count_reuse+ count_ABC+ count_Interface+ count_neither
        if total == 0: total=1
        results_reuse = "{:.2f}".format((count_reuse/total)*100)+" %"
        results_ABC = "{:.2f}".format((count_ABC/total)*100)+" %"
        results_Inter = "{:.2f}".format((count_Interface/total)*100)+" %"
        results_none = "{:.2f}".format((count_neither/total)*100)+" %"
        self.types_.append([results_reuse, results_ABC, results_Inter, results_none])
        return count_reuse, count_ABC, count_Interface, count_neither

    #-------------------------Abstract Class metrics----------------------
    def HierarchyCountPerAbstractClass(self, max_abstract_classes_per_hierarchy):
        total_hierarchies = [] 
        abstract_class_sequence = []
        for abstract_class_val in range(0, max(max_abstract_classes_per_hierarchy)+1, 1):
            count=0
            abstract_class_sequence.append(abstract_class_val)
            for abstract_class_ in max_abstract_classes_per_hierarchy:
                if abstract_class_val == abstract_class_:
                    count += 1
            total_hierarchies.append(count)    
        return abstract_class_sequence, total_hierarchies

    def BreachOfDIP(self, hierarchydata):
        dip_ = []
        Info = []
        # DIP = 0 (no DIP breach/ Abstract classes). DIP = 1 (direct breach of the DIP - abstract class inheriting from concrete class)
        for hierarchyinfo in hierarchydata:
            class_type_childclass = hierarchyinfo['TypeOfClass']
            if class_type_childclass == 'Abstract Class':
                childclass = hierarchyinfo['ClassName']
                for parentclassInfo in hierarchyinfo['SubClasses']:
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
        total_hierarchies = [] 
        dip_sequence = []
        for dip_val in range(0, max(dip)+1, 1):
            count=0
            dip_sequence.append(dip_val)
            for dip_ in dip:
                if dip_val == dip_:
                    count += 1
            total_hierarchies.append(count)    
        return dip_sequence, total_hierarchies

    def PrintingHierarchyData(self):
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

        public_pure_virtual_methods = []
        
        all_class_types_ = []
        class_types = []
        max_abstract_classes_per_hierarchy = []
        DIP_occurence_per_hierarchy = []
        # dipS = []
        # Info_ = []
        count=0

        # Types = {}
        # reuse = 0
        # role_modelling_ABC = 0
        # role_modelling_interface = 0
        # no_client_code = 0

        # for hierarchydata_index in self.HierarchiesData:
        abstract_classes = []
        concrete_classes = []
        interface_classes = []
        for project in self.HierarchiesData:
            count +=1
            
            classes_used_in_code = self.HierarchiesData[project]['ClassesUsed']
            for hierarchy in self.HierarchiesData[project]['Hierarchies']:
                # depth
                depths_per_hierarchy = len(self.HierarchiesData[project]['Hierarchies'][hierarchy])
                hierarchy_information = self.HierarchiesData[project]['Hierarchies'][hierarchy]
                DIT_Max.append(depths_per_hierarchy)

                for index, depths in enumerate(self.HierarchiesData[project]['Hierarchies'][hierarchy]):
                    for depth in depths:
                        
                        # widths
                        widths = self.WidthMetrics(depths[depth])
                        BIT_Max.append(max(widths))
                        # public interface
                        total_public_interfaces = self.PublicInterfaceMetrics(depths[depth])
                        max_public_interfaces_per_class += total_public_interfaces
                        # novel methods
                        additional_methods_occurrence,  depth_per_method = self.AdditionalMethodsMetrics(depths[depth])
                        novel_methods_class_occurrence_per_class += additional_methods_occurrence
                        max_additional_methods_occurrence_per_hierarchy.append(max(additional_methods_occurrence))
                        # overriden methods
                        overriden_methods_occurrence,  depth_per_method = self.OverridenMethodsMetrics(depths[depth])
                        overriden_methods_class_occurrence_per_class += overriden_methods_occurrence
                        max_overriden_methods_occurrence_per_hierarchy.append(max(overriden_methods_occurrence))

                        depth_per_method_data += depth_per_method

                        public_pure_virtual_method = self.PureVirtualMetrics(depths[depth])
                        public_pure_virtual_methods += public_pure_virtual_method
                        # class types
                        class_type, abstract_class_count, all_class_types, abstract_class, concrete_class, interface_class = self.ClassTypeMetrics(depths[depth])
                        class_types += class_type # for all hierarchies - types include abstract, concrete, and interface
                        all_class_types_ += all_class_types
                        max_abstract_classes_per_hierarchy.append(max(abstract_class_count)) #for all hierarchies -only abstract classes
                        
                        abstract_classes += abstract_class
                        concrete_classes += concrete_class
                        interface_classes += interface_class

                        # print(abstract_class, concrete_class, interface_class, '\n')
                        # store out of order occurrence
                        dip_, Info = self.BreachOfDIP(depths[depth])
                        # Info_ += Info
                        # dipS += dip_
                        DIP_occurence_per_hierarchy.append(max(dip_))

                self.MethodsPerDepthLargeHierarchies(hierarchy, hierarchy_information)
            self.CheckRoleModellingUse(abstract_classes, concrete_classes, interface_classes, classes_used_in_code)
            
                       # print(count_reuse, count_ABC, count_Interface, count_neither)
            # classes_used_in_code = self.HierarchiesData[project]['ClassesUsed']
            # print(count)# print('\n')
            # reuse += count_reuse
            # role_modelling_ABC += count_ABC
            # role_modelling_interface += count_Interface
            # no_client_code += count_neither
            
        # --------------------------- Plots --------------------------------------------
        # # depth metrics
        depth_ , num_of_hierarchy_per_depth = self.HierarchyCountPerDepth(DIT_Max)
        plt.figure(1)
        self.plotData(depth_, num_of_hierarchy_per_depth, "Depth", "Hierarchies",  "Number of hierarchies per depth")

        # # width metrics
        width_, num_of_hierarchy_per_width = self.HierarchyCountPerWidth(BIT_Max)
        plt.figure(2)
        self.plotData(width_, num_of_hierarchy_per_width, "Width", "Hierarchies",  "Number of hierarchies per width")

        # public interface metrics
        public_interface_, num_of_classes_per_public_interface = self.ClassesCountPerPublicInterface(max_public_interfaces_per_class)
        plt.figure(3)
        self.plotData(public_interface_, num_of_classes_per_public_interface, "Public Interface", "Classes",  "Number of Classes per public_interface")

        # methods per depth
        added_functions, overriden_functions = self.MethodsPerDepth(DIT_Max, novel_methods_class_occurrence_per_class, overriden_methods_class_occurrence_per_class, depth_per_method_data)
        plt.figure(4)
        self.plotData( added_functions['depth'],added_functions['methods'], "Depth", "Novel method",  "Number of novel methods per depth")
        plt.figure(5)
        self.plotData( overriden_functions['depth'], overriden_functions['methods'], "Depth",  "Overriden method",  "Number of overriden methods per depth")

        # methods per hierarchy
        novel_methods_hierarchy_occurrence = self.MethodsPerHierarchy(max_additional_methods_occurrence_per_hierarchy)
        overriden_methods_hierarchy_occurrence = self.MethodsPerHierarchy(max_overriden_methods_occurrence_per_hierarchy)
        plt.figure(6)
        self.plotData( novel_methods_hierarchy_occurrence['Method sequence'], novel_methods_hierarchy_occurrence['Total Hierarchies'], "Methods", "Hierarchies", "Hierarchies vs Novel Methods")
        plt.figure(7)
        self.plotData( overriden_methods_hierarchy_occurrence['Method sequence'], overriden_methods_hierarchy_occurrence['Total Hierarchies'], "Methods",  "Hierarchies",  "Hierarchies vs Overriden Methods") 

        # classses per method
        novel_methods_class_occurrence= self. MethodsPerClass(novel_methods_class_occurrence_per_class)
        overriden_methods_class_occurrence = self. MethodsPerClass(overriden_methods_class_occurrence_per_class)
        plt.figure(8)
        self.plotData( novel_methods_class_occurrence['Method sequence'], novel_methods_class_occurrence['Total Classes'], "Methods", "Classes",  "Classes vs Novel Methods")
        plt.figure(9)
        self.plotData( overriden_methods_class_occurrence['Method sequence'], overriden_methods_class_occurrence['Total Classes'], "Methods",  "Classes",  "Classes vs Overriden Methods")

        #class types 
        class_types_data, all_class_types_data = self.ClassTypesOccurrence(class_types, all_class_types_)
        labels = ['Abstract Classes', 'Concrete Classes', 'Interface Classes']
        fig, plot10 = plt.subplots()
        plt.title('Class Types for all hierarchy members')
        plot10.pie(all_class_types_data, labels=labels, autopct='%1.1f%%')
        plot10.axis('equal')       
        plt.savefig('../Class Types for all hierarchy members.svg', format='svg', dpi=1200)

        fig, plot11 = plt.subplots()
        plt.title('Class Types for hierarchy members inside the hierarchies (excluding hierarchy roots)')
        plot11.pie(class_types_data, labels=labels, autopct='%1.1f%%')
        plot11.axis('equal')
        plt.savefig('../Class Types for hierarchy members inside the hierarchies.svg', format='svg', dpi=1200)
        print(100 - (class_types_data[0]/all_class_types_data[0])*100, '% Of the abstract classes are hierarchy roots')

        #abstract classes
        abstract_classes_, num_of_hierarchy_per_abstract_class = self.HierarchyCountPerAbstractClass(max_abstract_classes_per_hierarchy)
        plt.figure(12)
        self.plotData( abstract_classes_, num_of_hierarchy_per_abstract_class, "Abstract Classes",  "Hierarchies",  "Abstract Classes vs Hierarchies")

        Out_of_Order_occurrence, num_of_hierarchy_out_of_order = self. HierarchyOutOfOrder(DIP_occurence_per_hierarchy)
        plt.figure(13)
        self.plotData( Out_of_Order_occurrence, num_of_hierarchy_out_of_order, "Out of Order (0 - no, 1 - yes)",  "Hierarchies",  "Hierarchies vs Out of Order")

        # Types = [count_reuse, count_ABC, count_Interface, count_neither ]
        # labels = ['Reuse', 'Role modelling - ABC', 'Role modelling - Interface', 'Not Used in client code']
        # fig, plot14 = plt.subplots()
        # plt.title('Class Types')
        # plot14.pie(Types, labels=labels, autopct='%1.1f%%')
        # plot14.axis('equal')

        # Add a table to show class type distribution amongst projects
        fig14, plot14 = plt.subplots()
        columns = ('Re-use', 'Role modelling - ABC', 'Role modelling - Interface', 'Not Used in client code')
        rows = ['Project %d' % h for h in self.project_count] 
        the_table = plot14.table(cellText=self.types_, rowLabels =rows,colLabels=columns, loc='center', bbox=[0.0, 0, 1, 1])
        plt.subplots_adjust(bottom = 0.3)
        plot14.axes.get_yaxis().set_visible(False)
        plot14.axes.get_xaxis().set_visible(False)
        plt.savefig('../Role Modelleing.svg', format='svg', dpi=1200)

        # all methods methods per class
        plt.figure(15)
        plt.plot(novel_methods_class_occurrence_per_class, 'bo', label = "Novel Methods")
        plt.plot(overriden_methods_class_occurrence_per_class, 'go', label = "Overriden methods")
        plt.plot(max_public_interfaces_per_class, 'r+', label = "Public Interface methods")
        plt.plot(public_pure_virtual_methods, 'm^', label = "Added and inheritted pure virtual methods")
        plt.xlabel('Classes')
        plt.ylabel('Number of functions')
        plt.title('Relationship between public functions in all classes')
        plt.legend()
        plt.savefig('../Relationship between public functions in all classes.svg', format='svg', dpi=1200)
        plt.show()

    def plotData(self, x_axis, y_axis, x_label, y_label, plot_title):
        '''This function plots y_axis vs x_axis'''
        x= x_axis
        y= y_axis
        plt.bar(x, y)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.title(plot_title)
        plt.savefig(f'../{plot_title}.svg', format='svg', dpi=1200)
# ProjectDataVisualize().PrintingHierarchyData()