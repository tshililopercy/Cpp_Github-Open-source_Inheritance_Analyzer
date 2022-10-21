import json
# import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

with open('results.json', 'r') as openfile:
    # Reading from json file
    json_object = json.load(openfile)
    x1 = json_object['Depth Metrics'][0]['Depth ']
    y1 = json_object['Depth Metrics'][0]['Number of hierachies per depth']
    x2 = json_object["Width Metrics"][0]["Width"]
    y2 = json_object["Width Metrics"][0]["Number of hierachies per width"]
    x3 = json_object["Public Interface Metrics"][0]["Public interface"]
    y3 = json_object["Public Interface Metrics"][0]["Number of hierachies per public_interface"]
    y4 = json_object["Methods Metrics"][0]["Novel methods"]

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

# df_public_interface_metrics = pd.DataFrame()
# df_public_interface_metrics["Public interfaces"] = x3
# df_public_interface_metrics["Number of hierachies per public_interface"] = y3
# plot3= df_public_interface_metrics.plot( x= 'width_', y = 'Number of hierachies per width', kind='histogram')
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

