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
        y3 = json_object_["Number of hierachies per public_interface"]
    
    for json_object_ in json_object['Methods Metrics']:
        y4 = json_object_["Novel methods"]
        y5 = json_object_["Overriden methods"]

df_depth_metrics = pd.DataFrame()
df_depth_metrics['Depth_'] = x1
df_depth_metrics['Number of hierachies per depth'] = y1
plot1 = df_depth_metrics.plot( x= 'Depth_', y = 'Number of hierachies per depth', kind='bar')
plt.show()

df_width_metrics = pd.DataFrame()
df_width_metrics['width_'] = x2
df_width_metrics['Number of hierachies per width'] = y2
plot2 = df_width_metrics.plot( x= 'width_', y = 'Number of hierachies per width', kind='bar')
plt.show()

plt.bar(x3, y3, align='center')
plt.xlabel('Public interfaces')
plt.ylabel("Number of hierachies per public_interface")
for i in range(len(y3)):
    plt.hlines(y3[i], 0, x3[i])
plt.show()

df_methods_metrics = pd.DataFrame()
df_methods_metrics["Novel methods"] = y4
plot4= df_methods_metrics.plot( y = 'Novel methods', kind='bar')
plt.show()

df_methods_metrics = pd.DataFrame()
df_methods_metrics["Overriden methods"] = y5
plot5= df_methods_metrics.plot( y = 'Overriden methods', kind='bar')
plt.show()

