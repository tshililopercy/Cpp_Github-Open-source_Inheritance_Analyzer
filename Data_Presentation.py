import json
# import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

with open('results.json', 'r') as openfile:
    # Reading data from the storage json file 
    json_object = json.load(openfile)
    for json_object_ in json_object['Depth Metrics']:
        x1 = json_object_['Depth ']
        y1 = json_object_['Number of hierachies per depth']

    for json_object_ in json_object['Width Metrics']:
        x2 = json_object_["Width"]
        y2 = json_object_["Number of hierachies per width"]

    for json_object_ in json_object['Public Interface Metrics']:
        x3 = json_object_["Public interface"]
        y3 = json_object_["Number of classes per public_interface"]
    
    for json_object_ in json_object['Methods vs Depth Metrics']:
        x4 = json_object_['Novel methods']['depth']
        y4 = json_object_['Novel methods']['methods']
        x5 = json_object_['Overriden methods']['depth']
        y5 = json_object_['Overriden methods']['methods']

    for json_object_ in json_object['Methods vs Class Metrics']:
        x6 = json_object_['Novel methods']['Method sequence']
        y6 = json_object_['Novel methods']['Total Hierarchies']
        x7 = json_object_['Overriden methods']['Method sequence']
        y7 = json_object_['Overriden methods']['Total Hierarchies']

    for json_object_ in json_object['Methods vs Hierarchy Metrics']:
        x8 = json_object_['Novel methods']['Method sequence']
        y8 = json_object_['Novel methods']['Total Hierarchies']
        x9 = json_object_['Overriden methods']['Method sequence']
        y9 = json_object_['Overriden methods']['Total Hierarchies']

df_depth_metrics = pd.DataFrame()
df_depth_metrics['Depth_'] = x1
df_depth_metrics['Number of hierachies per depth'] = y1
plot1 = df_depth_metrics.plot( x= 'Depth_', y = 'Number of hierachies per depth', kind='bar')

df_width_metrics = pd.DataFrame()
df_width_metrics['width_'] = x2
df_width_metrics['Number of hierachies per width'] = y2
plot2 = df_width_metrics.plot( x= 'width_', y = 'Number of hierachies per width', kind='bar')
# plt.show()

plt.bar(x3, y3, align='center')
plt.xlabel('Public interfaces')
plt.ylabel("Number of classes per public_interface")

df_methods_vs_depth_metrics = pd.DataFrame()
df_methods_vs_depth_metrics['Depth'] = x4
df_methods_vs_depth_metrics["Novel methods"] = y4
plot4= df_methods_vs_depth_metrics.plot( x = 'Depth', y = 'Novel methods', kind='bar')

df_methods_vs_depth_metrics = pd.DataFrame()
df_methods_vs_depth_metrics['Depth'] = x5
df_methods_vs_depth_metrics["Overriden methods"] = y5
plot5= df_methods_vs_depth_metrics.plot( x = 'Depth', y = 'Overriden methods', kind='bar')
# plt.show()

df_methods_vs_class_metrics = pd.DataFrame()
df_methods_vs_class_metrics['Class'] = x6
df_methods_vs_class_metrics["Novel methods"] = y6
plot6= df_methods_vs_class_metrics.plot( x = 'Class', y = 'Novel methods', kind='bar')

df_methods_vs_class_metrics = pd.DataFrame()
df_methods_vs_class_metrics['Class'] = x7
df_methods_vs_class_metrics["Overriden methods"] = y7
plot7= df_methods_vs_class_metrics.plot( x = 'Class', y = 'Overriden methods', kind='bar')
# plt.show()

df_methods_vs_hierarchy_metrics = pd.DataFrame()
df_methods_vs_hierarchy_metrics['Hierarchy'] = x8
df_methods_vs_hierarchy_metrics["Novel methods"] = y8
plot8= df_methods_vs_hierarchy_metrics.plot( x = 'Hierarchy', y = 'Novel methods',  kind='bar')

df_methods_vs_hierarchy_metrics = pd.DataFrame()
df_methods_vs_hierarchy_metrics['Hierarchy'] = x9
df_methods_vs_hierarchy_metrics["Overriden methods"] = y9
plot9= df_methods_vs_hierarchy_metrics.plot( x = 'Hierarchy', y = 'Overriden methods', kind='bar')
plt.show()